#!/usr/bin/env node
/**
 * 飞书消息测试脚本
 * 直接用 API 发送消息，不需要发布应用
 */

const https = require('https');

// 配置
const APP_ID = 'cli_a93d751f19395cc1';
const APP_SECRET = 'KJXQ3hqdRerYwyThNq999gL2btUSkOaR';

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

// 主函数
async function main() {
    console.log('🚀 飞书消息测试\n');
    console.log(`应用：OpenClaw 助手`);
    console.log(`App ID: ${APP_ID}\n`);

    try {
        // 获取 token
        console.log('📝 获取 access token...');
        const token = await getTenantAccessToken();
        console.log(`✅ Token 获取成功\n`);

        // 发送测试消息
        console.log('📬 准备发送测试消息...\n');
        
        // 提示用户输入接收者 ID
        console.log('请输入接收者的 open_id 或 user_id:');
        console.log('(在飞书里找到自己的 ID，或者用机器人的 ID 测试)\n');
        
        // 如果没有提供参数，显示使用说明
        const receiveId = process.argv[2];
        if (!receiveId) {
            console.log('❌ 缺少接收者 ID\n');
            console.log('用法：node test-feishu.js <your_open_id>\n');
            console.log('如何获取你的 open_id：');
            console.log('1. 打开飞书网页版 https://www.feishu.cn/');
            console.log('2. 点击右上角头像 -> 个人设置');
            console.log('3. 找到你的 open_id（通常以 ou_ 开头）\n');
            console.log('或者在飞书里搜索 "OpenClaw 助手"，添加机器人为好友后，');
            console.log('给机器人发一条消息，它就能收到你的 ID 并回复你！\n');
            process.exit(1);
        }

        const message = {
            text: `👋 你好！\n\n这是一条来自 OpenClaw 的测试消息。\n\n发送时间：${new Date().toLocaleString('zh-CN')}\n\n如果你看到这条消息，说明 API 配置成功！🎉`
        };

        const result = await sendMessage(
            receiveId, 
            receiveId.includes('ou_') ? 'open_id' : 'user_id', 
            message
        );

        console.log('✅ 消息发送成功！');
        console.log(`📬 消息 ID: ${result.message_id}`);
        console.log(`🕐 发送时间：${new Date(parseInt(result.create_time) / 1000000).toLocaleString('zh-CN')}\n`);
        console.log('🎉 测试完成！飞书 API 配置正确！\n');

    } catch (error) {
        console.error('❌ 测试失败：', error.message);
        console.log('\n可能的原因：');
        console.log('1. 接收者 ID 不正确');
        console.log('2. 应用权限未开通（需要在飞书开放平台开通 im:message 权限）');
        console.log('3. 应用未发布（某些 API 需要发布后才能用）\n');
        process.exit(1);
    }
}

main();
