#!/usr/bin/env node

/**
 * brave-loggedin-tag-browsing - 實際执行邏輯
 * 
 * 此模擬版本展示完整的工作流程
 * 實際部署時需與 OpenClaw browser 工具深度集成
 */

const { braveBrowseX } = require('./index');

// 如果直接執行此文件（CLI 模式）
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.error(JSON.stringify({
      error: "缺少必要參數：username",
      example: 'node execute.js realDonaldTrump 5 true',
      json_format: '{"username":"realDonaldTrump","maxTweets":5,"includeStats":true}'
    }, null, 2));
    process.exit(1);
  }
  
  const username = args[0];
  const maxTweets = parseInt(args[1]) || 5;
  const includeStats = args[2] !== 'false';
  
  braveBrowseX(username, { maxTweets, includeStats })
    .then(result => {
      console.log(JSON.stringify(result, null, 2));
    })
    .catch(err => {
      console.error(JSON.stringify({
        error: err.message,
        details: process.env.DEBUG ? err.stack : undefined
      }));
      process.exit(1);
    });
}

module.exports = { braveBrowseX };
