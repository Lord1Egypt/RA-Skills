#!/usr/bin/env node
/**
 * Agent Config Validator - OpenClaw 集成测试脚本
 * 
 * 此脚本用于在 OpenClaw 环境中测试配置验证器技能
 * 可以通过 OpenClaw 的 Agent 调用
 */

const { execSync } = require('child_process');
const path = require('path');

// 获取 OpenClaw 根目录
const openclawRoot = process.env.OPENCLAW_ROOT || 'D:\\OpenClaw';
const validatorPath = path.join(openclawRoot, '.openclaw', 'skills', 'agent-config-validator', 'src', 'validator.js');

console.log('🧪 Agent Config Validator - OpenClaw 集成测试\n');
console.log(`OpenClaw 根目录: ${openclawRoot}`);
console.log(`验证器路径: ${validatorPath}\n`);

try {
    // 运行验证器
    const result = execSync(
        `node "${validatorPath}" --verbose`,
        { 
            cwd: openclawRoot, 
            encoding: 'utf-8',
            stdio: 'inherit'
        }
    );
    
    console.log('\n✅ 测试完成！');
    process.exit(0);
} catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    process.exit(1);
}
