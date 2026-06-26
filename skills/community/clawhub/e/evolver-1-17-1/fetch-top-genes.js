// 获取 EvoMap 上质量最高的前 5 个基因
const https = require('https');
const fs = require('fs');

/**
 * 获取资产列表
 */
function getAssets(params = {}) {
    return new Promise((resolve, reject) => {
        const queryString = new URLSearchParams(params).toString();
        const path = `/a2a/assets${queryString ? '?' + queryString : ''}`;
        
        const options = {
            hostname: 'evomap.ai',
            port: 443,
            path: path,
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

/**
 * 获取 trending 资产
 */
function getTrending(limit = 50) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'evomap.ai',
            port: 443,
            path: `/a2a/trending?limit=${limit}`,
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
    console.log('🏆 查找 EvoMap 质量最高的前 5 个基因\n');
    
    // 获取大量 Gene 资产
    console.log('📊 获取 Gene 资产列表...\n');
    const genesResult = await getAssets({ type: 'Gene', limit: 200, status: 'promoted' });
    const genes = Array.isArray(genesResult) ? genesResult : (genesResult.assets || genesResult.data || []);
    
    console.log(`获取到 ${genes.length} 个 Gene\n`);
    
    // 获取 trending 资产
    console.log('📈 获取 Trending 资产...\n');
    const trendingResult = await getTrending(50);
    const trending = Array.isArray(trendingResult) ? trendingResult : (trendingResult.assets || trendingResult.data || []);
    
    console.log(`获取到 ${trending.length} 个 Trending 资产\n`);
    
    // 合并并筛选 Gene
    const allAssets = [...genes, ...trending];
    const allGenes = allAssets.filter(a => a.asset_type === 'Gene');
    
    // 去重
    const uniqueGenesMap = new Map();
    allGenes.forEach(g => {
        if (!uniqueGenesMap.has(g.asset_id)) {
            uniqueGenesMap.set(g.asset_id, g);
        }
    });
    const uniqueGenes = Array.from(uniqueGenesMap.values());
    
    console.log(`去重后共有 ${uniqueGenes.length} 个唯一 Gene\n`);
    
    // 按 GDI 分数排序（优先 gdi_score_mean，其次 gdi_score）
    uniqueGenes.sort((a, b) => {
        const scoreA = (a.gdi_score_mean || 0) || (a.gdi_score || 0);
        const scoreB = (b.gdi_score_mean || 0) || (b.gdi_score || 0);
        return scoreB - scoreA;
    });
    
    // 显示前 5 个
    console.log('🏆 Top 5 高质量基因:\n');
    console.log('='.repeat(120));
    
    const top5 = uniqueGenes.slice(0, 5);
    
    top5.forEach((gene, index) => {
        const gdiMean = gene.gdi_score_mean?.toFixed(1) || 'N/A';
        const gdiCurrent = gene.gdi_score?.toFixed(1) || 'N/A';
        const calls = gene.call_count || 0;
        const reuse = gene.reuse_count || 0;
        const title = gene.short_title || gene.payload?.summary?.substring(0, 50) || 'Untitled';
        const category = gene.payload?.category || 'N/A';
        
        console.log(`\n🥇 #${index + 1}: ${title}`);
        console.log('-'.repeat(120));
        console.log(`   基因 ID: ${gene.asset_id}`);
        console.log(`   GDI 分数：${gdiMean} (当前：${gdiCurrent})`);
        console.log(`   类别：${category}`);
        console.log(`   调用次数：${calls.toLocaleString()}`);
        console.log(`   复用次数：${reuse.toLocaleString()}`);
        console.log(`   触发信号：${gene.trigger_text || 'N/A'}`);
        
        if (gene.payload?.summary) {
            const summary = gene.payload.summary.length > 150 
                ? gene.payload.summary.substring(0, 150) + '...' 
                : gene.payload.summary;
            console.log(`   简介：${summary}`);
        }
        
        if (gene.payload?.strategy) {
            console.log(`   策略步骤：${gene.payload.strategy.length} 步`);
        }
        
        console.log(`   作者节点：${gene.source_node_id}`);
        console.log(`   创建时间：${gene.created_at}`);
        console.log(`   查看详情：https://evomap.ai/a2a/assets/${gene.asset_id}`);
    });
    
    console.log('\n' + '='.repeat(120));
    
    // 保存详细数据
    const output = {
        timestamp: new Date().toISOString(),
        top5: top5.map(g => ({
            rank: 0,
            title: g.short_title || g.payload?.summary?.substring(0, 50),
            asset_id: g.asset_id,
            gdi_score_mean: g.gdi_score_mean,
            gdi_score: g.gdi_score,
            category: g.payload?.category,
            call_count: g.call_count,
            reuse_count: g.reuse_count,
            trigger_text: g.trigger_text,
            summary: g.payload?.summary,
            strategy: g.payload?.strategy,
            url: `https://evomap.ai/a2a/assets/${g.asset_id}`
        })).map((g, i) => ({ ...g, rank: i + 1 })),
        total_genes_analyzed: uniqueGenes.length
    };
    
    fs.writeFileSync('top5-genes-detailed.json', JSON.stringify(output, null, 2));
    console.log('\n详细数据已保存到：top5-genes-detailed.json\n');
    
    // 创建 Markdown 报告
    const mdReport = generateMarkdownReport(output);
    fs.writeFileSync('top5-genes-report.md', mdReport);
    console.log('Markdown 报告已保存到：top5-genes-report.md\n');
}

function generateMarkdownReport(data) {
    let md = `# 🏆 EvoMap 质量最高的前 5 个基因\n\n`;
    md += `**生成时间**: ${new Date(data.timestamp).toLocaleString('zh-CN')}\n`;
    md += `**分析总数**: ${data.total_genes_analyzed} 个基因\n\n`;
    md += `---\n\n`;
    
    data.top5.forEach(gene => {
        md += `## 🥇 #${gene.rank}: ${gene.title || 'Untitled'}\n\n`;
        md += `| 指标 | 数值 |\n`;
        md += `|------|------|\n`;
        md += `| **基因 ID** | \`${gene.asset_id}\` |\n`;
        md += `| **GDI 分数** | ${gene.gdi_score_mean?.toFixed(1) || 'N/A'} (当前：${gene.gdi_score?.toFixed(1) || 'N/A'}) |\n`;
        md += `| **类别** | ${gene.category || 'N/A'} |\n`;
        md += `| **调用次数** | ${gene.call_count?.toLocaleString() || 0} |\n`;
        md += `| **复用次数** | ${gene.reuse_count?.toLocaleString() || 0} |\n`;
        md += `| **触发信号** | ${gene.trigger_text || 'N/A'} |\n\n`;
        
        if (gene.summary) {
            md += `### 📝 简介\n${gene.summary}\n\n`;
        }
        
        if (gene.strategy && gene.strategy.length > 0) {
            md += `### 🎯 执行策略\n`;
            gene.strategy.forEach((step, i) => {
                md += `${i + 1}. ${step}\n`;
            });
            md += `\n`;
        }
        
        md += `🔗 [查看详情](${gene.url})\n\n`;
        md += `---\n\n`;
    });
    
    md += `\n*数据来源于 EvoMap Hub API*\n`;
    return md;
}

main().catch(console.error);
