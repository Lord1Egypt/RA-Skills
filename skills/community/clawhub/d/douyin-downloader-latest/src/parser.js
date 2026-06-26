/**
 * 抖音视频链接解析器
 * 支持多种抖音分享链接格式
 */

import axios from 'axios';
import * as cheerio from 'cheerio';

// 抖音链接正则匹配
const DOUYIN_PATTERNS = [
  /https?:\/\/(?:www\.)?douyin\.com\/video\/(\d+)/,
  /https?:\/\/(?:www\.)?douyin\.com\/note\/(\d+)/,
  /modal_id=(\d+)/,  // 搜索页视频链接（灵活匹配）
  /https?:\/\/v\.douyin\.com\/([a-zA-Z0-9]+)/,
  /https?:\/\/m\.douyin\.com\/([a-zA-Z0-9]+)/,
  /https?:\/\/(?:www\.)?iesdouyin\.com\/([a-zA-Z0-9]+)/,
];

/**
 * 检查是否为抖音链接
 */
export function isDouyinUrl(url) {
  return DOUYIN_PATTERNS.some(pattern => pattern.test(url));
}

/**
 * 提取抖音链接中的关键部分
 */
export function extractDouyinId(url) {
  for (const pattern of DOUYIN_PATTERNS) {
    const match = url.match(pattern);
    if (match) {
      return match[1];
    }
  }
  return null;
}

/**
 * 解析抖音分享链接，获取视频信息
 * @param {string} url - 抖音分享链接
 * @returns {Promise<Object>} 视频信息对象
 */
export async function parseDouyinVideo(url) {
  try {
    // 处理短链接，获取重定向后的真实 URL
    const finalUrl = await getRedirectUrl(url);
    
    // 提取视频 ID
    const videoId = extractDouyinId(finalUrl);
    if (!videoId) {
      throw new Error('无法提取视频 ID');
    }

    // 获取视频页面 HTML
    const html = await fetchPage(finalUrl);
    const $ = cheerio.load(html);

    // 尝试从 script 标签中获取视频数据
    let videoData = null;
    $('script').each((_, script) => {
      const content = $(script).html();
      if (content && content.includes('video')) {
        try {
          // 尝试提取 JSON 数据
          const match = content.match(/window\._ROUTER_DATA\s*=\s*({.+?});/);
          if (match) {
            videoData = JSON.parse(match[1]);
          }
        } catch (e) {
          // 忽略解析错误
        }
      }
    });

    // 提取视频标题
    const title = $('title').text().replace(' - 抖音', '').trim();
    
    // 提取视频描述
    const description = $('meta[name="description"]').attr('content') || title;

    // 提取作者信息
    const author = $('meta[property="og:author"]').attr('content') || 
                   $('meta[name="author"]').attr('content') || 
                   '未知作者';

    // 提取封面图片
    const cover = $('meta[property="og:image"]').attr('content');

    // 提取无水印视频地址（需要进一步解析）
    const videoUrl = await extractVideoUrl(finalUrl, videoId);

    return {
      id: videoId,
      url: finalUrl,
      title,
      description,
      author,
      cover,
      videoUrl,
      parsedAt: new Date().toISOString()
    };
  } catch (error) {
    console.error('解析失败:', error.message);
    throw new Error(`解析抖音视频失败：${error.message}`);
  }
}

/**
 * 获取重定向后的真实 URL
 */
async function getRedirectUrl(url) {
  try {
    const response = await axios.get(url, {
      maxRedirects: 5,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      }
    });
    return response.request.res.responseUrl || url;
  } catch (error) {
    // 如果重定向失败，返回原 URL
    return url;
  }
}

/**
 * 获取页面 HTML
 */
async function fetchPage(url) {
  const response = await axios.get(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
  });
  return response.data;
}

/**
 * 提取视频下载地址
 * 注意：抖音会动态生成视频地址，这里使用备用方案
 */
async function extractVideoUrl(url, videoId) {
  // 方案 1: 尝试从 API 获取
  try {
    const apiUrl = `https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=${videoId}`;
    const response = await axios.get(apiUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': url,
      }
    });
    
    if (response.data && response.data.item_list && response.data.item_list[0]) {
      const video = response.data.item_list[0].video;
      // 优先获取无水印版本
      return video.play_addr.url_list[0] || video.download_addr.url_list[0];
    }
  } catch (error) {
    console.log('API 解析失败，使用备用方案');
  }

  // 方案 2: 返回一个标记，表示需要进一步处理
  return `https://www.douyin.com/video/${videoId}`;
}

/**
 * 批量解析链接
 */
export async function parseMultipleUrls(urls) {
  const results = [];
  const errors = [];

  for (const url of urls) {
    try {
      const result = await parseDouyinVideo(url);
      results.push(result);
    } catch (error) {
      errors.push({ url, error: error.message });
    }
  }

  return { results, errors };
}
