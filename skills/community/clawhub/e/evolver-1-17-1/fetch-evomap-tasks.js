// EvoMap 任务查询脚本
const https = require('https');
const fs = require('fs');
const path = require('path');

const NODE_ID_FILE = path.join(__dirname, '.node_id');

function getNodeId() {
    if (fs.existsSync(NODE_ID_FILE)) {
        return fs.readFileSync(NODE_ID_FILE, 'utf8').trim();
    }
    return null;
}

function getTasks() {
    const nodeId = getNodeId();
    
    if (!nodeId) {
        console.log('❌ 未找到节点 ID');
        return;
    }

    console.log('🔍 查询 EvoMap 可接任务...\n');

    // 查询任务列表
    const options = {
        hostname: 'evomap.ai',
        port: 443,
        path: '/a2a/tasks?status=open&limit=10',
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const req = https.request(options, (res) => {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => {
            try {
                const response = JSON.parse(body);
                
                if (response.tasks && response.tasks.length > 0) {
                    console.log(`📋 找到 ${response.tasks.length} 个可接任务:\n`);
                    
                    response.tasks.forEach((task, index) => {
                        console.log(`${index + 1}. **${task.title}**`);
                        console.log(`   任务 ID: ${task.task_id}`);
                        console.log(`   Bounty ID: ${task.bounty_id || '无'}`);
                        console.log(`   类型：${task.bounty_id ? '🎁 Bounty' : '📝 普通'}`);
                        console.log(`   最低声誉：${task.min_reputation || 0}`);
                        console.log(`   截止：${new Date(task.expires_at).toLocaleString('zh-CN')}`);
                        console.log(`   创建：${new Date(task.created_at).toLocaleString('zh-CN')}`);
                        
                        if (task.signals) {
                            console.log(`   信号：${task.signals}`);
                        }
                        
                        if (task.reward_credits) {
                            console.log(`   奖励：${task.reward_credits} 积分`);
                        }
                        
                        console.log('');
                    });
                } else {
                    console.log('✅ 没有找到可接任务');
                }
                
            } catch (e) {
                console.log('❌ 解析失败:', e.message);
                console.log('原始响应:', body);
            }
        });
    });

    req.on('error', (e) => {
        console.error('❌ 请求失败:', e.message);
    });

    req.end();
}

getTasks();
