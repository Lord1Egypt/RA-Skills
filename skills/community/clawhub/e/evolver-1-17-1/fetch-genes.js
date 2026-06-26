// EvoMap 基因搜索脚本
const crypto = require('crypto');
const https = require('https');
const fs = require('fs');
const path = require('path');

// 加载节点 ID
const NODE_ID_FILE = path.join(__dirname, '.node_id');
const nodeId = fs.readFileSync(NODE_ID_FILE, 'utf8').trim();

function generateMessageId() {
    return `msg_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
}

function fetchAssets(options = {}) {
    const { assetType = null, sort = 'ranked', limit = 20 } = options;
    
    const payload = {
        protocol: "gep-a2a",
        protocol_version: "1.0.0",
        message_type: "fetch",
        message_id: generateMessageId(),
        sender_id: nodeId,
        timestamp: new Date().toISOString(),
        payload: {
            asset_type: assetType,
            limit: limit
        }
    };

    const data = JSON.stringify(payload);
    
    const reqOptions = {
        hostname: 'evomap.ai',
        port: 443,
        path: `/a2a/assets?sort=${sort}&limit=${limit}${assetType ? '&type=' + assetType : ''}`,
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    return new Promise((resolve, reject) => {
        const req = https.request(reqOptions, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                try {
                    const response = JSON.parse(body);
                    resolve(response);
                } catch (e) {
                    resolve({ raw: body });
                }
            });
        });

        req.on('error', reject);
        req.end();
    });
}

async function main() {
    console.log('🔍 正在从 EvoMap 获取高质量基因...\n');
    
    // 获取按 GDI 分数排序的基因
    const result = await fetchAssets({ assetType: 'Gene', sort: 'ranked', limit: 15 });
    
    if (result.assets && result.assets.length > 0) {
        console.log(`✅ 找到 ${result.assets.length} 个高质量基因\n`);
        console.log('='.repeat(80));
        
        result.assets.forEach((asset, index) => {
            console.log(`\n🧬 基因 #${index + 1}`);
            console.log(`   类别：${asset.category || 'N/A'}`);
            console.log(`   GDI 分数：${asset.gdi_score || 'N/A'}`);
            console.log(`   摘要：${asset.summary}`);
            console.log(`   信号匹配：${(asset.signals_match || []).join(', ') || 'N/A'}`);
            console.log(`   来源节点：${asset.source_node || 'N/A'}`);
            console.log(`   Asset ID: ${asset.asset_id}`);
            
            if (asset.validation && asset.validation.length > 0) {
                console.log(`   验证步骤：${asset.validation.join(', ')}`);
            }
            
            console.log('-'.repeat(80));
        });
        
        console.log('\n💡 提示：使用 `node fetch-genes.js --detail <asset_id>` 查看完整详情');
    } else {
        console.log('未找到基因资产');
        console.log('原始响应:', JSON.stringify(result, null, 2));
    }
}

main().catch(console.error);
