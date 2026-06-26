// 每日早会简报生成脚本
// 使用OpenClaw内置工具链实现，无需外部依赖

async function generateMorningBrief() {
    console.log('开始生成每日早会简报...');
    
    const today = new Date().toISOString().split('T')[0];
    console.log(`日期: ${today}`);
    
    // 搜索关键词
    const queries = [
        `${today} 国内重要新闻`,
        `${today} 国际热点事件`,
        `${today} 财经要闻`,
        `${today} 科技行业动态`,
        `${today} 政策新规`
    ];
    
    let allNews = [];
    
    // 使用web_search工具搜索资讯
    for (const query of queries) {
        try {
            const result = await openclaw.tool('web_search', {
                query: query,
                count: 5
            });
            if (result && result.results) {
                allNews = allNews.concat(result.results);
            }
        } catch (error) {
            console.error(`搜索[${query}]失败:`, error.message);
        }
    }
    
    // 去重
    const seenUrls = new Set();
    const uniqueNews = allNews.filter(news => {
        const url = news.url || '';
        if (url && !seenUrls.has(url)) {
            seenUrls.add(url);
            return true;
        }
        return false;
    });
    
    // 生成简报内容
    let brief = `# 🌅 每日早会简报 ${today}\n\n`;
    brief += `---\n\n`;
    brief += `## 📢 今日重点资讯\n\n`;
    
    uniqueNews.slice(0, 15).forEach((news, idx) => {
        brief += `### ${idx + 1}. ${news.title || '无标题'}\n`;
        brief += `> ${news.snippet || '无摘要'}\n`;
        brief += `> 🔗 详情：${news.url || '无链接'}\n\n`;
    });
    
    brief += `---\n\n`;
    brief += `## 🎯 今日行动建议\n`;
    brief += `1. 各部门负责人梳理相关资讯对业务的影响\n`;
    brief += `2. 重点关注政策类动态，及时调整业务策略\n`;
    brief += `3. 行业相关新闻组织团队内部同步讨论\n`;
    
    // 保存简报
    const savePath = `C:\\Users\\Admin\\.qclaw\\workspace\\早会简报_${today}.md`;
    await openclaw.tool('write', {
        path: savePath,
        content: brief
    });
    
    console.log(`简报已保存: ${savePath}`);
    
    // 发送给CEO
    await openclaw.tool('message', {
        action: 'send',
        target: 'CEO',
        message: `【每日早会简报 ${today}】请查收今日最新资讯汇总。`,
        media: savePath
    });
    
    console.log('简报已发送给CEO');
    return brief;
}

// 导出函数
module.exports = { generateMorningBrief };

// 如果直接运行
if (require.main === module) {
    generateMorningBrief().catch(console.error);
}