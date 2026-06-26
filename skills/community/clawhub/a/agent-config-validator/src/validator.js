#!/usr/bin/env node
/**
 * Agent Config Validator
 * OpenClaw Agent 配置验证器
 * 
 * 功能：
 * 1. 验证 openclaw.json 与 agent 目录结构的一致性
 * 2. 检测核心文档中的过时引用
 * 3. 生成诊断报告
 * 4. 支持自动修复（带安全白名单机制）
 * 
 * 安全设计：
 * - 默认只读模式，不修改任何内容
 * - 安全修复白名单机制
 * - 敏感变更需要确认
 * - 核心文档永不自动修改
 * - 修改前自动备份
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

class AgentConfigValidator {
    constructor(openclawRoot) {
        // 自动检测 OpenClaw 根目录
        this.openclawRoot = openclawRoot || this.detectOpenClawRoot();
        this.configPath = path.join(this.openclawRoot, '.openclaw', 'openclaw.json');
        this.agentsDir = path.join(this.openclawRoot, '.openclaw', 'agents');
        this.issues = [];
        this.fixes = [];
        this.config = null;
        this.agentIds = new Set();
        
        // 安全修复白名单 - 这些配置项可以安全自动修复
        this.SAFE_TO_AUTO_FIX = [
            'subagents.allowAgents',
            'agentToAgent.allow',
            'bindings'
        ];
        
        // 需要人工确认的配置项
        this.REQUIRE_MANUAL_CONFIRM = [
            'agents.list',
            'models.primary',
            'models.fallbacks',
            'channels',
            'auth'
        ];
        
        // 严禁自动修改的文档
        this.PROTECTED_DOCUMENTS = [
            'IDENTITY.md',
            'SOUL.md',
            'MEMORY.md',
            'USER.md',
            'HEARTBEAT.md',
            'TOOLS.md'
        ];
    }

    /**
     * 自动检测 OpenClaw 根目录
     */
    detectOpenClawRoot() {
        // 1. 检查环境变量
        if (process.env.OPENCLAW_ROOT) {
            return process.env.OPENCLAW_ROOT;
        }

        // 2. 检查当前工作目录
        const cwd = process.cwd();
        if (fs.existsSync(path.join(cwd, '.openclaw', 'openclaw.json'))) {
            return cwd;
        }

        // 3. 检查上级目录
        let currentDir = cwd;
        for (let i = 0; i < 5; i++) {
            const parentDir = path.dirname(currentDir);
            if (parentDir === currentDir) break;
            
            if (fs.existsSync(path.join(parentDir, '.openclaw', 'openclaw.json'))) {
                return parentDir;
            }
            currentDir = parentDir;
        }

        // 4. 默认路径
        return 'D:\\OpenClaw';
    }

    /**
     * 检查配置项是否在安全白名单中
     */
    isSafeToAutoFix(configPath) {
        return this.SAFE_TO_AUTO_FIX.some(safe => configPath.includes(safe));
    }

    /**
     * 检查配置项是否需要人工确认
     */
    requiresManualConfirm(configPath) {
        return this.REQUIRE_MANUAL_CONFIRM.some(sensitive => configPath.includes(sensitive));
    }

    /**
     * 检查文档是否受保护
     */
    isProtectedDocument(filePath) {
        const basename = path.basename(filePath);
        return this.PROTECTED_DOCUMENTS.includes(basename);
    }

    /**
     * 交互式确认
     */
    async confirm(message) {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        return new Promise((resolve) => {
            rl.question(`${message} (y/N): `, (answer) => {
                rl.close();
                resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
            });
        });
    }

    /**
     * 加载配置
     */
    loadConfig() {
        try {
            if (!fs.existsSync(this.configPath)) {
                this.issues.push({
                    type: 'error',
                    category: 'config',
                    message: `配置文件不存在: ${this.configPath}`,
                    fixable: false
                });
                return false;
            }
            
            const configContent = fs.readFileSync(this.configPath, 'utf-8');
            this.config = JSON.parse(configContent);
            
            // 提取所有 agent ID
            if (this.config.agents && this.config.agents.list) {
                this.config.agents.list.forEach(agent => {
                    this.agentIds.add(agent.id);
                });
            }
            
            return true;
        } catch (error) {
            this.issues.push({
                type: 'error',
                category: 'config',
                message: `无法加载 openclaw.json: ${error.message}`,
                fixable: false
            });
            return false;
        }
    }

    /**
     * 获取实际存在的 agent 目录
     */
    getExistingAgents() {
        try {
            const entries = fs.readdirSync(this.agentsDir, { withFileTypes: true });
            return entries
                .filter(entry => entry.isDirectory())
                .map(entry => entry.name);
        } catch (error) {
            this.issues.push({
                type: 'error',
                category: 'filesystem',
                message: `无法读取 agents 目录: ${error.message}`,
                fixable: false
            });
            return [];
        }
    }

    /**
     * 验证 openclaw.json 配置
     */
    validateConfig() {
        if (!this.config) return;

        const existingAgents = this.getExistingAgents();

        // 1. 检查 agents.list 中的每个 agent 是否有对应目录
        if (this.config.agents && this.config.agents.list) {
            this.config.agents.list.forEach(agent => {
                const agentDir = path.join(this.agentsDir, agent.id);
                if (!fs.existsSync(agentDir)) {
                    this.issues.push({
                        type: 'error',
                        category: 'config',
                        message: `Agent "${agent.id}" 在配置中但目录不存在: ${agentDir}`,
                        fixable: false,
                        configPath: 'agents.list',
                        severity: 'high'
                    });
                }
            });
        }

        // 2. 检查 subagents.allowAgents（安全修复项）
        if (this.config.agents?.defaults?.subagents?.allowAgents) {
            const allowAgents = this.config.agents.defaults.subagents.allowAgents;
            const invalidAgents = allowAgents.filter(id => !this.agentIds.has(id));
            if (invalidAgents.length > 0) {
                this.issues.push({
                    type: 'warning',
                    category: 'config',
                    message: `subagents.allowAgents 包含无效 agent: ${invalidAgents.join(', ')}`,
                    fixable: true,
                    safeToFix: true,
                    configPath: 'agents.defaults.subagents.allowAgents',
                    fix: () => {
                        this.config.agents.defaults.subagents.allowAgents = 
                            allowAgents.filter(id => this.agentIds.has(id));
                    }
                });
            }
        }

        // 检查 main agent 的 subagents
        if (this.config.agents?.list) {
            const mainAgent = this.config.agents.list.find(a => a.id === 'main');
            if (mainAgent?.subagents?.allowAgents) {
                const allowAgents = mainAgent.subagents.allowAgents;
                const invalidAgents = allowAgents.filter(id => !this.agentIds.has(id));
                if (invalidAgents.length > 0) {
                    this.issues.push({
                        type: 'warning',
                        category: 'config',
                        message: `main agent 的 subagents.allowAgents 包含无效 agent: ${invalidAgents.join(', ')}`,
                        fixable: true,
                        safeToFix: true,
                        configPath: 'agents.list[main].subagents.allowAgents',
                        fix: () => {
                            mainAgent.subagents.allowAgents = 
                                allowAgents.filter(id => this.agentIds.has(id));
                        }
                    });
                }
            }
        }

        // 3. 检查 agentToAgent.allow（安全修复项）
        if (this.config.tools?.agentToAgent?.allow) {
            const allowList = this.config.tools.agentToAgent.allow;
            const invalidAgents = allowList.filter(id => !this.agentIds.has(id));
            if (invalidAgents.length > 0) {
                this.issues.push({
                    type: 'warning',
                    category: 'config',
                    message: `agentToAgent.allow 包含无效 agent: ${invalidAgents.join(', ')}`,
                    fixable: true,
                    safeToFix: true,
                    configPath: 'tools.agentToAgent.allow',
                    fix: () => {
                        this.config.tools.agentToAgent.allow = 
                            allowList.filter(id => this.agentIds.has(id));
                    }
                });
            }
        }

        // 4. 检查 bindings（安全修复项）
        if (this.config.bindings) {
            const invalidBindings = [];
            this.config.bindings.forEach((binding, index) => {
                if (!this.agentIds.has(binding.agentId)) {
                    invalidBindings.push({ index, agentId: binding.agentId });
                }
            });
            
            if (invalidBindings.length > 0) {
                invalidBindings.forEach(({ index, agentId }) => {
                    this.issues.push({
                        type: 'warning',
                        category: 'config',
                        message: `bindings[${index}] 引用无效 agent: "${agentId}"`,
                        fixable: true,
                        safeToFix: true,
                        configPath: `bindings[${index}]`,
                        fix: () => {
                            // 注意：这里需要重新查找索引，因为之前的修复可能已改变数组
                            const idx = this.config.bindings.findIndex(b => b.agentId === agentId);
                            if (idx !== -1) {
                                this.config.bindings.splice(idx, 1);
                            }
                        }
                    });
                });
            }
        }
    }

    /**
     * 检查文档中的过时引用
     */
    checkDocumentForOutdatedRefs(filePath, docType) {
        try {
            if (!fs.existsSync(filePath)) {
                this.issues.push({
                    type: 'warning',
                    category: 'documentation',
                    message: `文档不存在: ${filePath}`,
                    fixable: false,
                    protected: this.isProtectedDocument(filePath)
                });
                return;
            }

            const content = fs.readFileSync(filePath, 'utf-8');
            const lines = content.split('\n');
            const isProtected = this.isProtectedDocument(filePath);

            // 定义需要检查的模式
            const patterns = [
                { regex: /zoro|索隆/g, name: '索隆 (zoro)' },
                { regex: /sanji|山治/g, name: '山治 (sanji)' },
                { regex: /luobing|罗兵/g, name: '罗兵 (luobing)' },
                { regex: /qjoba|乔巴/g, name: '乔巴 (qjoba)' },
                { regex: /robin|罗宾/g, name: '罗宾 (robin)' }
            ];

            lines.forEach((line, index) => {
                patterns.forEach(pattern => {
                    if (pattern.regex.test(line)) {
                        this.issues.push({
                            type: 'warning',
                            category: 'documentation',
                            message: `${docType} 第${index + 1}行: 引用已删除的 agent "${pattern.name}"`,
                            file: filePath,
                            line: index + 1,
                            content: line.trim(),
                            fixable: false, // 文档内容永不自动修复
                            protected: isProtected,
                            reason: isProtected ? '受保护文档，严禁自动修改' : '文档内容需要人工审核'
                        });
                    }
                });
            });

            // 检查模型配置是否过时
            if (docType === 'AGENTS.md') {
                this.checkModelConfigInDocs(content, filePath);
            }

        } catch (error) {
            this.issues.push({
                type: 'error',
                category: 'documentation',
                message: `无法读取文档 ${filePath}: ${error.message}`,
                fixable: false
            });
        }
    }

    /**
     * 检查文档中的模型配置是否过时
     */
    checkModelConfigInDocs(content, filePath) {
        // 获取当前配置中的模型信息
        const modelInfo = {};
        if (this.config.agents?.list) {
            this.config.agents.list.forEach(agent => {
                if (agent.model?.primary) {
                    modelInfo[agent.id] = agent.model.primary;
                }
            });
        }

        // 检查是否包含旧的模型配置描述
        const outdatedPatterns = [
            { regex: /ollama\/qwen3\.5:27b.*路飞|路飞.*ollama\/qwen3\.5:27b/g, desc: '路飞模型配置过时' },
            { regex: /ollama\/qwen3\.5:9b.*娜美|娜美.*ollama\/qwen3\.5:9b/g, desc: '娜美模型配置过时' }
        ];

        const lines = content.split('\n');
        const isProtected = this.isProtectedDocument(filePath);
        
        lines.forEach((line, index) => {
            outdatedPatterns.forEach(pattern => {
                if (pattern.regex.test(line)) {
                    this.issues.push({
                        type: 'warning',
                        category: 'documentation',
                        message: `AGENTS.md 第${index + 1}行: ${pattern.desc}`,
                        file: filePath,
                        line: index + 1,
                        content: line.trim(),
                        fixable: false,
                        protected: isProtected,
                        reason: '文档内容需要人工审核'
                    });
                }
            });
        });
    }

    /**
     * 验证核心文档
     */
    validateCoreDocuments() {
        const mainAgentDir = path.join(this.agentsDir, 'main', 'agent');
        
        // 检查 main agent 的核心文档
        const coreDocs = ['AGENTS.md', 'IDENTITY.md', 'SOUL.md'];
        coreDocs.forEach(doc => {
            const docPath = path.join(mainAgentDir, doc);
            this.checkDocumentForOutdatedRefs(docPath, doc);
        });

        // 检查每个 agent 的自身文档
        this.agentIds.forEach(agentId => {
            if (agentId === 'main') return;
            
            const agentDocPath = path.join(this.agentsDir, agentId, 'agent', `${agentId}.md`);
            if (fs.existsSync(agentDocPath)) {
                this.checkAgentSelfDocument(agentDocPath, agentId);
            }
        });
    }

    /**
     * 检查 agent 自身文档
     */
    checkAgentSelfDocument(filePath, agentId) {
        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            const lines = content.split('\n');
            const isProtected = this.isProtectedDocument(filePath);

            let inCollaborationSection = false;
            lines.forEach((line, index) => {
                // 检测协作部分
                if (/协作|团队|配合/.test(line) && /[:：]/.test(line)) {
                    inCollaborationSection = true;
                }

                if (inCollaborationSection) {
                    // 检查是否引用了已删除的 agent
                    const deletedAgents = ['zoro', 'sanji', 'luobing', 'qjoba', 'robin'];
                    deletedAgents.forEach(deletedId => {
                        if (line.toLowerCase().includes(deletedId)) {
                            this.issues.push({
                                type: 'warning',
                                category: 'agent_document',
                                message: `${agentId}.md 第${index + 1}行: 引用已删除的 agent`,
                                file: filePath,
                                line: index + 1,
                                content: line.trim(),
                                fixable: false,
                                protected: isProtected,
                                reason: 'Agent 角色定义严禁自动修改'
                            });
                        }
                    });
                }

                // 退出协作部分
                if (inCollaborationSection && line.startsWith('##')) {
                    inCollaborationSection = false;
                }
            });

        } catch (error) {
            this.issues.push({
                type: 'error',
                category: 'agent_document',
                message: `无法读取 ${agentId} 文档: ${error.message}`,
                fixable: false
            });
        }
    }

    /**
     * 执行自动修复（带安全控制）
     */
    async applyFixes(options = {}) {
        const { safeMode = true, confirmSensitive = false, dryRun = false } = options;
        let fixCount = 0;
        let skippedCount = 0;
        let needsConfirm = [];
        
        // 分类处理问题
        const safeIssues = [];
        const sensitiveIssues = [];
        
        this.issues.forEach(issue => {
            if (issue.fixable && issue.fix) {
                if (issue.safeToFix || (safeMode === false && !this.requiresManualConfirm(issue.configPath || ''))) {
                    safeIssues.push(issue);
                } else if (!safeMode) {
                    sensitiveIssues.push(issue);
                } else {
                    skippedCount++;
                }
            }
        });

        // 1. 处理安全修复项
        if (safeIssues.length > 0) {
            console.log(`\n🔧 应用安全修复 (${safeIssues.length} 项)...`);
            
            for (const issue of safeIssues) {
                if (dryRun) {
                    console.log(`   [试运行] 将修复: ${issue.message}`);
                    fixCount++;
                    continue;
                }

                try {
                    issue.fix();
                    fixCount++;
                    this.fixes.push({
                        category: issue.category,
                        message: issue.message,
                        status: 'fixed',
                        safe: true
                    });
                    console.log(`   ✅ 已修复: ${issue.message}`);
                } catch (error) {
                    this.fixes.push({
                        category: issue.category,
                        message: issue.message,
                        status: 'failed',
                        error: error.message
                    });
                    console.log(`   ❌ 修复失败: ${issue.message} - ${error.message}`);
                }
            }
        }

        // 2. 处理敏感变更（需要确认）
        if (sensitiveIssues.length > 0 && confirmSensitive) {
            console.log(`\n⚠️  发现敏感变更 (${sensitiveIssues.length} 项)...`);
            
            for (const issue of sensitiveIssues) {
                console.log(`\n   ${issue.message}`);
                console.log(`   配置路径: ${issue.configPath || 'unknown'}`);
                
                if (dryRun) {
                    console.log(`   [试运行] 跳过敏感变更确认`);
                    continue;
                }

                const confirmed = await this.confirm('   是否应用此变更？');
                if (confirmed) {
                    try {
                        issue.fix();
                        fixCount++;
                        this.fixes.push({
                            category: issue.category,
                            message: issue.message,
                            status: 'fixed',
                            safe: false,
                            confirmed: true
                        });
                        console.log(`   ✅ 已修复: ${issue.message}`);
                    } catch (error) {
                        this.fixes.push({
                            category: issue.category,
                            message: issue.message,
                            status: 'failed',
                            error: error.message
                        });
                        console.log(`   ❌ 修复失败: ${error.message}`);
                    }
                } else {
                    this.fixes.push({
                        category: issue.category,
                        message: issue.message,
                        status: 'skipped',
                        reason: '用户取消'
                    });
                    console.log(`   ⏭️  已跳过`);
                }
            }
        }

        // 3. 保存修复后的配置
        if (fixCount > 0 && this.config && !dryRun) {
            try {
                // 创建备份
                const timestamp = Date.now();
                const backupPath = `${this.configPath}.backup.${timestamp}`;
                fs.copyFileSync(this.configPath, backupPath);
                
                // 保存新配置
                fs.writeFileSync(
                    this.configPath, 
                    JSON.stringify(this.config, null, 2),
                    'utf-8'
                );
                
                this.fixes.push({
                    category: 'config',
                    message: `配置已更新，备份保存至: ${backupPath}`,
                    status: 'fixed',
                    safe: true
                });
                console.log(`\n💾 配置已保存，备份: ${backupPath}`);
            } catch (error) {
                this.fixes.push({
                    category: 'config',
                    message: '保存配置失败',
                    status: 'failed',
                    error: error.message
                });
                console.log(`\n❌ 保存配置失败: ${error.message}`);
            }
        }

        // 4. 报告跳过的项目
        if (skippedCount > 0) {
            console.log(`\n⏭️  安全模式下跳过 ${skippedCount} 个非白名单修复项`);
            console.log(`   使用 --safe-mode=false 允许修复所有可修复项`);
        }

        return { fixCount, skippedCount };
    }

    /**
     * 生成报告
     */
    generateReport(outputPath) {
        const timestamp = new Date().toLocaleString('zh-CN');
        const errors = this.issues.filter(i => i.type === 'error');
        const warnings = this.issues.filter(i => i.type === 'warning');
        const fixableIssues = this.issues.filter(i => i.fixable);
        const safeFixable = this.issues.filter(i => i.fixable && i.safeToFix);
        const docIssues = this.issues.filter(i => i.category === 'documentation' || i.category === 'agent_document');

        let report = `# Agent Config Validation Report
生成时间: ${timestamp}

## 摘要
- 总 Agent 数: ${this.agentIds.size}
- 错误数: ${errors.length}
- 警告数: ${warnings.length}
- 可安全修复: ${safeFixable.length}
- 需人工确认: ${fixableIssues.length - safeFixable.length}
- 需人工处理: ${docIssues.length}
- 已修复: ${this.fixes.length}

## 安全状态
✅ 白名单修复: 启用
⚠️ 敏感变更确认: 需要
❌ 文档自动修复: 禁用（核心文档严禁自动修改）

## 详细结果

### 1. openclaw.json 配置检查
`;

        const configIssues = this.issues.filter(i => i.category === 'config');
        if (configIssues.length === 0) {
            report += '✅ 配置检查通过\n';
        } else {
            configIssues.forEach(issue => {
                const icon = issue.type === 'error' ? '❌' : '⚠️';
                const safeTag = issue.safeToFix ? ' [✅ 可安全自动修复]' : 
                               (issue.fixable ? ' [⚠️ 需人工确认]' : ' [❌ 不可自动修复]');
                report += `${icon} ${issue.message}${safeTag}\n`;
            });
        }

        report += '\n### 2. 文档过时检查\n';
        if (docIssues.length === 0) {
            report += '✅ 所有文档检查通过\n';
        } else {
            docIssues.forEach(issue => {
                const icon = issue.type === 'error' ? '❌' : '⚠️';
                const protectedTag = issue.protected ? ' [🔒 受保护文档]' : '';
                report += `${icon} ${issue.message}${protectedTag}\n`;
                if (issue.file && issue.line) {
                    report += `   文件: ${issue.file}:${issue.line}\n`;
                }
                if (issue.content) {
                    report += `   内容: \`${issue.content}\`\n`;
                }
                if (issue.reason) {
                    report += `   原因: ${issue.reason}\n`;
                }
            });
        }

        if (this.fixes.length > 0) {
            report += '\n### 3. 修复记录\n';
            this.fixes.forEach(fix => {
                const icon = fix.status === 'fixed' ? '✅' : 
                            fix.status === 'skipped' ? '⏭️' : '❌';
                const safeTag = fix.safe === true ? ' [安全]' : 
                               fix.safe === false ? ' [敏感]' : '';
                report += `${icon} ${fix.message}${safeTag}\n`;
                if (fix.error) {
                    report += `   错误: ${fix.error}\n`;
                }
                if (fix.reason) {
                    report += `   原因: ${fix.reason}\n`;
                }
            });
        }

        report += '\n## 修复建议\n';
        
        if (safeFixable.length > 0) {
            report += '\n### 可安全自动修复\n';
            safeFixable.forEach((issue, idx) => {
                report += `${idx + 1}. ${issue.message}\n`;
            });
            report += '\n命令: validate_agent_config({fix: true, safeMode: true})\n';
            report += '或: agent-config-validator --fix --safe-mode\n';
        }

        const manualIssues = docIssues.filter(i => !i.fixable);
        if (manualIssues.length > 0) {
            report += '\n### 需人工处理\n';
            manualIssues.forEach((issue, idx) => {
                report += `${idx + 1}. ${issue.message}\n`;
                if (issue.file && issue.line) {
                    report += `   位置: ${issue.file}:${issue.line}\n`;
                }
            });
        }

        const sensitiveFixable = fixableIssues.filter(i => i.fixable && !i.safeToFix);
        if (sensitiveFixable.length > 0) {
            report += '\n### 敏感变更（需确认）\n';
            sensitiveFixable.forEach((issue, idx) => {
                report += `${idx + 1}. ${issue.message}\n`;
            });
            report += '\n命令: validate_agent_config({fix: true, safeMode: false, confirmSensitive: true})\n';
        }

        if (errors.length === 0 && warnings.length === 0) {
            report += '\n✅ 所有检查通过，无需操作\n';
        }

        // 保存报告
        if (outputPath) {
            try {
                fs.writeFileSync(outputPath, report, 'utf-8');
                console.log(`报告已保存至: ${outputPath}`);
            } catch (error) {
                console.error(`保存报告失败: ${error.message}`);
            }
        }

        return report;
    }

    /**
     * 运行完整验证
     */
    async validate(options = {}) {
        // 默认选项：只读模式
        const { 
            fix = false, 
            verbose = true, 
            outputPath,
            safeMode = true,
            confirmSensitive = false,
            dryRun = false
        } = options;

        console.log('🔍 开始验证 Agent 配置...\n');
        
        if (dryRun) {
            console.log('🧪 试运行模式：显示会做什么但不执行\n');
        }

        // 1. 加载配置
        console.log('1️⃣ 加载 openclaw.json...');
        if (!this.loadConfig()) {
            console.log('❌ 配置加载失败\n');
            return false;
        }
        console.log(`   ✅ 已加载 ${this.agentIds.size} 个 agent\n`);

        // 2. 验证配置
        console.log('2️⃣ 验证配置一致性...');
        this.validateConfig();
        const configIssues = this.issues.filter(i => i.category === 'config');
        console.log(`   ${configIssues.length === 0 ? '✅' : '⚠️'} 发现 ${configIssues.length} 个配置问题\n`);

        // 3. 验证核心文档
        console.log('3️⃣ 检查核心文档...');
        this.validateCoreDocuments();
        const docIssues = this.issues.filter(i => i.category === 'documentation' || i.category === 'agent_document');
        console.log(`   ${docIssues.length === 0 ? '✅' : '⚠️'} 发现 ${docIssues.length} 个文档问题\n`);

        // 4. 应用修复
        if (fix) {
            console.log('4️⃣ 应用自动修复...');
            if (safeMode) {
                console.log('   🛡️ 安全模式：仅修复白名单内的配置项\n');
            }
            const { fixCount, skippedCount } = await this.applyFixes({ 
                safeMode, 
                confirmSensitive,
                dryRun 
            });
            console.log(`\n   ✅ 已修复 ${fixCount} 个问题`);
            if (skippedCount > 0) {
                console.log(`   ⏭️  跳过 ${skippedCount} 个非白名单项`);
            }
            console.log();
        }

        // 5. 生成报告
        console.log('5️⃣ 生成验证报告...');
        const report = this.generateReport(outputPath);
        
        if (verbose && !outputPath) {
            console.log('\n' + '='.repeat(60));
            console.log(report);
            console.log('='.repeat(60));
        }

        // 返回结果
        const hasErrors = this.issues.some(i => i.type === 'error');
        const hasWarnings = this.issues.some(i => i.type === 'warning');

        console.log('\n📊 验证完成!');
        console.log(`   错误: ${this.issues.filter(i => i.type === 'error').length}`);
        console.log(`   警告: ${this.issues.filter(i => i.type === 'warning').length}`);
        console.log(`   已修复: ${this.fixes.length}`);
        
        if (!fix && this.issues.some(i => i.fixable)) {
            console.log('\n💡 提示: 发现可修复问题，运行 --fix 自动修复');
        }

        return !hasErrors;
    }
}

// CLI 支持
async function main() {
    const args = process.argv.slice(2);
    const fix = args.includes('--fix') || args.includes('-f');
    const verbose = args.includes('--verbose') || args.includes('-v');
    const safeMode = !args.includes('--safe-mode=false') && !args.includes('--no-safe-mode');
    const confirmSensitive = args.includes('--confirm-sensitive') || args.includes('-c');
    const dryRun = args.includes('--dry-run') || args.includes('-d');
    
    const outputIndex = args.findIndex(arg => arg === '--output' || arg === '-o');
    const outputPath = outputIndex !== -1 ? args[outputIndex + 1] : null;

    const validator = new AgentConfigValidator();
    const success = await validator.validate({ 
        fix, 
        verbose, 
        outputPath,
        safeMode,
        confirmSensitive,
        dryRun
    });
    
    process.exit(success ? 0 : 1);
}

// 运行主函数
if (require.main === module) {
    main().catch(error => {
        console.error('错误:', error.message);
        process.exit(1);
    });
}

module.exports = AgentConfigValidator;
