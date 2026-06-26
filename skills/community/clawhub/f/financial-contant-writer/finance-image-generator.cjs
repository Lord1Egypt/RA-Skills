#!/usr/bin/env node

/**
 * 财税文章配图工具
 * 专为财税、审计、税务类文章定制
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const API_KEY = 'qekoFPuHK6YT6369knsRXQ6ZeUkgbI2xPZKZ3qaRvyk';
const IMAGES_DIR = path.join(__dirname, '../articles/images');

// 财税主题关键词映射
const FINANCE_KEYWORDS = {
    // 审计类
    '审计': ['accounting', 'audit', 'financial statements', 'calculator'],
    '财务报表': ['spreadsheet', 'charts', 'financial report', 'data'],
    '现金流量': ['money', 'cash', 'currency', 'banking'],

    // 税务类
    '税务': ['tax', 'tax preparation', 'taxes', 'document'],
    '增值税': ['invoice', 'receipt', 'business', 'accounting'],
    '企业所得税': ['business', 'office', 'corporate', 'meeting'],
    '个税': ['personal finance', 'money', 'tax', 'calculator'],

    // 政策解读
    '政策': ['document', 'law', 'regulation', 'business'],
    '法规': ['law', 'court', 'justice', 'legal'],
    '新规': ['document', 'announcement', 'news', 'update'],

    // 风险提示
    '风险': ['warning', 'risk', 'alert', 'attention'],
    '稽查': ['audit', 'inspection', 'review', 'checklist'],
    '合规': ['checklist', 'document', 'compliance', 'regulation'],

    // 技术工具
    'Excel': ['spreadsheet', 'computer', 'laptop', 'office'],
    '财务软件': ['software', 'technology', 'computer', 'app'],
    '数据分析': ['chart', 'graph', 'data', 'analytics'],

    // 行业场景
    '企业经营': ['business', 'office', 'meeting', 'teamwork'],
    '财务总监': ['business', 'leadership', 'meeting', 'professional'],
    '会计师事务所': ['office', 'professional', 'teamwork', 'meeting'],

    // 通用
    '财税': ['accounting', 'finance', 'calculator', 'money'],
    '审计': ['audit', 'review', 'checklist', 'document'],
    '财务': ['finance', 'money', 'banking', 'investment']
};

/**
 * 根据文章类型推荐关键词
 */
function getKeywordsForArticleType(articleType) {
    const typeMap = {
        '案例分析': ['office', 'business meeting', 'professional', 'teamwork'],
        '政策解读': ['document', 'law', 'regulation', 'announcement'],
        '风险提示': ['warning', 'risk', 'alert', 'inspection'],
        '实务指南': ['checklist', 'document', 'spreadsheet', 'tutorial'],
        '经验分享': ['professional', 'business', 'success', 'achievement'],
        '技术教程': ['computer', 'software', 'spreadsheet', 'technology'],
        '行业洞察': ['business', 'analytics', 'chart', 'growth'],
        '税务': ['tax', 'document', 'calculator', 'money'],
        '审计': ['audit', 'review', 'checklist', 'document'],
        '财务': ['finance', 'spreadsheet', 'chart', 'analytics']
    };

    return typeMap[articleType] || ['business', 'document', 'office'];
}

/**
 * 搜索并下载图片
 */
async function downloadImage(keyword, orientation, filename) {
    const url = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(keyword)}&orientation=${orientation}&per_page=1&client_id=${API_KEY}`;

    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                if (res.statusCode === 200) {
                    try {
                        const json = JSON.parse(data);
                        const results = json.results || [];

                        if (results.length > 0) {
                            const img = results[0];
                            const imageUrl = img.urls.regular;

                            https.get(imageUrl, (imgRes) => {
                                if (imgRes.statusCode === 200) {
                                    const filePath = path.join(IMAGES_DIR, filename);
                                    const stream = fs.createWriteStream(filePath);
                                    imgRes.pipe(stream);
                                    stream.on('close', () => {
                                        console.log(`✅ ${filename}`);
                                        resolve({
                                            filename,
                                            keyword,
                                            url: imageUrl,
                                            description: img.description || img.alt_description,
                                            author: img.user.name
                                        });
                                    });
                                    stream.on('error', reject);
                                } else {
                                    reject(new Error(`下载失败: ${imgRes.statusCode}`));
                                }
                            }).on('error', reject);
                        } else {
                            console.log(`⚠️  ${filename} (未找到 "${keyword}" 的图片)`);
                            resolve(null);
                        }
                    } catch (e) {
                        reject(e);
                    }
                } else {
                    reject(new Error(`API错误: ${res.statusCode}`));
                }
            });
        }).on('error', reject);
    });
}

/**
 * 为财税文章生成配图
 */
async function generateFinanceImages(articlePath, articleType = '税务', articleTopic = '财税') {
    console.log(`\n📸 正在为财税文章生成配图...`);
    console.log(`📄 文章: ${articlePath}`);
    console.log(`📝 类型: ${articleType}`);
    console.log(`🎯 主题: ${articleTopic}\n`);

    // 确保目录存在
    if (!fs.existsSync(IMAGES_DIR)) {
        fs.mkdirSync(IMAGES_DIR, { recursive: true });
    }

    // 获取关键词
    const keywords = getKeywordsForArticleType(articleType);

    // 如果主题有特定关键词，优先使用
    const topicKeywords = FINANCE_KEYWORDS[articleTopic];
    if (topicKeywords) {
        keywords.unshift(...topicKeywords.slice(0, 2));
    }

    // 生成图片配置
    const images = [];
    const timestamp = new Date().toISOString().split('T')[0].replace(/-/g, '');

    // 封面图
    images.push({ name: `01-封面-${timestamp}`, keyword: keywords[0], orientation: 'landscape' });
    images.push({ name: `02-封面备选-${timestamp}`, keyword: keywords[1] || 'business', orientation: 'landscape' });

    // 正文配图（根据类型）
    const contentImages = keywords.slice(0, 4);
    contentImages.forEach((keyword, index) => {
        images.push({ name: `0${index + 3}-正文-${keyword}`, keyword, orientation: 'landscape' });
    });

    // 结尾图
    images.push({ name: `07-结尾-${timestamp}`, keyword: 'success', orientation: 'landscape' });

    // 下载图片
    const results = [];
    for (const img of images) {
        const filename = `${img.name}.jpg`;
        try {
            const result = await downloadImage(img.keyword, img.orientation, filename);
            if (result) {
                results.push(result);
            }
            await new Promise(resolve => setTimeout(resolve, 500));
        } catch (e) {
            console.error(`❌ ${filename}: ${e.message}`);
        }
    }

    console.log(`\n✅ 下载完成!`);
    console.log(`📊 成功下载: ${results.length}/${images.length} 张图片\n`);

    return results;
}

/**
 * 主函数
 */
async function main() {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log(`
📸 财税文章配图工具

用法:
  node finance-image-generator.cjs <文章路径> [选项]

选项:
  --type <类型>   文章类型 (审计/税务/财务/政策/风险/案例/指南/经验/技术/洞察)
  --topic <主题>  文章主题
  --output <文件> 输出配图信息到文件

示例:
  # 为税务文章生成配图
  node finance-image-generator.cjs ../articles/税务文章.md --type 税务

  # 为审计文章生成配图
  node finance-image-generator.cjs ../articles/审计文章.md --type 审计

  # 为财务分析文章生成配图
  node finance-image-generator.cjs ../articles/财务分析.md --type 财务

  # 自定义主题
  node finance-image-generator.cjs ../articles/文章.md --topic 增值税

支持的类型:
  - 审计
  - 税务
  - 财务
  - 政策
  - 风险
  - 案例 (案例分析)
  - 指南 (实务指南)
  - 经验 (经验分享)
  - 技术 (技术教程)
  - 洞察 (行业洞察)
        `);
        return;
    }

    const articlePath = args[0];
    let articleType = '税务';
    let articleTopic = '财税';
    let outputFile = null;

    // 解析参数
    for (let i = 1; i < args.length; i++) {
        if (args[i] === '--type' && args[i + 1]) {
            articleType = mapTypeAlias(args[i + 1]);
            i++;
        } else if (args[i] === '--topic' && args[i + 1]) {
            articleTopic = args[i + 1];
            i++;
        } else if (args[i] === '--output' && args[i + 1]) {
            outputFile = args[i + 1];
            i++;
        }
    }

    // 生成配图
    const results = await generateFinanceImages(articlePath, articleType, articleTopic);

    // 输出图片信息
    console.log('📖 图片列表:\n');
    results.forEach((img, index) => {
        console.log(`${index + 1}. ${img.filename}`);
        console.log(`   关键词: ${img.keyword}`);
        console.log(`   描述: ${img.description || '无'}`);
        console.log(`   作者: ${img.author}`);
        console.log(`   路径: ${path.join(IMAGES_DIR, img.filename)}`);
        console.log('');
    });

    // 如果需要输出到文件
    if (outputFile) {
        let markdown = `# 财税文章配图\n\n`;
        markdown += `**生成时间**: ${new Date().toLocaleString('zh-CN')}\n\n`;
        markdown += `**文章类型**: ${articleType}\n\n`;
        markdown += `**文章主题**: ${articleTopic}\n\n`;

        markdown += `## 📷 图片列表\n\n`;
        results.forEach((img, index) => {
            markdown += `### ${index + 1}. ${img.filename}\n\n`;
            markdown += `- **关键词**: ${img.keyword}\n`;
            markdown += `- **描述**: ${img.description || '无'}\n`;
            markdown += `- **作者**: ${img.author}\n`;
            markdown += `- **路径**: \`${path.join(IMAGES_DIR, img.filename)}\`\n\n`;
        });

        fs.writeFileSync(outputFile, markdown, 'utf-8');
        console.log(`✅ 配图信息已保存到: ${outputFile}\n`);
    }
}

/**
 * 类型别名映射
 */
function mapTypeAlias(type) {
    const aliasMap = {
        '审计': '审计',
        '税': '税务',
        '税务': '税务',
        '财': '财务',
        '财务': '财务',
        '政策': '政策解读',
        '法规': '政策解读',
        '风险': '风险提示',
        '案例': '案例分析',
        '指南': '实务指南',
        '教程': '技术教程',
        '洞察': '行业洞察',
        '经验': '经验分享'
    };

    return aliasMap[type] || type;
}

// 运行
if (require.main === module) {
    main().catch(console.error);
}

module.exports = {
    generateFinanceImages,
    FINANCE_KEYWORDS
};
