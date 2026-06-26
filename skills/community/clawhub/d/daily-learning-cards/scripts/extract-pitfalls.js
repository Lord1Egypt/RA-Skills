#!/usr/bin/env node
/**
 * 从 extract.js 的 JSON 输出中提取踩坑记录
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
    const pitfalls = [];
    
    for (const chData of Object.values(data.channels || {})) {
      if (chData?.pitfalls) {
        chData.pitfalls.forEach(p => {
          if (p.problem) pitfalls.push({ problem: p.problem });
        });
      }
    }
    
    // 输出前3条
    pitfalls.slice(0, 3).forEach(p => console.log(p.problem));
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
});
