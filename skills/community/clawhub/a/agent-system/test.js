/**
 * Agent System - 测试脚本
 */

import { dispatch } from './src/orchestrator.js';

const testCases = [
    { name: '简单任务', input: '今天天气怎么样' },
    { name: '复杂任务 - 销售分析', input: '帮我分析销售下滑的原因' },
    { name: '中等任务 - 写邮件', input: '帮我写一封道歉邮件' }
];

async function runTests() {
    console.log('='.repeat(50));
    console.log('Agent System 测试开始');
    console.log('='.repeat(50));
    
    for (const test of testCases) {
        console.log(`\n📝 测试: ${test.name}`);
        console.log('-'.repeat(40));
        
        try {
            const result = await dispatch(test.input);
            
            console.log('✅ 成功');
            console.log(`   Intent: ${result.plan?.intent}`);
            console.log(`   Complexity: ${result.plan?.complexity}`);
            console.log(`   Tasks: ${result.plan?.tasks?.length || 1}`);
            console.log(`   Tokens: ${result.metrics?.tokens}`);
            console.log(`   Truncated: ${result.metrics?.truncated}`);
            console.log(`   Quality: ${result.metrics?.quality_score}`);
            console.log(`\n   Content: ${result.content?.substring(0, 80)}...`);
        } catch (error) {
            console.log('❌ 失败:', error.message);
        }
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('测试完成');
    console.log('='.repeat(50));
}

runTests().catch(console.error);
