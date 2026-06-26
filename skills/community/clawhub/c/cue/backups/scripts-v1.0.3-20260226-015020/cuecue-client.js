/**
 * CueCue Deep Research Client (Built-in version for Cue skill)
 * 
 * A standalone client for interacting with CueCue's deep research API.
 * This is a built-in version that doesn't require npm install.
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const { randomUUID } = require('crypto');

class CueCueDeepResearch {
    constructor(apiKey, baseUrl = 'https://cuecue.cn') {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl.replace(/\/$/, '');
    }

    /**
     * Execute a deep research query
     */
    async research(query, options = {}) {
        const conversationId = options.conversationId || randomUUID();
        const chatId = randomUUID();
        const messageId = `msg_${randomUUID()}`;
        const reportUrl = `${this.baseUrl}/c/${conversationId}`;

        console.log(`\n🔬 Starting Deep Research: ${query}\n`);
        console.log(`📊 Report URL: ${reportUrl}\n`);

        // 根据 mode 生成增强的调研指令（rewritten_mandate 格式）
        let enhancedQuery = query;
        if (options.mode && options.mode !== 'default') {
            const modeConfigs = {
                'advisor': {
                    role: '资深理财顾问',
                    focus: '投资建议、资产配置、风险控制、收益预期',
                    framework: '资产配置与风险收益评估框架',
                    method: '根据用户财务状况，提供个性化的投资组合建议，分析各类资产的风险收益特征',
                    sources: '公募基金报告、保险产品说明书、银行理财公告、权威财经媒体'
                },
                'researcher': {
                    role: '行业研究员',
                    focus: '产业链分析、竞争格局、技术趋势、市场空间',
                    framework: '产业链拆解与竞争力评估框架（Peer Benchmarking）',
                    method: '梳理上下游产业链结构，对比主要竞争对手的核心能力，研判技术演进趋势',
                    sources: '上市公司公告、券商研报、行业协会数据、专利数据库、技术白皮书'
                },
                'fund-manager': {
                    role: '基金经理',
                    focus: '估值模型、财务分析、投资决策、风险收益比',
                    framework: '基本面分析与估值模型框架',
                    method: '深度分析财务报表，构建估值模型（DCF/PE/PB等），评估内在价值与市场价格偏离度',
                    sources: '上市公司财报、交易所公告、Wind/同花顺数据、券商深度研报、管理层访谈纪要'
                },
                'trader': {
                    role: '短线交易分析师',
                    focus: '资金流向、席位动向、市场情绪、技术形态、游资博弈',
                    framework: '市场微观结构与资金流向分析框架（Timeline Reconstruction）',
                    method: '追踪龙虎榜席位动向，分析大单资金流向，识别市场情绪拐点，研判技术形态支撑压力位',
                    sources: '交易所龙虎榜、Level-2行情数据、东方财富/同花顺资金数据、游资席位追踪、实时财经快讯'
                }
            };
            
            const config = modeConfigs[options.mode];
            if (config) {
                enhancedQuery = `**【调研目标】**
以${config.role}的专业视角，针对"${query}"进行全网深度信息搜集与分析，旨在回答该主题下的核心投资/交易问题。

**【信息搜集与整合框架】**
1. **${config.framework}**：${config.method}。
2. **关键证据锚定**：针对核心争议点或关键数据，查找并引用权威信源（如官方公告、交易所数据、权威研报）的原始信息。
3. **多维视角交叉**：汇总不同利益相关方（如买方机构、卖方分析师、产业从业者）的观点差异与共识。

**【信源与边界】**
- 优先信源：${config.sources}。
- 时间窗口：结合当前日期，优先近6个月内的最新动态与数据。
- 排除信源：无明确来源的小道消息、未经证实的社交媒体传言。

**【核心关注】**
${config.focus}`;
            }
        }

        // Build request payload
        const requestData = {
            messages: [
                {
                    role: 'user',
                    content: enhancedQuery,
                    id: messageId,
                    type: 'text',
                },
            ],
            chat_id: chatId,
            conversation_id: conversationId,
            need_confirm: false,
            need_analysis: false,
            need_underlying: false,
            need_recommend: false,
        };

        if (options.templateId) {
            requestData.template_id = options.templateId;
        }
        if (options.mimicUrl) {
            requestData.mimic = { url: options.mimicUrl };
        }

        const result = {
            conversationId,
            chatId,
            tasks: [],
            report: '',
            reportUrl,
        };

        const state = { isReporter: false, currentAgent: null };
        const reportContent = [];

        try {
            await this.makeRequest('/api/chat/stream', requestData, result, reportContent, state, options);
            
            // 确保报告内容被保存
            if (!result.report && reportContent.length > 0) {
                result.report = reportContent.join('');
            }
            
            // 如果 reporter 还在运行，标记为结束
            if (state.isReporter) {
                state.isReporter = false;
                result.report = reportContent.join('');
            }
        } catch (error) {
            console.error(`❌ Request failed: ${error.message}`);
            throw error;
        }

        return result;
    }

    /**
     * Make HTTP request and handle SSE stream
     */
    makeRequest(path, requestData, result, reportContent, state, options) {
        return new Promise((resolve, reject) => {
            const url = new URL(this.baseUrl + path);
            const postData = JSON.stringify(requestData);

            const requestOptions = {
                hostname: url.hostname,
                port: url.port || 443,
                path: url.pathname,
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(postData),
                },
            };

            const client = url.protocol === 'https:' ? https : http;
            const req = client.request(requestOptions, (res) => {
                let buffer = '';
                let lastDataTime = Date.now();

                res.on('data', (chunk) => {
                    lastDataTime = Date.now();
                    buffer += chunk.toString('utf-8');
                    const lines = buffer.split('\n');
                    buffer = lines.pop() || '';

                    for (const line of lines) {
                        this.processSSELine(line, result, reportContent, state, options);
                    }
                });

                res.on('end', () => {
                    // 处理剩余数据
                    if (buffer) {
                        const lines = buffer.split('\n');
                        for (const line of lines) {
                            this.processSSELine(line, result, reportContent, state, options);
                        }
                    }
                    
                    // 确保 reporter 内容被保存
                    if (state.isReporter && reportContent.length > 0) {
                        result.report = reportContent.join('');
                    }
                    
                    resolve();
                });

                res.on('error', reject);
            });

            req.on('error', reject);
            req.write(postData);
            req.end();
        });
    }

    /**
     * Process a single SSE line
     */
    processSSELine(line, result, reportContent, state, options) {
        if (!line.startsWith('data: ')) return;

        try {
            const eventData = JSON.parse(line.slice(6));
            this.handleSSEEvent(eventData, result, reportContent, state, options);
        } catch (e) {
            // Ignore parse errors for non-JSON lines
        }
    }

    /**
     * Handle SSE event
     */
    handleSSEEvent(eventData, result, reportContent, state, options) {
        if (!eventData) return;

        // 处理 agent 信息（agent_name 存在表示 agent 开始）
        if (eventData.agent_name) {
            const agentName = eventData.agent_name;
            
            // 如果之前有 reporter，说明 reporter 结束了
            if (state.currentAgent === 'reporter' && agentName !== 'reporter') {
                state.isReporter = false;
                if (reportContent.length > 0) {
                    result.report = reportContent.join('');
                }
            }
            
            state.currentAgent = agentName;
            
            if (agentName === 'coordinator') {
                console.log(`🚀 Research started. View progress at: ${result.reportUrl}`);
            } else if (agentName === 'supervisor') {
                const taskRequirement = eventData.task_requirement;
                if (taskRequirement) {
                    result.tasks.push(taskRequirement);
                    console.log(`📋 Task: ${taskRequirement}`);
                }
            } else if (agentName === 'reporter') {
                state.isReporter = true;
                console.log('📝 Generating Report...');
            }
        }
        
        // 处理消息内容（delta 存在表示有内容）
        if (eventData.delta && state.isReporter) {
            const delta = eventData.delta;
            if (delta.content) {
                const content = delta.content.replace(/【\d+-\d+】/g, '');
                reportContent.push(content);
                if (options.verbose) {
                    process.stdout.write(content);
                }
            }
        }
        
        // 处理完成状态
        if (eventData.status === 'completed' || eventData.status === 'finished') {
            if (state.isReporter) {
                state.isReporter = false;
                if (reportContent.length > 0) {
                    result.report = reportContent.join('');
                }
            }
            console.log('\n✅ Research complete');
        }
    }
}

/**
 * CLI interface
 */
async function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
        console.log(`
CueCue Deep Research Client (Built-in)

Usage:
  node cuecue-client.js <query> [options]

Options:
  --api-key KEY      CueCue API key (or set CUECUE_API_KEY env var)
  --base-url URL     API base URL (default: https://cuecue.cn)
  --output FILE      Save report to file
  --verbose          Show detailed progress
  --conversation-id  Continue existing conversation

Examples:
  CUECUE_API_KEY=xxx node cuecue-client.js "宁德时代财报"
  node cuecue-client.js "特斯拉分析" --api-key xxx --output report.md
`);
        process.exit(0);
    }

    // Parse arguments
    let query = '';
    let apiKey = process.env.CUECUE_API_KEY;
    let baseUrl = process.env.CUECUE_BASE_URL || 'https://cuecue.cn';
    let outputFile = null;
    let verbose = false;
    let conversationId = null;
    let mode = 'default';

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--api-key') {
            apiKey = args[++i];
        } else if (arg === '--base-url') {
            baseUrl = args[++i];
        } else if (arg === '--output' || arg === '-o') {
            outputFile = args[++i];
        } else if (arg === '--verbose' || arg === '-v') {
            verbose = true;
        } else if (arg === '--conversation-id') {
            conversationId = args[++i];
        } else if (arg === '--mode') {
            mode = args[++i];
        } else if (!arg.startsWith('--') && !query) {
            query = arg;
        }
    }

    if (!apiKey) {
        console.error('❌ Error: API key is required. Set CUECUE_API_KEY or use --api-key');
        process.exit(1);
    }

    if (!query) {
        console.error('❌ Error: Research query is required');
        process.exit(1);
    }

    try {
        const client = new CueCueDeepResearch(apiKey, baseUrl);
        const result = await client.research(query, {
            conversationId,
            verbose,
            mode,
        });

        // Print summary
        console.log('\n' + '='.repeat(60));
        console.log('📊 Research Summary');
        console.log('='.repeat(60));
        console.log(`Report URL: ${result.reportUrl}`);
        console.log(`Tasks: ${result.tasks.length}`);
        console.log(`Report length: ${result.report.length} characters`);

        // Save to file if requested
        if (outputFile) {
            const reportWithUrl = result.report + `\n\n---\n\n**Report URL:** ${result.reportUrl}\n`;
            fs.writeFileSync(outputFile, reportWithUrl, 'utf-8');
            console.log(`✅ Report saved to: ${outputFile}`);
        }

        // Output JSON for scripting (always output for notifier)
        console.log('\n===JSON_RESULT===');
        console.log(JSON.stringify({
            success: true,
            reportUrl: result.reportUrl,
            conversationId: result.conversationId,
            tasks: result.tasks,
        }));
        
        // Also output to stderr for debugging
        console.error(`[DEBUG] Research completed: ${result.reportUrl}`);

    } catch (error) {
        console.error(`❌ Execution failed: ${error.message}`);
        process.exit(1);
    }
}

main();
