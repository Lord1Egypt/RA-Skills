#!/usr/bin/env node

/**
 * 轮询临摹图导入任务结果
 * 用法: node getBitmapTaskResult.js --token <token> --taskId <taskId>
 */

const https = require('https');

const args = process.argv.slice(2);
let token = '';
let taskId = '';

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--token' && args[i + 1]) token = args[i + 1];
    else if (args[i] === '--taskId' && args[i + 1]) taskId = args[i + 1];
}

if (!token || !taskId) {
    console.error('Error: --token and --taskId are required');
    process.exit(1);
}

const options = {
    hostname: 'oauth.kujiale.com',
    port: 443,
    path: `/oauth2/openapi/ai-design-skill/bitmap/floorplan-import/status?access_token=${encodeURIComponent(token)}&task_id=${taskId}`,
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