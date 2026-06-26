#!/usr/bin/env node
/**
 * 搜索飞书用户
 */

const https = require('https');

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

// 搜索用户
async function searchUsers(token, name) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'open.feishu.cn',
            port: 443,
            path: `/open-apis/contact/v3/users/search?user_id_type=open_id&name=${encodeURIComponent(name)}&page_size=10`,
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
                    reject(new Error(`搜索失败：${result.msg}`));
                }
            });
        });

        req.on('error', reject);
        req.end();
    });
}

// 获取用户详情
async function getUser(token, userId) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'open.feishu.cn',
            port: 443,
            path: `/open-apis/contact/v3/users/${userId}?user_id_type=open_id`,
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
                    reject(new Error(`获取详情失败：${result.msg}`));
                }
            });
        });

        req.on('error', reject);
        req.end();
    });
}

async function main() {
    const searchName = process.argv[2] || '尹为';
    
    console.log(`🔍 搜索飞书用户：${searchName}\n`);
    
    try {
        const token = await getTenantAccessToken();
        console.log('✅ Token 获取成功\n');
        
        // 尝试搜索用户
        console.log('📝 正在搜索用户...');
        const users = await searchUsers(token, searchName);
        
        if (users && users.items && users.items.length > 0) {
            console.log(`✅ 找到 ${users.items.length} 个用户:\n`);
            
            for (const user of users.items) {
                const details = await getUser(token, user.user_id);
                console.log(`👤 姓名：${details.name}`);
                console.log(`   ID: ${user.user_id}`);
                console.log(`   工号：${details.employee_no || 'N/A'}`);
                console.log(`   邮箱：${details.email || 'N/A'}`);
                console.log(`   手机：${details.mobile || 'N/A'}`);
                console.log(`   部门：${details.department_ids ? details.department_ids.join(', ') : 'N/A'}`);
                console.log('');
            }
            
            console.log('💡 使用第一个用户的 ID 发送测试消息：');
            console.log(`   node test-send-message.js ${users.items[0].user_id}\n`);
        } else {
            console.log('❌ 未找到用户，请检查名字是否正确\n');
        }
        
    } catch (error) {
        console.error('❌ 错误：', error.message);
        process.exit(1);
    }
}

main();
