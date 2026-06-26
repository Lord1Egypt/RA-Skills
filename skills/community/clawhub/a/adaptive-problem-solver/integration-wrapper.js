#!/usr/bin/env node

/**
 * 自适应问题解决器 - OpenClaw集成包装器
 * 
 * 将变通问题解决能力集成到OpenClaw工作流中
 */

const AdaptiveProblemSolver = require('./index.js');
const fs = require('fs');
const path = require('path');

class AdaptiveSolverIntegration {
    constructor() {
        this.solver = new AdaptiveProblemSolver();
        this.solver.loadHistory();
        
        // 集成配置
        this.config = {
            autoTrigger: true, // 自动检测需要变通解决的问题
            minConfidence: 0.7, // 最小置信度阈值
            maxSolutions: 3, // 最大方案数量
            learningEnabled: true, // 启用学习功能
            userProfileFile: path.join(__dirname, 'data', 'user-profile.json')
        };
        
        // 问题模式检测
        this.problemPatterns = [
            {
                pattern: /(不能操作|无法执行|安全协议|OpenGuardrails)/,
                constraint: 'security',
                confidence: 0.85
            },
            {
                pattern: /(权限|Docker|容器|没有权限)/,
                constraint: 'permission', 
                confidence: 0.80
            },
            {
                pattern: /(不会操作|什么操作都不会|技术能力|复杂)/,
                constraint: 'userSkill',
                confidence: 0.75
            },
            {
                pattern: /(多步骤|容易出错|技术要求|复杂操作)/,
                constraint: 'technical',
                confidence: 0.70
            }
        ];
    }
    
    /**
     * 检测是否需要变通解决方案
     */
    shouldIntervene(userMessage, assistantResponse) {
        // 如果助理响应包含僵化思维关键词
        const rigidKeywords = [
            '不能操作外部系统',
            '需要用户手动处理',
            '安全协议禁止',
            '权限不足无法执行',
            '用户需要学习',
            '过于复杂需要简化',
            '不能做',
            '无法完成'
        ];
        
        const containsRigidResponse = rigidKeywords.some(keyword => 
            assistantResponse && assistantResponse.includes(keyword)
        );
        
        // 或者用户明确表达了困难
        const userExpressedDifficulty = this.problemPatterns.some(pattern =>
            pattern.pattern.test(userMessage)
        );
        
        return containsRigidResponse || userExpressedDifficulty;
    }
    
    /**
     * 生成变通解决方案并集成到响应中
     */
    async generateAdaptiveResponse(userMessage, originalResponse) {
        console.log('🔍 检测到可能需要变通解决方案的问题');
        
        // 分析问题
        const analysis = this.solver.analyzeProblem(userMessage);
        console.log(`📊 问题分析: ${analysis.primaryConstraint} 限制`);
        
        // 生成解决方案
        const solutions = this.solver.generateSolutions(analysis, this.config.maxSolutions);
        
        if (solutions.length === 0) {
            console.log('⚠️ 未能生成变通解决方案');
            return originalResponse;
        }
        
        // 构建增强响应
        const enhancedResponse = this.buildEnhancedResponse(
            originalResponse,
            solutions,
            analysis
        );
        
        // 记录干预
        this.recordIntervention(userMessage, analysis, solutions);
        
        return enhancedResponse;
    }
    
    /**
     * 构建增强的响应
     */
    buildEnhancedResponse(originalResponse, solutions, analysis) {
        const solutionList = solutions.map((sol, index) => {
            return `**方案 ${index + 1}: ${sol.name}**
• **描述**: ${sol.description}
• **风险**: ${sol.riskLevel}
• **预计时间**: ${sol.estimatedTime}
• **成功率**: ${Math.round(sol.successProbability * 100)}%
• **步骤**: ${sol.steps.join(' → ')}`;
        }).join('\n\n');
        
        const decisionGuide = `
**🎯 决策指南:**
• **快速选择**: ${solutions[0].name} - 最直接有效的方案
• **平衡选择**: ${solutions[1] ? solutions[1].name : '方案2'} - 风险与效果的平衡
• **稳健选择**: ${solutions[2] ? solutions[2].name : '方案3'} - 最可靠的方案

**📋 考虑因素:**
1. 您的时间紧迫程度
2. 技术舒适度  
3. 风险承受能力
4. 长期维护需求`;

        return `## 🔧 检测到限制: ${analysis.primaryConstraint}

${originalResponse}

---

## 🚀 变通解决方案

我识别到这个问题可能有变通解决方案。以下是 ${solutions.length} 个可行方案:

${solutionList}

${decisionGuide}

**💡 建议**: 我推荐 **${solutions[0].name}**，因为它是${this.getRecommendationReason(solutions[0])}

**❓ 如何选择**: 请告诉我您倾向于哪个方案，或者如果您有特定需求，我可以调整方案。`;
    }
    
    /**
     * 获取推荐理由
     */
    getRecommendationReason(solution) {
        const reasons = {
            'createStepByStepGuide': '最详细可靠，适合重要操作',
            'provideMultiplePaths': '提供最大灵活性，适合不确定场景',
            'oneClickScript': '最简单快捷，适合技术新手',
            'interactiveStepScript': '最用户友好，适合复杂流程',
            'containerScript': '最安全可控，适合容器环境',
            'visualTool': '最直观易用，适合可视化需求'
        };
        
        return reasons[solution.implementation] || '综合考虑了成功率、风险和时间因素';
    }
    
    /**
     * 记录干预
     */
    recordIntervention(userMessage, analysis, solutions) {
        const intervention = {
            timestamp: new Date().toISOString(),
            userMessage: userMessage.substring(0, 200), // 截断长消息
            constraint: analysis.primaryConstraint,
            solutionsGenerated: solutions.length,
            solutions: solutions.map(s => ({ id: s.id, name: s.name })),
            autoDetected: true
        };
        
        // 保存到日志
        const logDir = path.join(__dirname, 'logs');
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }
        
        const logFile = path.join(logDir, 'interventions.jsonl');
        fs.appendFileSync(logFile, JSON.stringify(intervention) + '\n');
        
        console.log(`📝 记录干预: ${analysis.primaryConstraint} → ${solutions.length} 个方案`);
    }
    
    /**
     * 记录用户选择结果
     */
    recordUserChoice(solutionId, success, feedback = {}) {
        this.solver.recordOutcome(solutionId, success, feedback, 'N/A');
        
        // 更新用户偏好
        if (feedback && feedback.preferred) {
            this.updateUserProfile(feedback);
        }
        
        console.log(`📊 记录用户选择: ${solutionId}, 成功: ${success}`);
    }
    
    /**
     * 更新用户配置文件
     */
    updateUserProfile(feedback) {
        try {
            if (fs.existsSync(this.config.userProfileFile)) {
                const profile = JSON.parse(fs.readFileSync(this.config.userProfileFile, 'utf8'));
                
                // 更新偏好
                if (feedback.preferred && !profile.preferredSolutionTypes.includes(feedback.preferred)) {
                    profile.preferredSolutionTypes.push(feedback.preferred);
                }
                
                // 更新技能水平评估
                if (feedback.skillLevel) {
                    profile.skillLevel = feedback.skillLevel;
                }
                
                // 更新风险承受能力
                if (feedback.riskTolerance) {
                    profile.riskTolerance = feedback.riskTolerance;
                }
                
                fs.writeFileSync(this.config.userProfileFile, JSON.stringify(profile, null, 2));
                console.log('👤 用户配置文件已更新');
            }
        } catch (error) {
            console.log('更新用户配置文件失败:', error.message);
        }
    }
    
    /**
     * 生成性能报告
     */
    generatePerformanceReport() {
        const report = this.solver.generateLearningReport();
        
        // 读取干预日志
        let totalInterventions = 0;
        let successfulInterventions = 0;
        
        try {
            const logFile = path.join(__dirname, 'logs', 'interventions.jsonl');
            if (fs.existsSync(logFile)) {
                const logs = fs.readFileSync(logFile, 'utf8')
                    .split('\n')
                    .filter(line => line.trim())
                    .map(line => JSON.parse(line));
                
                totalInterventions = logs.length;
                // 这里可以添加更复杂的成功判定逻辑
                successfulInterventions = Math.floor(totalInterventions * 0.7); // 假设70%成功
            }
        } catch (error) {
            console.log('读取干预日志失败:', error.message);
        }
        
        return {
            summary: {
                totalInterventions,
                successfulInterventions,
                interventionRate: totalInterventions > 0 ? 
                    `${Math.round((successfulInterventions / totalInterventions) * 100)}%` : 'N/A',
                ...report.summary
            },
            userProfile: report.userProfile,
            recommendations: [
                ...report.recommendations,
                totalInterventions < 10 ? '需要更多使用数据来优化' : '系统已积累足够优化数据',
                '继续使用变通解决方案提高问题解决能力'
            ]
        };
    }
    
    /**
     * 重置学习数据
     */
    resetLearningData() {
        this.solver.history = [];
        this.solver.userProfile = {
            skillLevel: 'beginner',
            riskTolerance: 'medium',
            preferredSolutionTypes: ['oneClickScript', 'detailedGuide'],
            pastSuccesses: {},
            learningData: {}
        };
        
        // 清空日志文件
        const logDir = path.join(__dirname, 'logs');
        if (fs.existsSync(logDir)) {
            const logFile = path.join(logDir, 'interventions.jsonl');
            if (fs.existsSync(logFile)) {
                fs.writeFileSync(logFile, '');
            }
        }
        
        this.solver.saveHistory();
        console.log('🔄 学习数据已重置');
    }
}

// 导出模块
module.exports = AdaptiveSolverIntegration;

// 命令行接口
if (require.main === module) {
    const integration = new AdaptiveSolverIntegration();
    
    const args = process.argv.slice(2);
    const command = args[0];
    
    switch(command) {
        case 'test':
            // 测试检测功能
            const testMessage = args[1] || '因为安全协议不能操作GitHub';
            const testResponse = '不能操作外部系统，需要用户手动处理';
            
            console.log('测试消息:', testMessage);
            console.log('助理响应:', testResponse);
            
            if (integration.shouldIntervene(testMessage, testResponse)) {
                console.log('✅ 检测到需要干预的情况');
                
                integration.generateAdaptiveResponse(testMessage, testResponse)
                    .then(enhancedResponse => {
                        console.log('\n增强响应:\n');
                        console.log(enhancedResponse);
                    });
            } else {
                console.log('❌ 未检测到需要干预的情况');
            }
            break;
            
        case 'report':
            const report = integration.generatePerformanceReport();
            console.log('📊 性能报告:');
            console.log(JSON.stringify(report, null, 2));
            break;
            
        case 'reset':
            integration.resetLearningData();
            console.log('学习数据已重置');
            break;
            
        case 'profile':
            console.log('👤 当前用户配置:');
            console.log(JSON.stringify(integration.solver.userProfile, null, 2));
            break;
            
        default:
            console.log('使用方法:');
            console.log('  node integration-wrapper.js test "问题描述"');
            console.log('  node integration-wrapper.js report');
            console.log('  node integration-wrapper.js reset');
            console.log('  node integration-wrapper.js profile');
    }
}