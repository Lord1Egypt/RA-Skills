#!/usr/bin/env node

/**
 * 通过户型ID创建装修方案
 * 用法: node createDesign.js --token <token> --planId <planId> [--name <方案名>]
 */

const https = require('https');

const args = process.argv.slice(2);
let token = '';
let planId = '';
let name = '';

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--token' && args[i + 1]) token = args[i + 1];
    else if (args[i] === '--planId' && args[i + 1]) planId = args[i + 1];
    else if (args[i] === '--name' && args[i + 1]) name = args[i + 1];
}

if (!token || !planId) {
    console.error('Error: --token and --planId are required');
    process.exit(1);
}

let path = `/oauth2/openapi/ai-design-skill/design/creation?access_token=${encodeURIComponent(token)}&plan_id=${planId}`;
if (name) path += `&name=${encodeURIComponent(name)}`;

const options = {
    hostname: 'oauth.kujiale.com',
    port: 443,
    path: path,
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' }
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
req.end();