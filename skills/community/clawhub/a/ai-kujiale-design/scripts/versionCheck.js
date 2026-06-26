#!/usr/bin/env node

/**
 * 版本校验
 * 用法: node versionCheck.js --token <token> --version <version>
 */

const https = require('https');

const args = process.argv.slice(2);
let token = '';
let version = '';

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--token' && args[i + 1]) token = args[i + 1];
    else if (args[i] === '--version' && args[i + 1]) version = args[i + 1];
}

if (!token || !version) {
    console.error('Error: --token and --version are required');
    process.exit(1);
}

const options = {
    hostname: 'oauth.kujiale.com',
    port: 443,
    path: `/oauth2/openapi/ai-design-skill/version/check?access_token=${encodeURIComponent(token)}&version=${version}`,
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