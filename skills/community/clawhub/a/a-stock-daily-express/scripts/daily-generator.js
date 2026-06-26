// A-Share Daily Express - Daily report generator
// Get market data, analyze, generate content for different platforms

const { execSync } = require('child_process');

function getMarketData() {
    // Use Python akshare to get market data
    try {
        const pythonCode = `
import akshare as ak
import json

# Get general market info
stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sh000001")
latest = stock_zh_index_daily_df.iloc[-1]

# Get up/down count
stock_zh_a_spot_df = ak.stock_zh_a_spot()
up_count = sum(stock_zh_a_spot_df['changepercent'] > 0)
down_count = sum(stock_zh_a_spot_df['changepercent'] < 0)

# Get top gainers
top_gainers = stock_zh_a_spot_df.sort_values('changepercent', ascending=False).head(10)
top_losers = stock_zh_a_spot_df.sort_values('changepercent', ascending=True).head(10)

# Get industry sectors
stock_zh_a_industry_df = ak.stock_zh_a_industry()
industry_summary = stock_zh_a_industry_df.groupby('industry')['changepercent'].mean().sort_values(ascending=False).head(5)

result = {
    "date": latest.name.strftime('%Y-%m-%d'),
    "shanghai": {
        "close": float(latest.close),
        "change": float((latest.close - latest.open) / latest.open * 100)
    },
    "upCount": int(up_count),
    "downCount": int(down_count),
    "topGainers": top_gainers[['name', 'code', 'changepercent']].to_dict('records'),
    "topLosers": top_losers[['name', 'code', 'changepercent']].to_dict('records'),
    "hotIndustries": list(industry_summary.items())
}

print(json.dumps(result, ensure_ascii=False))
`;
        const output = execSync(`python -c "${pythonCode.replace(/"/g, '\\"')}"`, { encoding: 'utf8', maxBuffer: 1024 * 1024 * 2 });
        return JSON.parse(output);
    } catch (e) {
        console.error('Failed to get market data:', e.message);
        console.log('Make sure you have akshare installed: pip install akshare');
        return null;
    }
}

function generateXiaohongshu(data) {
    let content = `# 📈 A股今日收盘快报 ${data.date}\n\n`;
    
    content += `**上证指数**: ${data.shanghai.close.toFixed(2)}  ${data.shanghai.change >= 0 ? '+' : ''}${data.shanghai.change.toFixed(2)}%  ${data.shanghai.change >= 0 ? '📈' : '📉'}\n`;
    content += `**涨跌分布**: 上涨 ${data.upCount} 家  |  下跌 ${data.downCount} 家\n\n`;
    
    content += '🔥 热门板块 (涨幅前5):\n';
    data.hotIndustries.forEach(([name, change], i) => {
        content += `${i+1}. ${name}  ${change >= 0 ? '+' : ''}${change.toFixed(2)}%\n`;
    });
    content += '\n';
    
    content += '🏆 涨幅榜 TOP 5:\n';
    data.topGainers.slice(0, 5).forEach((stock, i) => {
        content += `${i+1}. **${stock.name}** (${stock.code})  +${stock.changepercent.toFixed(2)}%\n`;
    });
    content += '\n';
    
    if (data.topLosers.length > 0) {
        content += '📉 跌幅榜 TOP 3:\n';
        data.topLosers.slice(0, 3).forEach((stock, i) => {
            content += `${i+1}. **${stock.name}** (${stock.code})  ${stock.changepercent.toFixed(2)}%\n`;
        });
        content += '\n';
    }
    
    content += '💬 今日小结:\n';
    if (data.upCount > data.downCount) {
        content += '今天普涨行情，多头占优，持股待涨就好～\n';
    } else {
        content += '今天调整为主，控制好仓位，等待机会～\n';
    }
    content += '\n';
    
    // Tags
    content += '#A股 #股票 #投资理财 #每日行情 #炒股 #投资 #财经\n';
    
    return content;
}

function generateWechat(data) {
    let content = `# 📈 A 股每日收盘快报 - ${data.date}\n\n`;
    
    content += '## 大盘概况\n\n';
    content += `- **上证指数**: ${data.shanghai.close.toFixed(2)}  (${data.shanghai.change >= 0 ? '+' : ''}${data.shanghai.change.toFixed(2)}%)\n`;
    content += `- **涨跌分布**: 上涨 ${data.upCount} 家，下跌 ${data.downCount} 家\n\n`;
    
    content += '## 热门板块\n\n';
    data.hotIndustries.forEach(([name, change], i) => {
        content += `${i+1}. **${name}**: ${change >= 0 ? '+' : ''}${change.toFixed(2)}%\n`;
    });
    content += '\n';
    
    content += '## 涨幅榜 TOP 10\n\n';
    content += '| 排名 | 股票名称 | 代码 | 涨幅 |\n';
    content += '|------|----------|------|------|\n';
    data.topGainers.forEach((stock, i) => {
        content += `| ${i+1} | ${stock.name} | ${stock.code} | **${stock.changepercent.toFixed(2)}%** |\n`;
    });
    content += '\n';
    
    content += '## 今日小结\n\n';
    if (data.upCount > data.downCount) {
        content += '今天整体上涨，市场情绪偏暖，可以轻仓参与热点。控制仓位，不要追高。\n';
    } else {
        content += '今天整体调整，耐心等待回调到位，不要着急抄底。\n';
    }
    
    return content;
}

function generate朋友圈(data) {
    let content = `📈 ${data.date} 收盘\n\n`;
    content += `上证指数: ${data.shanghai.close.toFixed(2)} ${data.shanghai.change >= 0 ? '+' : ''}${data.shanghai.change.toFixed(2)}%\n`;
    content += `上涨 ${data.upCount} | 下跌 ${data.downCount}\n\n`;
    content += `热门: ${data.hotIndustries.slice(0, 3).map(([name, c]) => name).join('、')}\n`;
    content += '\n平常心炒股，慢慢复利😊';
    
    return content;
}

function generateReport(data, platform = 'xiaohongshu') {
    switch (platform.toLowerCase()) {
        case 'xiaohongshu':
        case '小红书':
            return generateXiaohongshu(data);
        case 'wechat':
        case 'weixin':
        case '公众号':
            return generateWechat(data);
        case 'moments':
        case '朋友圈':
            return generate朋友圈(data);
        default:
            return generateXiaohongshu(data);
    }
}

module.exports = {
    getMarketData,
    generateReport,
    generateXiaohongshu,
    generateWechat
};

// CLI run
if (require.main === module) {
    const date = process.argv[2];
    const platform = process.argv[3] || 'xiaohongshu';
    
    console.log('Fetching market data...');
    const data = getMarketData();
    if (!data) {
        console.error('Failed to get market data');
        process.exit(1);
    }
    
    const report = generateReport(data, platform);
    console.log('\n' + '='.repeat(50));
    console.log(report);
    console.log('='.repeat(50));
}
