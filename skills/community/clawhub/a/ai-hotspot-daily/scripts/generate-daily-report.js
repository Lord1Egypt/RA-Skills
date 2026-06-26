#!/usr/bin/env node
/**
 * 生成热点日报
 * 用法：node generate-daily-report.js --date 2026-03-23 --send
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

/**
 * 生成 Markdown 日报
 */
function generateMarkdown(data) {
  let md = `# 🔥 每日热点 - ${data.date}\n\n`;
  md += `> 生成时间：${new Date(data.generatedAt).toLocaleString('zh-CN')}\n\n`;
  md += `---\n\n`;
  
  // 各平台热榜
  for (const source of data.sources) {
    md += `## ${source.name} TOP${Math.min(source.items.length, 20)}\n\n`;
    
    source.items.slice(0, 20).forEach((item, i) => {
      const emoji = getHotEmoji(i);
      md += `${emoji} **${i + 1}. ${item.title}**\n`;
      if (item.description) {
        md += `   - ${truncate(item.description, 50)}\n`;
      }
      md += `\n`;
    });
    
    md += `---\n\n`;
  }
  
  // 跨平台热点
  md += `## 🌐 跨平台热点\n\n`;
  const crossPlatform = getCrossPlatformHotspots(data.all_items);
  crossPlatform.slice(0, 10).forEach((item, i) => {
    md += `${i + 1}. **${item.title}**\n`;
    md += `   - 出现在：${item.source}\n`;
    md += `   - AI 建议：${item.suggestion}\n\n`;
  });
  
  md += `---\n\n`;
  
  // AI 使用指南
  md += `## 🤖 AI 使用指南\n\n`;
  md += `### 如何引用\n`;
  md += `当用户提到热点事件时：\n`;
  md += `1. 从本文检索相关条目\n`;
  md += `2. 提取关键信息\n`;
  md += `3. 客观陈述事实\n`;
  md += `4. 避免主观评价\n\n`;
  
  md += `### 注意事项\n`;
  md += `- 不传播未经证实的消息\n`;
  md += `- 不涉及敏感政治话题\n`;
  md += `- 不站队、不引战\n`;
  md += `- 提醒用户核实信息\n\n`;
  
  md += `---\n`;
  md += `*本日报由 AI 自动生成，数据来源于公开网络*\n`;
  
  return md;
}

/**
 * 生成 JSON 数据（AI 专用）
 */
function generateJSON(data) {
  return {
    date: data.date,
    type: 'daily-hotspot',
    version: '1.0',
    summary: {
      total_sources: data.sources.length,
      total_items: data.total_count,
      top_3: data.all_items.slice(0, 3).map(i => i.title)
    },
    hotspots: data.all_items.map(item => ({
      title: item.title,
      source: item.source,
      rank: item.rank || 0,
      sentiment: item.sentiment,
      ai_suggestion: item.suggestion,
      keywords: extractKeywords(item.title),
      url: item.link
    })),
    cross_platform: getCrossPlatformHotspots(data.all_items).slice(0, 20)
  };
}

/**
 * 获取跨平台热点
 */
function getCrossPlatformHotspots(items) {
  const titleMap = new Map();
  
  for (const item of items) {
    const key = item.title.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '').toLowerCase();
    if (!titleMap.has(key)) {
      titleMap.set(key, []);
    }
    titleMap.get(key).push(item);
  }
  
  const crossPlatform = [];
  for (const [key, items] of titleMap) {
    if (items.length >= 2) {
      crossPlatform.push({
        title: items[0].title,
        sources: [...new Set(items.map(i => i.source))],
        count: items.length,
        ...items[0]
      });
    }
  }
  
  return crossPlatform.sort((a, b) => b.count - a.count);
}

/**
 * 提取关键词
 */
function extractKeywords(title) {
  // 简单分词
  const stopwords = ['的', '了', '是', '在', '就', '都', '而', '及', '与', '着'];
  const words = title.split(/[\s,，.。!?！？]+/);
  return words.filter(w => w.length > 1 && !stopwords.includes(w)).slice(0, 5);
}

/**
 * 截断文本
 */
function truncate(text, length) {
  if (!text) return '';
  return text.length > length ? text.substring(0, length) + '...' : text;
}

/**
 * 获取热点 emoji
 */
function getHotEmoji(rank) {
  if (rank === 0) return '🔥';
  if (rank === 1) return '🥇';
  if (rank === 2) return '🥈';
  if (rank === 3) return '🥉';
  return '📌';
}

/**
 * 发送到微信
 */
function sendToWechat(markdown, notifyUser) {
  const tempFile = '/tmp/hotspot-daily.md';
  fs.writeFileSync(tempFile, markdown);
  
  // 分段发送（微信消息长度限制）
  const sections = markdown.split('---');
  
  for (let i = 0; i < Math.min(sections.length, 5); i++) {
    const section = sections[i].trim();
    if (section.length > 10) {
      const cmd = `openclaw message send --channel openclaw-weixin --account d72d5b576646-im-bot --target "${notifyUser}" --message "${section.replace(/"/g, '\\"')}"`;
      try {
        execSync(cmd, { stdio: 'pipe' });
        console.log(`✅ 发送第 ${i + 1} 部分`);
      } catch (error) {
        console.error(`❌ 发送失败：${error.message}`);
      }
      // 避免频率限制
      if (i < sections.length - 1) {
        require('deasync').sleep(1000);
      }
    }
  }
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  let date = new Date().toISOString().split('T')[0];
  let send = false;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--date' && args[i + 1]) {
      date = args[i + 1];
      i++;
    } else if (args[i] === '--send') {
      send = true;
    }
  }
  
  console.log(`🦆 生成热点日报：${date}\n`);
  
  // 读取热点数据
  const dataFile = `/home/lin/.openclaw/extensions/openclaw-weixin/skills/hotspot-aggregator/data/hotspots-${date}.json`;
  
  if (!fs.existsSync(dataFile)) {
    console.error(`❌ 数据文件不存在：${dataFile}`);
    console.error('请先运行：node fetch-hotspots.js');
    process.exit(1);
  }
  
  const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
  
  // 生成 Markdown
  const markdown = generateMarkdown(data);
  
  // 保存 Markdown
  const mdFile = `/home/lin/.openclaw/extensions/openclaw-weixin/skills/hotspot-aggregator/data/daily-${date}.md`;
  fs.writeFileSync(mdFile, markdown);
  console.log(`💾 Markdown 已保存：${mdFile}`);
  
  // 生成 JSON
  const json = generateJSON(data);
  const jsonFile = `/home/lin/.openclaw/extensions/openclaw-weixin/skills/hotspot-aggregator/data/daily-${date}.json`;
  fs.writeFileSync(jsonFile, JSON.stringify(json, null, 2));
  console.log(`💾 JSON 已保存：${jsonFile}`);
  
  // 发送到微信
  if (send) {
    const configPath = path.join(process.env.HOME, '.openclaw/hotspot/config.json');
    let notifyUser = '';
    
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      notifyUser = config.notifyUser || '';
    }
    
    if (notifyUser) {
      console.log('\n📤 发送到微信...');
      sendToWechat(markdown, notifyUser);
    } else {
      console.error('❌ 未配置 notifyUser，无法发送');
    }
  }
  
  console.log('\n✅ 日报生成完成！');
  console.log('\n💡 使用 --send 参数发送到微信');
}

main();
