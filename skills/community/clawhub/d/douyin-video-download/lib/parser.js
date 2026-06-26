/**
 * 抖音链接解析模块
 * 使用 Playwright 绕过反爬，获取视频下载链接
 */

const { chromium } = require('playwright-chromium');
const { URL } = require('url');

/**
 * 解析短链接
 */
async function resolveShortUrl(shortUrl) {
  console.log(`  🔍 解析短链接: ${shortUrl}`);
  
  let browser;
  try {
    browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
  } catch (error) {
    if (error.message.includes('executable doesn\'t exist')) {
      throw new Error('Playwright 浏览器未安装。请运行: npx playwright install chromium');
    }
    throw error;
  }
  
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
  });
  
  const page = await context.newPage();
  
  try {
    await page.goto(shortUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(3000);
    
    const finalUrl = page.url();
    console.log(`  ✓ 解析完成: ${finalUrl}`);
    
    await browser.close();
    return finalUrl;
  } catch (error) {
    await browser.close();
    throw error;
  }
}

/**
 * 从完整 URL 中提取视频 ID
 */
function extractVideoId(url) {
  const match = url.match(/\/video\/(\d+)/);
  if (match) return match[1];
  
  const paths = url.split('/');
  for (const path of paths) {
    if (/^\d{10,}$/.test(path)) {
      return path;
    }
  }
  return Date.now().toString();
}

/**
 * 解析视频信息（播放器页面数据提取）
 */
async function fetchVideoInfo(url) {
  console.log(`  🌐 启动浏览器获取视频信息...`);
  
  let browser;
  try {
    browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
  } catch (error) {
    return { success: false, error: error.message };
  }
  
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
  });
  
  const page = await context.newPage();
  
  try {
    let videoId = null;
    
    // 关键优化：优先通过拦截 XHR/Fetch 请求来获取真正的 video_id 或 play_addr
    page.on('response', async (response) => {
      const resUrl = response.url();
      if (resUrl.includes('aweme/v1/web/aweme/detail')) {
          try {
              const json = await response.json();
              if (json?.aweme_detail?.video?.play_addr?.uri) {
                  videoId = json.aweme_detail.video.play_addr.uri;
              }
          } catch (e) {}
      }
    });

    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    
    // 方案 2: 从内容中正则表达式提取 video_id
    const content = await page.content();
    if (!videoId) {
        const vidMatch = content.match(/\"vid\":\"([a-z0-9A-Z_]+)\"/i) ||
                         content.match(/video_id=([a-z0-9A-Z_]+)/i) || 
                         content.match(/vid=([a-z0-9A-Z_]+)/i) ||
                         content.match(/\"uri\":\"([a-z0-9A-Z_]+)\"/i);
        if (vidMatch) videoId = vidMatch[1];
    }
    
    // 方案 3: 路径提取
    if (!videoId) {
      const urlMatch = url.match(/\/video\/(\d+)/);
      if (urlMatch) videoId = urlMatch[1];
    }

    // 统一构造无水印 1080P 下载链接
    let finalDownloadUrl = videoId ? `https://aweme.snssdk.com/aweme/v1/play/?video_id=${videoId}&ratio=1080p&line=0` : null;
    
    const videoInfo = await page.evaluate(() => {
      return {
        title: document.title,
        description: document.querySelector('meta[name="description"]')?.content
      };
    });
    
    await browser.close();
    
    return {
      success: !!finalDownloadUrl,
      downloadUrl: finalDownloadUrl,
      videoId,
      info: videoInfo
    };
  } catch (error) {
    await browser.close();
    return { success: false, error: error.message };
  }
}

/**
 * 主解析函数
 */
async function parseDouyinUrl(inputUrl) {
  try {
    let targetUrl = inputUrl;
    if (inputUrl.includes('v.douyin.com')) {
      targetUrl = await resolveShortUrl(inputUrl);
    }
    
    const result = await fetchVideoInfo(targetUrl);
    
    // 最终兜底：强制转换任何链接为无水印版
    if (result.downloadUrl) {
      result.downloadUrl = result.downloadUrl.replace('playwm', 'play');
    }

    return {
      videoId: result.videoId || extractVideoId(targetUrl),
      originalUrl: inputUrl,
      targetUrl,
      ...result
    };
  } catch (error) {
    throw new Error(`解析失败: ${error.message}`);
  }
}

module.exports = {
  parseDouyinUrl,
  resolveShortUrl,
  extractVideoId,
  fetchVideoInfo
};
