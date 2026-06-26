#!/usr/bin/env node
/**
 * 从 extract.js 的 JSON 输出中提取金句
 */

const fs = require('fs');

let input = '';
process.stdin.setEncoding('utf8');

process.stdin.on('data', (chunk) => {
  input += chunk;
});

process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const insights = new Set();
    
    for (const chData of Object.values(data.channels || {})) {
      if (chData?.insights) {
        chData.insights.forEach(i => insights.add(i));
      }
    }
    
    // 输出前3条
    let count = 0;
    for (const i of insights) {
      if (count >= 3) break;
      console.log(i);
      count++;
    }
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
});
