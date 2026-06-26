#!/usr/bin/env node

/**
 * brave-loggedin-tag-browsing - 執行入口
 * 
 * 使用方式：
 *   echo '{"username":"realDonaldTrump","maxTweets":5}' | node cli.js
 * 
 * 或利用 OpenClaw sessions_spawn 執行
 */

const { braveBrowsePlatform } = require('./index');

// 從標準輸入讀取參數
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', async () => {
  try {
    const options = input ? JSON.parse(input) : {};
    const username = options.username || process.argv[2];
    
    if (!username) {
      console.error(JSON.stringify({
        error: "缺少必要參數：username",
        usage: '{"username":"account","maxTweets":5,"includeStats":true}'
      }));
      process.exit(1);
    }
    
    const result = await braveBrowsePlatform(username, options);
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  } catch (err) {
    console.error(JSON.stringify({
      error: err.message,
      stack: process.env.DEBUG ? err.stack : undefined
    }));
    process.exit(1);
  }
});
