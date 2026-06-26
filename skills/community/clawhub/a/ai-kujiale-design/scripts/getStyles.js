#!/usr/bin/env node

/**
 * 查询硬装风格库
 * 用法: node getStyles.js --token <token> --tagItemIds <tagItemId1,tagItemId2,...>
 */

const https = require('https');

const args = process.argv.slice(2);
let token = '';
let tagItemIds = '';

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--token' && args[i + 1]) token = args[i + 1];
    else if (args[i] === '--tagItemIds' && args[i + 1]) tagItemIds = args[i + 1];
}

if (!token) {
    console.error('Error: --token is required');
    process.exit(1);
}

const body = tagItemIds ? JSON.stringify({ tagItemIds: tagItemIds.split(',') }) : '{}';

const options = {
    hostname: 'oauth.kujiale.com',
    port: 443,
    path: `/oauth2/openapi/ai-design-skill/style/list?access_token=${encodeURIComponent(token)}`,
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
    }
};

const req = https.request(options, (res) => {
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
});

req.on('error', err => console.error('Request error:', err.message));
req.write(body);
req.end();