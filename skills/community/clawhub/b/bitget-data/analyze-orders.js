#!/usr/bin/env node
// Bitget 挂单合理性分析 + 优化建议

const fs = require('fs');

const CONFIG = JSON.parse(fs.readFileSync(__dirname + '/config.json'));
const SETTINGS = JSON.parse(fs.readFileSync(__dirname + '/grid_settings.json'));

// 当前价格 (从之前查询)
const prices = {
    BTCUSDT: 67550.09,
    SOLUSDT: 82.86
};

console.log('\n' + '='.repeat(80));
console.log('📊 Bitget 网格挂单合理性分析');
console.log('时间：' + new Date().toLocaleString('zh-CN'));
console.log('='.repeat(80));

// 分析函数
function analyzeGrid(name, grid, currentPrice) {
    const { symbol, gridNum, priceMin, priceMax, amount, maxPosition } = grid;
    
    console.log(`\n${name.toUpperCase()} 网格分析:`);
    console.log('-'.repeat(60));
    
    // 1. 价格区间分析
    const rangeSize = priceMax - priceMin;
    const rangePercent = (rangeSize / priceMin * 100).toFixed(2);
    const pricePosition = ((currentPrice - priceMin) / rangeSize * 100).toFixed(2);
    
    console.log(`📍 价格区间：${priceMin} - ${priceMax} USDT`);
    console.log(`   区间宽度：${rangeSize} USDT (${rangePercent}%）`);
    console.log(`   当前价格：${currentPrice} USDT`);
    console.log(`   价格位置：${pricePosition}% (从底部算起)`);
    
    // 2. 网格密度分析
    const gridSpacing = (rangeSize / gridNum).toFixed(2);
    const gridSpacingPercent = (gridSpacing / currentPrice * 100).toFixed(3);
    
    console.log(`\n📐 网格参数:`);
    console.log(`   网格数量：${gridNum} 格`);
    console.log(`   每格间距：${gridSpacing} USDT (${gridSpacingPercent}%）`);
    
    // 3. 资金分析
    const totalInvestment = amount * gridNum;
    const usdtPerBuy = amount;
    const coinPerSell = amount / currentPrice;
    
    console.log(`\n💰 资金配置:`);
    console.log(`   每格金额：${amount} USDT`);
    console.log(`   总需求：${totalInvestment} USDT`);
    console.log(`   最大持仓：${maxPosition} USDT`);
    
    // 4. 合理性评估
    console.log(`\n✅ 合理性评估:`);
    
    const issues = [];
    const suggestions = [];
    
    // 检查 1: 网格间距
    if (parseFloat(gridSpacingPercent) < 0.3) {
        issues.push(`⚠️  网格过密 (${gridSpacingPercent}%)，容易频繁成交但利润微薄`);
        suggestions.push(`建议：增加网格间距到 0.5-1.0% 或减少网格数量`);
    } else if (parseFloat(gridSpacingPercent) > 3) {
        issues.push(`⚠️  网格过疏 (${gridSpacingPercent}%)，成交机会少`);
        suggestions.push(`建议：减小网格间距到 0.5-2.0% 或增加网格数量`);
    } else {
        console.log(`   ✅ 网格间距合理 (${gridSpacingPercent}%)`);
    }
    
    // 检查 2: 价格位置
    if (parseFloat(pricePosition) < 20) {
        issues.push(`⚠️  价格接近区间底部 (${pricePosition}%)，可能持续买入`);
        suggestions.push(`建议：扩大价格区间下限或准备追加 USDT`);
    } else if (parseFloat(pricePosition) > 80) {
        issues.push(`⚠️  价格接近区间顶部 (${pricePosition}%)，可能持续卖出`);
        suggestions.push(`建议：扩大价格区间上限或准备追加持仓`);
    } else {
        console.log(`   ✅ 价格位置适中 (${pricePosition}%)`);
    }
    
    // 检查 3: 资金效率
    const capitalEfficiency = (totalInvestment / maxPosition * 100).toFixed(2);
    if (parseFloat(capitalEfficiency) < 50) {
        issues.push(`⚠️  资金利用率低 (${capitalEfficiency}%)`);
        suggestions.push(`建议：增加每格金额或减少最大持仓限制`);
    } else if (parseFloat(capitalEfficiency) > 90) {
        issues.push(`⚠️  资金利用过高 (${capitalEfficiency}%)，可能爆仓`);
        suggestions.push(`建议：降低每格金额或增加最大持仓`);
    } else {
        console.log(`   ✅ 资金利用率合理 (${capitalEfficiency}%)`);
    }
    
    // 检查 4: 网格数量
    if (gridNum < 10) {
        issues.push(`⚠️  网格数量偏少 (${gridNum}格)，平滑度不够`);
        suggestions.push(`建议：增加到 15-30 格`);
    } else if (gridNum > 50) {
        issues.push(`⚠️  网格数量过多 (${gridNum}格)，管理复杂`);
        suggestions.push(`建议：减少到 20-40 格`);
    } else {
        console.log(`   ✅ 网格数量合理 (${gridNum}格)`);
    }
    
    // 检查 5: 区间宽度
    if (parseFloat(rangePercent) < 5) {
        issues.push(`⚠️  价格区间过窄 (${rangePercent}%)，容易突破`);
        suggestions.push(`建议：扩大区间到±10-20%`);
    } else if (parseFloat(rangePercent) > 50) {
        issues.push(`⚠️  价格区间过宽 (${rangePercent}%)，资金分散`);
        suggestions.push(`建议：缩小区间到±15-30%`);
    } else {
        console.log(`   ✅ 价格区间合理 (${rangePercent}%)`);
    }
    
    // 显示问题和an
    if (issues.length > 0) {
        console.log(`\n⚠️  发现问题:`);
        issues.forEach((issue, i) => console.log(`   ${i+1}. ${issue}`));
    }
    
    if (suggestions.length > 0) {
        console.log(`\n💡 优化建议:`);
        suggestions.forEach((sug, i) => console.log(`   ${i+1}. ${sug}`));
    }
    
    if (issues.length === 0) {
        console.log(`   ✅ 所有检查通过，配置合理！`);
    }
    
    return { issues, suggestions };
}

// 分析两个网格
const btcAnalysis = analyzeGrid('BTC', SETTINGS.btc, prices.BTCUSDT);
const solAnalysis = analyzeGrid('SOL', SETTINGS.sol, prices.SOLUSDT);

// 总体建议
console.log('\n' + '='.repeat(80));
console.log('📋 总体评估');
console.log('='.repeat(80));

const totalIssues = btcAnalysis.issues.length + solAnalysis.issues.length;
if (totalIssues === 0) {
    console.log('\n✅ 两个网格策略配置都很合理，无需调整！');
} else if (totalIssues <= 3) {
    console.log(`\n⚠️  发现 ${totalIssues} 个问题，建议优化（见上文）`);
} else {
    console.log(`\n🔴 发现 ${totalIssues} 个问题，强烈建议调整配置！`);
}

// 改进方案
console.log('\n' + '='.repeat(80));
console.log('🎯 推荐改进方案');
console.log('='.repeat(80));

console.log('\n方案 A: 保守优化 (小幅调整)');
console.log('─'.repeat(60));
console.log('BTC 网格:');
console.log('  - 网格数：25 → 30 格');
console.log('  - 区间：66500-69500 → 65000-70000 USDT');
console.log('  - 间距：~1.2% → ~1.5%');
console.log('SOL 网格:');
console.log('  - 网格数：20 → 25 格');
console.log('  - 区间：81-89 → 78-92 USDT');
console.log('  - 间距：~4% → ~5%');

console.log('\n方案 B: 激进优化 (重新设计)');
console.log('─'.repeat(60));
console.log('BTC 网格:');
console.log('  - 网格数：25 → 40 格');
console.log('  - 区间：66500-69500 → 60000-75000 USDT (±10%)');
console.log('  - 每格：15 → 10 USDT');
console.log('  - 总资金：375 → 400 USDT');
console.log('SOL 网格:');
console.log('  - 网格数：20 → 30 格');
console.log('  - 区间：81-89 → 70-100 USDT (±18%)');
console.log('  - 每格：25 → 15 USDT');
console.log('  - 总资金：500 → 450 USDT');

console.log('\n方案 C: 保持现状');
console.log('─'.repeat(60));
console.log('当前配置基本合理，可以继续运行观察');
console.log('优点：无需调整，继续盈利');
console.log('缺点：可能错过更优配置');

console.log('\n' + '='.repeat(80));
console.log('💡 最终建议:');
console.log('='.repeat(80));

if (btcAnalysis.issues.length === 0 && solAnalysis.issues.length === 0) {
    console.log('\n✅ 推荐方案 C - 保持现状');
    console.log('当前配置合理，无需调整，继续运行即可！\n');
} else {
    console.log('\n⚠️  推荐方案 A - 保守优化');
    console.log('小幅调整即可改善问题，风险低，效果好！\n');
}

console.log('='.repeat(80) + '\n');
