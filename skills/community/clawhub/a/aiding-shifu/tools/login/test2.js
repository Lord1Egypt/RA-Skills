const https = require('https');

function checkStatus(sceneId) {
    return new Promise((resolve, reject) => {
        const req = https.request({
            hostname: 'mes.dderp.cn',
            path: `/mob/wechat/checkLoginStatus?sceneId=${sceneId}`,
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        }, (res) => {
            const chunks = [];
            res.on('data', c => chunks.push(c));
            res.on('end', () => {
                const data = JSON.parse(Buffer.concat(chunks).toString());
                console.log('原始返回:', JSON.stringify(data, null, 2));
                resolve(data);
            });
        });
        req.on('error', reject);
        req.end();
    });
}

// 测试
checkStatus('login_4d05c86400c24f1b88020252b3f28e47').then(r => {
    console.log('\n返回数据:', r);
}).catch(console.error);
