const https = require('https');
const { exec } = require('child_process');
const os = require('os');
const path = require('path');
const fs = require('fs');

console.log('正在生成登录二维码...\n');

const req = https.request({
    hostname: 'mes.dderp.cn',
    path: '/mob/wechat/createLoginQrCode',
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
}, (res) => {
    const chunks = [];
    res.on('data', c => chunks.push(c));
    res.on('end', () => {
        const data = JSON.parse(Buffer.concat(chunks).toString());
        console.log('SceneId:', data.data.sceneId);
        console.log('请用微信扫码...\n');
        
        const qrUrl = 'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=' + encodeURIComponent(data.data.url);
        const qrPath = path.join(os.tmpdir(), 'aiding-login.png');
        
        https.get(qrUrl, (r) => {
            const f = fs.createWriteStream(qrPath);
            r.pipe(f);
            f.on('finish', () => {
                console.log('二维码已打开!');
                exec('start "" "' + qrPath + '"');
                
                // 开始轮询
                console.log('\n⏳ 等待扫码（按 Ctrl+C 退出）...\n');
                
                const poll = setInterval(() => {
                    https.get({
                        hostname: 'mes.dderp.cn',
                        path: '/mob/wechat/checkLoginStatus?sceneId=' + data.data.sceneId,
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }
                    }, (res2) => {
                        const chunks2 = [];
                        res2.on('data', c => chunks2.push(c));
                        res2.on('end', () => {
                            const result = JSON.parse(Buffer.concat(chunks2).toString());
                            const status = result.status;
                            process.stdout.write('\r[' + new Date().toLocaleTimeString() + '] ' + status + '    ');
                            
                            if (status === 'confirmed' || status === '登录成功') {
                                console.log('\n\n🎉 登录成功！');
                                console.log('Token:', result.token || result.wxUnionid || result.data?.token);
                                clearInterval(poll);
                                process.exit(0);
                            } else if (status === 'expired' || status === '已过期') {
                                console.log('\n\n❌ 二维码已过期，请重新运行');
                                clearInterval(poll);
                                process.exit(1);
                            }
                        });
                    });
                }, 2000);
            });
        });
    });
});

req.on('error', console.error);
req.end();
