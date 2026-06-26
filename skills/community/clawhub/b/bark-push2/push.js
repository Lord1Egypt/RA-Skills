const https = require('https');
const fs = require('fs');
const path = require('path');

/**
 * 🔒 自动获取 Bark Key 的逻辑
 */
function getBarkKey() {
  // 1. 优先从环境变量读取
  if (process.env.BARK_KEY) return process.env.BARK_KEY;

  // 2. 备选：从 USER.md 中解析
  try {
    const userMdPath = path.join(__dirname, '../../USER.md');
    if (fs.existsSync(userMdPath)) {
      const content = fs.readFileSync(userMdPath, 'utf-8');
      const match = content.match(/BARK_KEY\*\*:\s*([a-zA-Z0-9]+)/);
      if (match && match[1]) return match[1];
    }
  } catch (e) {
    console.error('无法读取 USER.md 配置文件');
  }
  return null;
}

/**
 * 🛠️ 推送主逻辑
 */
async function sendPush(message, title = 'OpenClaw') {
  const key = getBarkKey();
  if (!key) {
    console.error('❌ 错误: 未能在环境变量或 USER.md 中找到 BARK_KEY。');
    process.exit(1);
  }

  const fullUrl = `https://api.day.app/${key}/${encodeURIComponent(title)}/${encodeURIComponent(message)}`;
  
  console.log(`正在从本地配置加载 Key 并推送至 Bark...`);

  return new Promise((resolve, reject) => {
    https.get(fullUrl, (res) => {
      if (res.statusCode === 200) {
        console.log('✅ 永久配置加载成功，推送完成！');
        resolve();
      } else {
        reject(new Error(`HTTP ${res.statusCode}`));
      }
    }).on('error', reject);
  });
}

(async () => {
  const args = process.argv.slice(2);
  if (args.length < 1) process.exit(1);

  const message = args[0];
  let title = '系统通知';
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--title' && args[i + 1]) title = args[i + 1];
  }

  try {
    await sendPush(message, title);
  } catch (e) {
    console.error(`推送失败: ${e.message}`);
    process.exit(1);
  }
})();
