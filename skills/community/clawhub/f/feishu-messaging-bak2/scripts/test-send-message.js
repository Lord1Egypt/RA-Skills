#!/usr/bin/env node
/**
 * 测试飞书消息发送
 * 使用 feishu-messaging skill 的 API
 */

const https = require('https');

// 从环境变量读取配置
const APP_ID = process.env.FEISHU_APP_ID || 'cli_a93d0180c0b99cba';
const APP_SECRET = process.env.FEISHU_APP_SECRET || 'KJXQ3hqdRerYwyThNq999gL2btUSkOaR';

// 获取 tenant_access_token
function getTenantAccessToken() {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify({
            app_id: APP_ID,
            app_secret: APP_SECRET
        });

        const options = {
            hostname: 'open.feishu.cn',
            port: 443,
            path: '/open-apis/auth/v3/tenant_access_token/internal',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };

        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                const result = JSON.parse(body);
                if (result.code === 0) {
                    resolve(result.tenant_access_token);
                } else {
                    reject(new Error(`获取 token 失败：${result.msg}`));
                }
            });
        });

        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

// 发送消息
async function sendMessage(receiveId, receiveIdType, content, msgType = 'text') {
    const token = await getTenantAccessToken();
    
    return new Promise((resolve, reject) => {
        const data = JSON.stringify({
            receive_id: receiveId,
            msg_type: msgType,
            content: typeof content === 'string' ? content : JSON.stringify(content)
        });

        const options = {
            hostname: 'open.feishu.cn',
            port: 443,
            path: `/open-apis/im/v1/messages?receive_id_type=${receiveIdType}`,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length,
                'Authorization': `Bearer ${token}`
            }
        };

        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                const result = JSON.parse(body);
                if (result.code === 0) {
                    resolve(result.data);
                } else {
                    reject(new Error(`发送失败：${result.msg}`));
                }
            });
        });

        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

// 获取当前用户信息
async function getMe(token) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'open.feishu.cn',
            port: 443,
            path: '/open-apis/authen/v1/user_info',
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        };

        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                const result = JSON.parse(body);
                if (result.code === 0) {
                    resolve(result.data);
                } else {
                    reject(new Error(`获取用户信息失败：${result.msg}`));
                }
            });
        });

        req.on('error', reject);
        req.end();
    });
}

// 主函数
async function main() {
    console.log('🚀 开始测试飞书消息发送...\n');
    console.log(`App ID: ${APP_ID}`);
    console.log(`App Secret: ${APP_SECRET.substring(0, 8)}...\n`);

    try {
        // 1. 获取 token
        console.log('📝 步骤 1: 获取 tenant_access_token...');
        const token = await getTenantAccessToken();
        console.log(`✅ Token 获取成功：${token.substring(0, 20)}...\n`);

        // 2. 获取当前用户信息（用 app_access_token）
        console.log('📝 步骤 2: 测试 API 调用...');
        console.log('ℹ️  提示：需要用你的飞书 user_id 或 open_id 来接收测试消息\n');
        console.log('📬 请在飞书中找到自己的 user_id 或 open_id，然后重新运行脚本\n');
        console.log('   或者用下面的方式获取：\n');
        console.log('   1. 打开飞书网页版：https://www.feishu.cn/\n');
        console.log('   2. 点击头像 -> 个人设置\n');
        console.log('   3. 复制你的 user_id 或 open_id\n');
        
        // 3. 发送测试消息（需要用户提供接收者 ID）
        const receiveId = process.argv[2];
        if (!receiveId) {
            console.log('\n❌ 缺少接收者 ID\n');
            console.log('用法：node test-send-message.js <your_user_id_or_open_id>\n');
            console.log('例如：node test-send-message.js ou_7d8a6e6df7621556ce0d21922b676706ccs\n');
            process.exit(1);
        }
        
        console.log(`📝 步骤 3: 发送测试消息给 ${receiveId}...`);
        const message = {
            text: `👋 你好！\n\n这是一条来自 OpenClaw 的测试消息。\n\n发送时间：${new Date().toLocaleString('zh-CN')}`
        };
        
        const result = await sendMessage(receiveId, receiveId.includes('ou_') ? 'open_id' : 'user_id', message);
        console.log('✅ 消息发送成功！');
        console.log(`📬 消息 ID: ${result.message_id}`);
        console.log(`🕐 发送时间：${new Date(parseInt(result.create_time) / 1000000).toLocaleString('zh-CN')}\n`);

        console.log('🎉 测试完成！飞书集成配置正确！');
        
    } catch (error) {
        console.error('❌ 测试失败：', error.message);
        process.exit(1);
    }
}

main();
