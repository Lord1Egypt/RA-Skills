#!/usr/bin/env node

/**
 * AI Daily Brief - Tavily Search Script
 * 使用 Tavily API 搜索 AI 行业新闻
 * 优先级：Tavily > 博查 > SearXNG
 */

import { execSync } from 'child_process';

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
    return result; // Return raw markdown output
  } catch (error) {
    console.error(`Tavily search failed for query: ${query}`);
    console.error(error.message);
    return null;
  }
}

// 主函数
async function main() {
  console.log('🔍 Starting AI Daily Brief search...\n');
  
  const results = {
    companies: null,
    leaders: null,
    products: null,
    papers: null
  };
  
  // 优先使用 Tavily
  console.log('📊 Searching AI company news (Tavily)...');
  results.companies = searchTavily(queries.companies, 10, 'news');
  
  console.log('💬 Searching AI leader statements (Tavily)...');
  results.leaders = searchTavily(queries.leaders, 8, 'news');
  
  console.log('🛠️  Searching AI product releases (Tavily)...');
  results.products = searchTavily(queries.products, 10, 'news');
  
  console.log('📄 Searching AI research papers (Tavily)...');
  results.papers = searchTavily(queries.papers, 10, 'general');
  
  // 输出结果摘要
  console.log('\n✅ Search complete!\n');
  console.log('=== AI Company News ===');
  console.log(results.companies || 'No results');
  console.log('\n=== AI Leader Statements ===');
  console.log(results.leaders || 'No results');
  console.log('\n=== AI Product Releases ===');
  console.log(results.products || 'No results');
  console.log('\n=== AI Research Papers ===');
  console.log(results.papers || 'No results');
}

main().catch(console.error);
