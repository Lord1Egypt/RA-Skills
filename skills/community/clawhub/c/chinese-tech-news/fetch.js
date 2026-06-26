// 中文科技资讯抓取 - 钛媒体 + 虎嗅 + 36氪 + 爱范儿
// 使用 RSS 源，无 API Key 依赖

const https = require('https');

function fetchUrl(url) {
    return new Promise((resolve, reject) => {
        https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
            // 跟随重定向
            if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
                https.get(res.headers.location, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res2) => {
                    let data = '';
                    res2.on('data', chunk => data += chunk);
                    res2.on('end', () => resolve(data));
                }).on('error', reject);
                return;
            }
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve(data));
        }).on('error', reject);
    });
}

function parseRSS(xml, sourceName) {
    const articles = [];
    const itemRegex = /<item>([\s\S]*?)<\/item>/g;
    let itemMatch;
    while ((itemMatch = itemRegex.exec(xml)) !== null) {
        const item = itemMatch[1];
        const titleMatch = /<title[^>]*><!\[CDATA\[([\s\S]*?)\]\]><\/title>|<title[^>]*>([^<]+)<\/title>/.exec(item);
        const linkMatch = /<link>([^<]+)<\/link>|<link[^>]*><!\[CDATA\[([^\]]+)\]\]><\/link>|<link[^>]*href="([^"]+)"[^>]*>/.exec(item);
        const title = titleMatch ? (titleMatch[1] || titleMatch[2]).replace(/<[^>]+>/g, '').trim() : '';
        const url = linkMatch ? (linkMatch[1] || linkMatch[2] || linkMatch[3] || '').replace(/<!\[CDATA\[|\]\]>/g, '').trim() : '';
        if (title && url && !url.startsWith('http://pic')) {
            articles.push({ title, url, source: sourceName });
        }
    }
    return articles;
}

async function main() {
    console.log('正在抓取中文科技资讯...\n');
    
    const sources = [
        { name: '钛媒体', url: 'https://www.tmtpost.com/rss' },
        { name: '虎嗅', url: 'https://www.huxiu.com/rss/0.xml' },
        { name: '36氪', url: 'https://36kr.com/feed' },
        { name: '爱范儿', url: 'https://www.ifanr.com/feed' }
    ];
    
    const results = [];
    for (const s of sources) {
        try {
            const xml = await fetchUrl(s.url);
            const articles = parseRSS(xml, s.name);
            results.push({ source: s.name, count: articles.length, articles: articles.slice(0, 8) });
            console.log(`${s.name}: ${articles.length} 条`);
        } catch(e) {
            console.log(`${s.name}: 获取失败 (${e.message})`);
        }
    }
    
    console.log('\n--- 合并输出（前20条）---\n');
    
    // 按时间合并（简单取所有）
    const all = results.flatMap(r => r.articles);
    const top20 = all.slice(0, 20);
    
    top20.forEach((a, i) => {
        console.log(`${i+1}. [${a.source}] ${a.title}`);
        console.log(`   ${a.url}\n`);
    });
}

main().catch(e => { console.error(e.message); process.exit(1); });
