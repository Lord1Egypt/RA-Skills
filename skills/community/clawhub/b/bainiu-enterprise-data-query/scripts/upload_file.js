/**
 * 企业查询文件检查与上传脚本
 *
 * 用法:
 *   node upload_file.js <txt文件路径>
 *
 * 示例:
 *   node upload_file.js data.txt
 *   node upload_file.js "C:\path\to\file.txt"
 *
 * 文件格式要求:
 *   - 必须为 .txt 文本文件
 *   - 每条数据单独占一行
 *   - 不允许空行或仅含空白字符的行
 *
 * 环境变量:
 *   BAINIU_API_KEY - API Key（必需）
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const { URL } = require('url');
const { getAPIKey, printAPIKeyConfigGuide, ENV_API_KEY } = require('./env');

const UPLOAD_API_URL = 'https://skillapi.bainiudata.com/ent_batch_export/batch_export/';
const HEADER_API_KEY = 'X-API-Key';
const REQUEST_TIMEOUT = 60000;
const MAX_FILE_SIZE = 5 * 1024 * 1024;
const MAX_LINE_LENGTH = 10000;
const MAX_LINE_COUNT = 10000;

/**
 * 校验文本文件
 * @param {string} filePath - 文件绝对路径
 * @returns {{valid: boolean, errors: string[], lineCount: number, lines: string[]}} 校验结果
 */
function validateFile(filePath) {
    const errors = [];

    if (!fs.existsSync(filePath)) {
        return { valid: false, errors: [`文件不存在: ${filePath}`], lineCount: 0, lines: [] };
    }

    const stat = fs.statSync(filePath);
    if (!stat.isFile()) {
        return { valid: false, errors: [`路径不是文件: ${filePath}`], lineCount: 0, lines: [] };
    }

    if (path.extname(filePath).toLowerCase() !== '.txt') {
        errors.push(`文件类型错误: 期望 .txt 文件，实际为 "${path.extname(filePath)}"`);
    }

    if (stat.size === 0) {
        errors.push('文件为空');
        return { valid: false, errors, lineCount: 0, lines: [] };
    }

    if (stat.size > MAX_FILE_SIZE) {
        errors.push(`文件过大: 文件大小 ${ (stat.size / 1024 / 1024).toFixed(2) }MB，超过限制 ${MAX_FILE_SIZE / 1024 / 1024}MB`);
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split(/\r?\n/);

    if (lines.length > 0 && lines[lines.length - 1] === '') {
        lines.pop();
    }

    if (lines.length > MAX_LINE_COUNT) {
        errors.push(`行数超限: 共 ${lines.length} 行，超过最大限制 ${MAX_LINE_COUNT} 行`);
    }

    const emptyLineNumbers = [];
    const whitespaceOnlyLineNumbers = [];
    const tooLongLineNumbers = [];

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const lineNum = i + 1;

        if (line === '') {
            emptyLineNumbers.push(lineNum);
        } else if (line.trim() === '') {
            whitespaceOnlyLineNumbers.push(lineNum);
        }

        if (line.length > MAX_LINE_LENGTH) {
            tooLongLineNumbers.push(lineNum);
        }
    }

    if (emptyLineNumbers.length > 0) {
        const display = emptyLineNumbers.length <= 20
            ? emptyLineNumbers.join(', ')
            : emptyLineNumbers.slice(0, 20).join(', ') + ` ... 等共 ${emptyLineNumbers.length} 行`;
        errors.push(`存在空行: 第 ${display} 行`);
    }

    if (whitespaceOnlyLineNumbers.length > 0) {
        const display = whitespaceOnlyLineNumbers.length <= 20
            ? whitespaceOnlyLineNumbers.join(', ')
            : whitespaceOnlyLineNumbers.slice(0, 20).join(', ') + ` ... 等共 ${whitespaceOnlyLineNumbers.length} 行`;
        errors.push(`存在仅含空白字符的行: 第 ${display} 行`);
    }

    if (tooLongLineNumbers.length > 0) {
        const display = tooLongLineNumbers.length <= 20
            ? tooLongLineNumbers.join(', ')
            : tooLongLineNumbers.slice(0, 20).join(', ') + ` ... 等共 ${tooLongLineNumbers.length} 行`;
        errors.push(`行内容过长（超过 ${MAX_LINE_LENGTH} 字符）: 第 ${display} 行`);
    }

    if (errors.length > 0) {
        return { valid: false, errors, lineCount: lines.length, lines: [] };
    }

    return { valid: true, errors: [], lineCount: lines.length, lines };
}

/**
 * 构建 multipart/form-data 请求体
 * @param {string} boundary - 分隔符
 * @param {string} fieldName - 表单字段名
 * @param {string} fileName - 文件名
 * @param {string|Buffer} fileContent - 文件内容
 * @returns {Buffer} 请求体 Buffer
 */
function buildMultipartBody(boundary, fieldName, fileName, fileContent) {
    const separator = `\r\n--${boundary}\r\n`;
    const closing = `\r\n--${boundary}--\r\n`;

    const header = `Content-Disposition: form-data; name="${fieldName}"; filename="${fileName}"\r\nContent-Type: text/plain\r\n\r\n`;

    const headerBuffer = Buffer.from(separator + header, 'utf-8');
    const bodyBuffer = Buffer.isBuffer(fileContent) ? fileContent : Buffer.from(fileContent, 'utf-8');
    const closingBuffer = Buffer.from(closing, 'utf-8');

    return Buffer.concat([headerBuffer, bodyBuffer, closingBuffer]);
}

/**
 * 上传文件到服务端
 * @param {string} apiKey - API Key
 * @param {string} filePath - 文件路径
 * @returns {Promise<string>} 格式化的 JSON 结果
 */
function uploadFile(apiKey, filePath) {
    return new Promise((resolve, reject) => {
        const fileName = path.basename(filePath);
        const fileContent = fs.readFileSync(filePath);

        const boundary = `----FormBoundary${Date.now()}`;
        const body = buildMultipartBody(boundary, 'file', fileName, fileContent);

        const fullURL = new URL(UPLOAD_API_URL);
        const isHTTPS = fullURL.protocol === 'https:';
        const requestModule = isHTTPS ? https : http;

        const options = {
            hostname: fullURL.hostname,
            port: fullURL.port || (isHTTPS ? 443 : 80),
            path: fullURL.pathname + fullURL.search,
            method: 'POST',
            headers: {
                'Content-Type': `multipart/form-data; boundary=${boundary}`,
                'Content-Length': body.length,
                [HEADER_API_KEY]: apiKey
            },
            timeout: REQUEST_TIMEOUT
        };

        const req = requestModule.request(options, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                try {
                    const jsonData = JSON.parse(data);
                    if (jsonData.result && jsonData.result.file_link) {
                        jsonData.result.file_link = encodeURI(jsonData.result.file_link);
                    }
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

        req.write(body);
        req.end();
    });
}

/**
 * 打印使用说明
 */
function printUsage() {
    console.log('用法:');
    console.log();
    console.log('  node upload_file.js <txt文件路径>');
    console.log();
    console.log('参数说明:');
    console.log('  txt文件路径    要上传的 .txt 文本文件路径（必需）');
    console.log();
    console.log('文件格式要求:');
    console.log('  - 必须为 .txt 文本文件');
    console.log('  - 每条数据单独占一行');
    console.log('  - 不允许空行或仅含空白字符的行');
    console.log(`  - 单行长度不超过 ${MAX_LINE_LENGTH} 字符`);
    console.log(`  - 总行数不超过 ${MAX_LINE_COUNT} 行`);
    console.log(`  - 文件大小不超过 ${MAX_FILE_SIZE / 1024 / 1024}MB`);
    console.log();
    console.log('示例:');
    console.log('  node upload_file.js data.txt');
    console.log('  node upload_file.js "C:\\path\\to\\file.txt"');
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

    const filePath = path.resolve(args[0]);

    const apiKey = getAPIKey();
    if (!apiKey) {
        printAPIKeyConfigGuide();
        process.exit(1);
    }

    try {
        const result = validateFile(filePath);

        if (!result.valid) {
            console.error('文件校验未通过:');
            for (const error of result.errors) {
                console.error(`  - ${error}`);
            }
            process.exit(1);
        }

        const response = await uploadFile(apiKey, filePath);
        console.log(response);
    } catch (e) {
        console.error(`错误: ${e.message}`);
        process.exit(1);
    }
}

main();
