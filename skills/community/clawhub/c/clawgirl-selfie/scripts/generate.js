#!/usr/bin/env node

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

const prompt = process.argv[2];

// 尝试从环境变量获取 API Key，如果没有则从配置文件读取
let apiKey = process.env.CLAWGIRL_API_KEY;

if (!apiKey) {
  // 尝试从 openclaw.json 读取
  const configPaths = [
    path.join(os.homedir(), '.openclaw', 'openclaw.json'),
    path.join(os.homedir(), '.openclaw', 'openclaw.json.bak'),
    path.join(os.homedir(), '.openclaw', 'openclaw.json.bak.1'),
  ];

  for (const configPath of configPaths) {
    try {
      if (fs.existsSync(configPath)) {
        const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        apiKey = config?.skills?.entries?.clawgirl?.env?.CLAWGIRL_API_KEY;
        if (apiKey) break;
      }
    } catch (e) {
      // 配置文件解析失败，记录并继续尝试下一个
      if (process.env.CLAWGIRL_DEBUG) {
        console.warn(`[DEBUG] 配置文件解析失败 ${configPath}: ${e.message}`);
      }
    }
  }
}

if (!apiKey) {
  console.log("ERROR: 未配置 API Key。请先同步 skill 配置并提供可用的 CLAWGIRL_API_KEY。");
  process.exit(1);
}

function encodeTextResponse(text) {
  return Buffer.from(String(text), 'utf8').toString('base64');
}

const SAAS_API_URL = 'https://clawgirl.date/api/v1/chat';
const requestData = JSON.stringify({
  message: prompt || '来张自拍',
  history: []
});

const options = {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`,
    'Content-Length': Buffer.byteLength(requestData)
  }
};

const req = https.request(SAAS_API_URL, options, (res) => {
  let responseBody = '';

  res.on('data', (chunk) => {
    responseBody += chunk;
  });

  res.on('end', () => {
    try {
      const data = JSON.parse(responseBody);
      if (res.statusCode === 200 && data.imageUrl) {
        const timestamp = Date.now();
        const mediaDir = process.env.OPENCLAW_MEDIA_DIR || path.join(os.homedir(), '.openclaw', 'media');
        const localPath = path.join(mediaDir, `selfie_${timestamp}.png`);

        downloadImage(data.imageUrl, localPath, (success) => {
          if (success) {
            console.log(`IMAGE_PATH=${localPath}`);
          } else {
            console.log(`IMAGE_URL=${data.imageUrl}`);
            console.log(`DOWNLOAD_FAILED=true`);
          }
        });
      } else if (
        res.statusCode === 200 &&
        data.shouldGenerateImage === false &&
        typeof data.response === 'string' &&
        data.response.trim()
      ) {
        console.log(`TEXT_RESPONSE_BASE64=${encodeTextResponse(data.response.trim())}`);
      } else if (res.statusCode === 401) {
        console.log('ERROR: API Key 无效或已过期。请更新本地 CLAWGIRL_API_KEY 配置，并保持宿主环境中的 skill 密钥为最新值。');
        process.exit(1);
      } else if (res.statusCode === 403) {
        console.log(`ERROR: 生成次数已用完，请前往 https://clawgirl.date 充值。`);
        process.exit(1);
      } else {
        console.log(`ERROR: ${data.error || '服务端错误'}`);
        process.exit(1);
      }
    } catch (e) {
      console.log(`ERROR: ${e.message}`);
      process.exit(1);
    }
  });
});

req.on('error', (e) => {
  console.log(`ERROR: ${e.message}`);
  process.exit(1);
});

req.write(requestData);
req.end();

function downloadImage(url, localPath, callback) {
  const protocol = url.startsWith('https') ? https : http;

  const dir = path.dirname(localPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  const request = protocol.get(url, (response) => {
    if (response.statusCode === 301 || response.statusCode === 302) {
      downloadImage(response.headers.location, localPath, callback);
      return;
    }

    if (response.statusCode !== 200) {
      callback(false);
      return;
    }

    const file = fs.createWriteStream(localPath);
    response.pipe(file);

    file.on('finish', () => {
      file.close();
      callback(true);
    });

    file.on('error', () => {
      fs.unlinkSync(localPath);
      callback(false);
    });
  });

  request.on('error', () => {
    callback(false);
  });

  request.setTimeout(30000, () => {
    request.destroy();
    callback(false);
  });
}
