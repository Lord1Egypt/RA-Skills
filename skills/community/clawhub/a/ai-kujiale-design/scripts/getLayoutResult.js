#!/usr/bin/env node

/**
 * 查询智能布局结果
 * 用法: node getLayoutResult.js --token <token> --designId <designId>
 */

const https = require('https');

const args = process.argv.slice(2);
let token = '';
let designId = '';

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--token' && args[i + 1]) token = args[i + 1];
    else if (args[i] === '--designId' && args[i + 1]) designId = args[i + 1];
}

if (!token || !designId) {
    console.error('Error: --token and --designId are required');
    process.exit(1);
}

const options = {
    hostname: 'oauth.kujiale.com',
    port: 443,
    path: `/oauth2/openapi/ai-design-skill/design/layout-res?access_token=${encodeURIComponent(token)}&designId=${designId}`,
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