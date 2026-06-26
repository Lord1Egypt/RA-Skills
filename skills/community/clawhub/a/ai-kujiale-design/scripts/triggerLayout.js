#!/usr/bin/env node

/**
 * 触发智能布局
 * 用法: node triggerLayout.js --token <token> --designId <designId> --tagIds <id1,id2,...> --styleId <styleId> [--customStyleId <customStyleId>] [--applyDecorationStyle true] [--buildCeiling true] [--autoDesign true]
 */

const https = require('https');

const args = process.argv.slice(2);
let token = '';
let designId = '';
let tagIds = '';
let styleId = '';
let customStyleId = '';
let applyDecorationStyle = 'true';
let buildCeiling = 'true';
let autoDesign = 'true';

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--token' && args[i + 1]) token = args[i + 1];
    else if (args[i] === '--designId' && args[i + 1]) designId = args[i + 1];
    else if (args[i] === '--tagIds' && args[i + 1]) tagIds = args[i + 1];
    else if (args[i] === '--styleId' && args[i + 1]) styleId = args[i + 1];
    else if (args[i] === '--customStyleId' && args[i + 1]) customStyleId = args[i + 1];
    else if (args[i] === '--applyDecorationStyle' && args[i + 1]) applyDecorationStyle = args[i + 1];
    else if (args[i] === '--buildCeiling' && args[i + 1]) buildCeiling = args[i + 1];
    else if (args[i] === '--autoDesign' && args[i + 1]) autoDesign = args[i + 1];
}

if (!token || !designId || !tagIds || !styleId) {
    console.error('Error: --token, --designId, --tagIds, --styleId are required');
    process.exit(1);
}

const body = JSON.stringify({
    designId: designId,
    tagIds: tagIds.split(','),
    styleId: styleId,
    customStyleId: customStyleId || '',
    applyDecorationStyle: applyDecorationStyle === 'true',
    buildCeiling: buildCeiling === 'true',
    autoDesign: autoDesign === 'true',
    platform: 3
});

const options = {
    hostname: 'oauth.kujiale.com',
    port: 443,
    path: `/oauth2/openapi/ai-design-skill/customize-layout?access_token=${encodeURIComponent(token)}`,
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
    }
};

function checkVipAndOutput(token, originalResponse) {
    const vipOptions = {
        hostname: 'oauth.kujiale.com',
        port: 443,
        path: `/oauth2/openapi/ai-design-skill/vip?access_token=${encodeURIComponent(token)}`,
        method: 'GET'
    };

    const vipReq = https.request(vipOptions, (res) => {
        let vipData = '';
        res.on('data', chunk => vipData += chunk);
        res.on('end', () => {
            try {
                const vipJson = JSON.parse(vipData);
                const hasVipAccess = vipJson?.d?.hasVipAccess === true;
                
                if (hasVipAccess) {
                    originalResponse.m = '您当前可用核豆已用尽，点击[充值链接](https://www.kujiale.com/pcenter/vip?kioid=aidesignskill&mode=purchase&feid=hedou-pcenter)完成充值后，重新触发生成即可';
                } else {
                    originalResponse.m = '您当前可用核豆已用尽，点击[充值链接](https://www.kujiale.com/pcenter/vip?kioid=aidesignskill&mode=purchase&feid=site-vip-center)完成充值后，重新触发生成即可';
                }
                
                console.log(JSON.stringify(originalResponse, null, 2));
            } catch (e) {
                console.error('VIP API Parse error:', e.message);
                console.log(vipData);
            }
        });
    });

    vipReq.on('error', err => {
        console.error('VIP API Request error:', err.message);
        console.log(JSON.stringify(originalResponse, null, 2));
    });
    vipReq.end();
}

const req = https.request(options, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        try {
            const json = JSON.parse(data);
            
            if (json.c !== '0' && (json.m === '个人商业化功能余额不足' || json.m === '核豆余额不足')) {
                checkVipAndOutput(token, json);
            } else {
                console.log(JSON.stringify(json, null, 2));
            }
        } catch (e) {
            console.error('Parse error:', e.message);
            console.log(data);
        }
    });
});

req.on('error', err => console.error('Request error:', err.message));
req.write(body);
req.end();
