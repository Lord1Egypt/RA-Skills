/**
 * 使用 Playwright 获取抖音视频真实地址
 */

import { chromium } from 'playwright';

/**
 * 从抖音视频页获取真实视频 URL
 * @param {string} videoId - 视频 ID
 * @returns {Promise<Object>} 视频信息
 */
export async function getVideoWithPlaywright(videoId) {
  const url = `https://www.douyin.com/video/${videoId}`;
  let browser = null;
  
  try {
    console.log('启动浏览器...');
    browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage({
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    
    console.log('访问页面:', url);
    await page.goto(url, { 
      waitUntil: 'domcontentloaded',
      timeout: 30000 
    });
    
    // 等待页面基本加载
    console.log('等待页面内容...');
    await page.waitForTimeout(5000);
    
    // 等待视频元素加载
    console.log('等待视频加载...');
    try {
      await page.waitForSelector('video, [data-e2e="video-player"]', { timeout: 10000 });
    } catch (e) {
      console.log('未找到视频元素，尝试查找其他数据源...');
    }
    
    // 截取屏幕用于调试
    try {
      await page.screenshot({ path: 'debug-screenshot.png', fullPage: false });
      console.log('已保存调试截图：debug-screenshot.png');
    } catch (e) {
      console.log('截图失败:', e.message);
    }
    
    // 尝试从页面中提取视频信息
    const videoInfo = await page.evaluate(() => {
      const result = {
        videoUrl: null,
        title: null,
        author: null,
        cover: null
      };
      
      // 1. 尝试从 video 标签获取
      const videoEl = document.querySelector('video');
      if (videoEl && videoEl.src) {
        result.videoUrl = videoEl.src;
      }
      
      // 2. 尝试从 script 标签中获取数据
      const scripts = document.querySelectorAll('script');
      for (const script of scripts) {
        const content = script.innerHTML;
        if (content.includes('play_addr') || content.includes('video')) {
          // 尝试提取 JSON 数据
          const jsonMatch = content.match(/\{[^{}]*"play_addr"[^{}]*\}/);
          if (jsonMatch) {
            try {
              const data = JSON.parse(jsonMatch[0]);
              if (data.play_addr?.url_list?.[0]) {
                result.videoUrl = data.play_addr.url_list[0];
              }
            } catch (e) {}
          }
        }
      }
      
      // 3. 获取标题
      const titleEl = document.querySelector('h1, title, meta[property="og:title"]');
      if (titleEl) {
        result.title = titleEl.content || titleEl.textContent?.trim();
      }
      
      // 4. 获取作者
      const authorEl = document.querySelector('[data-e2e="user-name"], meta[property="og:author"]');
      if (authorEl) {
        result.author = authorEl.content || authorEl.textContent?.trim();
      }
      
      // 5. 获取封面
      const coverEl = document.querySelector('meta[property="og:image"]');
      if (coverEl) {
        result.cover = coverEl.content;
      }
      
      return result;
    });
    
    console.log('初步提取结果:', videoInfo);
    
    // 如果还是没找到，尝试从网络请求中拦截
    if (!videoInfo.videoUrl) {
      console.log('尝试从网络请求中获取...');
      const capturedUrls = [];
      
      // 拦截所有视频相关请求
      await page.route('**/*', route => {
        const url = route.request().url();
        if (url.includes('.mp4') || url.includes('video') || url.includes('aweme')) {
          console.log('捕获请求:', url);
          if (!capturedUrls.includes(url) && !url.includes('effect')) {
            capturedUrls.push(url);
            // 优先保存非 effect 的视频 URL
            if (!videoInfo.videoUrl) {
              videoInfo.videoUrl = url;
            }
          }
        }
        route.continue();
      });
      
      // 等待一段时间让视频开始加载
      await page.waitForTimeout(10000);
      
      if (capturedUrls.length > 0) {
        console.log('成功捕获', capturedUrls.length, '个视频相关 URL');
        console.log('第一个 URL:', capturedUrls[0]);
      }
    }
    
    // 更新成功状态
    if (videoInfo.videoUrl) {
      videoInfo.success = true;
    }
    
    return {
      success: !!videoInfo.videoUrl,
      videoId,
      url,
      ...videoInfo
    };
    
  } catch (error) {
    console.error('获取失败:', error.message);
    return {
      success: false,
      error: error.message,
      videoId,
      url
    };
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// 测试运行
if (process.argv[1]?.includes('browser-extract.js')) {
  const videoId = process.argv[2] || '7477287476999015732';
  console.log('测试视频 ID:', videoId);
  getVideoWithPlaywright(videoId).then(result => {
    console.log('\n=== 最终结果 ===');
    console.log(JSON.stringify(result, null, 2));
  });
}
