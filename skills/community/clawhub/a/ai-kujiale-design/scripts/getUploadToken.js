#!/usr/bin/env node

/**
 * 获取OUS上传凭证
 * 用法: node getUploadToken.js --token <token>
 */

const https = require('https');

const args = process.argv.slice(2);
let token = '';

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--token' && args[i + 1]) token = args[i + 1];
}

if (!token) {
    console.error('Error: --token is required');
    process.exit(1);
}

const options = {
    hostname: 'oauth.kujiale.com',
    port: 443,
    path: `/oauth2/openapi/ai-design-skill/upload/token?access_token=${encodeURIComponent(token)}`,
    method: 'GET'
};

https.get(options, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        try {
            const json = JSON.parse(data);
            console.log(JSON.stringify(json, null, 2));
        } catch (e) {
            console.error('Parse error:', e.message);
            console.log(data);
        }
    });
}).on('error', err => console.error('Request error:', err.message));