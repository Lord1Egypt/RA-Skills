/**
 * 企业查询工具查找脚本
 * 
 * 用法:
 *   node find_tool.js "查询意图描述"
 * 
 * 示例:
 *   node find_tool.js "企业模糊搜索"
 *   node find_tool.js "查询企业工商信息"
 * 
 * 环境变量:
 *   BAINIU_API_KEY - API Key（必需）
 */

const https = require('https');
const { URL } = require('url');
const { getAPIKey, printAPIKeyConfigGuide, ENV_API_KEY } = require('./env');

const API_HOST = 'https://skillapi.bainiudata.com/';
const FOUND_TOOL_PATH = 'ent_query_skill/find_tool/';
const HEADER_API_KEY = 'X-API-Key';
const REQUEST_TIMEOUT = 30000;

/**
 * 查找匹配的工具
 * @param {string} apiKey - API Key
 * @param {string} keyword - 查询意图描述
 * @returns {Promise<string>} 格式化的 JSON 结果
 */
function findTools(apiKey, keyword) {
    return new Promise((resolve, reject) => {
        const formData = new URLSearchParams();
        formData.append('keyword', keyword);
        
        const fullURL = new URL(FOUND_TOOL_PATH, API_HOST);
        
        const options = {
            hostname: fullURL.hostname,
            port: 443,
            path: fullURL.pathname,
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                [HEADER_API_KEY]: apiKey
            },
            timeout: REQUEST_TIMEOUT
        };
        
        const req = https.request(options, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    const jsonData = JSON.parse(data);
                    resolve(JSON.stringify(jsonData, null, 2));
                } catch (e) {
                    reject(new Error(`解析响应失败: ${e.message}`));
                }
            });
        });
        
        req.on('error', (e) => {
            reject(new Error(`请求失败: ${e.message}`));
        });
        
        req.on('timeout', () => {
            req.destroy();
            reject(new Error('请求超时'));
        });
        
        req.write(formData.toString());
        req.end();
    });
}

/**
 * 打印使用说明
 */
function printUsage() {
    console.log('用法:');
    console.log();
    console.log('  node find_tool.js "查询意图描述"');
    console.log();
    console.log('示例:');
    console.log('  node find_tool.js "企业模糊搜索"');
    console.log('  node find_tool.js "企业股东"');
    console.log('  node find_tool.js "企业照面信息"');
    console.log();
    console.log('环境变量:');
    console.log(`  ${ENV_API_KEY} - API Key（必需）`);
}

async function main() {
    const args = process.argv.slice(2);
    
    if (args.length < 1) {
        printUsage();
        process.exit(1);
    }
    
    const keyword = args[0];
    
    if (keyword === '-h' || keyword === '--help') {
        printUsage();
        process.exit(0);
    }
    
    const apiKey = getAPIKey();
    if (!apiKey) {
        printAPIKeyConfigGuide();
        process.exit(1);
    }
    
    try {
        const result = await findTools(apiKey, keyword);
        console.log(result);
    } catch (e) {
        console.error(`错误: ${e.message}`);
        process.exit(1);
    }
}

main();
