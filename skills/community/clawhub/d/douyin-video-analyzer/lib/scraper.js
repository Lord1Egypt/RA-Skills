/**
 * 网页抓取模块
 * 抓取抖音视频页面数据
 */

const https = require('https');
const urlResolver = require('./url-resolver');

const USER_AGENTS = [
  'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
  'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
];

function getRandomUserAgent() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function fetchPage(url) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    
    const options = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || 443,
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'GET',
      headers: {
        'User-Agent': getRandomUserAgent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'identity',
        'Connection': 'keep-alive',
        'Referer': 'https://www.douyin.com/'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      const statusCode = res.statusCode;
      const headers = res.headers;

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        resolve({
          statusCode,
          headers,
          body: data
        });
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.setTimeout(15000, () => {
      req.destroy();
      reject(new Error('请求超时'));
    });

    req.end();
  });
}

function extractVideoData(html) {
  const data = {
    videoId: null,
    title: '',
    author: '',
    authorId: '',
    likes: 0,
    comments: 0,
    shares: 0,
    collects: 0,
    publishTime: '',
    duration: 0,
    cover: '',
    videoUrl: '',
    music: '',
    hashtags: []
  };

  try {
    const renderDataMatch = html.match(/RENDER_DATA\s*=\s*(\{[\s\S]*?\})\s*<\/script>/i);
    if (renderDataMatch) {
      const renderData = JSON.parse(decodeURIComponent(renderDataMatch[1]));
      const videoDetail = renderData?.app?.videoDetail || renderData?.videoDetail;
      
      if (videoDetail) {
        data.videoId = videoDetail.id || videoDetail.aweme_id;
        data.title = videoDetail.desc || '';
        data.author = videoDetail.author?.nickname || videoDetail.author?.unique_id || '';
        data.authorId = videoDetail.author?.uid || videoDetail.author?.unique_id || '';
        data.likes = videoDetail.statistics?.digg_count || 0;
        data.comments = videoDetail.statistics?.comment_count || 0;
        data.shares = videoDetail.statistics?.share_count || 0;
        data.collects = videoDetail.statistics?.collect_count || 0;
        data.duration = videoDetail.video?.duration || 0;
        data.cover = videoDetail.video?.cover?.url_list?.[0] || videoDetail.video?.origin_cover?.url_list?.[0] || '';
        data.videoUrl = videoDetail.video?.play_addr?.url_list?.[0] || '';
        data.music = videoDetail.music?.title || '';
        
        if (videoDetail.text_extra) {
          data.hashtags = videoDetail.text_extra
            .filter(item => item.hashtag_name)
            .map(item => item.hashtag_name);
        }
      }
    }
  } catch (error) {
    console.error('解析视频数据失败:', error.message);
  }

  try {
    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    if (titleMatch && !data.title) {
      data.title = titleMatch[1].replace(' - 抖音', '').trim();
    }

    const ogImageMatch = html.match(/<meta[^>]*property="og:image"[^>]*content="([^"]+)"/i);
    if (ogImageMatch && !data.cover) {
      data.cover = ogImageMatch[1];
    }
  } catch (error) {
    // Ignore parsing errors
  }

  return data;
}

async function scrapeVideoData(url) {
  const resolved = await urlResolver.resolveDouyinUrl(url);
  
  if (!resolved.resolvedUrl) {
    throw new Error('无法解析视频链接');
  }

  await sleep(500);

  let targetUrl = resolved.resolvedUrl;
  
  if (!targetUrl.includes('www.douyin.com')) {
    targetUrl = `https://www.douyin.com/video/${resolved.videoId}`;
  }

  try {
    const response = await fetchPage(targetUrl);
    
    if (response.statusCode !== 200) {
      throw new Error(`HTTP 错误: ${response.statusCode}`);
    }

    const videoData = extractVideoData(response.body);
    videoData.originalUrl = resolved.originalUrl;
    videoData.resolvedUrl = resolved.resolvedUrl;
    videoData.videoId = videoData.videoId || resolved.videoId;

    return videoData;
  } catch (error) {
    throw new Error(`抓取失败: ${error.message}`);
  }
}

function formatNumber(num) {
  if (num >= 100000000) {
    return (num / 100000000).toFixed(1) + '亿';
  } else if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万';
  }
  return num.toLocaleString();
}

function formatDuration(ms) {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

module.exports = {
  scrapeVideoData,
  fetchPage,
  extractVideoData,
  formatNumber,
  formatDuration
};
