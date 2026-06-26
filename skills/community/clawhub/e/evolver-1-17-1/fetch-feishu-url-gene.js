// 获取飞书 URL 自动识别基因的完整详情
const https = require('https');

const assetId = 'sha256:8a893c405830091953ef1c43a59af15d007dbc844b3b8d2fde81e9515ce6ced4';

function getAssetDetail() {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'evomap.ai',
            port: 443,
            path: `/a2a/assets/${assetId}?detailed=true`,
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        };

        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                try {
                    const response = JSON.parse(body);
                    resolve(response);
                } catch (e) {
                    resolve({ raw: body, error: e.message });
                }
            });
        });

        req.on('error', reject);
        req.end();
    });
}

async function main() {
    console.log('🔍 获取飞书 URL 自动识别基因详情...\n');
    const asset = await getAssetDetail();
    
    console.log('完整响应:');
    console.log(JSON.stringify(asset, null, 2));
}

main().catch(console.error);
