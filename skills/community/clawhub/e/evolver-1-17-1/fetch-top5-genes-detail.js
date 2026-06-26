// 获取 Top 5 基因的详细信息
const https = require('https');
const fs = require('fs');

// Top 5 基因 ID（从上一个脚本结果）
const top5Ids = [
    'sha256:2ef95a08d3df6bf62e245a80793e40fe7c45ce5084e55b3785dc7438192894aa',
    'sha256:d31fd02d27d6b2dbbff18cf7d9085b54f4b4cbe140a99809a95a4f545f8a7220',
    'sha256:82ad9e9a773f03cfeda5ce4ca8fc50c40b74652dc8fd1eb25b4d0eb8126c7544',
    'sha256:82317306c585d9a531122903d459647cc9a2bf61af14b821736840ea7af0d9d8',
    'sha256:8a893c405830091953ef1c43a59af15d007dbc844b3b8d2fde81e9515ce6ced4',
];

/**
 * 获取资产详情
 */
function getAssetDetail(assetId) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'evomap.ai',
            port: 443,
            path: `/a2a/assets/${assetId}?detailed=true`,
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        };

        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(body));
                } catch (e) {
                    resolve({ raw: body, error: e.message });
                }
            });
        });

        req.on('error', reject);
        req.end();
    });
}

async function main() {
    console.log('📖 获取 Top 5 基因的详细信息...\n');
    
    const details = [];
    
    for (let i = 0; i < top5Ids.length; i++) {
        const assetId = top5Ids[i];
        console.log(`[${i + 1}/5] 获取 ${assetId.substring(0, 20)}...`);
        
        const detail = await getAssetDetail(assetId);
        
        if (detail.error) {
            console.log(`  ✗ 失败：${detail.error}`);
        } else {
            console.log(`  ✓ 成功`);
            details.push(detail);
        }
    }
    
    console.log('\n\n========================================');
    console.log('🏆 EvoMap Top 5 高质量基因\n');
    console.log('========================================\n');
    
    details.forEach((gene, index) => {
        const title = gene.short_title || 'Untitled';
        const gdiMean = gene.gdi_score_mean?.toFixed(1) || 'N/A';
        const gdiCurrent = gene.gdi_score?.toFixed(1) || 'N/A';
        const calls = (gene.call_count || 0).toLocaleString();
        const reuse = (gene.reuse_count || 0).toLocaleString();
        const category = gene.payload?.category || 'N/A';
        const summary = gene.payload?.summary || gene.nl_summary || 'N/A';
        const trigger = gene.trigger_text || gene.payload?.trigger?.join(', ') || 'N/A';
        
        console.log(`🥇 #${index + 1}: ${title}`);
        console.log('─'.repeat(80));
        console.log(`   GDI 分数：${gdiMean} (当前：${gdiCurrent})`);
        console.log(`   类别：${category}`);
        console.log(`   调用：${calls} | 复用：${reuse}`);
        console.log(`   触发：${trigger.substring(0, 80)}${trigger.length > 80 ? '...' : ''}`);
        console.log(`\n   简介：${summary.substring(0, 150)}${summary.length > 150 ? '...' : ''}`);
        
        if (Array.isArray(gene.payload?.strategy) && gene.payload.strategy.length > 0) {
            console.log(`\n   策略:`);
            gene.payload.strategy.forEach((step, i) => {
                console.log(`     ${i + 1}. ${step.substring(0, 70)}${step.length > 70 ? '...' : ''}`);
            });
        }
        
        console.log(`\n   🔗 https://evomap.ai/a2a/assets/${gene.asset_id}\n`);
    });
    
    // 保存详细数据
    fs.writeFileSync('top5-genes-full.json', JSON.stringify(details, null, 2));
    console.log('完整数据已保存到：top5-genes-full.json\n');
    
    // 生成 Markdown 报告
    const mdReport = generateFullMarkdownReport(details);
    fs.writeFileSync('top5-genes-full-report.md', mdReport);
    console.log('Markdown 报告已保存到：top5-genes-full-report.md\n');
}

function generateFullMarkdownReport(genes) {
    let md = `# 🏆 EvoMap 质量最高的前 5 个基因\n\n`;
    md += `**生成时间**: ${new Date().toLocaleString('zh-CN')}\n\n`;
    md += `---\n\n`;
    
    genes.forEach((gene, index) => {
        const title = gene.short_title || 'Untitled';
        md += `## 🥇 #${index + 1}: ${title}\n\n`;
        
        md += `### 📊 关键指标\n\n`;
        md += `| 指标 | 数值 |\n`;
        md += `|------|------|\n`;
        md += `| **基因 ID** | \`${gene.asset_id}\` |\n`;
        md += `| **GDI 分数** | ${gene.gdi_score_mean?.toFixed(1) || 'N/A'} (平均) / ${gene.gdi_score?.toFixed(1) || 'N/A'} (当前) |\n`;
        md += `| **类别** | ${gene.payload?.category || 'N/A'} |\n`;
        md += `| **调用次数** | ${(gene.call_count || 0).toLocaleString()} |\n`;
        md += `| **复用次数** | ${(gene.reuse_count || 0).toLocaleString()} |\n`;
        md += `| **成功率** | ${(gene.bundle_capsule?.payload?.outcome?.score * 100)?.toFixed(0) || 'N/A'}% |\n`;
        md += `| **作者** | ${gene.author || gene.source_node_id || 'N/A'} |\n\n`;
        
        const summary = gene.payload?.summary || gene.nl_summary || '暂无简介';
        md += `### 📝 简介\n\n${summary}\n\n`;
        
        const trigger = gene.trigger_text || gene.payload?.trigger?.join(', ') || 'N/A';
        md += `### 🎯 触发信号\n\n\`${trigger}\`\n\n`;
        
        if (Array.isArray(gene.payload?.strategy) && gene.payload.strategy.length > 0) {
            md += `### 🎯 执行策略\n\n`;
            gene.payload.strategy.forEach((step, i) => {
                md += `${i + 1}. ${step}\n`;
            });
            md += `\n`;
        }
        
        if (gene.payload?.preconditions?.length > 0) {
            md += `### ⚠️ 前置条件\n\n`;
            gene.payload.preconditions.forEach((pre, i) => {
                md += `- ${pre}\n`;
            });
            md += `\n`;
        }
        
        if (gene.bundle_capsule) {
            md += `### 💊 配套 Capsule\n\n`;
            md += `- **ID**: \`${gene.bundle_capsule.asset_id}\`\n`;
            md += `- **总结**: ${gene.bundle_capsule.summary || 'N/A'}\n`;
            if (gene.bundle_capsule.payload?.outcome) {
                md += `- **成功率**: ${(gene.bundle_capsule.payload.outcome.score * 100).toFixed(0)}%\n`;
            }
            md += `\n`;
        }
        
        md += `🔗 [查看详情](https://evomap.ai/a2a/assets/${gene.asset_id})\n\n`;
        md += `---\n\n`;
    });
    
    md += `\n*数据来源于 EvoMap Hub API | 按 GDI 分数排序*\n`;
    return md;
}

main().catch(console.error);
