/**
 * 抖音解析服务 (Node.js 版本)
 * 从 window._ROUTER_DATA 解析视频信息
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

// User-Agent 模拟移动端
const USER_AGENT = 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36';
const REFERER = 'https://www.douyin.com/?is_from_mobile_home=1&recommend=1';

/**
 * 从文本中提取URL
 */
function extractUrl(text) {
    if (!text) {
        return null;
    }
    const match = text.match(/(https?:\/\/[^\s]+)/);
    return match ? match[1] : null;
}

/**
 * 处理短链接重定向
 */
function resolveShortUrl(url) {
    return new Promise((resolve) => {
        if (!url.includes('v.douyin.com')) {
            resolve(url);
            return;
        }

        const parsedUrl = new URL(url);
        const isHttps = parsedUrl.protocol === 'https:';
        const client = isHttps ? https : http;

        const options = {
            headers: {
                'User-Agent': USER_AGENT
            },
            timeout: 10000
        };

        const req = client.request(url, options, (res) => {
            // 检查是否有重定向
            if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
                console.log('发现重定向到:', res.headers.location);
                // 递归处理重定向
                resolveShortUrl(res.headers.location).then(resolve);
            } else {
                resolve(res.responseUrl || url);
            }
        });

        req.on('error', (e) => {
            console.error('重定向失败:', e.message);
            resolve(url);
        });

        req.setTimeout(10000, () => {
            req.destroy();
            resolve(url);
        });
        
        req.end();
    });
}

/**
 * 发送HTTP请求
 */
function fetch(url, options = {}) {
    return new Promise((resolve, reject) => {
        const parsedUrl = new URL(url);
        const isHttps = parsedUrl.protocol === 'https:';
        const client = isHttps ? https : http;

        const defaultOptions = {
            headers: {
                'User-Agent': USER_AGENT,
                'Referer': REFERER,
                ...options.headers
            },
            timeout: 30000
        };

        const req = client.get(url, defaultOptions, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve(data));
        });

        req.on('error', reject);
        req.setTimeout(30000, () => {
            req.destroy();
            reject(new Error('Request timeout'));
        });
    });
}

/**
 * 提取抖音ID - 支持多种URL格式
 */
function extractDouyinId(url) {
    // 格式1: /share/video/123456789
    let match = url.match(/\/share\/video\/(\d+)/);
    if (match) return match[1];
    
    // 格式2: /share/note/123456789
    match = url.match(/\/share\/note\/(\d+)/);
    if (match) return match[1];
    
    // 格式3: /share/slides/123456789
    match = url.match(/\/share\/slides\/(\d+)/);
    if (match) return match[1];
    
    // 格式4: v.douyin.com/xxxxx (短链接)
    match = url.match(/v\.douyin\.com\/([a-zA-Z0-9]+)/);
    if (match) return match[1];
    
    // 格式5: 直接是数字ID
    match = url.match(/(\d{18,})/);
    if (match) return match[1];
    
    return null;
}

/**
 * 解析视频信息
 */
async function parseVideo(inputUrl) {
    try {
        console.log('开始解析URL:', inputUrl);

        let url = inputUrl;
        
        // 如果是短链接，先获取重定向后的真实URL
        if (url.includes('v.douyin.com')) {
            console.log('检测到短链接，获取重定向...');
            const resolvedUrl = await resolveShortUrl(url);
            console.log('重定向后的URL:', resolvedUrl);
            url = resolvedUrl;
        }

        // 替换 slides 为 note（实况类型处理）
        url = url.replace('slides', 'note');

        const parseId = extractDouyinId(url);
        if (!parseId) {
            console.error('无法提取抖音ID');
            return null;
        }
        
        console.log('提取的抖音ID:', parseId);

        const html = await fetch(url);
        if (!html) {
            console.error('请求失败');
            return null;
        }

        // 使用正则提取 window._ROUTER_DATA
        const pattern = /window\._ROUTER_DATA\s*=\s*(\{.*?\})<\/script>/;
        const match = html.match(pattern);

        if (!match) {
            console.error('未找到 _ROUTER_DATA');
            return null;
        }

        const jsonStr = match[1];
        const jsonData = JSON.parse(jsonStr);
        console.log('成功解析 _ROUTER_DATA');

        // 提取 loaderData
        const loaderData = jsonData.loaderData;
        if (!loaderData) {
            console.error('loaderData为空');
            return null;
        }

        // 找到包含 videoInfoRes 的key
        let videoInfoRes = null;
        for (const key of Object.keys(loaderData)) {
            if (key.includes('video_') || key.includes('note_')) {
                const keyData = loaderData[key];
                if (keyData && keyData.videoInfoRes) {
                    videoInfoRes = keyData.videoInfoRes;
                    break;
                }
            }
        }

        if (!videoInfoRes) {
            console.error('未找到 videoInfoRes');
            return null;
        }

        const itemList = videoInfoRes.item_list;
        if (!itemList || itemList.length === 0) {
            console.error('未找到 item_list');
            return null;
        }

        const itemData = itemList[0];
        return extractVideoInfo(itemData, parseId);

    } catch (e) {
        console.error('解析失败:', e.message);
        return null;
    }
}

/**
 * 从 item_list 数据中提取视频信息
 */
function extractVideoInfo(itemData, parseId) {
    if (!itemData) {
        return null;
    }

    try {
        const videoInfo = {
            parseId: parseId,
            title: itemData.desc || '无标题',
            author: {},
            statistics: {},
            images: [],
            cover: '',
            videoUrl: ''
        };

        // 作者信息
        if (itemData.author) {
            const authorObj = itemData.author;
            videoInfo.author = {
                nickname: authorObj.nickname || '',
                avatar: authorObj.avatar_thumb?.url_list?.[0] || ''
            };
        }

        // 统计信息
        if (itemData.statistics) {
            videoInfo.statistics = {
                digg: itemData.statistics.digg_count || 0,
                comment: itemData.statistics.comment_count || 0,
                share: itemData.statistics.share_count || 0
            };
        }

        // 检查是否为图集类型
        const images = itemData.images;
        if (images && images.length > 0) {
            console.log('检测到图集类型，图片数量:', images.length);
            videoInfo.images = images.map(img => img.url_list?.[0] || '');
            videoInfo.cover = videoInfo.images[0] || '';
        } else {
            // 视频类型
            console.log('检测到视频类型');
            const video = itemData.video;
            if (video) {
                // 获取封面
                videoInfo.cover = video.cover?.url_list?.[0] 
                    || video.origin_cover?.url_list?.[0] 
                    || '';

                // 获取视频地址
                const playAddr = video.play_addr;
                if (playAddr && playAddr.url_list && playAddr.url_list.length > 0) {
                    let videoUrl = playAddr.url_list[0];
                    
                    // 去除水印
                    videoUrl = videoUrl.replace('playwm', 'play');
                    videoUrl = videoUrl.replace('-watermark-', '');

                    videoInfo.videoUrl = videoUrl;
                    console.log('提取的视频URL:', videoUrl);
                } else {
                    // 备用方案：使用URI构造
                    const uri = playAddr?.uri;
                    if (uri && !uri.includes('mp3')) {
                        videoInfo.videoUrl = 'https://www.douyin.com/aweme/v1/play/?video_id=' + uri;
                    } else if (uri) {
                        videoInfo.videoUrl = uri;
                    }
                }
            }
        }

        return videoInfo;

    } catch (e) {
        console.error('提取视频信息失败:', e.message);
        return null;
    }
}

/**
 * 下载视频流 - 支持重定向
 */
function downloadVideo(videoUrl) {
    return new Promise((resolve, reject) => {
        const parsedUrl = new URL(videoUrl);
        const isHttps = parsedUrl.protocol === 'https:';
        const client = isHttps ? https : http;

        const options = {
            headers: {
                'User-Agent': USER_AGENT,
                'Referer': 'https://www.douyin.com/'
            },
            method: 'GET',
            followAllRedirects: true
        };

        const req = client.request(videoUrl, options, (res) => {
            // 检查是否有重定向
            if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
                console.log('视频流重定向到:', res.headers.location);
                downloadVideo(res.headers.location).then(resolve).catch(reject);
                return;
            }
            resolve(res);
        });

        req.on('error', reject);
        req.setTimeout(30000, () => {
            req.destroy();
            reject(new Error('Download timeout'));
        });
        
        req.end();
    });
}

// 导出模块
module.exports = {
    extractUrl,
    resolveShortUrl,
    parseVideo,
    downloadVideo,
    fetch
};

// 下载图片到本地 - 支持重定向
async function downloadImage(url, filename) {
    return new Promise((resolve, reject) => {
        const parsedUrl = new URL(url);
        const isHttps = parsedUrl.protocol === 'https:';
        const client = isHttps ? https : http;

        const options = {
            headers: {
                'User-Agent': USER_AGENT,
                'Referer': 'https://www.douyin.com/'
            },
            method: 'GET',
            followAllRedirects: true
        };

        const req = client.request(url, options, (res) => {
            // 检查是否有重定向
            if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
                console.log('图片下载重定向到:', res.headers.location);
                downloadImage(res.headers.location, filename).then(resolve).catch(reject);
                return;
            }
            
            const data = [];
            res.on('data', chunk => data.push(chunk));
            res.on('end', () => {
                const fs = require('fs');
                fs.writeFileSync(filename, Buffer.concat(data));
                resolve(filename);
            });
        });

        req.on('error', reject);
        req.setTimeout(30000, () => {
            req.destroy();
            reject(new Error('Download timeout'));
        });
        
        req.end();
    });
}

/**
 * 自动识别类型并下载
 * @param {string} url - 抖音链接
 * @param {string} outputDir - 输出目录（默认 ./output）
 * @returns {object} 下载结果
 */
async function parseAndDownload(url, outputDir = './output') {
    const result = await parseVideo(url);
    if (!result) {
        return { success: false, error: '解析失败' };
    }

    const output = {
        type: result.videoUrl ? 'video' : 'image',
        info: result,
        files: []
    };

    if (result.videoUrl) {
        // 视频类型
        console.log('检测到视频类型，下载中...');
        const videoPath = `${outputDir}/video_${result.parseId}.mp4`;
        await downloadVideoToFile(result.videoUrl, videoPath);
        output.files.push(videoPath);
        console.log('视频下载完成:', videoPath);
    } else if (result.images && result.images.length > 0) {
        // 图文类型
        const totalImages = result.images.length;
        const maxSend = 3;
        const imagesToSend = result.images.slice(0, maxSend);
        
        console.log(`检测到图文类型，共${totalImages}张图片，发送前${maxSend}张...`);
        
        for (let i = 0; i < imagesToSend.length; i++) {
            const imgPath = `${outputDir}/image_${result.parseId}_${i + 1}.jpg`;
            await downloadImage(imagesToSend[i], imgPath);
            output.files.push(imgPath);
        }
        
        output.remaining = totalImages - maxSend;
        console.log(`图文下载完成，前${maxSend}张`);
    }

    return output;
}

/**
 * 下载视频到文件 - 支持重定向
 */
async function downloadVideoToFile(videoUrl, filepath) {
    return new Promise((resolve, reject) => {
        const parsedUrl = new URL(videoUrl);
        const isHttps = parsedUrl.protocol === 'https:';
        const client = isHttps ? https : http;

        const options = {
            headers: {
                'User-Agent': USER_AGENT,
                'Referer': 'https://www.douyin.com/'
            },
            method: 'GET',
            followAllRedirects: true
        };

        const req = client.request(videoUrl, options, (res) => {
            // 检查是否有重定向
            if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
                console.log('视频下载重定向到:', res.headers.location);
                // 递归处理重定向
                downloadVideoToFile(res.headers.location, filepath).then(resolve).catch(reject);
                return;
            }
            
            const data = [];
            res.on('data', chunk => data.push(chunk));
            res.on('end', () => {
                const fs = require('fs');
                fs.writeFileSync(filepath, Buffer.concat(data));
                resolve(filepath);
            });
        });

        req.on('error', reject);
        req.setTimeout(60000, () => {
            req.destroy();
            reject(new Error('Download timeout'));
        });
        
        req.end();
    });
}

// 如果直接运行
if (require.main === module) {
    const url = process.argv[2] || 'https://v.douyin.com/IVher83Fp0Q/';
    const outputDir = process.argv[3] || './output'; // 默认当前目录的 output 文件夹
    
    (async () => {
        try {
            const result = await parseVideo(url);
            console.log('\n=== 解析结果 ===');
            console.log(JSON.stringify(result, null, 2));
            
            // 确保输出目录存在
            const fs = require('fs');
            if (!fs.existsSync(outputDir)) {
                fs.mkdirSync(outputDir, { recursive: true });
            }
            
            // 如果有视频URL，自动下载
            if (result && result.videoUrl) {
                console.log('\n自动下载视频...');
                const videoPath = `${outputDir}/video_${result.parseId}.mp4`;
                await downloadVideoToFile(result.videoUrl, videoPath);
                console.log('视频已保存到:', videoPath);
            }
        } catch (e) {
            console.error('错误:', e.message);
        }
    })();
}
