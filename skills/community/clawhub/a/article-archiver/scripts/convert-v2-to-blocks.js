#!/usr/bin/env node

/**
 * 将 v2 格式转换为 contentBlocks 格式
 * 输入：v2 的 JSON 输出（content 字符串 + images 数组）
 * 输出：contentBlocks 数组（文本和图片交替）
 */

const fs = require('fs');

if (process.argv.length < 3) {
  console.error('Usage: node convert-v2-to-blocks.js <v2_json_file>');
  process.exit(1);
}

const v2Data = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

// 解析 content，找到所有 ![图片](...) 标记
const content = v2Data.content;
const images = v2Data.images || [];

// 分割内容，按图片标记分段
const contentBlocks = [];
let currentText = '';
let imageIndex = 0;

// 正则匹配 ![图片](url) 格式
const imageRegex = /!\[图片\]\([^\)]+\)/g;
let lastIndex = 0;
let match;

while ((match = imageRegex.exec(content)) !== null) {
  // 添加图片前的文本
  const textBefore = content.substring(lastIndex, match.index);
  if (textBefore.trim()) {
    contentBlocks.push({
      type: 'text',
      content: textBefore.trim()
    });
  }
  
  // 添加图片
  if (imageIndex < images.length) {
    contentBlocks.push({
      type: 'image',
      url: images[imageIndex] + '?format=jpg&name=large'
    });
    imageIndex++;
  }
  
  lastIndex = match.index + match[0].length;
}

// 添加最后的文本
const textAfter = content.substring(lastIndex);
if (textAfter.trim()) {
  contentBlocks.push({
    type: 'text',
    content: textAfter.trim()
  });
}

// 输出结果
const result = {
  title: v2Data.title,
  author: v2Data.author,
  username: v2Data.username,
  contentBlocks
};

console.log(JSON.stringify(result, null, 2));
