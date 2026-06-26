#!/usr/bin/env node
/**
 * scraper-stealth.js - Playwright 隐身模式反爬虫抓取
 *
 * 核心特性：
 * - 隐藏 navigator.webdriver
 * - 随机真实 User-Agent（桌面 + 移动端）
 * - 随机延迟 1-3 秒模拟人类
 * - 随机视口大小
 * - 禁用 WebGL / Canvas 指纹
 * - 插件 & 语言伪装
 *
 * Usage:
 *   node scripts/scraper-stealth.js <URL> [options]
 *
 * Options:
 *   --wait <ms>          页面等待时间（默认 2000）
 *   --selector <css>     CSS 选择器精确提取
 *   --proxy <url>        代理地址
 *   --screenshot <path>  截图保存路径
 *   --html <path>        HTML 保存路径
 *   --cookie <json>      自定义 cookie（JSON 数组）
 *   --scroll             自动滚动加载
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ══════════════════════════════════════════════════════════
//  User-Agent 池 (12 个真实 UA，桌面 + 移动端)
// ══════════════════════════════════════════════════════════
const USER_AGENTS = [
  // Chrome Desktop (Windows)
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
  // Chrome Desktop (macOS)
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  // Firefox Desktop (Windows)
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
  // Firefox Desktop (macOS)
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0',
  // Safari Desktop (macOS)
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15',
  // Edge Desktop (Windows)
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
  // Chrome Mobile (Android)
  'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
  // Safari Mobile (iOS)
  'Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1',
  // Samsung Browser
  'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/26.0 Chrome/122.0.0.0 Mobile Safari/537.36',
  // Chrome Mobile (iOS)
  'Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/131.0.6778.103 Mobile/15E148 Safari/604.1',
  // Firefox Mobile (Android)
  'Mozilla/5.0 (Android 14; Mobile; rv:133.0) Gecko/133.0 Firefox/133.0',
];

// ══════════════════════════════════════════════════════════
//  桌面视口池
// ══════════════════════════════════════════════════════════
const VIEWPORTS = [
  { width: 1920, height: 1080 },
  { width: 1536, height: 864 },
  { width: 1440, height: 900 },
  { width: 1366, height: 768 },
  { width: 1280, height: 720 },
  { width: 1600, height: 900 },
  { width: 2560, height: 1440 },
  { width: 1280, height: 800 },
];

// 移动端视口
const MOBILE_VIEWPORTS = [
  { width: 412, height: 915 },
  { width: 390, height: 844 },
  { width: 360, height: 780 },
  { width: 414, height: 896 },
  { width: 375, height: 812 },
];

// ══════════════════════════════════════════════════════════
//  工具函数
// ══════════════════════════════════════════════════════════
function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randomDelay(min = 1000, max = 3000) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function isMobileUA(ua) {
  return /Mobile|Android|iPhone|iPad/i.test(ua);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ══════════════════════════════════════════════════════════
//  参数解析
// ══════════════════════════════════════════════════════════
function parseArgs(argv) {
  const args = argv.slice(2);
  const opts = {
    url: null,
    wait: 2000,
    selector: null,
    proxy: null,
    screenshot: null,
    html: null,
    cookie: null,
    scroll: false,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--wait':
        opts.wait = parseInt(args[++i], 10);
        break;
      case '--selector':
        opts.selector = args[++i];
        break;
      case '--proxy':
        opts.proxy = args[++i];
        break;
      case '--screenshot':
        opts.screenshot = args[++i];
        break;
      case '--html':
        opts.html = args[++i];
        break;
      case '--cookie':
        opts.cookie = args[++i];
        break;
      case '--scroll':
        opts.scroll = true;
        break;
      default:
        if (!args[i].startsWith('--') && !opts.url) {
          opts.url = args[i];
        }
    }
  }

  if (!opts.url) {
    console.error(
      'Usage: node scraper-stealth.js <URL> [--wait <ms>] [--selector <css>] [--proxy <url>] [--screenshot <path>] [--html <path>] [--cookie <json>] [--scroll]'
    );
    process.exit(1);
  }
  return opts;
}

// ══════════════════════════════════════════════════════════
//  反检测注入脚本
// ══════════════════════════════════════════════════════════
function getStealthScript(ua) {
  const hwConcurrency = pick([2, 4, 8, 12, 16]);
  const deviceMemory = pick([2, 4, 8]);
  const maxTouchPoints = isMobileUA(ua) ? pick([1, 5, 10]) : 0;
  const platform = isMobileUA(ua)
    ? ua.includes('iPhone')
      ? 'iPhone'
      : 'Linux armv81'
    : ua.includes('Mac')
    ? 'MacIntel'
    : 'Win32';

  return `
    // ─── 1. 隐藏 navigator.webdriver ───
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined,
      configurable: true,
    });

    // 删除 Playwright / Chromium 注入的标记
    delete window.__playwright;
    delete window.__pw_manual;
    delete window.__PW_inspect;

    // ─── 2. 伪造 navigator.plugins ───
    const fakePlugins = [
      { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format', length: 1 },
      { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: '', length: 1 },
      { name: 'Native Client', filename: 'internal-nacl-plugin', description: '', length: 2 },
    ];
    Object.defineProperty(navigator, 'plugins', {
      get: () => {
        const arr = fakePlugins;
        arr.length = fakePlugins.length;
        arr.item = (i) => fakePlugins[i] || null;
        arr.namedItem = (n) => fakePlugins.find((p) => p.name === n) || null;
        arr.refresh = () => {};
        return arr;
      },
      configurable: true,
    });

    // ─── 3. 伪造 navigator.languages ───
    Object.defineProperty(navigator, 'languages', {
      get: () => ['zh-CN', 'zh', 'en-US', 'en'],
      configurable: true,
    });
    Object.defineProperty(navigator, 'language', {
      get: () => 'zh-CN',
      configurable: true,
    });

    // ─── 4. 伪造 hardwareConcurrency & deviceMemory ───
    Object.defineProperty(navigator, 'hardwareConcurrency', {
      get: () => ${hwConcurrency},
      configurable: true,
    });
    Object.defineProperty(navigator, 'deviceMemory', {
      get: () => ${deviceMemory},
      configurable: true,
    });

    // ─── 5. 伪造 platform ───
    Object.defineProperty(navigator, 'platform', {
      get: () => '${platform}',
      configurable: true,
    });

    // ─── 6. 伪造 maxTouchPoints ───
    Object.defineProperty(navigator, 'maxTouchPoints', {
      get: () => ${maxTouchPoints},
      configurable: true,
    });

    // ─── 7. 禁用 WebGL 指纹 ───
    (function () {
      const getParameterOrig = WebGLRenderingContext.prototype.getParameter;
      WebGLRenderingContext.prototype.getParameter = function (param) {
        // UNMASKED_VENDOR_WEBGL
        if (param === 0x9245) return 'Intel Inc.';
        // UNMASKED_RENDERER_WEBGL
        if (param === 0x9246) return 'Intel Iris OpenGL Engine';
        return getParameterOrig.call(this, param);
      };
      if (typeof WebGL2RenderingContext !== 'undefined') {
        const getParameter2Orig = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function (param) {
          if (param === 0x9245) return 'Intel Inc.';
          if (param === 0x9246) return 'Intel Iris OpenGL Engine';
          return getParameter2Orig.call(this, param);
        };
      }
    })();

    // ─── 8. Canvas 指纹噪声 ───
    (function () {
      const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
      HTMLCanvasElement.prototype.toDataURL = function (type) {
        const ctx = this.getContext('2d');
        if (ctx) {
          const shift = Math.floor(Math.random() * 10) - 5;
          const style = ctx.fillStyle;
          ctx.fillStyle = 'rgba(' + shift + ',' + shift + ',' + shift + ',0.01)';
          ctx.fillRect(0, 0, 1, 1);
          ctx.fillStyle = style;
        }
        return origToDataURL.apply(this, arguments);
      };

      const origToBlob = HTMLCanvasElement.prototype.toBlob;
      HTMLCanvasElement.prototype.toBlob = function (cb, type, quality) {
        const ctx = this.getContext('2d');
        if (ctx) {
          const shift = Math.floor(Math.random() * 10) - 5;
          const style = ctx.fillStyle;
          ctx.fillStyle = 'rgba(' + shift + ',' + shift + ',' + shift + ',0.01)';
          ctx.fillRect(0, 0, 1, 1);
          ctx.fillStyle = style;
        }
        return origToBlob.apply(this, arguments);
      };

      // getImageData 噪声
      const origGetImageData = CanvasRenderingContext2D.prototype.getImageData;
      CanvasRenderingContext2D.prototype.getImageData = function () {
        const imageData = origGetImageData.apply(this, arguments);
        // 对少量像素加噪声
        for (let i = 0; i < Math.min(imageData.data.length, 40); i += 4) {
          imageData.data[i] = imageData.data[i] ^ (Math.random() > 0.5 ? 1 : 0);
        }
        return imageData;
      };
    })();

    // ─── 9. 修复 Permissions API ───
    if (navigator.permissions) {
      const origQuery = navigator.permissions.query;
      navigator.permissions.query = function (params) {
        if (params.name === 'notifications') {
          return Promise.resolve({ state: Notification.permission });
        }
        return origQuery.apply(this, arguments);
      };
    }

    // ─── 10. 隐藏 chrome 相关 ───
    if (!window.chrome) {
      window.chrome = {
        runtime: {
          onMessage: { addListener: function() {}, removeListener: function() {} },
          sendMessage: function() {},
          connect: function() { return { onMessage: { addListener: function() {} }, postMessage: function() {} }; },
        },
        loadTimes: function() { return {}; },
        csi: function() { return {}; },
      };
    }

    // ─── 11. 伪造 connection 信息 ───
    if (navigator.connection) {
      Object.defineProperty(navigator.connection, 'rtt', { get: () => ${pick([50, 100, 150, 200])} });
      Object.defineProperty(navigator.connection, 'downlink', { get: () => ${pick([1.5, 5, 10, 20])} });
      Object.defineProperty(navigator.connection, 'effectiveType', { get: () => '4g' });
    }
  `;
}

// ══════════════════════════════════════════════════════════
//  自动滚动
// ══════════════════════════════════════════════════════════
async function autoScroll(page) {
  await page.evaluate(async () => {
    await new Promise((resolve) => {
      let totalHeight = 0;
      const distance = 300 + Math.floor(Math.random() * 200);
      const timer = setInterval(() => {
        const scrollHeight = document.body.scrollHeight;
        window.scrollBy(0, distance);
        totalHeight += distance;
        if (totalHeight >= scrollHeight) {
          clearInterval(timer);
          resolve();
        }
      }, 200 + Math.floor(Math.random() * 300));
      // 最多滚动 30 秒
      setTimeout(() => {
        clearInterval(timer);
        resolve();
      }, 30000);
    });
  });
}

// ══════════════════════════════════════════════════════════
//  内容提取
// ══════════════════════════════════════════════════════════
async function extractContent(page, selector) {
  return page.evaluate((sel) => {
    const root = sel ? document.querySelector(sel) : document.body;
    if (!root) return { content: '', links: [], images: [] };

    const content = root.innerText || root.textContent || '';

    const linkEls = root.querySelectorAll('a[href]');
    const links = Array.from(linkEls)
      .map((a) => ({ text: (a.innerText || '').trim(), href: a.href }))
      .filter((l) => l.href && l.href.startsWith('http'))
      .slice(0, 200);

    const imgEls = root.querySelectorAll('img[src]');
    const images = Array.from(imgEls)
      .map((img) => ({ alt: img.alt || '', src: img.src }))
      .filter((i) => i.src)
      .slice(0, 100);

    return { content, links, images };
  }, selector);
}

async function extractMetadata(page) {
  return page.evaluate(() => {
    const getMeta = (name) => {
      const el =
        document.querySelector(`meta[name="${name}"]`) ||
        document.querySelector(`meta[property="${name}"]`) ||
        document.querySelector(`meta[property="og:${name}"]`);
      return el ? el.getAttribute('content') : '';
    };
    return {
      description: getMeta('description'),
      keywords: getMeta('keywords'),
      author: getMeta('author'),
      ogTitle: getMeta('og:title'),
      ogDescription: getMeta('og:description'),
      ogImage: getMeta('og:image'),
    };
  });
}

// ══════════════════════════════════════════════════════════
//  主流程
// ══════════════════════════════════════════════════════════
async function main() {
  const opts = parseArgs(process.argv);
  const startTime = Date.now();

  // 选择 UA 和视口
  const userAgent = pick(USER_AGENTS);
  const isMobile = isMobileUA(userAgent);
  const viewport = isMobile ? pick(MOBILE_VIEWPORTS) : pick(VIEWPORTS);

  // 构建启动选项
  const launchOpts = {
    headless: true,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--disable-features=IsolateOrigins,site-per-process',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--disable-gpu',
      '--no-first-run',
      '--no-zygote',
      '--disable-infobars',
      '--window-size=' + viewport.width + ',' + viewport.height,
    ],
  };

  if (opts.proxy) {
    launchOpts.proxy = { server: opts.proxy };
  }

  let browser;
  try {
    browser = await chromium.launch(launchOpts);

    const context = await browser.newContext({
      userAgent,
      viewport,
      locale: 'zh-CN',
      timezoneId: 'Asia/Shanghai',
      deviceScaleFactor: isMobile ? pick([2, 3]) : 1,
      isMobile,
      hasTouch: isMobile,
      javaScriptEnabled: true,
      ignoreHTTPSErrors: true,
    });

    // 注入反检测脚本（页面加载前执行）
    await context.addInitScript(getStealthScript(userAgent));

    // 注入 cookie
    if (opts.cookie) {
      try {
        const cookies = JSON.parse(opts.cookie);
        if (Array.isArray(cookies)) {
          await context.addCookies(cookies);
        }
      } catch (e) {
        console.error('Warning: Invalid cookie JSON:', e.message);
      }
    }

    const page = await context.newPage();

    // 随机延迟再导航（模拟人类）
    await sleep(randomDelay(500, 1500));

    // 导航
    await page.goto(opts.url, { waitUntil: 'domcontentloaded', timeout: 60000 });

    // 随机延迟
    await sleep(randomDelay(1000, 3000));

    // 等待
    if (opts.wait > 0) {
      await page.waitForTimeout(opts.wait);
    }

    // 自动滚动
    if (opts.scroll) {
      await autoScroll(page);
      await sleep(randomDelay(1000, 2000));
    }

    // 保存截图
    if (opts.screenshot) {
      const ssDir = path.dirname(path.resolve(opts.screenshot));
      if (!fs.existsSync(ssDir)) fs.mkdirSync(ssDir, { recursive: true });
      await page.screenshot({ path: opts.screenshot, fullPage: true });
    }

    // 保存 HTML
    if (opts.html) {
      const htmlDir = path.dirname(path.resolve(opts.html));
      if (!fs.existsSync(htmlDir)) fs.mkdirSync(htmlDir, { recursive: true });
      const htmlContent = await page.content();
      fs.writeFileSync(opts.html, htmlContent, 'utf-8');
    }

    // 提取内容
    const title = await page.title();
    const { content, links, images } = await extractContent(page, opts.selector);
    const metadata = await extractMetadata(page);

    const result = {
      success: true,
      url: opts.url,
      title,
      content: content.slice(0, 50000),
      links,
      images,
      metadata,
      stealth: {
        userAgent,
        viewport,
        isMobile,
        scrolled: opts.scroll,
      },
      elapsedSeconds: parseFloat(((Date.now() - startTime) / 1000).toFixed(2)),
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    const result = {
      success: false,
      url: opts.url,
      error: err.message,
      elapsedSeconds: parseFloat(((Date.now() - startTime) / 1000).toFixed(2)),
    };
    console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  } finally {
    if (browser) await browser.close();
  }
}

main();
