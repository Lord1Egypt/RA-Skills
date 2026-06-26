// 上传本地图片到微信素材库
const https = require('https');
const fs = require('fs');
const path = require('path');

// 加载环境变量
function loadEnv() {
  const envPaths = [
    path.join(__dirname, '..', '.env'),
    path.join(__dirname, '..', '..', 'wechat-publisher', '.env')
  ];
  
  for (const envPath of envPaths) {
    if (fs.existsSync(envPath)) {
      const envContent = fs.readFileSync(envPath, 'utf8');
      envContent.split('\n').forEach(line => {
        const parts = line.split('=');
        if (parts[0] && parts[1]) process.env[parts[0].trim()] = parts[1].trim();
      });
    }
  }
}
loadEnv();

const CONFIG = {
  APPID: process.env.WECHAT_APPID,
  SECRET: process.env.WECHAT_SECRET
};

function request(options, body, isFile = false) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (!data) return reject(new Error('Empty response'));
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(e.message)); }
      });
    });
    req.on('error', reject);
    if (body) {
      if (isFile) {
        const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
        req.setHeader('Content-Type', 'multipart/form-data; boundary=' + boundary);
        const parts = [];
        parts.push(Buffer.from('--' + boundary + '\r\n'));
        parts.push(Buffer.from('Content-Disposition: form-data; name="media"; filename="cover.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'));
        parts.push(body);
        parts.push(Buffer.from('\r\n--' + boundary + '--\r\n'));
        const bodyData = Buffer.concat(parts);
        req.setHeader('Content-Length', bodyData.length);
        req.write(bodyData);
      } else {
        const json = JSON.stringify(body);
        req.setHeader('Content-Type', 'application/json');
        req.setHeader('Content-Length', Buffer.byteLength(json));
        req.write(json);
      }
    }
    req.end();
  });
}

async function getAccessToken() {
  const p = '/cgi-bin/token?grant_type=client_credential&appid=' + CONFIG.APPID + '&secret=' + CONFIG.SECRET;
  const res = await request({ hostname: 'api.weixin.qq.com', path: p, method: 'GET' });
  if (!res.access_token) throw new Error('获取 Token 失败：' + JSON.stringify(res));
  return res.access_token;
}

async function uploadImage(imagePath, type = 'thumb') {
  console.log('📤 上传图片:', path.basename(imagePath));
  
  if (!fs.existsSync(imagePath)) {
    throw new Error('图片文件不存在：' + imagePath);
  }
  
  const imageBuffer = fs.readFileSync(imagePath);
  console.log('📊 图片大小:', (imageBuffer.length / 1024 / 1024).toFixed(2), 'MB');
  
  const token = await getAccessToken();
  
  // 上传到微信服务器
  const apiPath = type === 'thumb' 
    ? '/cgi-bin/material/add_material?access_token=' + token + '&type=image'
    : '/cgi-bin/material/add_material?access_token=' + token + '&type=thumb';
  
  console.log('📤 上传中...');
  const res = await request({
    hostname: 'api.weixin.qq.com',
    path: apiPath,
    method: 'POST'
  }, imageBuffer, true);
  
  if (res.errcode) {
    throw new Error('上传失败：' + res.errmsg);
  }
  
  console.log('✅ 上传成功！');
  console.log('📌 media_id:', res.media_id);
  if (res.url) {
    console.log('📌 url:', res.url);
  }
  
  return res;
}

async function listImages() {
  console.log('📋 查找本地图片...\n');
  
  const targetDir = process.argv[2] || 'D:\\DocsAutoWrter\\SGLang';
  
  if (!fs.existsSync(targetDir)) {
    console.log('❌ 目录不存在:', targetDir);
    return [];
  }
  
  const images = [];
  
  function findImages(dir) {
    const items = fs.readdirSync(dir);
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        findImages(fullPath);
      } else if (/\.(jpg|jpeg|png|gif)$/i.test(item)) {
        images.push({
          path: fullPath,
          name: item,
          size: stat.size
        });
      }
    }
  }
  
  findImages(targetDir);
  
  console.log('✅ 找到', images.length, '张图片:\n');
  images.forEach((img, i) => {
    console.log(`  ${i + 1}. ${img.name} - ${(img.size / 1024).toFixed(2)} KB`);
  });
  
  return images;
}

async function main() {
  console.log('🖼️  微信公众号图片上传工具\n');
  console.log('=' .repeat(60), '\n');
  
  const images = await listImages();
  
  if (images.length === 0) {
    console.log('\n❌ 没有找到图片文件');
    process.exit(1);
  }
  
  console.log('\n' + '=' .repeat(60), '\n');
  console.log('💡 请选择要上传的图片（输入序号，多个用逗号分隔）:');
  console.log('   或输入 "all" 上传所有图片\n');
  
  // 简单处理：上传第一张图片作为封面
  const targetImage = images[0];
  
  console.log('📌 默认使用第一张图片作为封面:\n');
  console.log('   文件:', targetImage.name);
  console.log('   路径:', targetImage.path);
  console.log('   大小:', (targetImage.size / 1024).toFixed(2), 'KB\n');
  
  try {
    const result = await uploadImage(targetImage.path, 'thumb');
    
    // 更新 .env 文件
    const envPath = path.join(__dirname, '..', '..', 'wechat-publisher', '.env');
    if (fs.existsSync(envPath)) {
      let envContent = fs.readFileSync(envPath, 'utf8');
      envContent = envContent.replace(/WECHAT_THUMB_MEDIA_ID=.*/, 'WECHAT_THUMB_MEDIA_ID=' + result.media_id);
      fs.writeFileSync(envPath, envContent, 'utf8');
      console.log('\n✅ .env 文件已更新');
    }
    
    console.log('\n✅ 封面图上传完成！下次发布将使用新封面。');
    console.log('\n💡 现在可以运行发布命令:');
    console.log('   node examples/publish-any.js "D:\\DocsAutoWrter\\SGLang"');
    
  } catch (err) {
    console.error('\n❌ 错误:', err.message);
    process.exit(1);
  }
}

main();
