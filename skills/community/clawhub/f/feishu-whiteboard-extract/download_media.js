/**
 * download_media.js — 下载飞书白板节点图片
 * 用法: node download_media.js <file_token> [save_path]
 *
 * 使用 drive/v1/medias/{file_token}/download（而非 files endpoint）
 * tenant_access_token 即可，不需要用户级 token。
 */
const https = require('https');
const fs = require('fs');
const path = require('path');
const os = require('os');

const fileToken = process.argv[2];
const savePath = process.argv[3];

if (!fileToken) {
    console.error(JSON.stringify({ error: 'file_token is required' }));
    process.exit(1);
}

const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const { appId, appSecret } = config.channels.feishu;

async function getTenantToken() {
    return new Promise((resolve, reject) => {
        const body = JSON.stringify({ app_id: appId, app_secret: appSecret });
        const req = https.request({
            hostname: 'open.feishu.cn',
            path: '/open-apis/auth/v3/tenant_access_token/internal',
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
        }, res => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => {
                const d = JSON.parse(data);
                if (d.tenant_access_token) resolve(d.tenant_access_token);
                else reject(new Error('Failed to get tenant token: ' + data));
            });
        });
        req.on('error', reject);
        req.write(body);
        req.end();
    });
}

async function downloadMedia(token, fileToken, finalPath) {
    return new Promise((resolve, reject) => {
        const req = https.request({
            hostname: 'open.feishu.cn',
            // 关键: medias endpoint，不是 files endpoint
            path: `/open-apis/drive/v1/medias/${fileToken}/download`,
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        }, res => {
            if (res.statusCode !== 200) {
                let errData = '';
                res.on('data', c => errData += c);
                res.on('end', () => reject(new Error(`HTTP ${res.statusCode}: ${errData}`)));
                return;
            }
            // Detect extension from content-type
            const ct = res.headers['content-type'] || '';
            let ext = '.png';
            if (ct.includes('jpeg') || ct.includes('jpg')) ext = '.jpg';
            else if (ct.includes('gif')) ext = '.gif';
            else if (ct.includes('webp')) ext = '.webp';

            const outPath = finalPath || path.join(
                os.homedir(), '.openclaw', 'workspace', 'input', 'feishu_downloads',
                `${fileToken}${ext}`
            );
            fs.mkdirSync(path.dirname(outPath), { recursive: true });
            const ws = fs.createWriteStream(outPath);
            res.pipe(ws);
            ws.on('finish', () => resolve(outPath));
            ws.on('error', reject);
        });
        req.on('error', reject);
        req.end();
    });
}

async function main() {
    try {
        const token = await getTenantToken();
        const outputDir = path.join(os.homedir(), '.openclaw', 'workspace', 'input', 'feishu_downloads');
        fs.mkdirSync(outputDir, { recursive: true });
        const finalPath = savePath || path.join(outputDir, `${fileToken}.png`);
        const savedPath = await downloadMedia(token, fileToken, finalPath);
        console.log(JSON.stringify({ success: true, path: savedPath }));
    } catch(e) {
        console.error(JSON.stringify({ error: e.message }));
        process.exit(1);
    }
}
main();
