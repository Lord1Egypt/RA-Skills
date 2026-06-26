#!/usr/bin/env node

const https = require('https');

const DOUBAO_API = 'https://doubao-free-api.vercel.app';
const SESSIONID = process.env.DOUBAO_SESSIONID;

if (!SESSIONID) {
  console.error('错误：需要设置 DOUBAO_SESSIONID 环境变量');
  process.exit(1);
}

function chat(prompt) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: 'doubao',
      messages: [
        { role: 'system', content: '你是一个有帮助的 AI 助手。' },
        { role: 'user', content: prompt }
      ],
      stream: false
    });

    const options = {
      hostname: 'doubao-free-api.vercel.app',
      port: 443,
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${SESSIONID}`,
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
            resolve(result.choices[0].message.content);
          } else {
            reject(new Error('Invalid response: ' + responseData));
          }
        } catch (e) {
          reject(new Error('Failed to parse response: ' + responseData));
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function main() {
  const prompt = process.argv[2];
  if (!prompt) {
    console.log('用法：node chat.js <问题>');
    process.exit(1);
  }

  try {
    console.log('豆包思考中...');
    const response = await chat(prompt);
    console.log('\n豆包：' + response);
  } catch (error) {
    console.error('错误:', error.message);
    process.exit(1);
  }
}

main();
