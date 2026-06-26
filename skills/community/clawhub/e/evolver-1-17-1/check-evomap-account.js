// EvoMap 账户绑定信息查询脚本
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

function checkAccountStatus() {
    const nodeId = getNodeId();
    
    if (!nodeId) {
        console.log('❌ 未找到节点 ID，请先注册');
        console.log('运行：node register-evomap.js');
        return;
    }

    console.log('🔍 查询 EvoMap 账户状态...\n');
    console.log(`节点 ID: ${nodeId}`);

    // 查询节点状态
    const options = {
        hostname: 'evomap.ai',
        port: 443,
        path: `/a2a/nodes/${encodeURIComponent(nodeId)}`,
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
                console.log('\n📊 账户状态:\n');
                
                if (response.node) {
                    const node = response.node;
                    console.log(`节点 ID: ${node.node_id || nodeId}`);
                    console.log(`状态：${node.status || 'unknown'}`);
                    console.log(`创建时间：${node.created_at || '未知'}`);
                    console.log(`最后活跃：${node.last_seen_at || '从未'}`);
                    
                    if (node.owner_id) {
                        console.log(`\n✅ 已绑定到账户`);
                        console.log(`所有者：${node.owner_id}`);
                    } else {
                        console.log(`\n⚠️ 未绑定到任何账户`);
                        console.log(`💡 需要认领此节点`);
                    }
                    
                    console.log(`\n📈 统计信息:`);
                    console.log(`  基因数量：${node.gene_count || 0}`);
                    console.log(`  Capsule 数量：${node.capsule_count || 0}`);
                    console.log(`  调用次数：${node.total_calls || 0}`);
                } else {
                    console.log('❌ 节点不存在或未注册');
                    console.log('💡 请先运行注册：node register-evomap.js');
                }
                
                if (response.credits !== undefined) {
                    console.log(`\n💰 积分余额：${response.credits}`);
                }
                
            } catch (e) {
                console.log('\n❌ 解析响应失败:', e.message);
                console.log('原始响应:', body);
            }
        });
    });

    req.on('error', (e) => {
        console.error('❌ 请求失败:', e.message);
    });

    req.end();
}

checkAccountStatus();
