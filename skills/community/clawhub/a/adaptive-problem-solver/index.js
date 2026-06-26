#!/usr/bin/env node

/**
 * Adaptive Problem Solver - 智能变通问题解决器
 * 
 * 目标：在安全协议限制下，提供多种变通解决方案
 * 而不是简单地说"不能做"或"需要用户手动处理"
 */

const fs = require('fs');
const path = require('path');

class AdaptiveProblemSolver {
    constructor() {
        this.solutionLibrary = {
            // 安全协议限制的变通方案
            securityConstraints: [
                {
                    id: 'sec-001',
                    name: '详细用户指南',
                    description: '创建分步执行指南，用户可照做',
                    riskLevel: 'low',
                    implementation: 'createStepByStepGuide',
                    successRate: 0.85,
                    avgTime: '5-15分钟'
                },
                {
                    id: 'sec-002', 
                    name: '本地模拟测试',
                    description: '在安全环境中模拟外部操作',
                    riskLevel: 'low',
                    implementation: 'createLocalSimulation',
                    successRate: 0.70,
                    avgTime: '2-5分钟'
                },
                {
                    id: 'sec-003',
                    name: '多路径选择',
                    description: '提供3-4种不同技术路径',
                    riskLevel: 'low',
                    implementation: 'provideMultiplePaths',
                    successRate: 0.90,
                    avgTime: '3-10分钟'
                },
                {
                    id: 'sec-004',
                    name: '渐进式实施',
                    description: '分阶段逐步实施，降低风险',
                    riskLevel: 'low',
                    implementation: 'phasedImplementation',
                    successRate: 0.80,
                    avgTime: '10-30分钟'
                }
            ],
            
            // 权限限制的变通方案
            permissionConstraints: [
                {
                    id: 'perm-001',
                    name: '宿主机命令',
                    description: '提供在宿主机执行的命令',
                    riskLevel: 'medium',
                    implementation: 'hostMachineCommands',
                    successRate: 0.75,
                    avgTime: '3-8分钟'
                },
                {
                    id: 'perm-002',
                    name: '容器内脚本',
                    description: '创建容器内可执行的脚本',
                    riskLevel: 'low',
                    implementation: 'containerScript',
                    successRate: 0.85,
                    avgTime: '2-5分钟'
                },
                {
                    id: 'perm-003',
                    name: '环境变量传递',
                    description: '通过环境变量传递必要信息',
                    riskLevel: 'low',
                    implementation: 'envVariableSolution',
                    successRate: 0.70,
                    avgTime: '1-3分钟'
                }
            ],
            
            // 用户技能限制的变通方案
            userSkillConstraints: [
                {
                    id: 'skill-001',
                    name: '一键脚本',
                    description: '复制粘贴即可用的完整脚本',
                    riskLevel: 'low',
                    implementation: 'oneClickScript',
                    successRate: 0.95,
                    avgTime: '1-2分钟'
                },
                {
                    id: 'skill-002',
                    name: '可视化工具',
                    description: '创建简单的网页工具',
                    riskLevel: 'low',
                    implementation: 'visualTool',
                    successRate: 0.80,
                    avgTime: '5-15分钟'
                },
                {
                    id: 'skill-003',
                    name: '屏幕录制指导',
                    description: '提供屏幕录制演示',
                    riskLevel: 'low',
                    implementation: 'screenRecording',
                    successRate: 0.90,
                    avgTime: '3-7分钟'
                }
            ],
            
            // 技术复杂性的变通方案
            technicalConstraints: [
                {
                    id: 'tech-001',
                    name: '分步交互脚本',
                    description: '交互式分步执行脚本',
                    riskLevel: 'low',
                    implementation: 'interactiveStepScript',
                    successRate: 0.88,
                    avgTime: '5-12分钟'
                },
                {
                    id: 'tech-002',
                    name: '错误自动恢复',
                    description: '包含错误检测和自动恢复',
                    riskLevel: 'low',
                    implementation: 'autoRecoveryScript',
                    successRate: 0.82,
                    avgTime: '3-8分钟'
                },
                {
                    id: 'tech-003',
                    name: '进度保存恢复',
                    description: '支持中断后继续执行',
                    riskLevel: 'low',
                    implementation: 'progressSaveRestore',
                    successRate: 0.78,
                    avgTime: '4-10分钟'
                }
            ]
        };
        
        this.userProfile = {
            skillLevel: 'beginner', // beginner, intermediate, advanced
            riskTolerance: 'medium', // low, medium, high
            preferredSolutionTypes: ['oneClickScript', 'detailedGuide'],
            pastSuccesses: {},
            learningData: {}
        };
        
        this.history = [];
    }
    
    /**
     * 分析问题并识别限制类型
     */
    analyzeProblem(problemDescription, context = {}) {
        const analysis = {
            problem: problemDescription,
            constraints: [],
            primaryConstraint: null,
            severity: 'medium'
        };
        
        // 检测安全协议限制
        if (problemDescription.includes('安全协议') || 
            problemDescription.includes('OpenGuardrails') ||
            problemDescription.includes('不能操作外部系统')) {
            analysis.constraints.push('security');
            analysis.primaryConstraint = 'security';
        }
        
        // 检测权限限制
        if (problemDescription.includes('权限') ||
            problemDescription.includes('Docker') ||
            problemDescription.includes('容器') ||
            problemDescription.includes('不能执行')) {
            analysis.constraints.push('permission');
            if (!analysis.primaryConstraint) analysis.primaryConstraint = 'permission';
        }
        
        // 检测用户技能限制
        if (problemDescription.includes('不会操作') ||
            problemDescription.includes('什么操作都不会') ||
            problemDescription.includes('技术能力') ||
            problemDescription.includes('复杂')) {
            analysis.constraints.push('userSkill');
            if (!analysis.primaryConstraint) analysis.primaryConstraint = 'userSkill';
        }
        
        // 检测技术复杂性限制
        if (problemDescription.includes('复杂') ||
            problemDescription.includes('多步骤') ||
            problemDescription.includes('容易出错') ||
            problemDescription.includes('技术要求高')) {
            analysis.constraints.push('technical');
            if (!analysis.primaryConstraint) analysis.primaryConstraint = 'technical';
        }
        
        // 如果没有检测到特定限制，默认为综合限制
        if (analysis.constraints.length === 0) {
            analysis.constraints = ['security', 'permission', 'userSkill', 'technical'];
            analysis.primaryConstraint = 'composite';
        }
        
        return analysis;
    }
    
    /**
     * 生成变通解决方案
     */
    generateSolutions(problemAnalysis, count = 3) {
        const solutions = [];
        const primaryType = problemAnalysis.primaryConstraint;
        
        // 获取主要限制类型的解决方案
        let candidateSolutions = [];
        switch(primaryType) {
            case 'security':
                candidateSolutions = this.solutionLibrary.securityConstraints;
                break;
            case 'permission':
                candidateSolutions = this.solutionLibrary.permissionConstraints;
                break;
            case 'userSkill':
                candidateSolutions = this.solutionLibrary.userSkillConstraints;
                break;
            case 'technical':
                candidateSolutions = this.solutionLibrary.technicalConstraints;
                break;
            default:
                // 复合类型，混合所有方案
                candidateSolutions = [
                    ...this.solutionLibrary.securityConstraints,
                    ...this.solutionLibrary.permissionConstraints,
                    ...this.solutionLibrary.userSkillConstraints,
                    ...this.solutionLibrary.technicalConstraints
                ];
        }
        
        // 根据用户偏好和成功率排序
        candidateSolutions.sort((a, b) => {
            // 优先用户偏好的方案类型
            const aPreference = this.userProfile.preferredSolutionTypes.includes(a.implementation) ? 1 : 0;
            const bPreference = this.userProfile.preferredSolutionTypes.includes(b.implementation) ? 1 : 0;
            
            if (aPreference !== bPreference) return bPreference - aPreference;
            
            // 然后按成功率排序
            return b.successRate - a.successRate;
        });
        
        // 选择前N个方案
        const selected = candidateSolutions.slice(0, Math.min(count, candidateSolutions.length));
        
        // 转换为完整方案对象
        selected.forEach((solution, index) => {
            solutions.push({
                id: solution.id,
                name: solution.name,
                description: solution.description,
                type: primaryType,
                riskLevel: solution.riskLevel,
                implementation: solution.implementation,
                estimatedTime: solution.avgTime,
                successProbability: solution.successRate,
                priority: index + 1,
                steps: this.generateImplementationSteps(solution.implementation, problemAnalysis.problem)
            });
        });
        
        return solutions;
    }
    
    /**
     * 生成实施方案步骤
     */
    generateImplementationSteps(implementationType, problem) {
        const steps = [];
        
        switch(implementationType) {
            case 'createStepByStepGuide':
                steps.push(
                    '分析问题并分解为具体步骤',
                    '为每个步骤创建详细说明',
                    '提供必要的命令和代码示例',
                    '包含错误处理和故障排除',
                    '创建验证步骤确保成功'
                );
                break;
                
            case 'provideMultiplePaths':
                steps.push(
                    '识别3-4种不同的技术路径',
                    '评估每种路径的优缺点',
                    '提供路径选择决策树',
                    '为每种路径创建实施指南',
                    '设置回退机制'
                );
                break;
                
            case 'oneClickScript':
                steps.push(
                    '创建完整的可执行脚本',
                    '添加详细的注释说明',
                    '包含错误检测和处理',
                    '提供简单的使用说明',
                    '创建测试用例验证功能'
                );
                break;
                
            case 'interactiveStepScript':
                steps.push(
                    '设计交互式命令行界面',
                    '实现分步执行逻辑',
                    '添加进度显示和状态反馈',
                    '包含步骤跳过和回退功能',
                    '实现自动保存和恢复'
                );
                break;
                
            default:
                steps.push(
                    '分析具体实施需求',
                    '设计解决方案架构',
                    '创建实施计划',
                    '开发必要工具或脚本',
                    '测试和验证解决方案'
                );
        }
        
        return steps;
    }
    
    /**
     * 呈现解决方案选择
     */
    presentSolutions(problem, solutions) {
        const presentation = {
            problem: problem,
            analysis: `识别到主要限制: ${solutions[0].type}`,
            recommendation: `推荐方案: ${solutions[0].name}`,
            options: solutions.map(sol => ({
                name: sol.name,
                description: sol.description,
                risk: sol.riskLevel,
                time: sol.estimatedTime,
                success: `${Math.round(sol.successProbability * 100)}%`,
                steps: sol.steps.length
            })),
            decisionGuide: this.generateDecisionGuide(solutions)
        };
        
        return presentation;
    }
    
    /**
     * 生成决策指南
     */
    generateDecisionGuide(solutions) {
        const guide = {
            quickChoice: '如果您想要最快最简单的方案，选择方案1',
            balancedChoice: '如果您想要平衡风险和效果，选择方案2',
            robustChoice: '如果您需要最可靠的方案，选择方案3',
            factors: [
                '时间紧迫程度',
                '技术舒适度',
                '风险承受能力',
                '长期维护需求'
            ]
        };
        
        return guide;
    }
    
    /**
     * 记录执行结果用于学习
     */
    recordOutcome(solutionId, success, userFeedback, executionTime) {
        this.history.push({
            solutionId,
            success,
            feedback: userFeedback,
            executionTime,
            timestamp: new Date().toISOString()
        });
        
        // 更新用户偏好
        if (userFeedback && userFeedback.preferred) {
            if (!this.userProfile.preferredSolutionTypes.includes(userFeedback.preferred)) {
                this.userProfile.preferredSolutionTypes.push(userFeedback.preferred);
            }
        }
        
        // 保存历史记录
        this.saveHistory();
    }
    
    /**
     * 保存历史记录到文件
     */
    saveHistory() {
        const dataDir = path.join(__dirname, 'data');
        if (!fs.existsSync(dataDir)) {
            fs.mkdirSync(dataDir, { recursive: true });
        }
        
        const historyFile = path.join(dataDir, 'solver-history.json');
        const profileFile = path.join(dataDir, 'user-profile.json');
        
        fs.writeFileSync(historyFile, JSON.stringify(this.history, null, 2));
        fs.writeFileSync(profileFile, JSON.stringify(this.userProfile, null, 2));
    }
    
    /**
     * 加载历史记录
     */
    loadHistory() {
        try {
            const historyFile = path.join(__dirname, 'data', 'solver-history.json');
            const profileFile = path.join(__dirname, 'data', 'user-profile.json');
            
            if (fs.existsSync(historyFile)) {
                this.history = JSON.parse(fs.readFileSync(historyFile, 'utf8'));
            }
            
            if (fs.existsSync(profileFile)) {
                this.userProfile = JSON.parse(fs.readFileSync(profileFile, 'utf8'));
            }
        } catch (error) {
            console.log('加载历史记录失败，使用默认配置:', error.message);
        }
    }
    
    /**
     * 生成学习报告
     */
    generateLearningReport() {
        const totalAttempts = this.history.length;
        if (totalAttempts === 0) {
            return {
                message: '尚无足够数据生成学习报告',
                recommendations: ['继续使用系统积累数据']
            };
        }
        
        const successes = this.history.filter(h => h.success).length;
        const successRate = successes / totalAttempts;
        
        // 分析最成功的方案类型
        const solutionStats = {};
        this.history.forEach(h => {
            const solutionId = h.solutionId;
            if (!solutionStats[solutionId]) {
                solutionStats[solutionId] = { attempts: 0, successes: 0 };
            }
            solutionStats[solutionId].attempts++;
            if (h.success) solutionStats[solutionId].successes++;
        });
        
        // 找出最优方案
        let bestSolution = null;
        let bestSuccessRate = 0;
        
        Object.entries(solutionStats).forEach(([solutionId, stats]) => {
            const rate = stats.successes / stats.attempts;
            if (rate > bestSuccessRate && stats.attempts >= 3) {
                bestSuccessRate = rate;
                bestSolution = solutionId;
            }
        });
        
        return {
            summary: {
                totalAttempts,
                successRate: `${Math.round(successRate * 100)}%`,
                bestSolution,
                bestSuccessRate: bestSolution ? `${Math.round(bestSuccessRate * 100)}%` : 'N/A'
            },
            userProfile: {
                skillLevel: this.userProfile.skillLevel,
                preferredSolutions: this.userProfile.preferredSolutionTypes,
                riskTolerance: this.userProfile.riskTolerance
            },
            recommendations: [
                bestSolution ? `优先使用方案: ${bestSolution}` : '继续测试不同方案',
                successRate > 0.8 ? '当前策略有效，继续保持' : '考虑调整解决方案策略',
                '定期审查和更新用户偏好'
            ]
        };
    }
}

// 导出模块
module.exports = AdaptiveProblemSolver;

// 如果直接运行，提供命令行接口
if (require.main === module) {
    const solver = new AdaptiveProblemSolver();
    solver.loadHistory();
    
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.log('使用方法:');
        console.log('  node index.js "问题描述"');
        console.log('示例:');
        console.log('  node index.js "因为安全协议不能操作GitHub仓库"');
        process.exit(0);
    }
    
    const problem = args.join(' ');
    console.log('🔍 分析问题:', problem);
    
    const analysis = solver.analyzeProblem(problem);
    console.log('📊 问题分析:', analysis);
    
    const solutions = solver.generateSolutions(analysis);
    console.log('🚀 生成的解决方案:');
    
    solutions.forEach((sol, index) => {
        console.log(`\n方案 ${index + 1}: ${sol.name}`);
        console.log(`   描述: ${sol.description}`);
        console.log(`   风险: ${sol.riskLevel}`);
        console.log(`   预计时间: ${sol.estimatedTime}`);
        console.log(`   成功率: ${Math.round(sol.successProbability * 100)}%`);
    });
    
    console.log('\n📋 决策指南:');
    const guide = solver.generateDecisionGuide(solutions);
    console.log('  快速选择:', guide.quickChoice);
    console.log('  平衡选择:', guide.balancedChoice);
    console.log('  稳健选择:', guide.robustChoice);
}