#!/usr/bin/env node

const { chromium } = require('playwright');
const path = require('path');
const os = require('os');

const CDP_PORT = 18800;

// 平台配置
const PLATFORMS = {
  x: { name: "X/Twitter", container: 'article[data-testid="tweet"]', text: 'div[data-testid="tweetText"]', time: 'time[datetime]', accountBtn: 'button[data-testid="accountButton"], button[aria-label="Account menu"]', profileName: 'h1[data-testid="UserName"], h1', profileBio: '[data-testid="UserDescription"]', profileFollowers: 'a[href*="/verified_followers"]' },
  twitter: { name: "X/Twitter", container: 'article[data-testid="tweet"]', text: 'div[data-testid="tweetText"]', time: 'time[datetime]', accountBtn: 'button[data-testid="accountButton"], button[aria-label="Account menu"]', profileName: 'h1[data-testid="UserName"], h1', profileBio: '[data-testid="UserDescription"]', profileFollowers: 'a[href*="/verified_followers"]' },
  facebook: { name: "Facebook", container: 'div[role="article"], div[data-pagelet^="TimelineFeedUnit_"]', text: '[data-ad-preview], [data-testid="post_message"], .x1lliihq', time: 'time, abbr[title], span[data-utime]', accountBtn: 'button[aria-label*="個人檔案"], a[href*="/settings"]', profileName: 'h1, span[aria-label*="Profile"]', profileBio: '[data-testid="profile_bio"], div[data-biosignature]', profileFollowers: 'a[href*="/followers"]' }
};

function getUrl(platform, username) {
  if (platform === 'x' || platform === 'twitter') return `https://x.com/${username}`;
  if (platform === 'facebook' || platform === 'fb') return `https://www.facebook.com/${username}`;
  throw new Error('不支援的平台: ' + platform);
}

let browser, context, page, connectionMode;

async function ensure() {
  if (browser && context && page) return;
  
  try {
    browser = await chromium.connectOverCDP(`http://localhost:${CDP_PORT}`);
    const ctxs = browser.contexts();
    if (ctxs.length > 0) {
      context = ctxs[0];
      const pages = context.pages();
      page = pages[0] || await context.newPage();
      connectionMode = 'opencdl';
      console.log('✅ 連接到 OpenClaw Brave');
      return;
    }
  } catch (e) {}

  const userDataDir = path.join(os.homedir(), '.config', 'google-chrome');
  context = await chromium.launchPersistentContext(userDataDir, { 
    headless: false, 
    viewport: null, 
    executablePath: '/usr/bin/brave-browser', 
    args: ['--no-sandbox'] 
  });
  const pages = context.pages();
  page = pages[0] || await context.newPage();
  connectionMode = 'launch';
  console.log('✅ 啟動新的 Brave');
}

async function getLoginStatus(sel) {
  const btn = await page.$(sel.accountBtn);
  if (btn) {
    const text = await btn.innerText();
    if (text && text.trim()) return text.trim();
  }
  return '未檢測到登入';
}

async function getProfile(sel) {
  return {
    name: (await page.$(sel.profileName)) ? (await (await page.$(sel.profileName)).innerText()).trim() : null,
    bio: (await page.$(sel.profileBio)) ? (await (await page.$(sel.profileBio)).innerText()).trim() : null,
    followers: (await page.$(sel.profileFollowers)) ? (await (await page.$(sel.profileFollowers)).innerText()).trim() : null
  };
}

async function getPosts(sel, max, withStats) {
  await page.waitForSelector(sel.container, { timeout: 8000 }).catch(() => {});
  
  return await page.evaluate((params) => {
    const nodes = document.querySelectorAll(params.container);
    console.log(`[browser] 找到 ${nodes.length} 個帖子`);
    const res = [];
    nodes.forEach((post, i) => {
      if (i >= params.max) return;
      try {
        const txtEl = post.querySelector(params.text);
        const timeEl = post.querySelector(params.time);
        let text = null;
        if (txtEl) {
          const txt = txtEl.innerText;
          text = txt ? txt.trim() : null;
        }
        let time = null;
        if (timeEl) {
          const dt = timeEl.getAttribute('datetime') || timeEl.getAttribute('data-utime') || timeEl.getAttribute('title');
          time = dt ? dt.trim() : (timeEl.innerText ? timeEl.innerText.trim() : null);
        }
        const item = { time, text };
        if (params.withStats) {
          const getStat = (sel) => {
            const el = post.querySelector(sel);
            const val = el ? el.innerText : '';
            return val.trim() || null;
          };
          item.stats = {
            replies: getStat('[data-testid="comment"], .x1i10hfl'),
            shares: getStat('[data-testid="share"], .x1n2onr6'),
            likes: getStat('[data-testid="like"], [aria-label*="like"]')
          };
        }
        res.push(item);
      } catch (e) {}
    });
    return res;
  }, { ...sel, max, withStats });
}

async function braveBrowsePlatform(username, options = {}) {
  const platform = (options.platform || 'x').toLowerCase();
  const cfg = PLATFORMS[platform];
  if (!cfg) throw new Error(`不支援的平台: ${platform}。支援：x, twitter, facebook`);
  
  const max = options.maxPosts || options.maxTweets || 5;
  const withStats = options.includeStats !== false;

  console.log(`\n📘 提取 ${cfg.name} @${username}（最多 ${max} 篇）`);
  await ensure();

  const url = getUrl(platform, username);
  console.log(`🌐 ${url}`);
  try { await page.goto(url, { waitUntil: 'load', timeout: 15000 }); } catch (e) {}
  await page.waitForTimeout(platform === 'facebook' ? 4000 : 2000);

  const loginStatus = await getLoginStatus(cfg);
  console.log(`🔐 登入狀態: ${loginStatus}`);

  const posts = await getPosts(cfg, max, withStats);
  console.log(`✅ 提取 ${posts.length} 篇帖子`);

  const profile = await getProfile(cfg);

  return {
    username, platform, loginStatus, profile, posts,
    metadata: { maxPosts: max, includeStats: withStats, timestamp: new Date().toISOString(), connectionMode }
  };
}

// CLI
if (require.main === module) {
  let input = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', async () => {
    try {
      const opts = input ? JSON.parse(input) : {};
      const args = process.argv.slice(2);
      const username = opts.username || args[0];
      const platform = opts.platform || args[1] || 'x';
      const max = opts.maxPosts || opts.maxTweets || parseInt(args[2]) || 5;
      const stats = opts.includeStats !== undefined ? opts.includeStats : (args[3] !== 'false');

      if (!username) {
        console.error(JSON.stringify({ error: "缺少 username" }, null, 2));
        process.exit(1);
      }

      const result = await braveBrowsePlatform(username, { platform, maxPosts: max, includeStats: stats });
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    } catch (err) {
      console.error(JSON.stringify({ error: err.message }, null, 2));
      process.exit(1);
    }
  });
}

module.exports = { braveBrowsePlatform };
