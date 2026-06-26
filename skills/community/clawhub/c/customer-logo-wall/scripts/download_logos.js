/**
 * download_logos.js
 * 用 playwright + 百度图片批量下载公司 Logo
 *
 * 用法：
 *   NODE_PATH=<node_modules路径> node download_logos.js \
 *     --output <logo输出目录> \
 *     --companies <公司JSON文件路径或JSON字符串>
 *
 * companies JSON 格式：
 *   [{"name": "公司中文名", "en": "English Name", "file": "output.png", "query": "搜索关键词(可选)"}]
 */

const { chromium } = require('playwright');
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// ── 命令行参数 ──────────────────────────────────────────────
const args = process.argv.slice(2);
function getArg(name) {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : null;
}

const outputDir = getArg('--output') || './logos/';
const companiesArg = getArg('--companies');
if (!companiesArg) {
  console.error('用法: node download_logos.js --output <目录> --companies <json文件或JSON字符串>');
  process.exit(1);
}

let companies;
try {
  if (fs.existsSync(companiesArg)) {
    companies = JSON.parse(fs.readFileSync(companiesArg, 'utf8'));
  } else {
    companies = JSON.parse(companiesArg);
  }
} catch (e) {
  console.error('无法解析 companies JSON：', e.message);
  process.exit(1);
}

fs.mkdirSync(outputDir, { recursive: true });

// ── 图片下载 ────────────────────────────────────────────────
function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    const file = fs.createWriteStream(dest);
    const req = protocol.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://image.baidu.com/',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
      },
      timeout: 20000
    }, (response) => {
      if ([301, 302].includes(response.statusCode)) {
        file.close();
        fs.unlink(dest, () => {});
        const loc = response.headers.location;
        if (loc && loc.startsWith('http')) return downloadFile(loc, dest).then(resolve).catch(reject);
        return reject(new Error('bad redirect'));
      }
      if (response.statusCode !== 200) {
        file.close(); fs.unlink(dest, () => {});
        return reject(new Error('HTTP ' + response.statusCode));
      }
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        const size = fs.statSync(dest).size;
        if (size < 1000) { fs.unlink(dest, () => {}); return reject(new Error(`文件太小(${size}b)`)); }
        resolve(dest);
      });
    });
    req.on('error', (e) => { file.close(); fs.unlink(dest, () => {}); reject(e); });
    req.on('timeout', () => { req.destroy(); file.close(); fs.unlink(dest, () => {}); reject(new Error('超时')); });
  });
}

// ── 百度图片搜索 ─────────────────────────────────────────────
async function searchBaidu(page, query) {
  const url = `https://image.baidu.com/search/index?tn=baiduimage&word=${encodeURIComponent(query)}`;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
  await page.waitForTimeout(3000);

  return page.evaluate(() => {
    const urls = new Set();
    document.querySelectorAll('[data-objurl]').forEach(el => {
      const u = el.getAttribute('data-objurl');
      if (u && u.startsWith('http') && !u.includes('baidu.com/img/')) urls.add(u);
    });
    document.querySelectorAll('img[data-src]').forEach(img => {
      const u = img.getAttribute('data-src');
      if (u && u.startsWith('http')) urls.add(u);
    });
    return [...urls].slice(0, 10);
  });
}

// ── Bing 图片搜索（备选，中文公司百度效果差时使用）──────────────
async function searchBing(page, query) {
  const url = `https://www.bing.com/images/search?q=${encodeURIComponent(query)}&qft=+filterui:imagesize-medium`;
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
  await page.waitForTimeout(3000);

  return page.evaluate(() => {
    const urls = new Set();
    document.querySelectorAll('a.iusc').forEach(el => {
      try {
        const m = JSON.parse(el.getAttribute('m') || '{}');
        if (m.murl && m.murl.startsWith('http')) urls.add(m.murl);
      } catch(e) {}
    });
    document.querySelectorAll('.mimg').forEach(img => {
      const src = img.getAttribute('src') || img.getAttribute('data-src');
      if (src && src.startsWith('http') && !src.includes('bing.com') && !src.includes('bing.net')) {
        urls.add(src);
      }
    });
    return [...urls].slice(0, 10);
  });
}

// ── 官网尝试 ─────────────────────────────────────────────────
async function tryOfficialSite(page, officialUrl, destPath) {
  try {
    await page.goto(officialUrl, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await page.waitForTimeout(2000);
    const logoEl = await page.$('header img, .logo img, [class*="logo"] img, nav img, #logo img');
    if (logoEl) {
      const src = await logoEl.getAttribute('src');
      if (src) {
        const fullUrl = src.startsWith('http') ? src : new URL(src, officialUrl).href;
        await downloadFile(fullUrl, destPath);
        return true;
      }
    }
  } catch (e) { /* 忽略 */ }
  return false;
}

// ── 主流程 ───────────────────────────────────────────────────
(async () => {
  console.log(`\n🚀 开始下载 ${companies.length} 个公司 Logo...\n`);

  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    viewport: { width: 1440, height: 900 },
    locale: 'zh-CN'
  });
  const page = await context.newPage();

  let success = 0;
  const failed = [];
  const results = [];

  for (const c of companies) {
    const destPath = path.join(outputDir, c.file);
    
    // 已存在则跳过
    if (fs.existsSync(destPath) && fs.statSync(destPath).size > 1000) {
      console.log(`✓ 已有: ${c.name}`);
      results.push({ ...c, status: 'exists' });
      success++;
      continue;
    }

    console.log(`\n搜索: ${c.name} (${c.en || ''})`);

    // 构造搜索词
    const query = c.query || `${c.name} ${c.en || ''} logo`;

    // 策略1：百度图片
    let ok = false;
    try {
      const urls = await searchBaidu(page, query);
      console.log(`  百度图片找到 ${urls.length} 个URL`);
      for (let i = 0; i < Math.min(urls.length, 6); i++) {
        try {
          await downloadFile(urls[i], destPath);
          console.log(`  ✅ 下载成功 (URL${i+1})`);
          ok = true;
          break;
        } catch (e) {
          console.log(`  ✗ URL${i+1}: ${e.message.slice(0, 60)}`);
        }
      }
    } catch (e) {
      console.log(`  百度搜索失败: ${e.message.slice(0, 60)}`);
    }

    // 策略2：官网
    if (!ok && c.official) {
      console.log(`  尝试官网: ${c.official}`);
      ok = await tryOfficialSite(page, c.official, destPath);
      if (ok) console.log(`  ✅ 官网下载成功`);
    }

    // 策略3：Bing 图片搜索（英文关键词，适合国际公司）
    if (!ok) {
      const bingQuery = c.en ? `${c.en} company logo PNG` : `${c.name} logo PNG`;
      try {
        const bingUrls = await searchBing(page, bingQuery);
        console.log(`  Bing找到 ${bingUrls.length} 个URL`);
        for (let i = 0; i < Math.min(bingUrls.length, 6); i++) {
          try {
            await downloadFile(bingUrls[i], destPath);
            console.log(`  ✅ Bing下载成功 (URL${i+1})`);
            ok = true;
            break;
          } catch (e) {
            console.log(`  ✗ Bing URL${i+1}: ${e.message.slice(0, 60)}`);
          }
        }
      } catch (e) {
        console.log(`  Bing搜索失败: ${e.message.slice(0, 60)}`);
      }
    }

    results.push({ ...c, status: ok ? 'success' : 'failed' });
    if (ok) success++; else failed.push(c.name);

    await page.waitForTimeout(800);
  }

  await browser.close();

  // 输出结果 JSON（供 verify_logos.py 使用）
  const resultsPath = path.join(outputDir, '_download_results.json');
  fs.writeFileSync(resultsPath, JSON.stringify(results, null, 2));

  console.log(`\n${'═'.repeat(40)}`);
  console.log(`✅ 成功: ${success}/${companies.length}`);
  if (failed.length > 0) console.log(`❌ 失败: ${failed.join(', ')}`);
  console.log(`结果已写入: ${resultsPath}`);
  console.log('═'.repeat(40));
})();
