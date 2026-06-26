import puppeteer from 'puppeteer';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
// 配置常量
export const CONFIG = {
    // 超时时间 (毫秒)
    TIMEOUTS: {
        LOGIN_POLL_INTERVAL: 5000, // 登录状态轮询间隔
        COOKIE_VALIDATION_WAIT: 3000, // Cookie 验证等待时间
        PAGE_LOAD_WAIT: 3000, // 页面加载等待时间
        MIN_UPLOAD_WAIT: 15000, // 最小上传等待时间
        FORM_SUBMIT_WAIT: 2000, // 表单提交后等待时间
        PUBLISH_WAIT: 3000, // 发布操作等待时间
        NAVIGATION_TIMEOUT: 30000, // 页面导航超时
        FILE_INPUT_TIMEOUT: 10000, // 文件输入框等待超时
        TITLE_INPUT_TIMEOUT: 5000, // 标题输入框等待超时
        COVER_WAIT: 5000, // 封面设置等待时间
    },
    // 上传等待时间计算 (基于文件大小)
    UPLOAD_WAIT_MULTIPLIER: 1024, // fileSize / UPLOAD_WAIT_MULTIPLIER = 额外等待毫秒数
};
export class DouyinUploader {
    cookiesPath;
    userDataDir;
    constructor() {
        this.cookiesPath = path.join(__dirname, 'douyin-cookies.json');
        this.userDataDir = path.join(__dirname, 'chrome-user-data');
    }
    async login(headless = false, timeout = 180000) {
        let browser = null;
        try {
            browser = await this.launchBrowser(headless);
            const page = await browser.newPage();
            // 访问抖音创作者平台
            await page.goto('https://creator.douyin.com', {
                waitUntil: 'domcontentloaded',
                timeout: CONFIG.TIMEOUTS.NAVIGATION_TIMEOUT
            });
            // 等待用户登录
            console.error('Waiting for user login...');
            const startTime = Date.now();
            while (Date.now() - startTime < timeout) {
                await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.LOGIN_POLL_INTERVAL));
                const currentUrl = page.url();
                const isLoggedIn = !currentUrl.includes('/login') &&
                    !currentUrl.includes('passport') &&
                    (currentUrl.includes('creator.douyin.com/creator') ||
                        currentUrl.includes('creator.douyin.com/home'));
                if (isLoggedIn) {
                    // 获取用户信息
                    const user = await this.getUserInfo(page);
                    // 保存cookies
                    const cookies = await page.cookies();
                    await fs.writeFile(this.cookiesPath, JSON.stringify(cookies, null, 2));
                    // Restrict cookie file permissions (owner read/write only)
                    await fs.chmod(this.cookiesPath, 0o600).catch(() => { });
                    await browser.close();
                    return {
                        success: true,
                        user,
                        cookieCount: cookies.length
                    };
                }
            }
            await browser.close();
            return {
                success: false,
                error: 'Login timeout'
            };
        }
        catch (error) {
            if (browser)
                await browser.close();
            return {
                success: false,
                error: error instanceof Error ? error.message : String(error)
            };
        }
    }
    async checkLogin(headless = true) {
        let browser = null;
        try {
            // 检查cookies文件
            const cookiesData = await fs.readFile(this.cookiesPath, 'utf-8');
            const cookies = JSON.parse(cookiesData);
            if (!cookies || cookies.length === 0) {
                return { isValid: false };
            }
            // 测试cookies
            browser = await this.launchBrowser(headless);
            const page = await browser.newPage();
            await page.setCookie(...cookies);
            await page.goto('https://creator.douyin.com', {
                waitUntil: 'networkidle2',
                timeout: CONFIG.TIMEOUTS.NAVIGATION_TIMEOUT
            });
            await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.COOKIE_VALIDATION_WAIT));
            const currentUrl = page.url();
            const isValid = !currentUrl.includes('login');
            let user = undefined;
            if (isValid) {
                user = await this.getUserInfo(page);
            }
            await browser.close();
            return { isValid, user };
        }
        catch (error) {
            if (browser)
                await browser.close();
            return { isValid: false };
        }
    }
    async uploadVideo(params) {
        let browser = null;
        try {
            // 验证视频文件
            const videoStats = await fs.stat(params.videoPath);
            if (!videoStats.isFile()) {
                throw new Error('Video file not found');
            }
            // 加载cookies
            const cookiesData = await fs.readFile(this.cookiesPath, 'utf-8');
            const cookies = JSON.parse(cookiesData);
            if (!cookies || cookies.length === 0) {
                throw new Error('No login cookies found. Please login first.');
            }
            // 启动浏览器
            browser = await this.launchBrowser(params.headless || false);
            const page = await browser.newPage();
            // 设置cookies
            await page.setCookie(...cookies);
            // 访问上传页面
            await page.goto('https://creator.douyin.com/creator-micro/content/upload', {
                waitUntil: 'networkidle2',
                timeout: CONFIG.TIMEOUTS.NAVIGATION_TIMEOUT
            });
            await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.PAGE_LOAD_WAIT));
            // 检查登录状态
            if (page.url().includes('login')) {
                await browser.close();
                throw new Error('Login expired. Please login again.');
            }
            // 上传视频
            const fileInput = await page.waitForSelector('input[type="file"]', {
                timeout: CONFIG.TIMEOUTS.FILE_INPUT_TIMEOUT,
                visible: false
            });
            if (!fileInput) {
                throw new Error('Upload input not found');
            }
            await fileInput.uploadFile(params.videoPath);
            // 等待上传
            const fileSize = videoStats.size;
            const waitTime = Math.max(CONFIG.TIMEOUTS.MIN_UPLOAD_WAIT, fileSize / CONFIG.UPLOAD_WAIT_MULTIPLIER);
            await new Promise(r => setTimeout(r, waitTime));
            // 填写标题
            try {
                await page.waitForSelector('input[placeholder*="标题"]', { timeout: CONFIG.TIMEOUTS.TITLE_INPUT_TIMEOUT });
                await page.click('input[placeholder*="标题"]');
                // 检测操作系统，使用正确的修饰键
                const isMac = process.platform === 'darwin';
                const modifierKey = isMac ? 'Meta' : 'Control';
                await page.keyboard.down(modifierKey);
                await page.keyboard.press('A');
                await page.keyboard.up(modifierKey);
                await page.keyboard.type(params.title);
            }
            catch (titleError) {
                // 备用方法：直接操作 DOM
                console.error('Title input via selector failed, trying fallback method:', titleError instanceof Error ? titleError.message : String(titleError));
                await page.evaluate((title) => {
                    const input = document.querySelector('input[type="text"]');
                    if (input) {
                        input.value = title;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }, params.title);
            }
            // 填写描述
            if (params.description) {
                try {
                    const descInput = await page.$('div[contenteditable="true"]');
                    if (descInput) {
                        await descInput.click();
                        await page.keyboard.type(params.description);
                    }
                }
                catch (descError) {
                    console.error('Failed to fill description:', descError instanceof Error ? descError.message : String(descError));
                }
            }
            // 添加标签
            if (params.tags && params.tags.length > 0) {
                const tagText = params.tags.map(tag => `#${tag}`).join(' ');
                try {
                    const descInput = await page.$('div[contenteditable="true"]');
                    if (descInput) {
                        await descInput.click();
                        await page.keyboard.type(' ' + tagText);
                    }
                }
                catch (tagError) {
                    console.error('Failed to add tags:', tagError instanceof Error ? tagError.message : String(tagError));
                }
            }
            await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.FORM_SUBMIT_WAIT));
            // 设置封面（必填项）
            await this.setCover(page);
            await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.FORM_SUBMIT_WAIT));
            // 发布
            let published = false;
            if (params.autoPublish !== false) {
                // 先检查发布按钮是否可用
                const publishButtonState = await page.evaluate(() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const publishBtn = buttons.find(btn => {
                        const text = btn.textContent?.trim() || '';
                        return text === '发布' || text === '立即发布';
                    });
                    if (!publishBtn)
                        return 'not_found';
                    if (publishBtn.disabled)
                        return 'disabled';
                    return 'enabled';
                });
                if (publishButtonState === 'disabled') {
                    // 发布按钮禁用，可能是封面未设置，再次尝试设置封面
                    console.error('⚠️  Publish button is disabled, retrying cover setup...');
                    await this.setCover(page);
                    await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.FORM_SUBMIT_WAIT));
                }
                published = await page.evaluate(() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const publishBtn = buttons.find(btn => {
                        const text = btn.textContent?.trim() || '';
                        return text === '发布' || text === '立即发布';
                    });
                    if (publishBtn && !publishBtn.disabled) {
                        publishBtn.click();
                        return true;
                    }
                    return false;
                });
                if (published) {
                    await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.PUBLISH_WAIT));
                    // 检查是否出现短信验证
                    const hasSmsVerification = await page.evaluate(() => {
                        const text = document.body.innerText || '';
                        return text.includes('短信验证') || text.includes('验证码') || text.includes('手机验证');
                    });
                    if (hasSmsVerification) {
                        console.error('\n📱 检测到短信验证页面');
                        // 尝试点击发送验证码按钮
                        const smsSent = await page.evaluate(() => {
                            const buttons = Array.from(document.querySelectorAll('button'));
                            const sendBtn = buttons.find(btn => {
                                const text = btn.textContent?.trim() || '';
                                return text.includes('发送') || text.includes('获取验证码') || text === '验证';
                            });
                            if (sendBtn && !sendBtn.disabled) {
                                sendBtn.click();
                                return true;
                            }
                            return false;
                        });
                        if (smsSent) {
                            console.error('✅ 已发送验证码到您的手机');
                        }
                        else {
                            console.error('ℹ️  验证码可能已发送，请查看手机');
                        }
                        // 无论是否成功点击发送按钮，都等待用户输入验证码
                        console.error('\n请输入收到的验证码：');
                        // 等待用户输入验证码
                        const readline = await import('readline');
                        const rl = readline.createInterface({
                            input: process.stdin,
                            output: process.stdout
                        });
                        const verifyCode = await new Promise((resolve) => {
                            rl.question('验证码: ', (answer) => {
                                rl.close();
                                resolve(answer.trim());
                            });
                        });
                        // 输入验证码
                        const codeInputs = await page.$$('input[type="text"], input[type="tel"], input[placeholder*="验证码"]');
                        if (codeInputs.length > 0) {
                            // 如果是多个输入框（每位一个框）
                            if (codeInputs.length === 6 || codeInputs.length === 4) {
                                for (let i = 0; i < verifyCode.length && i < codeInputs.length; i++) {
                                    await codeInputs[i].type(verifyCode[i]);
                                }
                            }
                            else {
                                // 单个输入框
                                await codeInputs[0].type(verifyCode);
                            }
                        }
                        // 点击确认按钮
                        await page.evaluate(() => {
                            const buttons = Array.from(document.querySelectorAll('button'));
                            const confirmBtn = buttons.find(btn => {
                                const text = btn.textContent?.trim() || '';
                                return text.includes('确认') || text.includes('确定') || text.includes('提交') || text === '验证';
                            });
                            if (confirmBtn && !confirmBtn.disabled) {
                                confirmBtn.click();
                            }
                        });
                        console.error('✅ 验证码已提交');
                        await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.PUBLISH_WAIT));
                        // 再次尝试发布
                        await page.evaluate(() => {
                            const buttons = Array.from(document.querySelectorAll('button'));
                            const publishBtn = buttons.find(btn => {
                                const text = btn.textContent?.trim() || '';
                                return text === '发布' || text === '立即发布' || text.includes('确认发布');
                            });
                            if (publishBtn && !publishBtn.disabled) {
                                publishBtn.click();
                            }
                        });
                        await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.PUBLISH_WAIT));
                    }
                    else {
                        // 处理普通确认弹窗
                        await page.evaluate(() => {
                            const confirmBtns = document.querySelectorAll('button');
                            for (const btn of confirmBtns) {
                                const text = btn.textContent || '';
                                if (text.includes('确认') || text.includes('确定')) {
                                    btn.click();
                                    return;
                                }
                            }
                        });
                    }
                    await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.PUBLISH_WAIT));
                }
            }
            await browser.close();
            return {
                success: true,
                title: params.title,
                published,
                status: published ? 'Published' : 'Draft saved'
            };
        }
        catch (error) {
            if (browser)
                await browser.close();
            return {
                success: false,
                error: error instanceof Error ? error.message : String(error)
            };
        }
    }
    async getCookiesInfo() {
        try {
            const cookiesData = await fs.readFile(this.cookiesPath, 'utf-8');
            const cookies = JSON.parse(cookiesData);
            const stats = await fs.stat(this.cookiesPath);
            return {
                exists: true,
                count: cookies.length,
                created: stats.mtime.toLocaleString()
            };
        }
        catch (error) {
            // Cookie 文件不存在是正常情况，不需要记录错误
            return { exists: false };
        }
    }
    async clearData() {
        try {
            await fs.unlink(this.cookiesPath);
        }
        catch (error) {
            // 文件不存在时忽略错误
            if (error.code !== 'ENOENT') {
                console.error('Failed to delete cookies file:', error instanceof Error ? error.message : String(error));
            }
        }
        try {
            await fs.rm(this.userDataDir, { recursive: true, force: true });
        }
        catch (error) {
            // 目录不存在时忽略错误
            if (error.code !== 'ENOENT') {
                console.error('Failed to delete user data directory:', error instanceof Error ? error.message : String(error));
            }
        }
    }
    async launchBrowser(headless) {
        const browser = await puppeteer.launch({
            headless,
            slowMo: headless ? 0 : 50,
            args: [
                '--window-size=1400,900',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--use-fake-ui-for-media-stream',
                '--use-fake-device-for-media-stream',
                '--disable-notifications'
            ],
            defaultViewport: headless ? { width: 1400, height: 900 } : null,
            userDataDir: this.userDataDir,
            ignoreDefaultArgs: ['--enable-automation']
        });
        // 设置默认权限
        if (!headless) {
            const context = browser.defaultBrowserContext();
            // Only request permissions needed for video upload workflow
            await context.overridePermissions('https://creator.douyin.com', [
                'clipboard-read',
                'clipboard-write'
            ]).catch((error) => {
                console.error('Failed to override permissions for creator.douyin.com:', error instanceof Error ? error.message : String(error));
            });
        }
        return browser;
    }
    async getUserInfo(page) {
        try {
            return await page.evaluate(() => {
                const selectors = ['.user-name', '.nickname', '[class*="username"]', '[class*="user"]'];
                for (const selector of selectors) {
                    const element = document.querySelector(selector);
                    if (element && element.textContent) {
                        return element.textContent.trim();
                    }
                }
                return 'User';
            });
        }
        catch (error) {
            console.error('Failed to get user info:', error instanceof Error ? error.message : String(error));
            return 'User';
        }
    }
    async setCover(page) {
        try {
            console.error('🖼️  Setting video cover...');
            // 等待视频处理完成，封面选项才会出现
            await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.PAGE_LOAD_WAIT));
            // 方法1：尝试点击"选择封面"按钮
            const coverSet = await page.evaluate(() => {
                // 查找封面相关的按钮或链接
                const selectors = [
                    'button:has-text("选择封面")',
                    'button:has-text("设置封面")',
                    'span:has-text("选择封面")',
                    '[class*="cover"] button',
                    '[class*="Cover"] button',
                    'div[class*="cover-select"]',
                    'div[class*="coverSelect"]'
                ];
                // 查找包含"封面"文字的可点击元素
                const allElements = document.querySelectorAll('button, span, div[role="button"], a');
                for (const el of allElements) {
                    const text = el.textContent?.trim() || '';
                    if (text.includes('选择封面') || text.includes('设置封面') || text.includes('更换封面')) {
                        el.click();
                        return 'clicked_cover_button';
                    }
                }
                return 'no_cover_button';
            });
            if (coverSet === 'clicked_cover_button') {
                await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.FORM_SUBMIT_WAIT));
                // 等待封面选择弹窗出现，然后选择第一个推荐封面或视频帧
                const coverSelected = await page.evaluate(() => {
                    // 查找封面选择弹窗中的封面选项
                    const coverOptions = document.querySelectorAll('[class*="cover-item"], [class*="coverItem"], [class*="frame-item"], [class*="frameItem"], ' +
                        '[class*="cover"] img, [class*="Cover"] img, [class*="thumbnail"], ' +
                        'div[class*="cover-select"] img, div[class*="cover-list"] > div');
                    if (coverOptions.length > 0) {
                        // 点击第一个封面选项
                        coverOptions[0].click();
                        return 'selected_cover';
                    }
                    // 尝试查找并点击"使用当前帧"或类似按钮
                    const frameButtons = document.querySelectorAll('button, span');
                    for (const btn of frameButtons) {
                        const text = btn.textContent?.trim() || '';
                        if (text.includes('当前帧') || text.includes('使用此帧') || text.includes('截取封面')) {
                            btn.click();
                            return 'used_current_frame';
                        }
                    }
                    return 'no_cover_options';
                });
                if (coverSelected !== 'no_cover_options') {
                    await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.FORM_SUBMIT_WAIT));
                    // 点击确认按钮
                    await page.evaluate(() => {
                        const confirmButtons = document.querySelectorAll('button');
                        for (const btn of confirmButtons) {
                            const text = btn.textContent?.trim() || '';
                            if (text === '确定' || text === '确认' || text === '完成' || text.includes('使用')) {
                                btn.click();
                                return;
                            }
                        }
                    });
                    console.error('✅ Cover set successfully');
                    return true;
                }
            }
            // 方法2：尝试直接点击封面区域触发选择
            const directCoverClick = await page.evaluate(() => {
                // 查找封面预览区域
                const coverAreas = document.querySelectorAll('[class*="cover-preview"], [class*="coverPreview"], ' +
                    '[class*="cover-container"], [class*="coverContainer"], ' +
                    '[class*="cover-wrap"], [class*="coverWrap"], ' +
                    'div[class*="cover"]:has(img)');
                for (const area of coverAreas) {
                    const rect = area.getBoundingClientRect();
                    if (rect.width > 50 && rect.height > 50) {
                        area.click();
                        return 'clicked_cover_area';
                    }
                }
                return 'no_cover_area';
            });
            if (directCoverClick === 'clicked_cover_area') {
                await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.FORM_SUBMIT_WAIT));
                // 尝试选择第一个可用封面
                await page.evaluate(() => {
                    const options = document.querySelectorAll('[class*="cover"] img, [class*="frame"] img');
                    if (options.length > 0) {
                        options[0].click();
                    }
                });
                await new Promise(r => setTimeout(r, CONFIG.TIMEOUTS.FORM_SUBMIT_WAIT));
                // 确认选择
                await page.evaluate(() => {
                    const buttons = document.querySelectorAll('button');
                    for (const btn of buttons) {
                        const text = btn.textContent?.trim() || '';
                        if (text === '确定' || text === '确认' || text === '完成') {
                            btn.click();
                            return;
                        }
                    }
                });
                console.error('✅ Cover set via direct click');
                return true;
            }
            // 方法3：检查是否已有默认封面（有些情况下会自动选择）
            const hasDefaultCover = await page.evaluate(() => {
                const coverImages = document.querySelectorAll('[class*="cover"] img, [class*="Cover"] img');
                for (const img of coverImages) {
                    const src = img.src;
                    if (src && !src.includes('placeholder') && !src.includes('default')) {
                        return true;
                    }
                }
                return false;
            });
            if (hasDefaultCover) {
                console.error('✅ Default cover already set');
                return true;
            }
            console.error('⚠️  Could not auto-set cover, may need manual selection');
            return false;
        }
        catch (error) {
            console.error('Failed to set cover:', error instanceof Error ? error.message : String(error));
            return false;
        }
    }
}
//# sourceMappingURL=douyin-uploader.js.map