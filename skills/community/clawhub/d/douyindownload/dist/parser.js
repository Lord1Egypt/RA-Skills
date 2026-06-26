"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseVideo = parseVideo;
// 视频解析核心模块 - 基于 douyin.js 的成功逻辑
const axios_1 = __importDefault(require("axios"));
// 从分享文本中提取抖音URL
function extractDouyinUrl(text) {
    const patterns = [
        /(https?:\/\/v\.douyin\.com\/[a-zA-Z0-9_]+)/,
        /(https?:\/\/www\.douyin\.com\/video\/\d+)/,
        /(https?:\/\/www\.iesdouyin\.com\/share\/video\/\d+)/,
    ];
    for (const pattern of patterns) {
        const match = text.match(pattern);
        if (match)
            return match[1];
    }
    return null;
}
// 检测平台
function detectPlatform(url) {
    if (url.includes('douyin.com') || url.includes('v.douyin.com') || url.includes('iesdouyin.com'))
        return 'douyin';
    return 'unknown';
}
// 解析抖音视频（核心方法，基于 douyin.js 的 /api/parse 逻辑）
async function parseDouyin(url) {
    // 1. 从分享文本中提取真实URL
    const realUrl = extractDouyinUrl(url) || url;
    console.log('[douyin] 提取到的URL:', realUrl);
    let videoId = null;
    try {
        // 2. 获取重定向，确定真实 video ID
        const redirectResp = await axios_1.default.get(realUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
                'Referer': 'https://www.douyin.com/',
            },
            maxRedirects: 5,
            timeout: 15000,
        });
        const finalUrl = redirectResp.request.res.responseUrl || redirectResp.request.res.url;
        console.log('[douyin] 重定向后URL:', finalUrl);
        // 3. 提取视频ID
        const idMatch = finalUrl?.match(/video\/(\d+)/);
        videoId = idMatch ? idMatch[1] : null;
        if (!videoId) {
            return { success: false, platform: 'douyin', error: '无法获取视频ID' };
        }
        console.log('[douyin] 视频ID:', videoId);
    }
    catch (err) {
        // 如果重定向失败，尝试从URL直接提取ID
        const idMatch = realUrl.match(/video\/(\d+)/);
        if (idMatch) {
            videoId = idMatch[1];
        }
        else {
            return { success: false, platform: 'douyin', error: `重定向失败: ${err.message}` };
        }
    }
    // 4. 调用抖音 Web API（关键：aid=1128&channel=channel_pc_web）
    let videoData = null;
    try {
        const apiUrl = `https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id=${videoId}&aid=1128&channel=channel_pc_web&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=120.0.0.0`;
        const apiResp = await axios_1.default.get(apiUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.douyin.com/',
                'Accept': 'application/json',
            },
            timeout: 15000,
        });
        if (apiResp.data?.aweme_detail) {
            videoData = apiResp.data.aweme_detail;
        }
    }
    catch (apiErr) {
        console.log('[douyin] API失败，尝试备用方案:', apiErr.message);
    }
    // 5. 备用：从 iesdouyin.com HTML 解析
    if (!videoData) {
        try {
            const pageUrl = `https://www.iesdouyin.com/share/video/${videoId}/?from_ssr=1`;
            const pageResp = await axios_1.default.get(pageUrl, {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
                },
                timeout: 30000,
            });
            videoData = parseHtmlVideoData(pageResp.data, videoId);
        }
        catch (pageErr) {
            console.log('[douyin] HTML解析也失败:', pageErr.message);
        }
    }
    if (!videoData) {
        return { success: false, platform: 'douyin', error: '无法获取视频信息，请稍后重试', videoId };
    }
    // 6. 提取视频信息
    const title = videoData.desc || '';
    const nickname = videoData.author?.nickname || '';
    // 获取无水印视频地址
    let noWatermarkUrl = '';
    if (videoData.video?.play_addr?.url_list?.length > 0) {
        noWatermarkUrl = videoData.video.play_addr.url_list[0];
    }
    else if (videoData.video?.download_addr?.url_list?.length > 0) {
        noWatermarkUrl = videoData.video.download_addr.url_list[0];
    }
    else if (videoData.video?.bit_rate?.length > 0) {
        const bitRate = videoData.video.bit_rate[0];
        noWatermarkUrl = bitRate?.play_addr?.url_list?.[0] || '';
    }
    // 转换为无水印地址
    if (noWatermarkUrl) {
        if (noWatermarkUrl.startsWith('http')) {
            noWatermarkUrl = noWatermarkUrl.replace('/playwm/', '/play/');
            noWatermarkUrl = noWatermarkUrl.replace('&wm=2001', '&wm=2000');
            noWatermarkUrl = noWatermarkUrl.replace('&wm=3001', '&wm=3000');
        }
        else if (noWatermarkUrl.startsWith('v0') || noWatermarkUrl.startsWith('v1') || noWatermarkUrl.startsWith('v2') || noWatermarkUrl.startsWith('v3')) {
            noWatermarkUrl = `https://aweme.snssdk.com/aweme/v1/play/?video_id=${noWatermarkUrl}&ratio=720p&line=1`;
        }
        else if (noWatermarkUrl.startsWith('/')) {
            noWatermarkUrl = 'https://aweme.snssdk.com' + noWatermarkUrl;
        }
        noWatermarkUrl = noWatermarkUrl.replace('/playwm/', '/play/');
    }
    // 获取封面
    let cover = '';
    if (videoData.video?.cover?.url_list?.length > 0) {
        cover = videoData.video.cover.url_list[0];
    }
    else if (videoData.video?.origin_cover?.url_list?.length > 0) {
        cover = videoData.video.origin_cover.url_list[0];
    }
    return {
        success: !!noWatermarkUrl,
        title,
        author: nickname,
        coverUrl: cover,
        videoUrl: noWatermarkUrl,
        platform: 'douyin',
        videoId,
        error: noWatermarkUrl ? undefined : '未找到视频地址',
    };
}
// 从 HTML 中解析视频数据（备用）
function parseHtmlVideoData(html, videoId) {
    try {
        // 尝试多种 pattern 匹配 RENDER_DATA
        const patterns = [
            /"aweme_detail"\s*:\s*\{(.+?)\}(?=,\s*")/,
            /window\.__INITIAL_STATE__\s*=\s*(\{[^]+\})/,
            /"play_addr"\s*:\s*\{[^}]*"uri"\s*:\s*"([^"]+)"/,
        ];
        for (const pattern of patterns) {
            const match = html.match(pattern);
            if (match) {
                try {
                    // 对于复杂的 JSON，尝试提取 play_addr.uri
                    const uriMatch = html.match(/"play_addr"\s*:\s*\{[^}]*"uri"\s*:\s*"([^"]+)"/);
                    if (uriMatch) {
                        return {
                            video: {
                                play_addr: {
                                    url_list: [uriMatch[1].replace('/playwm/', '/play/')],
                                },
                            },
                        };
                    }
                }
                catch (e) {
                    // 继续
                }
            }
        }
        return null;
    }
    catch (e) {
        return null;
    }
}
// 主解析函数
async function parseVideo(url) {
    const platform = detectPlatform(url);
    console.log('[parser] 平台检测:', platform, '| URL:', url);
    switch (platform) {
        case 'douyin': return parseDouyin(url);
        default:
            return {
                success: false,
                platform: 'douyin',
                error: '不支持的平台，目前仅支持抖音视频链接',
            };
    }
}
//# sourceMappingURL=parser.js.map