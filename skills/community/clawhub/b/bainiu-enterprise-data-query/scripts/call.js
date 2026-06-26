/**
 * 企业查询工具调用脚本
 * 
 * 用法:
 *   node call.js <tool-id> 参数1=值1 参数2=值2 ...
 * 
 * 示例:
 *   node call.js A002 query="小米"
 *   node call.js A003_A3 entid="xxx" pindex=1 psize=20
 * 
 * 环境变量:
 *   BAINIU_API_KEY - API Key（必需）
 */

const https = require('https');
const { URL } = require('url');
const { getAPIKey, printAPIKeyConfigGuide, ENV_API_KEY } = require('./env');

const API_HOST = 'https://skillapi.bainiudata.com/';
const API_TOOL_CALL_URL = 'ent_query_skill/call_tool/';
const HEADER_API_KEY = 'X-API-Key';
const REQUEST_TIMEOUT = 30000;

/**
 * 解析命令行参数
 * @param {string[]} args - 命令行参数数组
 * @returns {{toolID: string, params: Object}} 解析结果
 */
function parseArguments(args) {
    if (args.length < 1) {
        throw new Error('缺少 tool-id 参数');
    }
    
    const toolID = args[0];
    const params = {};
    
    for (let i = 1; i < args.length; i++) {
        const arg = args[i];
        const eqIndex = arg.indexOf('=');
        if (eqIndex === -1) {
            throw new Error(`参数格式错误 '${arg}'，期望 key=value 格式`);
        }
        const key = arg.substring(0, eqIndex);
        const value = arg.substring(eqIndex + 1);
        params[key] = value;
    }
    
    return { toolID, params };
}

/**
 * 调用企业查询工具
 * @param {string} apiKey - API Key
 * @param {string} toolID - 工具ID
 * @param {Object} params - 工具参数
 * @returns {Promise<string>} 格式化的 JSON 结果
 */
function callTool(apiKey, toolID, params) {
    return new Promise((resolve, reject) => {
        const formData = new URLSearchParams();
        formData.append('tool_id', toolID);
        for (const [key, value] of Object.entries(params)) {
            formData.append(key, value);
        }
        
        const fullURL = new URL(API_TOOL_CALL_URL, API_HOST);
        
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
    console.log('  node call.js <tool-id> 参数1=值1 参数2=值2 ...');
    console.log();
    console.log('参数说明:');
    console.log('  tool-id    工具ID（必需）');
    console.log('  参数       key=value 格式的工具参数');
    console.log();
    console.log('示例:');
    console.log('  node call.js A002 query="小米"');
    console.log('  node call.js A003_A3 entid="xxx" pindex=1 psize=20');
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
    
    if (args[0] === '-h' || args[0] === '--help') {
        printUsage();
        process.exit(0);
    }
    
    const apiKey = getAPIKey();
    if (!apiKey) {
        printAPIKeyConfigGuide();
        process.exit(1);
    }
    
    try {
        const { toolID, params } = parseArguments(args);
        const result = await callTool(apiKey, toolID, params);
        console.log(result);
    } catch (e) {
        console.error(`错误: ${e.message}`);
        process.exit(1);
    }
}

main();
