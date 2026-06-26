#!/usr/bin/env node
/**
 * 艾登师傅 - 微信扫码登录工具
 * 用法: node login.js [--open-browser]
 */

const https = require('https');
const http = require('http');
const { exec, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const API_BASE = 'https://mes.dderp.cn/mob';

// 配置文件路径
const CONFIG_DIR = path.join(os.homedir(), '.workbuddy', 'skills', 'aiding-shifu');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

// 发送 HTTP 请求
function httpRequest(url, options = {}) {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(url);
        const protocol = urlObj.protocol === 'https:' ? https : http;
        
        const reqOptions = {
            hostname: urlObj.hostname,
            port: urlObj.port || (urlObj.protocol === 'https:' ? 443 : 80),
            path: urlObj.pathname + urlObj.search,
            method: options.method || 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*',
                ...options.headers
            }
        };

        const req = protocol.request(reqOptions, (res) => {
            const chunks = [];
            res.on('data', chunk => chunks.push(chunk));
            res.on('end', () => {
                const buffer = Buffer.concat(chunks);
                let data;
                
                // 尝试解析 JSON
                try {
                    const str = new TextDecoder('utf-8').decode(buffer);
                    data = JSON.parse(str);
                } catch {
                    data = buffer.toString();
                }
                
                resolve(data);
            });
        });

        req.on('error', reject);
        
        if (options.body) {
            req.write(JSON.stringify(options.body));
        }
        req.end();
    });
}

// 确保配置目录存在
function ensureConfigDir() {
    if (!fs.existsSync(CONFIG_DIR)) {
        fs.mkdirSync(CONFIG_DIR, { recursive: true });
    }
}

// 保存配置
function saveConfig(config) {
    ensureConfigDir();
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

// 加载配置
function loadConfig() {
    try {
        if (fs.existsSync(CONFIG_FILE)) {
            return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
        }
    } catch (e) {}
    return {};
}

// 生成二维码图片并保存
async function downloadQrCode(qrCodeUrl, savePath) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(savePath);
        https.get(qrCodeUrl, (response) => {
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                resolve(savePath);
            });
        }).on('error', (err) => {
            try { fs.unlinkSync(savePath); } catch (e) {}
            reject(err);
        });
    });
}

// 创建登录二维码
async function createLoginQrCode() {
    console.log('正在请求登录二维码...');
    const result = await httpRequest(`${API_BASE}/wechat/createLoginQrCode`, {
        method: 'POST'
    });
    
    if (result.code === 200 && result.data) {
        return {
            ticket: result.data.ticket,
            sceneId: result.data.sceneId,
            url: result.data.url,
            expireTime: Date.now() + (result.data.expire_seconds || 300) * 1000
        };
    } else {
        throw new Error(result.message || '获取二维码失败');
    }
}

// 生成二维码图片（使用在线 API）
function generateQrCodeUrl(text) {
    // 使用腾讯的 API 生成二维码
    return `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(text)}`;
}

// 检查登录状态
async function checkLoginStatus(sceneId) {
    const result = await httpRequest(`${API_BASE}/wechat/checkLoginStatus?sceneId=${sceneId}`, {
        method: 'POST'
    });
    
    // 返回格式: {status: "xxx", data: {token: "..."}}
    if (result.status) {
        return result;
    } else if (result.code === 200 && result.data) {
        return result.data;
    } else {
        throw new Error(result.message || '检查状态失败');
    }
}

// 轮询登录状态
async function pollLoginStatus(sceneId, onStatusChange) {
    return new Promise((resolve, reject) => {
        let attempts = 0;
        const maxAttempts = 150; // 最多轮询5分钟 (150 * 2秒)
        
        const poll = async () => {
            try {
                attempts++;
                const status = await checkLoginStatus(sceneId);
                
                onStatusChange(status);
                
                // 已授权 - 成功
                if (status.status === '已授权') {
                    resolve(status);
                }
                // 其他成功状态
                else if (status.status === 'confirmed' || status.status === '登录成功') {
                    resolve(status);
                }
                // 已过期
                else if (status.status === 'expired' || status.status === '已过期') {
                    reject(new Error('二维码已过期，请重新生成'));
                }
                // 超时
                else if (attempts >= maxAttempts) {
                    reject(new Error('登录超时，请重试'));
                }
                // 继续轮询
                else {
                    setTimeout(poll, 2000);
                }
            } catch (error) {
                reject(error);
            }
        };
        
        poll();
    });
}

// 打开文件/URL
function openPath(filePath) {
    const platform = process.platform;
    let cmd;
    
    if (platform === 'win32') {
        cmd = `start "" "${filePath}"`;
    } else if (platform === 'darwin') {
        cmd = `open "${filePath}"`;
    } else {
        cmd = `xdg-open "${filePath}"`;
    }
    
    exec(cmd);
}

// 主函数
async function main() {
    const args = process.argv.slice(2);
    const openBrowser = args.includes('--open-browser');
    
    try {
        // 1. 创建二维码
        const qrData = await createLoginQrCode();
        console.log('✅ 二维码获取成功');
        console.log(`📱 SceneId: ${qrData.sceneId}`);
        console.log(`⏰ 过期时间: ${new Date(qrData.expireTime).toLocaleString()}`);
        
        // 2. 生成并下载二维码图片
        const tmpDir = os.tmpdir();
        const qrPath = path.join(tmpDir, 'aiding-shifu-login-qr.png');
        const qrCodeUrl = generateQrCodeUrl(qrData.url);
        
        console.log('📥 正在生成二维码图片...');
        await downloadQrCode(qrCodeUrl, qrPath);
        console.log('✅ 二维码保存成功');
        
        // 3. 打开二维码
        console.log('🖼️  正在打开二维码...');
        openPath(qrPath);
        
        if (openBrowser) {
            // 打开 HTML 页面版本
            const htmlPath = path.join(__dirname, 'qr-login.html');
            openPath(htmlPath);
        }
        
        // 4. 轮询登录状态
        console.log('\n⏳ 等待扫码登录...\n');
        
        const finalStatus = await pollLoginStatus(qrData.sceneId, (status) => {
            switch (status.status) {
                case 'waiting':
                    process.stdout.write('\r📱 等待微信扫码...');
                    break;
                case 'scanned':
                    process.stdout.write('\r✅ 已扫码，请在微信中确认登录');
                    break;
                case 'confirmed':
                    process.stdout.write('\r');
                    break;
            }
        });
        
        // 5. 登录成功
        console.log('\n\n🎉 登录成功！');
        
        // 获取 token（access_token 在 data 里）
        const token = finalStatus.data?.access_token || finalStatus.token;
        
        if (token) {
            console.log(`\n🔑 Token: ${token.substring(0, 50)}...`);
            
            // 保存 Token
            const config = {
                token: token,
                loginTime: new Date().toISOString(),
                userInfo: finalStatus.data?.userInfo || finalStatus.userInfo,
                wxUnionid: finalStatus.data?.wxUnionid || finalStatus.wxUnionid
            };
            saveConfig(config);
            
            console.log('\n✅ Token 已保存到配置文件');
            console.log(`📁 ${CONFIG_FILE}`);
        }
        
        process.exit(0);
        
    } catch (error) {
        console.error('\n❌ 错误:', error.message);
        process.exit(1);
    }
}

// 导出函数供其他模块使用
module.exports = {
    createLoginQrCode,
    checkLoginStatus,
    saveConfig,
    loadConfig
};

// 如果直接运行
if (require.main === module) {
    main();
}
