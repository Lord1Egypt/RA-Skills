/**
 * 知网检索结果页面 — 筛选 & 排序操作模块（Node.js port）
 *
 * 元素定位（基于 2026-06-05 DOM 探测 + 唯一性验证 count=1）
 * --------------------------------------------------------
 *   筛选复选框 : <b>标题</b> → 最近 <dl> 容器 → <input value="...">
 *   排序按钮   : <ul id="orderList"> → <li id="FFD|PT|CF|DFR|ZH">
 *   排序状态   : 父级 <ul> 的 class 含 "DESC" / "ASC"，激活项 class="cur"
 *
 * 公开 API
 * --------
 *   filter(page, col, values)             批量勾选筛选项
 *   clickSort(page, sortName, target)     点排序（用按钮上的中文名）
 *   getCurrentSort(page)                  读当前排序状态
 */

// ===================== 编码映射 =====================
// 来源类别：中文名 → value（CNKI 后端编码，DOM 实测 2026-06-05）
export const SOURCE_TYPE_MAP = {
  '北大核心': 'P01',
  'WJCI':     'P12',
  'CSCD':     'P0210',
  'EI':       'P0202',
  'SCI':      'P0201',
  'CSSCI':    'P0209',
  'AMI':      'P13',
};

// 排序项 id → 中文名
export const SORT_FIELDS = {
  FFD: '相关度',     // 只能降序
  PT:  '发表时间',   // 可切
  CF:  '被引',       // 可切
  DFR: '下载',       // 可切
  ZH:  '综合',       // 只能降序
};

// 反向表：中文名 → id（clickSort 用）
export const SORT_NAME_TO_ID = Object.fromEntries(
  Object.entries(SORT_FIELDS).map(([k, v]) => [v, k])
);

// 哪些 col 需要"中文名 → value"翻译；其他 col 直接把传入值当 value
// （例如 "年度" 的 value 就是年份字符串本身，不需要翻译）
const TRANSLATIONS = {
  '来源类别': SOURCE_TYPE_MAP,
  // "年度": 留空，values 直接当 value 用（年份字符串）
};

// ===================== 等待时长（毫秒）=====================
export const WAIT_AFTER_CHECK_MS = 800;    // 勾选后等结果刷新
export const WAIT_AFTER_SORT_MS  = 500;    // 排序点击后等状态切换
export const WAIT_AFTER_EXPAND_MS = 500;   // 展开折叠分组后等 CSS 动画

// ===================== 内部辅助 =====================
function dlXpath(titleText) {
  /** 筛选项分组 dl 容器的 XPath。 */
  return (
    `xpath=//b[normalize-space(text())="${titleText}"]` +
    `/ancestor::dl[1]`
  );
}

function filterXpath(titleText, value) {
  /** 构造筛选项 checkbox 的 XPath。 */
  return (
    `xpath=//b[normalize-space(text())="${titleText}"]` +
    `/ancestor::dl[1]//input[@value="${value}"]`
  );
}

function ddXpath(titleText) {
  return (
    `xpath=//b[normalize-space(text())="${titleText}"]` +
    `/ancestor::dl[1]/dd`
  );
}

function arrowXpath(titleText) {
  return (
    `xpath=//b[normalize-space(text())="${titleText}"]` +
    `/parent::dt/i[contains(@class, "icon-arrow")]`
  );
}

/**
 * 检查分组是否处于折叠态（更严的判断）。
 *
 * 三种"看起来折叠"的实际状态都算折叠：
 *  1. display: none        —— 最常见
 *  2. visibility: hidden   —— 一些动画后会卡在这
 *  3. offsetHeight === 0   —— 父级 height:0 + overflow:hidden 也会让 checkbox 不可交互
 *
 * 为什么不直接看 dl class？因为知网 dl 的 class 命名（'is-up-fold off'）跟
 * 真实展开/折叠状态不直接对应；真正控制显示的是 <dd> 元素的 computed style。
 */
async function isFolded(page, groupTitle) {
  const dd = page.locator(ddXpath(groupTitle));
  if ((await dd.count()) === 0) return false;
  return await dd.evaluate(`el => {
    const s = getComputedStyle(el);
    return s.display === 'none'
        || s.visibility === 'hidden'
        || el.offsetHeight === 0;
  }`);
}

/**
 * 如果分组是折叠态，点击箭头 icon 展开，并等 <dd> 变可见。
 */
async function ensureExpanded(page, groupTitle) {
  if (!(await isFolded(page, groupTitle))) return;
  const arrow = page.locator(arrowXpath(groupTitle));
  if ((await arrow.count()) > 0) {
    await arrow.click();
    // 等 <dd> 真正变可见（display 不是 none）
    await page.locator(ddXpath(groupTitle)).waitFor({ state: 'visible', timeout: 3000 });
  }
}

/**
 * 内部用：勾选单个选项（先确保分组已展开）。
 */
async function checkOne(page, groupTitle, value) {
  await ensureExpanded(page, groupTitle);
  const cb = page.locator(filterXpath(groupTitle, value));
  // 等 input 真正可见/可交互（10s 比 Playwright 默认 30s 更早给出"卡哪"的反馈）
  try {
    await cb.waitFor({ state: 'visible', timeout: 10_000 });
  } catch (e) {
    // 给一个更可读的诊断
    const dd = page.locator(ddXpath(groupTitle));
    const ddDiag = await dd.evaluate(`el => {
      const s = getComputedStyle(el);
      return \`display=\${s.display} visibility=\${s.visibility} offsetHeight=\${el.offsetHeight} offsetParent=\${el.offsetParent?.tagName ?? 'null'}\`;
    }`).catch(() => '<无法读取>');
    throw new Error(
      `筛选项 ${groupTitle}=${value} 不可见: ${e.message}\n` +
      `    父 <dd> 状态: ${ddDiag}`
    );
  }
  if (!(await cb.isChecked())) {
    await cb.check();
    await page.waitForTimeout(WAIT_AFTER_CHECK_MS);
  }
}

// ===================== 公开 API：筛选 =====================
/**
 * 批量勾选筛选项。
 *
 * @param {import('playwright').Page} page
 * @param {string} col    筛选列名（页面上的分组标题），如 "来源类别" / "年度"
 * @param {string[]} values 选项列表
 *   - 若 col 在 TRANSLATIONS 中（如 "来源类别"）：传中文名
 *     filter 会查映射表转成 value
 *   - 否则：直接把 values 当 value 字符串（适合 "年度" 等）
 *
 * 异常
 * ----
 * 若 col 在 TRANSLATIONS 中、且 values 里出现未注册的中文名，抛 Error
 *
 * @example
 *   await filter(page, "来源类别", ["北大核心", "CSSCI"]);
 *   await filter(page, "年度", ["2023", "2024", "2025"]);
 */
export async function filter(page, col, values) {
  if (col in TRANSLATIONS) {
    const mapping = TRANSLATIONS[col];
    for (const v of values) {
      if (!(v in mapping)) {
        throw new Error(
          `${col} 选项 ${JSON.stringify(v)} 不在映射表中，可选: ${Object.keys(mapping)}`
        );
      }
      await checkOne(page, col, mapping[v]);
    }
  } else {
    // 未知 col：v 直接当 value 用（灵活支持未列出的分组）
    for (const v of values) {
      await checkOne(page, col, v);
    }
  }
}

// ===================== 公开 API：排序 =====================
/**
 * 点排序项，必要时二次点击切到目标升降序。
 *
 * @param {import('playwright').Page} page
 * @param {string} sortName 按钮上的中文名（不是 id）
 *   可选: "相关度" / "发表时间" / "被引" / "下载" / "综合"
 * @param {string} [target='DESC'] "DESC" 降序 ↓ | "ASC" 升序 ↑
 *
 * 注意
 * ----
 * "相关度" 和 "综合" 是 data-onlydesc="DESC"，只能降序；
 * 即便 target="ASC"，最终也只停留在降序。
 */
export async function clickSort(page, sortName, target = 'DESC') {
  if (!(sortName in SORT_NAME_TO_ID)) {
    throw new Error(
      `未知排序项 ${JSON.stringify(sortName)}，可选: ${Object.keys(SORT_NAME_TO_ID)}`
    );
  }
  const sortId = SORT_NAME_TO_ID[sortName];

  await page.locator(`#orderList > li#${sortId}`).click();
  await page.waitForTimeout(WAIT_AFTER_SORT_MS);

  const cls = (await page.locator('#orderList').getAttribute('class')) ?? '';
  if (!cls.toUpperCase().includes(target.toUpperCase())) {
    // 不在目标状态，再点一次切换
    await page.locator(`#orderList > li#${sortId}`).click();
    await page.waitForTimeout(WAIT_AFTER_SORT_MS);
  }
}

/**
 * 读当前排序状态。
 *
 * @returns {Promise<{field: string|null, order: 'DESC'|'ASC'|'?'}>}
 *   field : 当前激活的排序项 id（FFD | PT | CF | DFR | ZH）
 *   order : 'DESC' | 'ASC' | '?' （'?' 表示未识别，极少见）
 */
export async function getCurrentSort(page) {
  const cur = page.locator('#orderList li.cur');
  const field = (await cur.count()) ? await cur.getAttribute('id') : null;

  const cls = (await page.locator('#orderList').getAttribute('class')) ?? '';
  let order;
  if (cls.includes('ASC')) order = 'ASC';
  else if (cls.includes('DESC')) order = 'DESC';
  else order = '?';

  return { field, order };
}

// ===================== 独立调试入口 =====================
// 用 `node result_page_filters.js` 跑时打印编码映射速查
if (import.meta.url === `file:///${process.argv[1]?.replace(/\\/g, '/')}`) {
  console.log('=' .repeat(60));
  console.log('  result_page_filters — 编码映射速查');
  console.log('=' .repeat(60));
  console.log('  来源类别 SOURCE_TYPE_MAP（filter 传入 values 时用）：');
  for (const [k, v] of Object.entries(SOURCE_TYPE_MAP)) {
    console.log(`    ${v.padEnd(8)}  ${k}`);
  }
  console.log('');
  console.log('  排序 SORT_FIELDS（clickSort 传入 sortName 时用）：');
  for (const [name, sid] of Object.entries(SORT_NAME_TO_ID)) {
    console.log(`    ${name.padEnd(8)}  #${sid}`);
  }
  console.log('=' .repeat(60));
}
