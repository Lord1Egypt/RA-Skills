// EvoMap 节点注册脚本
const crypto = require('crypto');
const https = require('https');

// 生成或加载节点 ID
const NODE_ID_FILE = '.node_id';
const fs = require('fs');
const path = require('path');

function getNodeId() {
    const filePath = path.join(__dirname, NODE_ID_FILE);
    if (fs.existsSync(filePath)) {
        return fs.readFileSync(filePath, 'utf8').trim();
    }
    // 生成新的节点 ID
    const nodeId = 'node_' + crypto.randomBytes(8).toString('hex');
    fs.writeFileSync(filePath, nodeId);
    console.log(`✨ 生成新节点 ID: ${nodeId}`);
    return nodeId;
}

function generateMessageId() {
    return `msg_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
}

function sendHello() {
    const nodeId = getNodeId();
    const payload = {
        protocol: "gep-a2a",
        protocol_version: "1.0.0",
        message_type: "hello",
        message_id: generateMessageId(),
        sender_id: nodeId,
        timestamp: new Date().toISOString(),
        payload: {
            capabilities: {},
            gene_count: 0,
            capsule_count: 0,
            env_fingerprint: {
                platform: process.platform,
                arch: process.arch
            }
        }
    };

    const data = JSON.stringify(payload);
    
    const options = {
        hostname: 'evomap.ai',
        port: 443,
        path: '/a2a/hello',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': data.length
        }
    };

    console.log('🚀 正在注册到 EvoMap Hub...');
    console.log(`节点 ID: ${nodeId}`);
    
    const req = https.request(options, (res) => {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => {
            try {
                const response = JSON.parse(body);
                console.log('\n✅ 注册成功!');
                console.log('响应:', JSON.stringify(response, null, 2));
                
                if (response.claim_code) {
                    console.log(`\n📋 认领代码：${response.claim_code}`);
                    console.log(`🔗 认领 URL: https://evomap.ai/claim/${response.claim_code}`);
                    console.log('\n请访问认领 URL 将此节点绑定到你的 EvoMap 账户');
                }
                
                if (response.credits) {
                    console.log(`💰 初始积分：${response.credits}`);
                }
            } catch (e) {
                console.log('原始响应:', body);
            }
        });
    });

    req.on('error', (e) => {
        console.error('❌ 请求失败:', e.message);
    });

    req.write(data);
    req.end();
}

sendHello();
