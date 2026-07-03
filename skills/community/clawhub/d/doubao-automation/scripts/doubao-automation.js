/**
 * doubao-automation.js
 * 豆包 AI 自动化操作脚本
 * 
 * 基于 Playwright CDP (Chrome DevTools Protocol) 协议
 * 连接已登录的 Edge 浏览器，自动化操作豆包
 * 
 * 用法:
 *   node doubao-automation.js --action=chat --prompt="你好"
 *   node doubao-automation.js --action=generate-image --prompt="一只可爱的橘猫" --output="./output"
 *   node doubao-automation.js --action=download-last --output="./downloads"
 */

const playwrightCorePath = 'C:/Users/Owner/.workbuddy/binaries/node/workspace/node_modules/playwright-core';
const { chromium } = require(playwrightCorePath);
const path = require('path');
const fs = require('fs');
const https = require('https');
const http = require('http');

// ==================== 配置 ====================
const CONFIG = {
    cdpPort: 9222,
    doubaoUrl: 'https://www.doubao.com/chat/',
    // 超时配置（毫秒）
    timeout: {
        connect: 15000,       // CDP 连接超时
        navigation: 30000,    // 页面导航超时
        aiResponse: 180000,   // AI 生成响应超时 (3分钟)
        download: 60000,      // 下载超时
    },
    // 豆包页面的选择器（可能随页面更新而变化）
    selectors: {
        // 聊天输入框 — 多个备选
        chatInput: [
            'textarea[placeholder*="发消息"]',
            'textarea[placeholder*="输入"]',
            'textarea[placeholder*="聊天"]',
            'textarea[placeholder*="对话"]',
            '[contenteditable="true"]',
            '#chat-input textarea',
            '.chat-input textarea',
            'textarea.semi-input-textarea',
            '[data-testid="chat-input"]',
            '.chat-input__input',
        ],
        // 发送按钮
        sendButton: [
            '.seemkit-btn--primary',
            'button[type="submit"]',
            'button:has-text("发送")',
            '[data-testid="send-button"]',
            '.send-btn',
            'button:has(svg)',
        ],
        // AI 回复区域
        aiResponse: [
            '.message-item--ai',
            '.ai-message',
            '[class*="assistant"]',
            '[class*="bot"]',
            '.message:last-of-type',
        ],
        // 生成的图片
        generatedImage: [
            '.message-item--ai img',
            '.ai-message img',
            '[class*="assistant"] img',
            'img[src*="doubao"]',
        ],
        // 生成的视频
        generatedVideo: [
            '.message-item--ai video',
            '.ai-message video',
            '[class*="assistant"] video',
            'video[src*="doubao"]',
        ],
        // 新对话按钮
        newChatBtn: [
            'button:has-text("新对话")',
            'button:has-text("新建")',
            '[data-testid="new-chat"]',
            '.new-chat-btn',
        ],
        // 停止生成按钮（出现表示AI还在生成）
        stopBtn: [
            'button:has-text("停止")',
            '[data-testid="stop-button"]',
            '.stop-btn',
        ],
        // 图片转视频按钮
        imgToVideo: [
            'button:has-text("转视频")',
            'button:has-text("生成视频")',
            '[data-testid="image-to-video"]',
        ],
        // 下载按钮
        downloadBtn: [
            'button:has-text("下载")',
            'a[download]',
            '[data-testid="download"]',
        ],
    },
};

// ==================== 工具函数 ====================

/**
 * 带重试的 findElement — 遍历备选选择器，返回第一个可见元素
 */
async function findElement(page, selectorList, options = {}) {
    const { timeout = 5000, visible = true } = options;
    for (const selector of selectorList) {
        try {
            const element = await page.waitForSelector(selector, { timeout, state: visible ? 'visible' : 'attached' });
            if (element) {
                console.log(`  [选择器匹配] "${selector}"`);
                return element;
            }
        } catch {
            // 该选择器未匹配，尝试下一个
        }
    }
    return null;
}

/**
 * 等待 AI 响应完成
 * 策略：等待"停止生成"按钮消失或新消息出现
 */
async function waitForAIResponse(page, timeout = CONFIG.timeout.aiResponse) {
    console.log('  [等待 AI 响应...]');
    const startTime = Date.now();
    
    // 等待策略：检测是否有"停止生成"按钮
    try {
        await page.waitForFunction(
            () => {
                const stopBtns = document.querySelectorAll('button');
                for (const btn of stopBtns) {
                    if (btn.textContent.includes('停止')) return true;
                }
                return false;
            },
            { timeout: 5000 }
        ).catch(() => {});
        
        console.log('  AI 开始生成...');
    } catch {
        // "停止"按钮没出现，可能已经生成完了
    }
    
    // 等待"停止"按钮消失（表示生成完成）
    try {
        await page.waitForFunction(
            () => {
                const stopBtns = document.querySelectorAll('button');
                for (const btn of stopBtns) {
                    if (btn.textContent.includes('停止')) return false;
                }
                return true;
            },
            { timeout: timeout - (Date.now() - startTime), polling: 2000 }
        );
        console.log('  AI 生成完成');
    } catch {
        console.log('  [超时] AI 生成可能仍在进行中，继续执行...');
    }
    
    // 额外等待 2 秒确保内容渲染
    await page.waitForTimeout(2000);
}

/**
 * 下载 URL 内容到本地文件
 */
async function downloadFile(url, filePath) {
    return new Promise((resolve, reject) => {
        const protocol = url.startsWith('https') ? https : http;
        const dir = path.dirname(filePath);
        
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        
        const file = fs.createWriteStream(filePath);
        protocol.get(url, (response) => {
            // 处理重定向
            if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
                file.close();
                fs.unlinkSync(filePath);
                downloadFile(response.headers.location, filePath).then(resolve).catch(reject);
                return;
            }
            
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                resolve(filePath);
            });
        }).on('error', (err) => {
            fs.unlink(filePath, () => {});
            reject(err);
        });
    });
}

/**
 * 确保输出目录存在
 */
function ensureOutputDir(dirPath) {
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
    }
    return dirPath;
}

// ==================== 核心操作 ====================

/**
 * 连接到 Edge CDP 浏览器
 */
async function connectToEdge(port = CONFIG.cdpPort) {
    console.log(`[连接] 正在连接 Edge CDP (端口: ${port})...`);
    
    const browserWSEndpoint = `http://localhost:${port}`;
    let browser;
    
    try {
        browser = await chromium.connectOverCDP(browserWSEndpoint, {
            timeout: CONFIG.timeout.connect,
        });
        console.log('[成功] 已连接到 Edge 浏览器');
        return browser;
    } catch (err) {
        console.error('[失败] 无法连接到 Edge 浏览器');
        console.error(`  请确保已运行: start msedge --remote-debugging-port=${port}`);
        console.error(`  错误: ${err.message}`);
        throw new Error(`CDP连接失败: ${err.message}`);
    }
}

/**
 * 获取或创建豆包页面
 */
async function getDoubaoPage(browser) {
    const contexts = browser.contexts();
    if (contexts.length === 0) {
        throw new Error('浏览器没有可用的上下文，请确认 Edge 已正常启动');
    }
    
    const pages = contexts[0].pages();
    
    // 查找已打开的豆包页面
    for (const p of pages) {
        try {
            const url = p.url();
            if (url.includes('doubao.com')) {
                console.log('[复用] 找到已打开的豆包页面');
                return p;
            }
        } catch {}
    }
    
    // 创建新页面
    console.log('[新建] 创建新的豆包页面...');
    const page = await contexts[0].newPage();
    await page.goto(CONFIG.doubaoUrl, { 
        waitUntil: 'domcontentloaded',
        timeout: CONFIG.timeout.navigation 
    });
    
    // 等待页面加载完成
    await page.waitForTimeout(3000);
    return page;
}

/**
 * 在豆包中发送消息
 */
async function sendMessage(page, message) {
    console.log(`[发送] 内容: "${message.substring(0, 50)}${message.length > 50 ? '...' : ''}"`);
    
    // 找到输入框
    const input = await findElement(page, CONFIG.selectors.chatInput, { timeout: 10000 });
    if (!input) {
        // 截图用于调试
        const debugPath = path.join(process.cwd(), 'debug-input.png');
        await page.screenshot({ path: debugPath, fullPage: false });
        throw new Error('未找到聊天输入框，请检查豆包页面是否正常加载。截图已保存到 ' + debugPath);
    }
    
    // 聚焦并填入内容
    await input.click();
    await page.waitForTimeout(300);
    await input.fill(message);
    await page.waitForTimeout(500);
    
    // 推荐使用 Enter 键发送（比点击按钮更可靠）
    await input.press('Enter');
    console.log('  [已发送（Enter）]');
    
    // 等待 AI 响应
    await waitForAIResponse(page);
}

/**
 * 获取 AI 最后的回复文本
 */
async function getLastAIResponse(page) {
    const responseElements = await page.$$(CONFIG.selectors.aiResponse.join(', '));
    
    if (responseElements.length === 0) {
        return null;
    }
    
    const lastResponse = responseElements[responseElements.length - 1];
    const text = await lastResponse.textContent();
    return text.trim();
}

/**
 * 下载 AI 回复中的图片
 */
async function downloadGeneratedImages(page, outputDir) {
    ensureOutputDir(outputDir);
    console.log(`[下载图片] 保存到: ${outputDir}`);
    
    const images = await page.$$(CONFIG.selectors.generatedImage.join(', '));
    if (images.length === 0) {
        console.log('  [未找到] 没有可下载的图片');
        return [];
    }
    
    const downloaded = [];
    
    // 只下载最近回复中的图片
    const lastAiMessage = await findElement(page, CONFIG.selectors.aiResponse, { timeout: 3000 });
    if (!lastAiMessage) {
        // 如果找不到 AI 回复容器，下载页面上所有 doubao 图片
        const allImages = await page.$$('img[src*="doubao"], img[src*="volc"]');
        for (const img of allImages) {
            try {
                const src = await img.getAttribute('src');
                if (!src || src.startsWith('data:') || downloaded.includes(src)) continue;
                
                const timestamp = Date.now();
                const ext = src.includes('.png') ? 'png' : 'jpg';
                const filename = `doubao-image-${timestamp}.${ext}`;
                const filePath = path.join(outputDir, filename);
                
                await downloadFile(src, filePath);
                console.log(`  [已保存] ${filename}`);
                downloaded.push(filePath);
            } catch (err) {
                console.log(`  [跳过] 下载失败: ${err.message}`);
            }
        }
        return downloaded;
    }
    
    // 在最近回复中找图片
    const msgImages = await lastAiMessage.$$('img');
    for (const img of msgImages) {
        try {
            const src = await img.getAttribute('src');
            if (!src || src.startsWith('data:') || downloaded.includes(src)) continue;
            
            const timestamp = Date.now();
            const ext = src.includes('.png') ? 'png' : 'jpg';
            const filename = `doubao-image-${timestamp}.${ext}`;
            const filePath = path.join(outputDir, filename);
            
            await downloadFile(src, filePath);
            console.log(`  [已保存] ${filename}`);
            downloaded.push(filePath);
        } catch (err) {
            console.log(`  [跳过] 下载失败: ${err.message}`);
        }
    }
    
    return downloaded;
}

/**
 * 下载 AI 回复中的视频
 */
async function downloadGeneratedVideos(page, outputDir) {
    ensureOutputDir(outputDir);
    console.log(`[下载视频] 保存到: ${outputDir}`);
    
    const videos = await page.$$(CONFIG.selectors.generatedVideo.join(', '));
    if (videos.length === 0) {
        console.log('  [未找到] 没有可下载的视频');
        return [];
    }
    
    const downloaded = [];
    for (const video of videos) {
        try {
            const src = await video.getAttribute('src');
            if (!src || downloaded.includes(src)) continue;
            
            const timestamp = Date.now();
            const ext = '.mp4';
            const filename = `doubao-video-${timestamp}${ext}`;
            const filePath = path.join(outputDir, filename);
            
            await downloadFile(src, filePath);
            console.log(`  [已保存] ${filename}`);
            downloaded.push(filePath);
        } catch (err) {
            console.log(`  [跳过] 下载失败: ${err.message}`);
        }
    }
    
    // 也尝试从 video 标签的 source 子元素找
    const sources = await page.$$('video source');
    for (const source of sources) {
        try {
            const src = await source.getAttribute('src');
            if (!src || downloaded.includes(src)) continue;
            
            const timestamp = Date.now();
            const filename = `doubao-video-${timestamp}.mp4`;
            const filePath = path.join(outputDir, filename);
            
            await downloadFile(src, filePath);
            console.log(`  [已保存] ${filename}`);
            downloaded.push(filePath);
        } catch (err) {
            console.log(`  [跳过] 下载失败: ${err.message}`);
        }
    }
    
    return downloaded;
}

// ==================== 操作动作 ====================

/**
 * 纯文本对话
 */
async function actionChat(page, prompt) {
    console.log('\n=== 文本对话 ===');
    await sendMessage(page, prompt);
    const response = await getLastAIResponse(page);
    
    if (response) {
        console.log('\n--- AI 回复 ---');
        console.log(response.substring(0, 2000));
        if (response.length > 2000) {
            console.log('\n... (内容过长，已截断)');
        }
        console.log('--- 结束 ---\n');
    }
    
    return { type: 'chat', prompt, response };
}

/**
 * 生成图片
 */
async function actionGenerateImage(page, prompt, outputDir) {
    console.log('\n=== 生成图片 ===');
    
    // 构建专业的图片生成提示词
    const imagePrompt = `请帮我生成一张图片：${prompt}。请生成高质量、细节丰富的图片。`;
    
    await sendMessage(page, imagePrompt);
    
    // 尝试下载生成的图片
    let downloaded = [];
    if (outputDir) {
        await page.waitForTimeout(3000); // 等待图片渲染
        downloaded = await downloadGeneratedImages(page, outputDir);
    }
    
    const response = await getLastAIResponse(page);
    console.log('\n--- AI 回复摘要 ---');
    console.log((response || '无文本回复').substring(0, 300));
    
    return { 
        type: 'generate-image', 
        prompt, 
        response: response?.substring(0, 500),
        downloaded 
    };
}

/**
 * 生成视频（文本描述转视频）
 */
async function actionGenerateVideo(page, prompt, outputDir) {
    console.log('\n=== 生成视频 ===');
    
    const videoPrompt = `请帮我生成一段视频：${prompt}。`;
    
    await sendMessage(page, videoPrompt);
    
    let downloaded = [];
    if (outputDir) {
        await page.waitForTimeout(5000); // 视频生成较慢
        downloaded = await downloadGeneratedVideos(page, outputDir);
        if (downloaded.length === 0) {
            // 也可能生成了图片，再试试图片
            downloaded = await downloadGeneratedImages(page, outputDir);
        }
    }
    
    const response = await getLastAIResponse(page);
    console.log('\n--- AI 回复摘要 ---');
    console.log((response || '无文本回复').substring(0, 300));
    
    return { 
        type: 'generate-video', 
        prompt, 
        response: response?.substring(0, 500),
        downloaded 
    };
}

/**
 * 图片转视频（指定本地图片路径）
 */
async function actionImageToVideo(page, imagePath, prompt, outputDir) {
    console.log('\n=== 图片转视频 ===');
    
    if (!fs.existsSync(imagePath)) {
        throw new Error(`图片文件不存在: ${imagePath}`);
    }
    
    // 点击上传按钮或找到图片转视频入口
    // 尝试找到豆包的图片转视频功能入口
    
    // 先发送提示引导
    const fullPrompt = `请将这张图片转换为视频${prompt ? `，${prompt}` : ''}`;
    
    // 查找上传按钮
    const uploadBtn = await findElement(page, [
        'button:has-text("上传")',
        'input[type="file"]',
        '[data-testid="upload"]',
        '.upload-btn',
    ], { timeout: 5000 });
    
    if (uploadBtn) {
        // 如果是 input[type=file]，设置文件
        const tagName = await uploadBtn.evaluate(el => el.tagName.toLowerCase());
        if (tagName === 'input') {
            await uploadBtn.setInputFiles(imagePath);
        } else {
            // 点击上传按钮，然后找文件输入
            await uploadBtn.click();
            await page.waitForTimeout(1000);
            const fileInput = await page.$('input[type="file"]');
            if (fileInput) {
                await fileInput.setInputFiles(imagePath);
            }
        }
    } else {
        // 如果没有上传按钮，尝试直接拖拽或使用文本提示
        console.log('  [提示] 未找到上传按钮，使用文本指令触发');
        await sendMessage(page, fullPrompt);
    }
    
    let downloaded = [];
    if (outputDir) {
        await waitForAIResponse(page);
        downloaded = await downloadGeneratedVideos(page, outputDir);
    }
    
    return { 
        type: 'image-to-video', 
        imagePath, 
        prompt, 
        downloaded 
    };
}

/**
 * 下载最近生成的内容
 */
async function actionDownloadLast(page, outputDir) {
    console.log('\n=== 下载最近生成的内容 ===');
    
    ensureOutputDir(outputDir);
    
    // 尝试下载视频
    const videos = await downloadGeneratedVideos(page, outputDir);
    
    // 尝试下载图片
    const images = await downloadGeneratedImages(page, outputDir);
    
    const all = [...videos, ...images];
    console.log(`\n共下载 ${all.length} 个文件`);
    all.forEach(f => console.log(`  ${f}`));
    
    return { type: 'download', files: all };
}

// ==================== 主函数 ====================

function parseArgs() {
    // 使用 Node.js 内置参数解析
    const argv = process.argv.slice(2);
    const args = {
        action: 'chat',
        prompt: '你好，请介绍一下你自己',
        output: path.join(process.cwd(), 'doubao-output'),
        port: CONFIG.cdpPort,
        image: '',
    };
    
    for (let i = 0; i < argv.length; i++) {
        let arg = argv[i];
        let val = undefined;
        
        // Handle --key=value format
        if (arg.startsWith('--') && arg.includes('=')) {
            const eqIdx = arg.indexOf('=');
            val = arg.slice(eqIdx + 1);
            arg = arg.slice(0, eqIdx);
        }
        
        if (arg === '--action' || arg === '-a') {
            args.action = val !== undefined ? val : (argv[++i] || args.action);
        } else if (arg === '--prompt' || arg === '-p') {
            args.prompt = val !== undefined ? val : (argv[++i] || args.prompt);
        } else if (arg === '--output' || arg === '-o') {
            args.output = val !== undefined ? val : (argv[++i] || args.output);
        } else if (arg === '--image' || arg === '-i') {
            args.image = val !== undefined ? val : (argv[++i] || args.image);
        } else if (arg === '--port') {
            args.port = parseInt(val !== undefined ? val : argv[++i]) || CONFIG.cdpPort;
        } else if (arg.startsWith('--') && val === undefined) {
            const key = arg.slice(2);
            const next = argv[i + 1];
            if (next && !next.startsWith('--')) { args[key] = next; i++; }
            else args[key] = true;
        } else if (arg.startsWith('--') && val !== undefined) {
            args[arg.slice(2)] = val;
        }
    }
    
    return args;
}

async function main() {
    const args = parseArgs();
    
    console.log('╔══════════════════════════════════╗');
    console.log('║   豆包自动化操作工具 v1.0       ║');
    console.log('║   基于 Playwright CDP + Edge    ║');
    console.log('╚══════════════════════════════════╝');
    console.log(`操作: ${args.action}`);
    console.log(`输出: ${args.output}`);
    console.log('');
    
    let browser = null;
    
    try {
        // 1. 连接 Edge
        browser = await connectToEdge(args.port);
        
        // 2. 获取豆包页面
        const page = await getDoubaoPage(browser);
        
        // 3. 执行操作
        let result;
        switch (args.action) {
            case 'chat':
                result = await actionChat(page, args.prompt);
                break;
                
            case 'generate-image':
                result = await actionGenerateImage(page, args.prompt, args.output);
                break;
                
            case 'generate-video':
                result = await actionGenerateVideo(page, args.prompt, args.output);
                break;
                
            case 'image-to-video':
                result = await actionImageToVideo(page, args.image, args.prompt, args.output);
                break;
                
            case 'download-last':
                result = await actionDownloadLast(page, args.output);
                break;
                
            default:
                console.error(`未知操作: ${args.action}`);
                console.log('支持的操作: chat, generate-image, generate-video, image-to-video, download-last');
                process.exit(1);
        }
        
        console.log('\n✅ 操作完成');
        console.log(JSON.stringify(result, null, 2));
        
        // 不关闭浏览器，保持连接
        // await browser.close();
        
    } catch (err) {
        console.error(`\n❌ 操作失败: ${err.message}`);
        console.error(err.stack);
        process.exit(1);
    }
}

main();
