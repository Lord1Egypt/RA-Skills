#!/usr/bin/env node

/**
 * 搜索户型
 * 用法: node searchPlan.js --token <token> --query <小区名> --areaId <城市id> [--start 0] [--num 20]
 */

const https = require('https');

const args = process.argv.slice(2);
let token = '';
let query = '';
let areaId = '';
let start = '0';
let num = '20';

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--token' && args[i + 1]) token = args[i + 1];
    else if (args[i] === '--query' && args[i + 1]) query = args[i + 1];
    else if (args[i] === '--areaId' && args[i + 1]) areaId = args[i + 1];
    else if (args[i] === '--start' && args[i + 1]) start = args[i + 1];
    else if (args[i] === '--num' && args[i + 1]) num = args[i + 1];
}

if (!token) {
    console.error('Error: --token is required');
    process.exit(1);
}

let path = `/oauth2/openapi/ai-design-skill/floorplan/standard/search?access_token=${encodeURIComponent(token)}&start=${start}&num=${num}`;
if (query) path += `&query=${encodeURIComponent(query)}`;
if (areaId) path += `&area_id=${areaId}`;

const options = {
    hostname: 'oauth.kujiale.com',
    port: 443,
    path: path,
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