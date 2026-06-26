#!/usr/bin/env node

/**
 * AI 资讯小红书完整流程脚本（演示数据版）
 * 
 * 说明：
 * 由于 Node.js 脚本无法直接调用 OpenClaw 的 web_search 工具，
 * 此脚本使用内置演示数据。
 * 
 * 如需真实数据，请由 OpenClaw 主流程：
 * 1. 使用 web_search 工具搜索
 * 2. 调用 create-xiaohongshu-content.js --news-json '...'
 * 
 * 使用方式：
 * node scripts/run-full-flow.js
 */

const { execSync } = require('child_process');
const path = require('path');

const SKILL_DIR = path.join(__dirname, '..');
const SCRIPTS_DIR = __dirname;

/**
 * 从 URL 提取域名
 */
function extractDomain(url) {
  try {
    return new URL(url).hostname.replace('www.', '').split('.')[0];
  } catch (e) {
    return '网络来源';
  }
}

/**
 * 生成演示数据（模拟 24 小时内的 AI 资讯）
 */
function generateDemoNews() {
  // 这些是演示数据，实际应由 OpenClaw 主流程搜索真实数据
  return [
    {
      title: "OpenAI 发布 GPT-4.5，推理速度提升 3 倍",
      content: "OpenAI 今日凌晨突然发布 GPT-4.5 模型，在推理速度和准确性上都有显著提升，支持更快的实时对话和代码生成。",
      url: "https://openai.com/blog/gpt-4-5",
      time: "2 小时前",
      source: "OpenAI"
    },
    {
      title: "阿里千问 Qwen3 开源，直接对标 Llama3",
      content: "阿里达摩院宣布开源 Qwen3 系列模型，包含 7B、72B 等多个版本，性能大幅提升，支持多语言。",
      url: "https://qwenlm.github.io/",
      time: "5 小时前",
      source: "阿里达摩院"
    },
    {
      title: "MiniMax 完成 5 亿美元融资，估值破百亿",
      content: "国内 AI 独角兽 MiniMax 宣布完成新一轮融资，由红杉资本领投，投后估值超过 100 亿美元。",
      url: "https://www.minimax.io/",
      time: "8 小时前",
      source: "36 氪"
    },
    {
      title: "Anthropic 推出 Claude 3.5，安全性大幅提升",
      content: "Anthropic 发布 Claude 3.5 系列，在保持性能的同时显著提升了安全性，减少幻觉和有害输出。",
      url: "https://www.anthropic.com/",
      time: "12 小时前",
      source: "Anthropic"
    },
    {
      title: "Google Gemini 2.0 正式推送，多模态能力再升级",
      content: "Google 宣布 Gemini 2.0 正式向所有用户推送，图像理解和视频分析能力大幅提升，支持实时视频对话。",
      url: "https://deepmind.google/",
      time: "18 小时前",
      source: "Google DeepMind"
    }
  ];
}

/**
 * 主函数
 */
async function main() {
  console.log('🚀 AI 资讯小红书完整流程开始...\n');
  
  // 1. 准备资讯数据
  console.log('📡 阶段 1：准备 AI 资讯\n');
  
  const newsData = generateDemoNews();
  
  console.log(`✅ 共 ${newsData.length} 条资讯\n`);
  console.log('📝 资讯列表:');
  newsData.forEach((news, i) => {
    console.log(`  ${i + 1}. ${news.title} (${news.time}) - ${news.source}`);
  });
  console.log();
  
  // 2. 调用生成脚本
  console.log('🎨 阶段 2：生成小红书文案和 HTML 封面\n');
  
  try {
    const jsonStr = JSON.stringify(newsData);
    execSync(`node "${path.join(SCRIPTS_DIR, 'create-xiaohongshu-content.js')}" --news-json '${jsonStr}'`, {
      encoding: 'utf-8',
      stdio: 'inherit',
      cwd: SKILL_DIR
    });
    
    console.log('\n✅ 完整流程完成！\n');
    console.log('📌 提示：当前使用演示数据。如需真实搜索数据，请使用 OpenClaw 主流程调用。\n');
  } catch (e) {
    console.error('❌ 生成失败:', e.message);
    console.log('\n💡 请检查脚本权限和依赖\n');
    process.exit(1);
  }
}

// 运行
main().catch(console.error);
