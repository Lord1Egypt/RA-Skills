/**
 * 知网检索 + 筛选 + 排序 + 访问 + 下载 — 一站式 pipeline（Node.js port）
 *
 * 本模块是【对外唯一 API】，用户只需：
 *     import { runPipeline } from './cnki_pipeline.js';
 *     const result = await runPipeline({...});
 *
 * 内部使用 result_page_filters / result_page_navigator / pdf_downloader 三个模块。
 *
 * Config JSON Schema
 * ------------------
 * {
 *     "cnki_url":   str,              // 必填：知网入口 URL（从 user_config.json 注入）
 *     "keyword":    str,              // 必填：检索关键词
 *     "sort": {                       // 可选：排序设置
 *         "field": "发表时间" | "相关度" | "被引" | "下载" | "综合",
 *         "order": "DESC" | "ASC"
 *     },
 *     "filters": [                    // 可选：多个筛选条件
 *         {
 *             "col":   "来源类别" | "年度" | ...,
 *             "values": ["北大核心", "CSSCI"] | ["2024", "2025"]
 *         },
 *         ...
 *     ],
 *     "download_count": int           // 必填：>= 1，每次访问必下载
 * }
 *
 * 返回
 * ----
 * {
 *     "visited":    number,           // 实际访问的详情页数
 *     "downloaded": number,           // 实际下载成功的 PDF 数
 *     "errors":     string[],         // 错误信息列表
 *     "config":     object,           // 实际执行的 config（回显）
 * }
 *
 * 下载目录：固定为 ./download（自动创建）
 */

import path from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { chromium, errors } from 'playwright';
import { createInterface } from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';
// Playwright 1.40+ 不再顶层导出 TimeoutError，改放在 errors 命名空间下
const { TimeoutError: PWTimeout } = errors;

import * as rpf from './result_page_filters.js';
import { visitNPages } from './result_page_navigator.js';
import { downloadPdf } from './pdf_downloader.js';
import { ensureFiltersExpanded } from './cnki_filter_toggle.cjs'
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ===================== 路径与常量 =====================
const SCRIPT_DIR    = __dirname;
// 允许通过环境变量 CNKI_USER_DATA_DIR 指定外部 browser_data 目录，
// 用于跨脚本/跨项目共享登录态
// 不指定时使用本目录下的 browser_data/（独立 profile，需重新登录）
const USER_DATA_DIR =
  process.env.CNKI_USER_DATA_DIR
    ? path.resolve(process.env.CNKI_USER_DATA_DIR)
    : path.join(SCRIPT_DIR, 'browser_data');  // 持久化登录态
const DOWNLOAD_DIR  = path.join(SCRIPT_DIR, 'download');       // 固定下载目录

// CNKI_URL 在 runPipeline 中从 config 读取，并作为局部变量传下去

// ===================== 选择器 =====================
const SEL_SEARCH_INPUT  = '#txt_SearchText';   // 首页搜索框（textarea）
const SEL_SEARCH_BUTTON = '.search-btn';       // 首页检索按钮（div）
// 登录入口（未登录时**实际可见**；已登录时被 CSS 隐藏 display: none 或从 DOM 移除）
// 选择符说明：用 class（页面各只有一个 div），并用 onclick 属性加固，
// 这样不依赖按钮文本，避免 i18n / A/B 测试导致"div 在但内容不对"的误判
const SEL_ORG_LOGIN_BTN      = 'div.ecp_header_unit_loginbg[onclick*="showUnitLogin"]';
const SEL_PERSONAL_LOGIN_BTN = 'div.ecp_header_personal_loginbg[onclick*="showPersonalLogin"]';

// ===================== 等待配置 =====================
const LOGIN_WAIT_TIMEOUT_MS   = 300_000;   // 用户手动登录的最长等待（5 分钟）
const PAGE_LOAD_TIMEOUT_MS    = 20_000;    // 页面加载超时
const SEARCH_RETRY_MAX        = 3;         // 搜索被踢回登录页时的最大重试次数

// 人类节奏延迟（毫秒）
const HUMAN_DELAY_PAGE_LOAD    = [1_500, 2_500];
const HUMAN_DELAY_BEFORE_FILL  = [600,   1_200];
const HUMAN_DELAY_AFTER_FILL   = [400,   900];
const HUMAN_DELAY_BEFORE_CLICK = [500,   1_000];
const HUMAN_DELAY_AFTER_CLICK  = [800,   1_500];

// ===================== 内部辅助 =====================
function randInt(lo, hi) {
  return Math.floor(lo + Math.random() * (hi - lo + 1));
}

/** 模拟人类操作节奏的随机延迟。 */
async function humanDelay(page, hmin, hmax) {
  await page.waitForTimeout(randInt(hmin, hmax));
}

/**
 * 比较两个 URL 是否同源（hostname + protocol）。
 * 容忍末尾 / 的差异。
 */
function sameOrigin(a, b) {
  try {
    const ua = new URL(a);
    const ub = new URL(b);
    return ua.protocol === ub.protocol && ua.hostname === ub.hostname;
  } catch {
    return false;
  }
}

/**
 * 统一登录态判断。
 *
 * 触发条件：page.url() 包含 "cnki"（覆盖个人入口 www.cnki.net
 *           和各种高校代理入口）。
 *
 * 判断逻辑（用 display 状态）：
 *   - "机构登录"和"个人登录"两个 div **都实际可见**（bounding box width/height > 0） → 未登录
 *   - 任一不可见（display: none 或 div 被移除）→ 已登录
 *
 * 选符说明（不依赖文本）：
 *   - 主选 class：div.ecp_header_unit_loginbg / div.ecp_header_personal_loginbg
 *   - 加固属性：onclick*="showUnitLogin" / onclick*="showPersonalLogin"
 *   - 唯一性：cnki 主页上每个 class 只有一个 div（已用浏览器验证）
 *
 * 避免"网络延迟导致 div 还没加载"误判为已登录的策略：
 *   - 步骤 1：waitFor 两个 div 挂载到 DOM（短超时 3s）
 *   - 步骤 2：如果 3s 内没挂载，再等 1.5s 再 count() 一次
 *     - 持续缺失 → 真"已登录"（div 真的被移除）
 *     - 后来出现 → 之前是"加载慢"，继续走步骤 3
 *   - 步骤 3：读 boundingBox 判断可见性
 *     - 两个都 width/height > 0 → 未登录
 *     - 任一为 null 或 width/height = 0 → 已登录
 *
 * @param {import('playwright').Page} page
 * @returns {Promise<boolean>} true = 已登录，false = 未登录
 */
async function isLoggedIn(page) {
  if (!page.url().includes('cnki')) return false;

  const org = page.locator(SEL_ORG_LOGIN_BTN);
  const personal = page.locator(SEL_PERSONAL_LOGIN_BTN);

  // 步骤 1+2：等两个 div 挂载（带"二次确认"避免加载未完成误判）
  let attached = false;
  try {
    await Promise.all([
      org.first().waitFor({ state: 'attached', timeout: 3000 }),
      personal.first().waitFor({ state: 'attached', timeout: 3000 }),
    ]);
    attached = true;
  } catch {
    // 3s 内任一没挂载 → 等 1.5s 再确认一次
    await page.waitForTimeout(1500);
    const [oc, pc] = await Promise.all([org.count(), personal.count()]);
    if (oc === 0 || pc === 0) {
      return true; // 持续缺失 → 真"已登录"（div 真的从 DOM 移除）
    }
    // 1.5s 后出现了 → 之前是加载慢，继续走可见性判断
    attached = true;
  }

  if (!attached) return true;

  // 步骤 3：用 boundingBox 判断可见性
  //   - display: none → boundingBox() 返回 null
  //   - 父元素 display: none → boundingBox() 返回 null
  //   - 元素在视口外但渲染了 → boundingBox() 返回 {x, y, width, height}（width/height > 0）
  //   - 元素 width/height = 0 → boundingBox() 返回 {width: 0, height: 0, ...}
  const [orgBox, personalBox] = await Promise.all([
    org.first().boundingBox().catch(() => null),
    personal.first().boundingBox().catch(() => null),
  ]);

  const orgVisible = orgBox != null && orgBox.width > 0 && orgBox.height > 0;
  const personalVisible = personalBox != null && personalBox.width > 0 && personalBox.height > 0;

  // 两个都**实际可见**才视为未登录；任一不可见 = 已登录
  return !(orgVisible && personalVisible);
}

/** 等用户完成登录。扫描 context 里所有 tab，调 isLoggedIn 轮询。 */
async function waitForLogin(page, cnkiUrl) {
  const context = page.context();

  console.log('');
  console.log('⏳ ' + '=' .repeat(54));
  console.log('  检测到未登录，请在弹出的 Edge 浏览器中完成登录。');
  console.log(`  （最长等待 ${LOGIN_WAIT_TIMEOUT_MS / 1000} 秒）`);
  console.log('');
  console.log('  提示：');
  console.log('    · 一定要在 Playwright 打开的那个 Edge 窗口里登录');
  console.log('      （不是日常那个 Edge）');
  console.log('⏳ ' + '=' .repeat(54));
  console.log('');

  const startTime = Date.now();
  const pollMs = 3000;
  const REFRESH_COOLDOWN_MS = 20_000;   // 自动刷新冷却：避免打断用户输入
  let lastRefreshAt = 0;

  while (Date.now() - startTime < LOGIN_WAIT_TIMEOUT_MS) {
    // 扫描 context 里所有 tab，找已登录的那个
    const pages = context.pages();
    for (let i = 0; i < pages.length; i++) {
      const p = pages[i];
      try {
        if (await isLoggedIn(p)) {
          // 关闭多余 tab
          if (pages.length > 1) {
            for (let j = 0; j < pages.length; j++) {
              if (j !== i) {
                try { await pages[j].close(); } catch { /* noop */ }
              }
            }
          }
          console.log('✅ 登录完成，继续执行…');
          return p;
        }
      } catch {
        // 这个 tab 判断失败，继续看下一个
      }
    }

    // ===== 都没有已登录的 → 兜底刷新 =====
    const elapsed = Math.round((Date.now() - startTime) / 1000);

    // 兜底：单 tab + 在 cnki 域 + 冷却到了 → 自动 F5 一次
    if (pages.length === 1) {
      const url = pages[0].url();
      const onCnki = url.includes('cnki');
      const cooled = Date.now() - lastRefreshAt > REFRESH_COOLDOWN_MS;
      if (onCnki && cooled && elapsed > 15) {
        try {
          await pages[0].reload({ waitUntil: 'domcontentloaded' });
        } catch { /* noop */ }
        lastRefreshAt = Date.now();
      }
    }

    // 等一会儿再下一轮
    await new Promise((resolve) => setTimeout(resolve, pollMs));
  }

  // 超时
  const pages = context.pages();
  const finalDiags = [];
  for (let i = 0; i < pages.length; i++) {
    finalDiags.push(
      `  tab[${i}] url=${pages[i].url()}\n` +
      `            title=${(await pages[i].title().catch(() => '<无标题>')).slice(0, 50)}`
    );
  }
  throw new Error(
    `登录等待超时（${LOGIN_WAIT_TIMEOUT_MS / 1000} 秒）\n` +
    `  最后状态 (${pages.length} tabs):\n${finalDiags.join('\n')}\n` +
    `  可能原因：\n` +
    `    1) 登录到了错误的 Edge 窗口（不是 Playwright 开的那个）\n` +
    `    2) 登录完成后没刷新（CNKI / 代理入口登录后不会自动刷新主 tab）\n` +
    `    3) 代理入口需要 2FA / 验证码，未完成\n` +
    `    4) 浏览器被卡在第三方登录页（IdP / 统一认证）\n` +
    `    5) 登录成功但搜索框出现在 Playwright 上下文外的窗口（不可能）`
  );
}

/**
 * 登录态检测：统一判断 + 等待。
 * 通用实现（不区分 personnel / university），全部走 isLoggedIn。
 *
 * 注：isLoggedIn 内部已处理"页面加载未完成"的误判（3s 等 div 挂载 +
 *    1.5s 二次确认 + 文本验证），所以这里不用再 waitFor 搜索框。
 */
async function detectLoginState(page, cnkiUrl) {
  if (await isLoggedIn(page)) {
    console.log('      ✅ 已登录');
  } else {
    console.log('      ⏳ 未登录，等待用户完成登录…');
    page = await waitForLogin(page, cnkiUrl);
  }
  return page;
}

/**
 * 在知网首页输入关键词并点击检索按钮（人类节奏）。
 * 只负责"输入 + 点击"两步操作，不判断页面状态 —— 状态判定交给 waitForResultsOrLogin。
 *
 * @param {import('playwright').Page} page
 * @param {string} keyword
 */
async function performSearch(page, keyword) {
  await humanDelay(page, ...HUMAN_DELAY_BEFORE_FILL);
  await page.locator(SEL_SEARCH_INPUT).fill(keyword);
  await humanDelay(page, ...HUMAN_DELAY_AFTER_FILL);
  await humanDelay(page, ...HUMAN_DELAY_BEFORE_CLICK);
  await page.locator(SEL_SEARCH_BUTTON).click();
  await humanDelay(page, ...HUMAN_DELAY_AFTER_CLICK);
}

/**
 * 等点击检索后的页面跳到结果页。
 *
 * 判定逻辑（只信 URL）：
 *   - 等 URL 变成 /kns8s/**（最长 timeoutMs），成功 → 结果页
 *   - 超时 → URL 没变，被踢回登录页（或卡在首页/SSO 中转页）
 *
 * 不再做 isLoggedIn 二次校验：能进入 kns8s 就说明服务端接受了搜索请求；
 * 登录态判断交给外层 detectLoginState / waitForLogin 即可。
 *
 * @param {import('playwright').Page} page
 * @param {number} [timeoutMs=15_000]
 * @returns {Promise<'results' | 'login'>}
 */
async function waitForResultsOrLogin(page, timeoutMs = 15_000) {
  try {
    await page.waitForURL('**/kns8s/**', { timeout: timeoutMs });
    return 'results';
  } catch {
    return 'login';
  }
}

/**
 * 搜索封装：点击检索后，如果 URL 没在超时内跳到结果页（登录态失效被踢回登录页），
 * 自动调 waitForLogin 等待用户重新登录 + 再搜一次。最多重试 SEARCH_RETRY_MAX 次。
 *
 * 不再做 page.goto 回首页：
 *   - waitForLogin 返回的是登录完成后的 page
 *   - 下次 performSearch 找 #txt_SearchText，找不到会自然报错，错误信息清晰
 *
 * @param {import('playwright').Page} page
 * @param {string} keyword
 * @param {string} cnkiUrl
 * @param {number} [maxRetries=SEARCH_RETRY_MAX]
 * @returns {Promise<import('playwright').Page>} 落到结果页的 page 对象
 */
async function searchWithLoginRetry(page, keyword, cnkiUrl, maxRetries = SEARCH_RETRY_MAX) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    console.log(`      🔍 搜索尝试 ${attempt}/${maxRetries}: ${JSON.stringify(keyword)}`);

    await performSearch(page, keyword);
    const state = await waitForResultsOrLogin(page);

    if (state === 'results') {
      console.log('      ✅ 到达结果页');
      return page;
    }

    // URL 没跳 → 被踢回登录页（或卡住）
    console.log(`      ⚠ 搜索后 URL 未跳到结果页（登录态可能失效）`);

    if (attempt >= maxRetries) break;

    // waitForLogin 内部会打印"⏳ 检测到未登录…"那段提示语
    console.log(`      ⏳ 等待用户重新登录（第 ${attempt + 1}/${maxRetries} 次尝试）…`);
    page = await waitForLogin(page, cnkiUrl);
  }
  throw new Error(
    `搜索重试 ${maxRetries} 次后 URL 仍未跳到结果页，流程终止。\n` +
    `  可能原因：\n` +
    `    1) Cookie 被服务端强制清除（多端登录冲突 / 风控）\n` +
    `    2) 代理入口 IP 切换导致会话失效\n` +
    `    3) 登录账号本身过期 / 被踢出\n` +
    `    4) 登录后页面没回到带搜索框的首页，performSearch 找不到 #txt_SearchText\n` +
    `  建议：请在 Playwright 弹出的 Edge 窗口里手动重新登录，确认落在知网首页（带搜索框），再重跑。`
  );
}

/** 校验 config 必填项。 */
function validateConfig(config) {
  if (!config || typeof config !== 'object' || Array.isArray(config)) {
    throw new Error('config 必须是 object');
  }
  const cnkiUrl = config.cnki_url;
  if (!cnkiUrl || typeof cnkiUrl !== 'string') {
    throw new Error("config 必须包含 'cnki_url' (非空字符串，例: 'https://www.cnki.net/')");
  }
  try {
    // 顺手校验一下 URL 格式
    new URL(cnkiUrl);
  } catch (e) {
    throw new Error(`config['cnki_url'] 不是合法 URL: ${cnkiUrl}`);
  }
  const keyword = config.keyword;
  if (!keyword || typeof keyword !== 'string') {
    throw new Error("config 必须包含 'keyword' (非空字符串)");
  }
  const n = config.download_count;
  if (!Number.isInteger(n) || n < 1) {
    throw new Error("config 必须包含 'download_count' (integer >= 1)");
  }
  if (config.sort != null) {
    const s = config.sort;
    if (!s || typeof s !== 'object' || !('field' in s)) {
      throw new Error("config['sort'] 必须是 object 且包含 'field'");
    }
  }
  if (config.filters != null) {
    if (!Array.isArray(config.filters)) {
      throw new Error("config['filters'] 必须是 array");
    }
    for (let i = 0; i < config.filters.length; i++) {
      const f = config.filters[i];
      if (!f || typeof f !== 'object' || !('col' in f) || !('values' in f)) {
        throw new Error(
          `config['filters'][${i}] 必须是 object 且含 'col' 和 'values'`
        );
      }
    }
  }
}

// ===================== 对外 API =====================


/**
 * 一站式：根据 config 完成检索 + 筛选 + 排序 + 访问 + 下载。
 *
 * @param {object} config 见模块顶部 JSON Schema
 * @returns {Promise<{
 *   visited: number,
 *   downloaded: number,
 *   errors: string[],
 *   config: object,
 * }>}
 */
export async function runPipeline(config) {
  validateConfig(config);

  const keyword        = config.keyword;
  const sortCfg        = config.sort ?? null;
  const filtersCfg     = config.filters ?? [];
  const downloadCount  = config.download_count;
  const CNKI_URL       = config.cnki_url;

  // 启动前的目录
  await fs.mkdir(USER_DATA_DIR, { recursive: true });
  await fs.mkdir(DOWNLOAD_DIR,  { recursive: true });

  // 结果累计
  const result = {
    visited: 0,
    downloaded: 0,
    errors: [],
    config,
  };

  console.log('=' .repeat(60));
  console.log('  CNKI Pipeline 启动');
  console.log(`  CNKI_URL   : ${CNKI_URL}`);
  console.log('=' .repeat(60));
  console.log(`  关键词      : ${keyword}`);
  console.log(`  排序        : ${sortCfg || '默认'}`);
  console.log(`  筛选        : ${filtersCfg.length ? JSON.stringify(filtersCfg) : '无'}`);
  console.log(`  下载数      : ${downloadCount}`);
  console.log(`  browser_data: ${USER_DATA_DIR}`);
  console.log(`  下载目录    : ${DOWNLOAD_DIR}`);
  console.log('=' .repeat(60));

  const browser = await chromium.launchPersistentContext(USER_DATA_DIR, {
    headless: false,
    channel: 'msedge',
    viewport: { width: 1440, height: 900 },
    locale: 'zh-CN',
  });

  try {
    let page = browser.pages()[0] ?? (await browser.newPage());

    // ===== 1. 打开知网 =====
    console.log(`\n[1/5] 打开知网: ${CNKI_URL}`);
    await page.goto(CNKI_URL, { waitUntil: 'domcontentloaded', timeout: PAGE_LOAD_TIMEOUT_MS });
    await humanDelay(page, ...HUMAN_DELAY_PAGE_LOAD);

    // ===== 2. 检测登录态 =====
    console.log('[2/5] 检测登录态…');
    page = await detectLoginState(page, CNKI_URL);

    // ===== 3. 填词 + 检索（带登录态重试）=====
    console.log(`[3/5] 填入关键词并点击检索（带登录态重试）: ${JSON.stringify(keyword)}`);
    page = await searchWithLoginRetry(page, keyword, CNKI_URL);

    // ===== 4. 等结果页 DOM + 应用筛选 + 排序 =====
    console.log('[4/5] 等待结果页 DOM…');
    await page.waitForLoadState('domcontentloaded');

    // 等结果列表（AJAX 数据）渲染完成
    // waitForLoadState('domcontentloaded') 不够 —— 结果列表是异步加载的
    // 选择符用 href 锚点（业务签名），不用 class；详见 references/troubleshooting.md#BUG-002
    console.log('      等待结果列表…');
    try {
      await page.waitForSelector('a[href*="/kcms2/article/abstract"]', { timeout: 10_000 });
      console.log('      ✅ 结果列表已就绪');
    } catch {
      console.log('      ⚠ 10 秒内没等到结果列表（可能 0 结果或网络慢）');
    }

    // 应用筛选
    if (filtersCfg.length) {
      let groupitems = ['年度', '来源类别'];
      ensureFiltersExpanded(page,groupitems);
      console.log(`      应用 ${filtersCfg.length} 个筛选…`);
      for (const f of filtersCfg) {
        const { col, values } = f;
        try {
          await rpf.filter(page, col, values);
          console.log(`      · ${col} = ${JSON.stringify(values)}`);
        } catch (e) {
          const msg = `筛选 ${col}=${JSON.stringify(values)} 失败: ${e.message ?? e}`;
          console.log(`      ⚠ ${msg}`);
          result.errors.push(msg);
        }
      }
    }

    // 应用排序
    if (sortCfg) {
      const field = sortCfg.field;
      const order = (sortCfg.order ?? 'DESC').toUpperCase();
      try {
        await rpf.clickSort(page, field, order);
        console.log(`      · 排序: ${field} ${order}`);
      } catch (e) {
        const msg = `排序 ${field}/${order} 失败: ${e.message ?? e}`;
        console.log(`      ⚠ ${msg}`);
        result.errors.push(msg);
      }
    }
   
    // const rl = createInterface({ input, output });
    // const name = await rl.question('> ');
    // return
    // ===== 5. 访问 + 下载 N 篇 =====
    console.log(`[5/5] 访问 ${downloadCount} 个详情并下载 PDF…`);

    const onDetail = async (detailPage, title) => {
      result.visited += 1;
      const idx = result.visited;
      console.log(`      · [${idx}/${downloadCount}] 访问: ${title.slice(0, 50)}`);
      try {
        const savedPath = await downloadPdf(detailPage, DOWNLOAD_DIR);
        if (savedPath) {
          result.downloaded += 1;
          const stat = await fs.stat(savedPath);
          const sizeKb = stat.size / 1024;
          console.log(`        💾 ${path.basename(savedPath)} (${sizeKb.toFixed(0)} KB)`);
        } else {
          result.errors.push(`《${title}》下载返回 null`);
        }
      } catch (e) {
        const msg = `下载《${title}》失败: ${e.message ?? e}`;
        console.log(`        ⚠ ${msg}`);
        result.errors.push(msg);
      }
    };

    await visitNPages(page, downloadCount, onDetail);

  } catch (e) {
    if (e instanceof PWTimeout) {
      result.errors.push(`超时: ${e.message ?? e}`);
    } else {
      result.errors.push(`未预期错误: ${e?.name ?? 'Error'}: ${e?.message ?? e}`);
    }
  } finally {
    try {
      await browser.close();
    } catch {
      /* ignore */
    }
  }

  // 总结
  console.log('');
  console.log('=' .repeat(60));
  console.log('  ✅ Pipeline 完成');
  console.log(`  访问        : ${result.visited}/${downloadCount}`);
  console.log(`  下载成功    : ${result.downloaded}/${downloadCount}`);
  if (result.errors.length) {
    console.log(`  错误 (${result.errors.length}):`);
    for (const errMsg of result.errors) {
      console.log(`    - ${errMsg}`);
    }
  }
  console.log('=' .repeat(60));
  return result;
}
