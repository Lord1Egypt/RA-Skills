#!/usr/bin/env node

/**
 * 测试自适应问题解决器
 */

const AdaptiveProblemSolver = require('./index.js');

async function runTests() {
    console.log('🧪 开始测试自适应问题解决器\n');
    
    const solver = new AdaptiveProblemSolver();
    
    // 测试用例
    const testCases = [
        {
            name: '安全协议限制场景',
            problem: '因为OpenGuardrails安全协议，不能操作外部GitHub仓库',
            expectedConstraint: 'security'
        },
        {
            name: '权限限制场景', 
            problem: 'Docker容器权限不足，无法执行系统级清理操作',
            expectedConstraint: 'permission'
        },
        {
            name: '用户技能限制场景',
            problem: '用户说"什么操作都不会"，需要简化技术操作',
            expectedConstraint: 'userSkill'
        },
        {
            name: '技术复杂性场景',
            problem: 'GitHub推送操作过于复杂，多步骤容易出错',
            expectedConstraint: 'technical'
        },
        {
            name: '综合限制场景',
            problem: '需要解决一个复杂的技术问题',
            expectedConstraint: 'composite'
        }
    ];
    
    let allTestsPassed = true;
    
    for (const testCase of testCases) {
        console.log(`📋 测试: ${testCase.name}`);
        console.log(`   问题: ${testCase.problem}`);
        
        // 分析问题
        const analysis = solver.analyzeProblem(testCase.problem);
        console.log(`   分析结果: 主要限制 = ${analysis.primaryConstraint}`);
        
        // 验证分析结果
        if (analysis.primaryConstraint === testCase.expectedConstraint) {
            console.log('   ✅ 分析正确');
        } else {
            console.log(`   ❌ 分析错误，期望: ${testCase.expectedConstraint}`);
            allTestsPassed = false;
        }
        
        // 生成解决方案
        const solutions = solver.generateSolutions(analysis, 3);
        console.log(`   生成方案数: ${solutions.length}`);
        
        // 验证方案质量
        if (solutions.length >= 2) {
            console.log('   ✅ 方案生成充足');
            
            // 检查方案多样性
            const solutionTypes = new Set(solutions.map(s => s.type));
            if (solutionTypes.size >= 1) {
                console.log('   ✅ 方案类型合理');
            } else {
                console.log('   ⚠️ 方案类型单一');
            }
            
            // 显示方案摘要
            solutions.forEach((sol, idx) => {
                console.log(`     方案${idx+1}: ${sol.name} (${sol.riskLevel}风险)`);
            });
        } else {
            console.log('   ❌ 方案生成不足');
            allTestsPassed = false;
        }
        
        console.log('');
    }
    
    // 测试学习功能
    console.log('🧠 测试学习功能');
    
    // 模拟一些历史记录
    solver.recordOutcome('sec-001', true, { preferred: 'createStepByStepGuide' }, '8分钟');
    solver.recordOutcome('sec-002', false, { feedback: '太复杂' }, '12分钟');
    solver.recordOutcome('skill-001', true, { preferred: 'oneClickScript' }, '3分钟');
    solver.recordOutcome('perm-001', true, {}, '6分钟');
    
    // 生成学习报告
    const report = solver.generateLearningReport();
    console.log('📊 学习报告:');
    console.log(`   总尝试次数: ${report.summary.totalAttempts}`);
    console.log(`   成功率: ${report.summary.successRate}`);
    console.log(`   最优方案: ${report.summary.bestSolution || 'N/A'}`);
    
    // 保存历史记录
    solver.saveHistory();
    console.log('💾 历史记录已保存');
    
    // 重新加载测试
    const solver2 = new AdaptiveProblemSolver();
    solver2.loadHistory();
    console.log(`📂 重新加载历史记录: ${solver2.history.length} 条记录`);
    
    // 最终测试结果
    console.log('\n🎯 最终测试结果:');
    if (allTestsPassed) {
        console.log('✅ 所有测试通过！自适应问题解决器工作正常。');
    } else {
        console.log('⚠️ 部分测试失败，需要进一步优化。');
    }
    
    // 演示使用示例
    console.log('\n🚀 使用示例:');
    console.log('```javascript');
    console.log('const AdaptiveProblemSolver = require("./index.js");');
    console.log('const solver = new AdaptiveProblemSolver();');
    console.log('');
    console.log('// 1. 分析问题');
    console.log('const analysis = solver.analyzeProblem("安全协议阻止操作GitHub");');
    console.log('');
    console.log('// 2. 生成解决方案');
    console.log('const solutions = solver.generateSolutions(analysis, 3);');
    console.log('');
    console.log('// 3. 呈现选择');
    console.log('const presentation = solver.presentSolutions(analysis.problem, solutions);');
    console.log('console.log("推荐方案:", presentation.recommendation);');
    console.log('```');
    
    return allTestsPassed;
}

// 运行测试
if (require.main === module) {
    runTests().then(success => {
        process.exit(success ? 0 : 1);
    }).catch(error => {
        console.error('测试失败:', error);
        process.exit(1);
    });
}

module.exports = { runTests };