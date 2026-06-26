// 清空微信公众号草稿箱
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

async function getAccessToken() {
  const p = '/cgi-bin/token?grant_type=client_credential&appid=' + CONFIG.APPID + '&secret=' + CONFIG.SECRET;
  const res = await request({ hostname: 'api.weixin.qq.com', path: p, method: 'GET' });
  if (!res.access_token) throw new Error('获取 Token 失败：' + JSON.stringify(res));
  return res.access_token;
}

async function deleteDraft(mediaId) {
  const token = await getAccessToken();
  const res = await request({
    hostname: 'api.weixin.qq.com',
    path: '/cgi-bin/draft/delete?access_token=' + token,
    method: 'POST'
  }, { media_id: mediaId });
  
  if (res.errcode) {
    throw new Error(res.errmsg);
  }
  return true;
}

async function clearAllDrafts() {
  console.log('🗑️  开始清空草稿箱...\n');
  
  // 读取发布记录
  const recordPath = 'D:\\DocsAutoWrter\\SGLang\\published\\publish-record.json';
  let articles = [];
  
  if (fs.existsSync(recordPath)) {
    const record = JSON.parse(fs.readFileSync(recordPath, 'utf8'));
    articles = record.articles || record.published || [];
  }
  
  console.log('📋 找到', articles.length, '个已发布草稿\n');
  
  let deleted = 0;
  let failed = 0;
  
  for (const article of articles) {
    const mediaId = article.draftId || article.media_id;
    if (!mediaId) continue;
    
    try {
      console.log('🗑️  删除:', article.title);
      await deleteDraft(mediaId);
      deleted++;
      console.log('   ✅ 已删除\n');
      // 避免频率限制
      await new Promise(r => setTimeout(r, 500));
    } catch (err) {
      console.log('   ❌ 失败:', err.message, '\n');
      failed++;
    }
  }
  
  // 清空发布记录
  fs.writeFileSync(recordPath, JSON.stringify({ publishedAt: new Date().toISOString(), total: 0, articles: [] }, null, 2), 'utf8');
  
  console.log('✅ 清空完成！删除', deleted, '个草稿，失败', failed, '个\n');
  return { deleted, failed };
}

// 主函数
clearAllDrafts()
  .then(() => {
    console.log('✅ 所有操作完成！');
    process.exit(0);
  })
  .catch(err => {
    console.error('❌ 错误:', err.message);
    console.error(err.stack);
    process.exit(1);
  });
