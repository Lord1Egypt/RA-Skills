#!/usr/bin/env node

/**
 * 中文社交媒体内容生成器
 * 使用 DeepSeek API 生成适合各平台的内容
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG_PATH = path.join(process.env.HOME, '.openclaw', '.env');
const SKILL_DIR = __dirname;

// 读取 API Key
function getApiKey() {
  try {
    const envContent = fs.readFileSync(CONFIG_PATH, 'utf-8');
    const match = envContent.match(/DEEPSEEK_API_KEY=(.+)/);
    return match ? match[1].trim() : null;
  } catch {
    return null;
  }
}

// 调用 DeepSeek API
async function callDeepSeek(prompt) {
  const apiKey = getApiKey();
  if (!apiKey) {
    console.error('❌ 未配置 DEEPSEEK_API_KEY');
    console.log('请运行: node setup-ai.js deepseek');
    return null;
  }

  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: 'deepseek-chat',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.7
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

// 平台特性
const PLATFORMS = {
  juejin: {
    name: '掘金',
    maxTitle: 50,
    maxContent: 3000,
    style: '技术深度，代码示例'
  },
  zhihu: {
    name: '知乎',
    maxTitle: 40,
    maxContent: 5000,
    style: '长文，专业感'
  },
  gongzhonghao: {
    name: '公众号',
    maxTitle: 30,
    maxContent: 3000,
    style: '标题党，开头 50 字关键'
  },
  xiaohongshu: {
    name: '小红书',
    maxTitle: 20,
    maxContent: 1000,
    style: 'emoji，分段，图片'
  }
};

// 生成内容
async function generateContent(topic, platform = 'juejin') {
  const p = PLATFORMS[platform];
  if (!p) {
    console.error(`❌ 不支持的平台: ${platform}`);
    console.log(`支持的平台: ${Object.keys(PLATFORMS).join(', ')}`);
    return;
  }

  console.log(`\n📝 正在生成 ${p.name} 内容...`);
  console.log(`主题: ${topic}\n`);

  const prompt = `你是一位专业的${p.name}内容创作者。请根据以下主题生成一篇适合${p.name}的文章。

主题: ${topic}

平台特点:
- 最大标题长度: ${p.maxTitle}字
- 风格: ${p.style}

请输出:
1. 标题（吸引点击，${p.maxTitle}字以内）
2. 分类
3. 标签（3-5个）
4. 摘要（50字以内）
5. 正文大纲（3-5个要点）

格式要求：简洁清晰，可直接使用。`;

  try {
    const content = await callDeepSeek(prompt);
    if (content) {
      console.log(content);
      console.log('\n✅ 生成完成');
    }
  } catch (error) {
    console.error('❌ 生成失败:', error.message);
  }
}

// 解析命令行参数
const args = process.argv.slice(2);
const topicIndex = args.indexOf('--topic');
const platformIndex = args.indexOf('--platform');

if (topicIndex === -1) {
  console.log(`
📖 中文社交媒体内容生成器

用法:
  node generate.js --topic "主题" --platform 平台

平台:
  juejin      掘金
  zhihu       知乎
  gongzhonghao 公众号
  xiaohongshu 小红书

示例:
  node generate.js --topic "DeepSeek V3 实战" --platform juejin
`);
  process.exit(0);
}

const topic = args[topicIndex + 1];
const platform = platformIndex !== -1 ? args[platformIndex + 1] : 'juejin';

generateContent(topic, platform);
