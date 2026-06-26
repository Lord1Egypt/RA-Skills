// EvoMap 获取基因详情脚本
const https = require('https');
const fs = require('fs');
const path = require('path');

// 加载节点 ID
const NODE_ID_FILE = path.join(__dirname, '.node_id');
const nodeId = fs.readFileSync(NODE_ID_FILE, 'utf8').trim();

function getAssetDetail(assetId) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'evomap.ai',
            port: 443,
            path: `/a2a/assets/${assetId}`,
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
    // 从注册时返回的 starter_gene_pack 中获取基因列表
    const starterGenes = [
        {
            asset_id: "sha256:2ef95a08d3df6bf62e245a80793e40fe7c45ce5084e55b3785dc7438192894aa",
            summary: "PostgreSQL + Elasticsearch CDC 实时同步",
            category: "innovate",
            gdi_score: 69.9,
            signals: ["CDC", "Debezium", "PostgreSQL", "Elasticsearch", "data_sync"]
        },
        {
            asset_id: "sha256:9f07e60cdb22472da5d3b54e040b2f6069f93eb06029869a7c03006231c178ac",
            summary: "AI 角色自动配置（技能 + 记忆 + 生物钟）",
            category: "innovate",
            gdi_score: 69,
            signals: ["persona", "auto_setup", "cron_schedule", "character_mode"]
        },
        {
            asset_id: "sha256:d31fd02d27d6b2dbbff18cf7d9085b54f4b4cbe140a99809a95a4f545f8a7220",
            summary: "ScholarGraph: 学术文献 AI 工具包",
            category: "innovate",
            gdi_score: 69.3,
            signals: ["literature", "semantic_search", "knowledge_graph"]
        },
        {
            asset_id: "sha256:82ad9e9a773f03cfeda5ce4ca8fc50c40b74652dc8fd1eb25b4d0eb8126c7544",
            summary: "Python 正则 CJK 字符边界修复",
            category: "repair",
            gdi_score: 67.7,
            signals: ["Python", "regex", "CJK", "Unicode"]
        },
        {
            asset_id: "sha256:9c650225084f1af1e9dda04dddfb18c8b9510d9aa60b25ad9994b7c36f3a21f2",
            summary: "代码去重 - DRY 原则优化",
            category: "optimize",
            gdi_score: 66.9,
            signals: ["code_duplication", "dry_violation", "refactoring"]
        },
        {
            asset_id: "sha256:8a893c405830091953ef1c43a59af15d007dbc844b3b8d2fde81e9515ce6ced4",
            summary: "飞书 URL 类型自动识别（Doc/Sheet/Base）",
            category: "repair",
            gdi_score: 67.3,
            signals: ["feishu", "url_detection", "tool_routing"]
        },
        {
            asset_id: "sha256:acce5be22676155e3ca07ff2c5060acdd1de5529aded8ed5edcc946b03f20eae",
            summary: "JSON 自动修复（LLM 输出容错）",
            category: "repair",
            gdi_score: 66,
            signals: ["JSONParseError", "malformed_json", "heuristic_fix"]
        },
        {
            asset_id: "sha256:654ebf1c47be13b753937624d4c3d203b845bb5c61afb943bdf0dec1e1379706",
            summary: "播客/音频文件断点续传下载",
            category: "optimize",
            gdi_score: 63.6,
            signals: ["download", "resume", "retry", "timeout"]
        }
    ];

    console.log('🧬 EvoMap 高质量基因推荐 (来自 Starter Gene Pack)\n');
    console.log('='.repeat(90));
    
    starterGenes.forEach((gene, index) => {
        console.log(`\n📌 基因 #${index + 1} - ${gene.category.toUpperCase()}`);
        console.log(`   GDI 分数：⭐ ${gene.gdi_score}`);
        console.log(`   摘要：${gene.summary}`);
        console.log(`   信号：${gene.signals.join(', ')}`);
        console.log(`   Asset ID: \`${gene.asset_id}\``);
        
        // 根据类别给出学习建议
        if (gene.category === 'repair') {
            console.log(`   💡 学习价值：解决常见错误，适合新手学习`);
        } else if (gene.category === 'optimize') {
            console.log(`   💡 学习价值：提升代码质量，适合进阶优化`);
        } else if (gene.category === 'innovate') {
            console.log(`   💡 学习价值：创新功能设计，适合拓展思路`);
        }
        
        console.log('-'.repeat(90));
    });

    console.log('\n\n🎯 推荐学习路径：');
    console.log('   1. 先从 repair 类基因开始 - 解决实际问题');
    console.log('   2. 学习 optimize 类基因 - 提升代码质量');
    console.log('   3. 研究 innovate 类基因 - 拓展创新思维');
    
    console.log('\n📋 下一步操作：');
    console.log('   - 使用 `node fetch-asset-detail.js <asset_id>` 查看完整基因策略');
    console.log('   - 访问 https://evomap.ai/a2a/assets/<asset_id> 在浏览器中查看');
}

main().catch(console.error);
