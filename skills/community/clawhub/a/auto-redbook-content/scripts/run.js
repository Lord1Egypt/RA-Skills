#!/usr/bin/env node

/**
 * 主执行脚本
 * 流程：生成数据 → 构建提示词 → 保存本地
 */

const { fetchNotes } = require('./fetch');
const { rewriteNote } = require('./rewrite');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('开始执行 auto-redbook-content\n');
  
  try {
    const maxResults = parseInt(process.env.XHS_MAX_RESULTS || '3');
    
    // 1. 获取数据
    const notes = await fetchNotes(maxResults);
    console.log(`✓ 获取 ${notes.length} 条数据\n`);
    
    // 2. 生成提示词
    const results = [];
    for (let i = 0; i < notes.length; i++) {
      const note = notes[i];
      const rewriteData = await rewriteNote(note);
      results.push({
        ...note,
        rewrite_prompt: rewriteData.prompt
      });
    }
    
    // 3. 保存
    const outputDir = path.join(__dirname, '..', 'output');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    const outputFile = path.join(outputDir, `xiaohongshu_${timestamp}.json`);
    fs.writeFileSync(outputFile, JSON.stringify(results, null, 2));
    
    console.log(`✓ 保存到: ${outputFile}\n`);
    
  } catch (error) {
    console.error('执行失败:', error.message);
    process.exit(1);
  }
}

main();
