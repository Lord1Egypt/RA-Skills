// 上传向量数据库封面图到微信素材库
// 使用方法：node scripts/upload-cover.js

const https = require('https');
const fs = require('fs');
const path = require('path');

async function getAccessToken() {
  const APPID = 'wxebff9eadface1489';
  const SECRET = '44c10204ceb1bfb3f7ac096754976454';
  
  return new Promise((resolve, reject) => {
    const req = https.get(`https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${APPID}&secret=${SECRET}`, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          resolve(result.access_token);
        } catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
  });
}

async function uploadImage(accessToken, imagePath) {
  return new Promise((resolve, reject) => {
    const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
    const fileContent = fs.readFileSync(imagePath);
    
    const body = Buffer.concat([
      Buffer.from(`--${boundary}\r\n`),
      Buffer.from(`Content-Disposition: form-data; name="media"; filename="cover.png"\r\n`),
      Buffer.from(`Content-Type: image/png\r\n\r\n`),
      fileContent,
      Buffer.from(`\r\n--${boundary}--\r\n`)
    ]);
    
    const req = https.request({
      hostname: 'api.weixin.qq.com',
      path: `/cgi-bin/material/add_material?access_token=${accessToken}&type=image`,
      method: 'POST',
      headers: {
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length
      }
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.errcode && result.errcode !== 0) {
            reject(new Error(`微信 API 错误 ${result.errcode}: ${result.errmsg}`));
          } else {
            resolve(result.media_id);
          }
        } catch (e) { reject(e); }
      });
    });
    
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  console.log('🖼️  上传向量数据库封面图...\n');
  
  // 检查封面文件
  const coverPath = path.join(__dirname, '..', 'covers', 'vector-db-cover.png');
  
  if (!fs.existsSync(coverPath)) {
    console.log('❌ 封面文件不存在:', coverPath);
    console.log('\n💡 请先创建封面图文件，或使用现有封面。');
    return;
  }
  
  console.log('📄 封面文件:', coverPath);
  
  // 获取 Token
  console.log('🔑 获取 Access Token...');
  const token = await getAccessToken();
  console.log('   Token:', token.substring(0, 20) + '...');
  
  // 上传图片
  console.log('📤 上传封面图...');
  const mediaId = await uploadImage(token, coverPath);
  
  console.log('\n✅ 上传成功！');
  console.log('MediaID:', mediaId);
  
  // 更新 .env 文件
  const envPath = path.join(__dirname, '..', '.env');
  const envContent = fs.readFileSync(envPath, 'utf8');
  const newEnvContent = envContent.replace(
    /WECHAT_THUMB_MEDIA_ID=.*/,
    `WECHAT_THUMB_MEDIA_ID=${mediaId}`
  );
  fs.writeFileSync(envPath, newEnvContent, 'utf8');
  
  console.log('\n📝 已更新 .env 文件');
  console.log('   WECHAT_THUMB_MEDIA_ID=' + mediaId);
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
