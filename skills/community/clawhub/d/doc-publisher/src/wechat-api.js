/**
 * 微信公众号 API
 * 独立版本（不依赖 wechat-publisher）
 */

const https = require('https');
const path = require('path');
const fs = require('fs');

/**
 * 加载 .env 配置
 */
function loadEnv() {
  const envPath = path.join(__dirname, '..', '.env');
  if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    envContent.split('\n').forEach(line => {
      const parts = line.split('=');
      if (parts[0] && parts[1]) process.env[parts[0].trim()] = parts[1].trim();
    });
  }
}
loadEnv();

/**
 * 微信配置
 */
const CONFIG = {
  APPID: process.env.WECHAT_APPID,
  SECRET: process.env.WECHAT_SECRET,
  THUMB_MEDIA_ID: process.env.WECHAT_THUMB_MEDIA_ID || ''
};

/**
 * 设置封面图片 ID
 */
function setThumbMediaId(mediaId) {
  CONFIG.THUMB_MEDIA_ID = mediaId;
}

/**
 * HTTPS 请求
 */
function request(options, body) {
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
      const json = JSON.stringify(body);
      req.setHeader('Content-Type', 'application/json');
      req.setHeader('Content-Length', Buffer.byteLength(json));
      req.write(json);
    }
    req.end();
  });
}

/**
 * Token 缓存
 */
let tokenCache = { token: null, expires: 0 };

/**
 * 获取 Access Token
 */
async function getAccessToken() {
  const now = Date.now();
  if (tokenCache.token && now < tokenCache.expires) return tokenCache.token;
  
  const p = '/cgi-bin/token?grant_type=client_credential&appid=' + CONFIG.APPID + '&secret=' + CONFIG.SECRET;
  const res = await request({ hostname: 'api.weixin.qq.com', path: p, method: 'GET' });
  
  tokenCache = { token: res.access_token, expires: now + (res.expires_in - 300) * 1000 };
  return tokenCache.token;
}

/**
 * 创建草稿
 */
async function addDraft(article) {
  const token = await getAccessToken();
  
  const res = await request({
    hostname: 'api.weixin.qq.com',
    path: '/cgi-bin/draft/add?access_token=' + token,
    method: 'POST'
  }, {
    articles: [{
      title: article.title,
      author: article.author || 'Editor',
      digest: article.digest,
      content: article.content,
      thumb_media_id: CONFIG.THUMB_MEDIA_ID,
      show_cover_pic: 1
    }]
  });
  
  // 检查微信 API 错误
  if (res.errcode && res.errcode !== 0) {
    throw new Error(`微信 API 错误 ${res.errcode}: ${res.errmsg}`);
  }
  
  if (!res.media_id) {
    throw new Error('发布失败：未返回 media_id，响应：' + JSON.stringify(res));
  }
  
  return { media_id: res.media_id, created_at: Date.now(), title: article.title };
}

/**
 * 获取草稿列表
 */
async function getAllDrafts() {
  const token = await getAccessToken();
  
  const res = await request({
    hostname: 'api.weixin.qq.com',
    path: '/cgi-bin/draft/batchget?access_token=' + token,
    method: 'POST'
  }, {
    offset: 0,
    count: 50,
    no_content: 1
  });
  
  if (res.errcode && res.errcode !== 0) {
    throw new Error(`微信 API 错误 ${res.errcode}: ${res.errmsg}`);
  }
  
  return res.item || [];
}

/**
 * 删除草稿
 */
async function deleteDraft(mediaId) {
  const token = await getAccessToken();
  
  const res = await request({
    hostname: 'api.weixin.qq.com',
    path: '/cgi-bin/draft/delete?access_token=' + token,
    method: 'POST'
  }, { media_id: mediaId });
  
  if (res.errcode && res.errcode !== 0) {
    throw new Error(`微信 API 错误 ${res.errcode}: ${res.errmsg}`);
  }
  
  return true;
}

/**
 * 上传临时图片（用于封面等）
 */
async function uploadTempImage(imagePath) {
  const token = await getAccessToken();
  const fileContent = fs.readFileSync(imagePath);
  
  return new Promise((resolve, reject) => {
    const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
    const body = Buffer.concat([
      Buffer.from(`------WebKitFormBoundary\r\nContent-Disposition: form-data; name="media"; filename="cover.png"\r\nContent-Type: image/png\r\n\r\n`),
      fileContent,
      Buffer.from(`\r\n------WebKitFormBoundary\r\nContent-Disposition: form-data; name="description"\r\n\r\nLMStudio 封面\r\n------WebKitFormBoundary--\r\n`)
    ]);
    
    const req = https.request({
      hostname: 'api.weixin.qq.com',
      path: '/cgi-bin/material/add_material?access_token=' + token + '&type=image',
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data; boundary=' + boundary,
        'Content-Length': body.length
      }
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          console.log('上传结果:', result);
          if (result.errcode && result.errcode !== 0) {
            reject(new Error('上传失败：' + result.errmsg));
          } else {
            resolve(result.media_id);
          }
        } catch (e) {
          reject(new Error('解析失败：' + e.message));
        }
      });
    });
    
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

/**
 * 上传图片到微信素材库
 */
async function uploadImage(imagePath) {
  const token = await getAccessToken();
  
  return new Promise((resolve, reject) => {
    const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
    const formData = fs.readFileSync(imagePath);
    
    const body = [];
    body.push(Buffer.from('--' + boundary + '\r\n'));
    body.push(Buffer.from('Content-Disposition: form-data; name="media"; filename="' + path.basename(imagePath) + '"\r\n'));
    body.push(Buffer.from('Content-Type: image/jpeg\r\n'));
    body.push(Buffer.from('\r\n'));
    body.push(formData);
    body.push(Buffer.from('\r\n--' + boundary + '--\r\n'));
    
    const req = https.request({
      hostname: 'api.weixin.qq.com',
      path: '/cgi-bin/material/add_material?access_token=' + token + '&type=image',
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data; boundary=' + boundary
      }
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.media_id) {
            resolve(result);
          } else {
            reject(new Error(result.errmsg || 'Upload failed'));
          }
        } catch (e) {
          reject(new Error(e.message));
        }
      });
    });
    
    req.on('error', reject);
    req.write(Buffer.concat(body));
    req.end();
  });
}

module.exports = {
  getAccessToken,
  addDraft,
  deleteDraft,
  getAllDrafts,
  uploadImage,
  uploadTempImage,
  request,
  CONFIG,
  setThumbMediaId
};
