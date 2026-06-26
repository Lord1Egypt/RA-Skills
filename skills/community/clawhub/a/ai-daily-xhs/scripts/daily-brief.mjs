#!/usr/bin/env node

/**
 * AI Daily Brief - 完整简报生成脚本
 * 执行搜索 + 格式化输出 + 推送
 */

import { execSync } from 'child_process';
import { writeFile } from 'fs/promises';

// Tavily 脚本绝对路径
const TAVILY_SCRIPT = '/home/admin/.openclaw/workspace/skills/tavily-search/scripts/search.mjs';

// 搜索查询模板
const queries = {
  companies: "OpenAI OR Google AI OR Microsoft AI OR Meta AI OR Anthropic OR DeepMind news yesterday",
  leaders: "Sam Altman OR Satya Nadella OR Sundar Pichai OR Mark Zuckerberg OR Dario Amodei AI statement yesterday",
  products: "LLM OR AI Agent OR AI Skills OR RAG new release launch product announcement yesterday",
  papers: "arXiv cs.CL cs.LG cs.AI LLM Agent RAG knowledge base paper yesterday"
};

// 执行 Tavily 搜索
function searchTavily(query, count = 10, topic = 'news') {
  try {
    const cmd = `node "${TAVILY_SCRIPT}" "${query}" -n ${count} --topic ${topic}`;
    const result = execSync(cmd, { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 });
    return result;
  } catch (error) {
    console.error(`Tavily search failed for query: ${query}`);
    console.error(error.message);
    return null;
  }
}

// 解析 Tavily 结果，提取新闻条目
function parseTavilyResult(markdown) {
  if (!markdown) return [];
  
  const items = [];
  const lines = markdown.split('\n');
  let currentItem = null;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // 匹配新闻条目：- **标题** (relevance: XX%)
    if (line.startsWith('- **') && line.includes('relevance:')) {
      if (currentItem) items.push(currentItem);
      
      // 提取标题（去掉 relevance 部分）
      const titleMatch = line.match(/- \*\*(.+?)\*\* \(relevance:/);
      
      currentItem = {
        title: titleMatch ? titleMatch[1].trim() : '未知标题',
        url: '',
        source: '',
        snippet: ''
      };
    } else if (currentItem && line.trim().startsWith('http')) {
      // URL 行
      currentItem.url = line.trim().split(' ')[0];
    } else if (currentItem && line.trim().startsWith('*') && !line.startsWith('-')) {
      // 摘要行（以 * 开头但不是列表项）
      const snippet = line.replace(/^\*\s*/, '').trim();
      if (snippet && !snippet.includes('relevance:')) {
        currentItem.snippet = snippet;
      }
    }
  }
  
  if (currentItem && currentItem.url) items.push(currentItem);
  return items;
}

// 格式化新闻条目
function formatNewsItem(item, index) {
  if (!item || !item.title) return '';
  
  // 从 URL 提取来源
  let source = '未知来源';
  try {
    const url = new URL(item.url);
    source = url.hostname.replace('www.', '');
  } catch (e) {}
  
  return `**${index}. ${item.title.replace(/\*\*/g, '')}**
**来源：** ${source}
${item.snippet ? `**摘要：** ${item.snippet}\n` : ''}**链接：** ${item.url}`;
}

// 生成日期字符串
function getDateString() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const weekday = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][now.getDay()];
  return {
    full: `${year}-${month}-${day}`,
    display: `${year}/${month}/${day} (${weekday})`,
    time: now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  };
}

// 主函数
async function main() {
  console.log('🔍 开始生成 AI 每日简报...\n');
  
  const date = getDateString();
  
  // 执行搜索
  console.log('📊 搜索大公司新闻...');
  const companiesRaw = searchTavily(queries.companies, 10, 'news');
  const companies = parseTavilyResult(companiesRaw);
  
  console.log('💬 搜索巨头言论...');
  const leadersRaw = searchTavily(queries.leaders, 8, 'news');
  const leaders = parseTavilyResult(leadersRaw);
  
  console.log('🛠️  搜索技术产品...');
  const productsRaw = searchTavily(queries.products, 10, 'news');
  const products = parseTavilyResult(productsRaw);
  
  console.log('📄 搜索学术论文...');
  const papersRaw = searchTavily(queries.papers, 10, 'general');
  const papers = parseTavilyResult(papersRaw);
  
  // 生成简报
  console.log('\n📝 生成简报...\n');
  
  const brief = `# 🤖 AI 每日简报 | ${date.display}

> 过去 24 小时全球 AI 行业重要动态，助你起床即知天下 AI 事

---

## 🏢 大公司新闻

${companies.length > 0 ? companies.slice(0, 5).map((item, i) => formatNewsItem(item, i + 1)).join('\n\n---\n\n') : '今日暂无重要动态'}

---

## 💬 巨头言论

${leaders.length > 0 ? leaders.slice(0, 3).map((item, i) => formatNewsItem(item, i + 1)).join('\n\n---\n\n') : '今日暂无重要动态'}

---

## 🛠️ 技术产品

${products.length > 0 ? products.slice(0, 3).map((item, i) => formatNewsItem(item, i + 1)).join('\n\n---\n\n') : '今日暂无重要动态'}

---

## 📄 精选论文

${papers.length > 0 ? papers.slice(0, 2).map((item, i) => formatNewsItem(item, i + 1)).join('\n\n---\n\n') : '今日暂无重要动态'}

---

## 📊 今日概览

| 类别 | 数量 |
|------|------|
| 大公司新闻 | ${companies.length} 条 |
| 巨头言论 | ${leaders.length} 条 |
| 技术产品 | ${products.length} 条 |
| 精选论文 | ${papers.length} 条 |

---

*简报生成时间：${date.time} | 信源：权威媒体/官方博客/头部达人/arXiv*
`;

  // 输出到控制台
  console.log(brief);
  
  // 保存到文件
  await writeFile(`/tmp/ai-daily-brief-${date.full}.md`, brief);
  console.log(`\n✅ 简报已保存到 /tmp/ai-daily-brief-${date.full}.md`);
  
  // 输出到日志
  console.log('\n--- 日志结束 ---');
  
  // 返回数据供推送使用
  return { brief, date, counts: { companies: companies.length, leaders: leaders.length, products: products.length, papers: papers.length } };
}

main().catch(console.error);
