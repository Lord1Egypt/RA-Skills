const { chromium } = require('playwright-chromium');
const path = require('path');
const fs = require('fs');

/**
 * 使用 Playwright 在无头模式下解析抖音视频链接
 * @param {string} videoUrl 
 * @returns {Promise<Object>}
 */
async function fetchWithPlaywright(videoUrl) {
    console.log(`  🌐 启动无头浏览器处理: ${videoUrl}`);
    
    // 强制指定环境中的 Chromium 路径
    const browser = await chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        viewport: { width: 375, height: 667 }
    });

    const page = await context.newPage();
    let videoData = {
        title: '',
        author: '',
        downloadUrl: '',
        likes: 0,
        comments: 0
    };

    try {
        // 监听所有网络响应，寻找 aweme/detail API
        page.on('response', async (response) => {
            const url = response.url();
            if (url.includes('/aweme/v1/web/aweme/detail/')) {
                try {
                    const json = await response.json();
                    const detail = json.aweme_detail;
                    if (detail && detail.video) {
                        videoData.title = detail.desc;
                        videoData.author = detail.author?.nickname;
                        videoData.likes = detail.statistics?.digg_count;
                        videoData.comments = detail.statistics?.comment_count;

                        // 提取最高码率
                        const bitRates = detail.video.bit_rate || [];
                        if (bitRates.length > 0) {
                            bitRates.sort((a, b) => b.bit_rate - a.bit_rate);
                            videoData.downloadUrl = bitRates[0].play_addr?.url_list[0];
                        } else {
                            videoData.downloadUrl = detail.video.play_addr?.url_list[0];
                        }
                        
                        if (videoData.downloadUrl) {
                            console.log(`  ✅ 通过网络监听截获下载地址`);
                        }
                    }
                } catch (e) {}
            }
        });

        // 导航到页面
        await page.goto(videoUrl, { waitUntil: 'networkidle', timeout: 60000 });

        // 如果还没拿到地址，尝试从 DOM 中抠
        if (!videoData.downloadUrl) {
            console.log(`  ⚠️ 网络监听未命中，尝试 DOM 注入分析...`);
            const domUrl = await page.evaluate(() => {
                const video = document.querySelector('video');
                if (video && video.src && video.src.startsWith('http')) return video.src;
                const source = document.querySelector('video source');
                return source ? source.src : null;
            });
            if (domUrl) {
                videoData.downloadUrl = domUrl;
                console.log(`  ✅ 通过 DOM 提取成功`);
            }
        }

        // 提取标题和作者（作为兜底）
        if (!videoData.title) {
            videoData.title = await page.title();
        }

    } catch (error) {
        console.error(`  ❌ 模拟浏览器执行失败: ${error.message}`);
    } finally {
        await browser.close();
    }

    return videoData;
}

// 如果直接运行则进行测试
if (require.main === module) {
    const url = process.argv[2] || 'https://v.douyin.com/6biejtHeP30/';
    fetchWithPlaywright(url).then(res => {
        console.log('--- 结果 ---');
        console.log(JSON.stringify(res, null, 2));
    });
}

module.exports = { fetchWithPlaywright };
