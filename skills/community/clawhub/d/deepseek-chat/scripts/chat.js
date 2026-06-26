#!/usr/bin/env node

const https = require('https');

const API_KEY = process.env.DEEPSEEK_API_KEY;
const API_URL = 'https://api.deepseek.com';

if (!API_KEY) {
  console.error('错误：需要设置 DEEPSEEK_API_KEY 环境变量');
  process.exit(1);
}

function chat(prompt, model = 'deepseek-chat') {
  return new Promise((resolve, reject) => {
    const payload = {
      model: model,
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: prompt }
      ],
      stream: false
    };
    const data = JSON.stringify(payload);

    const options = {
      hostname: 'api.deepseek.com',
      port: 443,
      path: '/chat/completions',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    };

    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(responseData);
          if (result.choices && result.choices[0] && result.choices[0].message) {
            resolve({
              content: result.choices[0].message.content,
              usage: result.usage
            });
          } else {
            reject(new Error('Invalid response: ' + responseData));
          }
        } catch (e) {
          reject(new Error('Failed to parse: ' + responseData));
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('Timeout'));
    });
    req.write(data);
    req.end();
  });
}

async function main() {
  const [,, prompt, model] = process.argv;
  
  if (!prompt) {
    console.log('用法：node chat.js <问题> [模型]');
    console.log('模型：deepseek-chat (默认), deepseek-coder, deepseek-reasoner');
    process.exit(1);
  }

  const useModel = model || 'deepseek-chat';
  console.log(`使用模型：${useModel}`);
  console.log('DeepSeek 思考中...\n');
  
  try {
    const result = await chat(prompt, useModel);
    console.log('DeepSeek:', result.content);
    console.log('\n📊 Token 使用:', result.usage);
  } catch (error) {
    console.error('错误:', error.message);
    process.exit(1);
  }
}

main();
