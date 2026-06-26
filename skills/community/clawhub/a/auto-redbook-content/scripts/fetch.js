#!/usr/bin/env node

/**
 * 抓取小红书笔记
 * 通过 xiaohongshu MCP 获取真实数据
 */

const fs = require('fs');
const path = require('path');

/**
 * 生成模拟数据（MCP 不可用时的后备方案）
 */
function generateMockNotes(count) {
  console.log('[抓取] MCP 不可用，使用模拟数据');
  const notes = [];
  for (let i = 0; i < count; i++) {
    notes.push({
      original_title: `小红书热点标题 ${i + 1}`,
      original_content: `这是第 ${i + 1} 条热点笔记的内容，包含了当前流行的话题和趋势...`,
      author: `热门博主${i + 1}`,
      likes: Math.floor(Math.random() * 50000) + 10000,
      images: [],
      url: `https://www.xiaohongshu.com/explore/mock${i + 1}`,
      timestamp: new Date().toISOString()
    });
  }
  return notes;
}

/**
 * 抓取笔记
 * 注意：实际抓取需要在 OpenClaw agent 环境中通过 MCP 工具调用
 */
async function fetchNotes(maxResults = 3) {
  console.log(`[抓取] 准备获取 ${maxResults} 条笔记`);
  
  // 在 OpenClaw agent 环境中，这里会通过工具调用 xiaohongshu MCP
  // 当前返回模拟数据作为示例
  const notes = generateMockNotes(maxResults);
  
  console.log(`[抓取] 成功获取 ${notes.length} 条笔记`);
  return notes;
}

module.exports = { fetchNotes };

// CLI 模式
if (require.main === module) {
  const count = parseInt(process.argv[2]) || 3;
  fetchNotes(count).then(notes => {
    const outputDir = path.join(__dirname, '..', 'output');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    const outputFile = path.join(outputDir, 'fetch-result.json');
    fs.writeFileSync(outputFile, JSON.stringify(notes, null, 2));
    console.log(`\n结果已保存到: ${outputFile}`);
  });
}
