#!/usr/bin/env node

/**
 * 获取新闻详情
 * 用法：node get-article.js <article_id>
 * 示例：node get-article.js 8533
 */

const https = require('https');

function stripHtml(html) {
  if (!html) return '';
  return html
    .replace(/<p>/g, '\n')
    .replace(/<\/p>/g, '')
    .replace(/<br>/g, '\n')
    .replace(/<br\/>/g, '\n')
    .replace(/<strong>/g, '**')
    .replace(/<\/strong>/g, '**')
    .replace(/<[^>]*>/g, '')
    .trim();
}

function getArticleDetail(articleId) {
  if (!articleId) {
    console.error('❌ 请提供文章 ID');
    console.error('用法：node get-article.js <article_id>');
    console.error('示例：node get-article.js 8533');
    process.exit(1);
  }

  const url = `https://api.cjiot.cc/api/v1/articles/${articleId}`;

  https.get(url, (res) => {
    let data = '';

    res.on('data', (chunk) => {
      data += chunk;
    });

    res.on('end', () => {
      try {
        const result = JSON.parse(data);
        
        if (result.code !== 200) {
          console.error(`❌ API 返回错误：${result.message || '未知错误'}`);
          process.exit(1);
        }

        const article = result.data;
        const content = article.content || {};

        console.log('\n' + '═'.repeat(60));
        console.log(`\n📄 ${article.title}\n`);
        console.log('─'.repeat(60));
        console.log(`📁 分类：${article.category_name || '未知'}`);
        console.log(`🔥 热度：${article.heat}`);
        console.log(`🕐 发布时间：${article.publish_time || article.created_at}`);
        console.log('─'.repeat(60));

        if (article.summary) {
          console.log('\n📝 新闻摘要：\n');
          console.log(article.summary);
        }

        if (content.story) {
          console.log('\n📖 详细内容：\n');
          console.log(stripHtml(content.story));
        }

        if (content.impact) {
          console.log('\n💡 影响分析：\n');
          console.log(stripHtml(content.impact));
        }

        console.log('\n' + '═'.repeat(60) + '\n');

      } catch (error) {
        console.error(`❌ 解析 JSON 失败：${error.message}`);
        process.exit(1);
      }
    });
  }).on('error', (error) => {
    console.error(`❌ 请求失败：${error.message}`);
    process.exit(1);
  });
}

// 获取命令行参数
const articleId = process.argv[2];
getArticleDetail(articleId);
