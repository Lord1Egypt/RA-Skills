#!/usr/bin/env node
/**
 * 从 extract.js 的 JSON 输出中提取新概念
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
    const concepts = [];
    
    for (const chData of Object.values(data.channels || {})) {
      if (chData?.concepts) {
        chData.concepts.forEach(c => {
          if (c.term) concepts.push({ term: c.term, definition: c.definition });
        });
      }
    }
    
    // 去重并输出前3条
    const seen = new Set();
    const unique = concepts.filter(c => {
      if (seen.has(c.term)) return false;
      seen.add(c.term);
      return true;
    }).slice(0, 3);
    
    unique.forEach(c => {
      if (c.definition) {
        console.log(`${c.term}：${c.definition}`);
      } else {
        console.log(`${c.term}`);
      }
    });
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
});
