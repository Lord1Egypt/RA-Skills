/**
 * Binance Square Deep Scraper v4 — API Interception + Hashtag Drill
 *
 * Modes:
 *   node scrape-square.mjs                       # main feed (~200 posts)
 *   node scrape-square.mjs --scrolls 60          # more scrolls = more posts
 *   node scrape-square.mjs --coin RAVE           # drill into RAVE topic (200 posts)
 *   node scrape-square.mjs --coin RAVE --pages 20  # 20 pages = 400 posts
 *   node scrape-square.mjs --drill               # main feed + auto-drill top coins
 *   node scrape-square.mjs --drill --top 5       # drill top 5 mentioned coins
 *   node scrape-square.mjs --head                # visible browser
 */

import { writeFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

// puppeteer-core check with friendly error
let puppeteer;
try {
  puppeteer = (await import('puppeteer-core')).default;
} catch {
  console.error('ERROR: puppeteer-core is not installed.');
  console.error('Run: cd ~/.claude/skills/binance-square && npm install');
  process.exit(2);
}
import os from 'os';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── Cross-platform Chrome detection ─────────────────────────────
function findChrome() {
  if (process.env.CHROME_PATH && existsSync(process.env.CHROME_PATH)) {
    return process.env.CHROME_PATH;
  }
  const platform = os.platform();
  const candidates = {
    win32: [
      'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
      `${process.env.LOCALAPPDATA || ''}\\Google\\Chrome\\Application\\chrome.exe`,
      'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    ],
    darwin: [
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Chromium.app/Contents/MacOS/Chromium',
      '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    ],
    linux: [
      '/usr/bin/google-chrome',
      '/usr/bin/google-chrome-stable',
      '/usr/bin/chromium',
      '/usr/bin/chromium-browser',
      '/snap/bin/chromium',
    ],
  };
  for (const p of (candidates[platform] || [])) {
    if (p && existsSync(p)) return p;
  }
  try {
    const cmd = platform === 'win32' ? 'where chrome' : 'which google-chrome';
    const out = execSync(cmd, { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim().split('\n')[0];
    if (out && existsSync(out)) return out;
  } catch {}
  throw new Error('Chrome/Chromium not found. Install Chrome, or set CHROME_PATH env var.');
}

const CHROME_PATH = findChrome();

// ── CLI ─────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const flag = (name) => args.includes(name);
const opt = (name, fb) => { const i = args.indexOf(name); return i !== -1 && args[i + 1] ? args[i + 1] : fb; };

const scrollCount = Number(opt('--scrolls', '20'));
const coinMode = opt('--coin', null);
const hashtagPages = Number(opt('--pages', '10'));
const drillMode = flag('--drill');
const drillTop = Number(opt('--top', '3'));
const headless = !flag('--head');
const ts = new Date().toISOString().slice(0, 16).replace(/[T:]/g, '-');
const defaultName = coinMode ? `hashtag-${coinMode.toLowerCase()}-${ts}` : `square-${ts}`;
const outPath = resolve(opt('--out', resolve(__dirname, `${defaultName}.json`)));

// ── Tickers ─────────────────────────────────────────────────────
const KNOWN_TICKERS = new Set([
  'BTC','ETH','BNB','SOL','XRP','DOGE','ADA','AVAX','DOT','MATIC','POL',
  'LINK','UNI','AAVE','LTC','BCH','FIL','APT','ARB','OP','SUI',
  'TIA','SEI','JUP','WLD','PEPE','SHIB','FLOKI','WIF','BONK',
  'ORDI','STX','INJ','TRX','NEAR','ATOM','FTM','RUNE','ALGO',
  'SAND','MANA','AXS','ENJ','GALA','IMX','RAVE','FIDA','WLFI',
  'TON','NOT','DOGS','HMSTR','CATI','RENDER','FET','TAO','ONDO',
  'ENA','ETHFI','EIGEN','ZRO','W','DYM','STRK','PIXEL','PORTAL',
  'AI16Z','VIRTUAL','GRIFFAIN','GOAT','ACT','PNUT','USUAL',
]);

// Baseline coins to ignore in "anomaly" detection (always heavily discussed)
const BASELINE_COINS = new Set(['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'DOGE']);

// ── Helpers ─────────────────────────────────────────────────────
function classifyAuthor(authorName, username) {
  if (!authorName && !username) return 'UNKNOWN';
  if (/^Square-Creator-[a-f0-9]+$/i.test(username)) {
    if (authorName && authorName !== username && !/^Square-Creator-/i.test(authorName)) {
      return 'LIKELY_HUMAN';
    }
    return 'BOT_SUSPECT';
  }
  return 'LIKELY_HUMAN';
}

function extractCoins(text, coinPairList, tradingPairs) {
  const coins = new Set();
  if (coinPairList?.length) {
    for (const pair of coinPairList) {
      const m = pair.match(/\$?([A-Za-z]{2,12})/);
      if (m) coins.add(m[1].toUpperCase());
    }
  }
  if (tradingPairs?.length) {
    for (const tp of tradingPairs) {
      if (tp.code) coins.add(tp.code.toUpperCase());
    }
  }
  if (text) {
    for (const m of text.matchAll(/\$([A-Za-z]{2,12})/g)) coins.add(m[1].toUpperCase());
    for (const m of text.matchAll(/#([A-Za-z]{2,12})\b/g)) {
      const t = m[1].toUpperCase();
      if (KNOWN_TICKERS.has(t)) coins.add(t);
    }
  }
  return [...coins];
}

// ── Sentiment Analysis ──────────────────────────────────────────
const BULL_WORDS = [
  '做多','看涨','拉盘','起飞','暴涨','翻倍','抄底','梭哈','冲','多单',
  '买入','加仓','突破','利好','反弹','上涨','拉升','启动','牛市','底部',
  '入场','建仓','挂多','开多','马上拉','要涨','long','bullish','buy','moon',
  'pump','breakout','reversal','bottom','accumulate',
];
const BEAR_WORDS = [
  '做空','看跌','暴跌','爆仓','割肉','跑路','崩盘','砸盘','跌','空单',
  '卖出','减仓','破位','利空','下跌','瀑布','熊市','顶部','清仓','止损',
  '挂空','开空','被套','亏损','腰斩','归零','short','bearish','sell','dump',
  'crash','liquidat','rug','scam','诈骗','骗局',
];

function analyzeSentiment(text) {
  if (!text) return { score: 0, bull: 0, bear: 0, label: 'neutral' };
  const lower = text.toLowerCase();
  let bull = 0, bear = 0;
  for (const w of BULL_WORDS) if (lower.includes(w)) bull++;
  for (const w of BEAR_WORDS) if (lower.includes(w)) bear++;
  const score = bull - bear; // positive = bullish, negative = bearish
  const label = score > 0 ? 'bullish' : score < 0 ? 'bearish' : 'neutral';
  return { score, bull, bear, label };
}

function parseEngagement(n) {
  if (typeof n === 'number') return n;
  if (!n) return 0;
  const s = String(n).trim().toLowerCase().replace(/,/g, '');
  if (s.endsWith('k')) return Math.round(parseFloat(s) * 1000);
  if (s.endsWith('m')) return Math.round(parseFloat(s) * 1_000_000);
  return parseInt(s) || 0;
}

function transformVo(vo) {
  const authorName = vo.authorName || '';
  const username = vo.username || '';
  const content = vo.content || vo.title || '';
  return {
    id: vo.id,
    url: vo.webLink || `https://www.binance.com/zh-CN/square/post/${vo.id}`,
    content: content.slice(0, 500),
    authorName,
    username,
    authorType: classifyAuthor(authorName, username),
    authorVerified: vo.authorVerificationType === 1,
    authorRole: vo.authorRole,
    likes: parseEngagement(vo.likeCount),
    comments: parseEngagement(vo.commentCount),
    views: parseEngagement(vo.viewCount),
    shares: parseEngagement(vo.shareCount),
    quotes: parseEngagement(vo.quoteCount),
    date: vo.date ? new Date(vo.date).toISOString() : null,
    coins: extractCoins(content, vo.coinPairList, vo.tradingPairs),
    sentiment: analyzeSentiment(content),
    hashtags: (vo.hashtagList || []).map(h => h.name || h),
    hasImages: (vo.images || []).length > 0,
    hotComment: vo.hotComment?.content?.slice(0, 100) || null,
  };
}

function reclassifyBots(posts) {
  // Second-pass bot detection based on behavior patterns:
  // Rule 1: Default username + 3+ posts + avg views < 200 = BOT
  // Rule 2: Any author with 5+ posts + avg views < 100 = BOT (even custom username)
  const authorAgg = {};
  for (const p of posts) {
    const key = p.username || p.authorName;
    if (!key) continue;
    if (!authorAgg[key]) authorAgg[key] = { username: p.username, posts: 0, totalViews: 0 };
    authorAgg[key].posts++;
    authorAgg[key].totalViews += p.views;
  }

  const botUsernames = new Set();
  for (const [key, a] of Object.entries(authorAgg)) {
    const avgViews = a.posts > 0 ? a.totalViews / a.posts : 0;
    const isDefaultUsername = /^Square-Creator-/i.test(a.username);

    if (isDefaultUsername && a.posts >= 3 && avgViews < 200) {
      botUsernames.add(key);
    } else if (a.posts >= 5 && avgViews < 100) {
      botUsernames.add(key);
    }
  }

  let reclassified = 0;
  for (const p of posts) {
    const key = p.username || p.authorName;
    if (botUsernames.has(key) && p.authorType !== 'BOT_SUSPECT') {
      p.authorType = 'BOT_SUSPECT';
      reclassified++;
    }
  }

  if (reclassified > 0) {
    console.log(`  Bot reclassification: ${reclassified} posts from ${botUsernames.size} authors flagged`);
  }

  return posts;
}

function aggregate(posts) {
  // Reclassify bots before aggregating
  posts = reclassifyBots(posts);

  // Coin stats
  const coinStats = {};
  for (const post of posts) {
    for (const coin of post.coins) {
      if (!coinStats[coin]) {
        coinStats[coin] = {
          mentions: 0, botPosts: 0, humanPosts: 0, verifiedPosts: 0,
          totalLikes: 0, totalComments: 0, totalViews: 0,
          bullishPosts: 0, bearishPosts: 0, neutralPosts: 0, sentimentScore: 0,
          samplePosts: [],
        };
      }
      const s = coinStats[coin];
      s.mentions++;
      if (post.authorType === 'BOT_SUSPECT') s.botPosts++;
      else s.humanPosts++;
      if (post.authorVerified) s.verifiedPosts++;
      // Sentiment (only count human posts to avoid bot noise)
      if (post.authorType !== 'BOT_SUSPECT' && post.sentiment) {
        s.sentimentScore += post.sentiment.score;
        if (post.sentiment.label === 'bullish') s.bullishPosts++;
        else if (post.sentiment.label === 'bearish') s.bearishPosts++;
        else s.neutralPosts++;
      }
      s.totalLikes += post.likes;
      s.totalComments += post.comments;
      s.totalViews += post.views;
      if (s.samplePosts.length < 3) {
        s.samplePosts.push({
          author: post.authorName, type: post.authorType,
          content: post.content.slice(0, 80), views: post.views,
        });
      }
    }
  }
  const coinRanking = Object.entries(coinStats)
    .map(([coin, s]) => ({
      coin, mentions: s.mentions,
      botPct: s.mentions ? Math.round((s.botPosts / s.mentions) * 100) : 0,
      humanPosts: s.humanPosts, botPosts: s.botPosts, verifiedPosts: s.verifiedPosts,
      likes: s.totalLikes, comments: s.totalComments, views: s.totalViews,
      sentiment: {
        score: s.sentimentScore,
        bullish: s.bullishPosts, bearish: s.bearishPosts, neutral: s.neutralPosts,
        label: s.sentimentScore > 0 ? 'BULLISH' : s.sentimentScore < 0 ? 'BEARISH' : 'NEUTRAL',
      },
      samplePosts: s.samplePosts,
    }))
    .sort((a, b) => b.mentions - a.mentions);

  // Author stats
  const authorMap = {};
  for (const p of posts) {
    const key = p.username || p.authorName;
    if (!key) continue;
    if (!authorMap[key]) authorMap[key] = {
      name: p.authorName, username: p.username, type: p.authorType,
      verified: p.authorVerified, posts: 0, totalViews: 0,
    };
    authorMap[key].posts++;
    authorMap[key].totalViews += p.views;
  }
  const prolificAuthors = Object.values(authorMap)
    .filter(a => a.posts >= 2)
    .sort((a, b) => b.posts - a.posts);

  // Hashtags
  const hashtagMap = {};
  for (const p of posts) {
    for (const tag of p.hashtags) hashtagMap[tag] = (hashtagMap[tag] || 0) + 1;
  }
  const topHashtags = Object.entries(hashtagMap)
    .sort((a, b) => b[1] - a[1]).slice(0, 20)
    .map(([tag, count]) => ({ tag, count }));

  const summary = {
    totalPosts: posts.length,
    uniqueCoins: coinRanking.length,
    botSuspect: posts.filter(p => p.authorType === 'BOT_SUSPECT').length,
    likelyHuman: posts.filter(p => p.authorType === 'LIKELY_HUMAN').length,
    verified: posts.filter(p => p.authorVerified).length,
    botPct: posts.length
      ? Math.round((posts.filter(p => p.authorType === 'BOT_SUSPECT').length / posts.length) * 100) : 0,
    totalViews: posts.reduce((s, p) => s + p.views, 0),
    totalLikes: posts.reduce((s, p) => s + p.likes, 0),
    avgViewsPerPost: posts.length ? Math.round(posts.reduce((s, p) => s + p.views, 0) / posts.length) : 0,
  };

  return { summary, coinRanking, topHashtags, prolificAuthors };
}

function printSummary(label, summary, coinRanking, topHashtags, prolificAuthors) {
  const sep = '='.repeat(74);
  console.log(`\n${sep}`);
  console.log(`  ${label} — ${new Date().toISOString().slice(0, 16)}`);
  console.log(`  Posts: ${summary.totalPosts} | Human: ${summary.likelyHuman} | Bot: ${summary.botSuspect} (${summary.botPct}%) | Verified: ${summary.verified}`);
  console.log(`  Views: ${(summary.totalViews / 1000).toFixed(0)}K | Avg/post: ${(summary.avgViewsPerPost / 1000).toFixed(1)}K`);
  console.log(sep);

  if (coinRanking.length) {
    console.log(`\n  ${'Coin'.padEnd(12)} ${'Posts'.padEnd(7)} ${'Bot%'.padEnd(7)} ${'Sentiment'.padEnd(12)} ${'Views'.padEnd(10)} ${'Likes'.padEnd(7)}`);
    console.log(`  ${'-'.repeat(65)}`);
    for (const c of coinRanking.slice(0, 20)) {
      const v = c.views > 1000 ? `${(c.views / 1000).toFixed(1)}K` : String(c.views);
      const sn = c.sentiment;
      const arrow = sn.label === 'BULLISH' ? '+' + sn.score : sn.label === 'BEARISH' ? String(sn.score) : '0';
      const sentStr = `${sn.label.slice(0, 4)} ${arrow} (${sn.bullish}b/${sn.bearish}s)`;
      console.log(`  ${c.coin.padEnd(12)} ${String(c.mentions).padEnd(7)} ${(c.botPct + '%').padEnd(7)} ${sentStr.padEnd(12)} ${v.padEnd(10)} ${String(c.likes).padEnd(7)}`);
    }
  }

  if (topHashtags?.length) {
    console.log(`\n  Top Hashtags:`);
    for (const h of topHashtags.slice(0, 8)) console.log(`    #${h.tag} (${h.count})`);
  }

  if (prolificAuthors?.length) {
    console.log(`\n  Prolific Authors (2+ posts):`);
    for (const a of prolificAuthors.slice(0, 8)) {
      const v = a.totalViews > 1000 ? `${(a.totalViews / 1000).toFixed(0)}K` : String(a.totalViews);
      console.log(`    ${(a.name || '?').padEnd(20)} [${a.type}]${a.verified ? ' [V]' : ''}  ${a.posts}p, ${v} views`);
    }
  }
}

// ── Hashtag API Scraper ─────────────────────────────────────────
async function scrapeHashtag(page, coin, maxPages) {
  console.log(`\n  Drilling #${coin} (${maxPages} pages)...`);

  const allPosts = [];
  const seenIds = new Set();
  let hashtagInfo = null;

  for (let pi = 1; pi <= maxPages; pi++) {
    const result = await page.evaluate(async (hashtag, pageIndex) => {
      try {
        const url = `/bapi/composite/v4/friendly/pgc/content/queryByHashtag?hashtag=%23${hashtag}&pageIndex=${pageIndex}&pageSize=20&orderBy=HOT`;
        const res = await fetch(url);
        const json = await res.json();
        if (!json.data?.feedData) return { items: [], hashtag: null };

        const fd = json.data.feedData;
        const items = typeof fd === 'object' && !Array.isArray(fd)
          ? Object.keys(fd).filter(k => /^\d+$/.test(k)).map(k => fd[k])
          : (Array.isArray(fd) ? fd : []);

        return { items, hashtag: json.data.hashtag || null };
      } catch (e) {
        return { error: e.message, items: [] };
      }
    }, coin.toLowerCase(), pi);

    if (result.error) {
      console.log(`    Page ${pi}: ERROR - ${result.error}`);
      break;
    }

    if (pi === 1 && result.hashtag) {
      hashtagInfo = result.hashtag;
    }

    let newCount = 0;
    for (const vo of result.items) {
      if (vo.id && !seenIds.has(vo.id)) {
        seenIds.add(vo.id);
        allPosts.push(transformVo(vo));
        newCount++;
      }
    }

    if (pi % 5 === 0 || pi <= 2) {
      console.log(`    Page ${pi}/${maxPages}: +${newCount} (total: ${allPosts.length})`);
    }

    if (result.items.length === 0) {
      console.log(`    Page ${pi}: empty, stopping`);
      break;
    }

    // Small delay between pages
    await new Promise(r => setTimeout(r, 300 + Math.random() * 400));
  }

  console.log(`    #${coin} done: ${allPosts.length} posts`);
  return { posts: allPosts, hashtagInfo };
}

// ── Main Feed Scraper ───────────────────────────────────────────
async function scrapeMainFeed(page) {
  const allVos = [];
  const seenIds = new Set();
  let apiCallCount = 0;

  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('feed-recommend/list') && !url.includes('follow-feed')) {
      try {
        const json = await response.json();
        const vos = json.data?.vos || [];
        apiCallCount++;
        let newCount = 0;
        for (const vo of vos) {
          if (vo.id && !seenIds.has(vo.id)) {
            seenIds.add(vo.id);
            allVos.push(vo);
            newCount++;
          }
        }
        if (apiCallCount % 3 === 0 || apiCallCount <= 2) {
          console.log(`  API #${apiCallCount}: +${newCount} (total: ${allVos.length})`);
        }
      } catch {}
    }
  });

  console.log('Loading Binance Square main feed...');
  await page.goto('https://www.binance.com/zh-CN/square', {
    waitUntil: 'networkidle2', timeout: 30000,
  });
  await new Promise(r => setTimeout(r, 3000));
  console.log(`  Initial: ${allVos.length} posts`);

  console.log(`Scrolling ${scrollCount} times...`);
  for (let i = 0; i < scrollCount; i++) {
    await page.evaluate(() => window.scrollBy(0, window.innerHeight * 2));
    await new Promise(r => setTimeout(r, 1800 + Math.random() * 1200));
    if ((i + 1) % 5 === 0) {
      console.log(`  scroll ${i + 1}/${scrollCount} — collected: ${allVos.length}`);
    }
  }

  await new Promise(r => setTimeout(r, 3000));
  console.log(`Main feed: ${allVos.length} posts from ${apiCallCount} API calls`);

  return allVos.map(transformVo);
}

// ── Main ────────────────────────────────────────────────────────
async function main() {
  const mode = coinMode ? `coin: ${coinMode}` : drillMode ? 'feed + drill' : 'feed';
  console.log(`Binance Square Scraper v4 | mode: ${mode}`);

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--lang=zh-CN',
           '--disable-blink-features=AutomationControlled'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.setUserAgent(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  );
  await page.setExtraHTTPHeaders({ 'Accept-Language': 'zh-CN,zh;q=0.9' });

  let feedPosts = [];
  let drillResults = {};

  // ── Mode: Single coin hashtag ─────────────────────────────────
  if (coinMode) {
    // Load any binance page first to establish session
    await page.goto('https://www.binance.com/zh-CN/square', {
      waitUntil: 'networkidle2', timeout: 30000,
    });
    await new Promise(r => setTimeout(r, 2000));

    const { posts, hashtagInfo } = await scrapeHashtag(page, coinMode, hashtagPages);
    feedPosts = posts;

    if (hashtagInfo) {
      console.log(`\n  #${coinMode} stats: ${hashtagInfo.contentCount} total posts, ${hashtagInfo.viewCount} total views`);
    }
  }

  // ── Mode: Main feed (+ optional drill) ────────────────────────
  else {
    feedPosts = await scrapeMainFeed(page);

    // Auto-drill top mentioned coins
    if (drillMode) {
      const { coinRanking } = aggregate(feedPosts);
      // Pick top N non-baseline coins to drill
      const drillTargets = coinRanking
        .filter(c => !BASELINE_COINS.has(c.coin) && c.mentions >= 2)
        .slice(0, drillTop)
        .map(c => c.coin);

      if (drillTargets.length) {
        console.log(`\nDrilling into top coins: ${drillTargets.join(', ')}`);

        for (const coin of drillTargets) {
          const { posts, hashtagInfo } = await scrapeHashtag(page, coin, hashtagPages);
          drillResults[coin] = {
            posts: posts.length,
            hashtagInfo,
            ...aggregate(posts),
          };
        }
      }
    }
  }

  // ── Aggregate & report ────────────────────────────────────────
  const { summary, coinRanking, topHashtags, prolificAuthors } = aggregate(feedPosts);

  const report = {
    timestamp: new Date().toISOString(),
    mode: coinMode ? `hashtag:${coinMode}` : drillMode ? 'feed+drill' : 'feed',
    config: { scrollCount, hashtagPages, drillTop, headless },
    summary,
    coinRanking,
    topHashtags,
    prolificAuthors: prolificAuthors.slice(0, 30),
    drillResults: Object.fromEntries(
      Object.entries(drillResults).map(([coin, dr]) => [coin, {
        totalPosts: dr.posts,
        hashtagInfo: dr.hashtagInfo ? {
          contentCount: dr.hashtagInfo.contentCount,
          viewCount: dr.hashtagInfo.viewCount,
        } : null,
        summary: dr.summary,
        coinRanking: dr.coinRanking?.slice(0, 10),
        prolificAuthors: dr.prolificAuthors?.slice(0, 10),
      }])
    ),
    posts: feedPosts,
  };

  writeFileSync(outPath, JSON.stringify(report, null, 2));
  console.log(`\nSaved: ${outPath}`);

  // ── Print ─────────────────────────────────────────────────────
  const label = coinMode ? `#${coinMode} HASHTAG SCAN` : 'BINANCE SQUARE FEED';
  printSummary(label, summary, coinRanking, topHashtags, prolificAuthors);

  // Print drill results
  for (const [coin, dr] of Object.entries(drillResults)) {
    printSummary(
      `DRILL: #${coin} (${dr.hashtagInfo?.contentCount || '?'} total posts on topic)`,
      dr.summary, dr.coinRanking, null, dr.prolificAuthors
    );
  }

  console.log('');
  await browser.close();
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
