#!/usr/bin/env node

/**
 * 获取户型图信息
 * 用法: node getFloorplanInfo.js --planId <planId>
 */

const https = require('https');

const args = process.argv.slice(2);
let planId = '';

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--planId' && args[i + 1]) planId = args[i + 1];
}

if (!planId) {
    console.error('Error: --planId is required');
    process.exit(1);
}

const options = {
    hostname: 'www.kujiale.com',
    port: 443,
    path: `/api/designinfo/floorplans?planid=${planId}`,
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