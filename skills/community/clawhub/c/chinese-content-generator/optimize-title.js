#!/usr/bin/env node

/**
 * 标题优化器
 * 使用 AI 优化文章标题
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG_PATH = path.join(process.env.HOME, '.openclaw', '.env');

function getApiKey() {
  try {
    const envContent = fs.readFileSync(CONFIG_PATH, 'utf-8');
    const match = envContent.match(/DEEPSEEK_API_KEY=(.+)/);
    return match ? match[1].trim() : null;
  } catch {
    return null;
  }
}

async function callDeepSeek(prompt) {
  const apiKey = getApiKey();
  if (!apiKey) {
    return null;
  }

  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: 'deepseek-chat',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.8
    });

    const options = {
      hostname: 'api.deepseek.com',
      port: 443,
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(body);
          resolve(json.choices[0].message.content);
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function optimizeTitle(originalTitle) {
  console.log(`\n📊 原标题: ${originalTitle}\n`);

  const prompt = `你是一位专业的标题优化专家。请优化以下文章标题，使其更具吸引力。

原标题: ${originalTitle}

请提供:
1. 分析原标题的问题
2. 3-5 个优化后的标题选项
3. 每个选项的优化理由
4. 推荐最佳选项

要求:
- 标题要吸引点击
- 不要过度夸张
- 适合中文社交媒体（掘金/知乎/公众号）

格式简洁清晰。`;

  try {
    const content = await callDeepSeek(prompt);
    if (content) {
      console.log(content);
      console.log('\n✅ 优化完成\n');
    } else {
      console.log('❌ 未配置 API Key，使用默认建议\n');
      console.log('优化建议:');
      console.log(`1. ${originalTitle}：完整指南（权威感）`);
      console.log(`2. 我用 ${originalTitle}，真香（故事性）`);
      console.log(`3. ${originalTitle} 实战：从入门到精通（实用性）`);
    }
  } catch (error) {
    console.error('❌ 优化失败:', error.message);
  }
}

// 解析参数
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log(`
📖 标题优化器

用法:
  node optimize-title.js "原标题"

示例:
  node optimize-title.js "DeepSeek V3 使用教程"
`);
  process.exit(0);
}

optimizeTitle(args[0]);
