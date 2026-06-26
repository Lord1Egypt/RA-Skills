/**
 * 公共环境变量处理模块
 * 
 * 提供统一的 .env 文件加载和 API Key 获取功能
 */

const fs = require('fs');
const path = require('path');

const ENV_API_KEY = 'BAINIU_API_KEY';

/**
 * 查找 .env 文件路径
 * 从当前脚本所在目录开始，逐级向上遍历父目录（最多5层）
 * @returns {string|null} .env 文件路径，未找到返回 null
 */
function getEnvFilePath() {
    let currentDir = __dirname;
    
    for (let i = 0; i < 5; i++) {
        const envPath = path.join(currentDir, '.env');
        if (fs.existsSync(envPath)) {
            return envPath;
        }
        const parentDir = path.dirname(currentDir);
        if (parentDir === currentDir) {
            break;
        }
        currentDir = parentDir;
    }
    
    const defaultPath = path.join(__dirname, '..', '.env');
    if (fs.existsSync(defaultPath)) {
        return defaultPath;
    }
    
    return null;
}

/**
 * 从 .env 文件加载环境变量
 * @param {string} envPath - .env 文件路径
 */
function loadEnvFile(envPath) {
    if (!fs.existsSync(envPath)) {
        return;
    }
    
    const content = fs.readFileSync(envPath, 'utf-8');
    const lines = content.split('\n');
    
    for (const line of lines) {
        const trimmedLine = line.trim();
        
        if (trimmedLine === '' || trimmedLine.startsWith('#')) {
            continue;
        }
        
        const eqIndex = trimmedLine.indexOf('=');
        if (eqIndex === -1) {
            continue;
        }
        
        const key = trimmedLine.substring(0, eqIndex).trim();
        let value = trimmedLine.substring(eqIndex + 1).trim();
        
        if ((value.startsWith('"') && value.endsWith('"')) ||
            (value.startsWith("'") && value.endsWith("'"))) {
            value = value.slice(1, -1);
        }
        
        if (!process.env[key]) {
            process.env[key] = value;
        }
    }
}

/**
 * 获取 API Key
 * 优先从系统环境变量获取，不存在则从 .env 文件加载
 * @returns {string|null} API Key
 */
function getAPIKey() {
    if (process.env[ENV_API_KEY]) {
        return process.env[ENV_API_KEY];
    }
    
    const envPath = getEnvFilePath();
    if (envPath) {
        loadEnvFile(envPath);
    }
    
    return process.env[ENV_API_KEY] || null;
}

/**
 * 打印 API Key 配置指南
 */
function printAPIKeyConfigGuide() {
    console.log('API Key 未配置');
    console.log();
    console.log('请通过以下方式之一配置 API Key:');
    console.log();
    console.log('  方式1: 在.env文件中配置（推荐）');
    console.log('    在技能目录下创建或编辑 .env 文件：');
    console.log(`    ${ENV_API_KEY}=your_api_key_here`);
    console.log();
    console.log('  方式2: 设置系统环境变量');
    console.log(`    Windows (CMD): set ${ENV_API_KEY}=your_api_key_here`);
    console.log(`    Windows (PowerShell): $env:${ENV_API_KEY}="your_api_key_here"`);
    console.log(`    Linux/Mac: export ${ENV_API_KEY}=your_api_key_here`);
    console.log();
    console.log('配置优先级: 系统环境变量 > .env文件');
    console.log();
}

module.exports = {
    ENV_API_KEY,
    getEnvFilePath,
    loadEnvFile,
    getAPIKey,
    printAPIKeyConfigGuide
};
