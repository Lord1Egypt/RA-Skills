/**
 * URL 解析模块
 * 处理抖音视频链接，支持短链转长链
 */

const https = require('https');
const http = require('http');

const USER_AGENTS = [
  'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
  'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
];

function getRandomUserAgent() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function isShortUrl(url) {
  const shortPatterns = [
    /v\.douyin\.com/i,
    /vm\.douyin\.com/i,
    /douyin\.com\/video\/\d+/i
  ];
  return shortPatterns.some(pattern => pattern.test(url));
}

function normalizeUrl(url) {
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://' + url;
  }
  return url;
}

function followRedirect(url, maxRedirects = 5) {
  return new Promise((resolve, reject) => {
    if (maxRedirects <= 0) {
      reject(new Error('重定向次数过多'));
      return;
    }

    const protocol = url.startsWith('https') ? https : http;
    const parsedUrl = new URL(url);

    const options = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'HEAD',
      headers: {
        'User-Agent': getRandomUserAgent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
      }
    };

    const req = protocol.request(options, (res) => {
      const statusCode = res.statusCode;
      const location = res.headers.location;

      if (statusCode >= 300 && statusCode < 400 && location) {
        let redirectUrl = location;
        if (!location.startsWith('http')) {
          redirectUrl = `${parsedUrl.protocol}//${parsedUrl.hostname}${location}`;
        }
        followRedirect(redirectUrl, maxRedirects - 1)
          .then(resolve)
          .catch(reject);
      } else if (statusCode >= 200 && statusCode < 300) {
        resolve(url);
      } else {
        resolve(url);
      }
    });

    req.on('error', (error) => {
      resolve(url);
    });

    req.setTimeout(10000, () => {
      req.destroy();
      resolve(url);
    });

    req.end();
  });
}

function extractVideoId(url) {
  const patterns = [
    /video\/(\d+)/i,
    /\/(\d{19,})/i,
    /mod_id=(\d+)/i,
    /item_ids=(\d+)/i
  ];

  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) {
      return match[1];
    }
  }

  return null;
}

async function resolveDouyinUrl(inputUrl) {
  const url = normalizeUrl(inputUrl);
  
  if (!isShortUrl(url)) {
    const videoId = extractVideoId(url);
    return {
      originalUrl: inputUrl,
      resolvedUrl: url,
      videoId: videoId,
      isShortUrl: false
    };
  }

  try {
    const resolvedUrl = await followRedirect(url);
    const videoId = extractVideoId(resolvedUrl);
    
    return {
      originalUrl: inputUrl,
      resolvedUrl: resolvedUrl,
      videoId: videoId,
      isShortUrl: true
    };
  } catch (error) {
    return {
      originalUrl: inputUrl,
      resolvedUrl: url,
      videoId: extractVideoId(url),
      isShortUrl: true,
      error: error.message
    };
  }
}

module.exports = {
  resolveDouyinUrl,
  extractVideoId,
  isShortUrl,
  normalizeUrl,
  getRandomUserAgent
};
