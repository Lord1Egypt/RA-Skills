// 获取 Python 正则 CJK 修复基因的完整详情
const https = require('https');

const assetId = 'sha256:82ad9e9a773f03cfeda5ce4ca8fc50c40b74652dc8fd1eb25b4d0eb8126c7544';

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
    console.log('🔍 获取 Python 正则 CJK 修复基因详情...\n');
    const asset = await getAssetDetail();
    
    console.log('完整响应:');
    console.log(JSON.stringify(asset, null, 2));
}

main().catch(console.error);
