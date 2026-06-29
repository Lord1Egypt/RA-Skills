/**
 * 知网检索结果页面 — 详情页访问与翻页模块（Node.js port）
 *
 * 元素定位（基于 2026-06-23 DOM 探测 + 唯一性验证 count 核对）
 * ----------------------------------------------------------
 *   标题链接   : <a class="fz14 inline" target="_blank" href=".../kcms2/article/abstract?v=...">
 *                选择器: a[href*="/kcms2/article/abstract"]
 *                【理由】用 href 业务签名定位，不用 CSS class。原因：
 *                  1) class="fz14 inline" 在 SPA hydration 中间态偶发只剩 "fz14"，sel #a.fz14.inline 会 0 命中
 *                  2) fz14 / inline 都是 CSS 钩子类（font-size / display），跨改版不稳定
 *                  3) href 路径 /kcms2/article/abstract 是 CNKI 内部 API 契约，跨代理稳定
 *                实测每页 20 个，与"业务基准集合"完全一致（无误抓）。
 *                详见 references/troubleshooting.md#BUG-002。
 *   下一页按钮 : <a id="PageNext" class="pagesnums" data-curpage="N">下一页</a>
 *                选择器: #PageNext（id 唯一）
 *                【注意】翻页控件按需生成，最后一页 #PageNext 不存在
 *
 * 公开 API
 * --------
 *   getTitleLinks(page)        返回当前页所有标题文字
 *   hasNextPage(page)          是否还有下一页
 *   visitOne(page, index)      访问当前页第 index 个（0-based），返回是否成功
 *   visitNPages(page, n)       从当前页起访问 n 个详情，自动翻页
 *
 * 所有操作后均加 waitForTimeout 留节奏，模拟真人操作。
 */

// ===================== 选择器 =====================
// 业务签名：标题链接的 href 一定包含 /kcms2/article/abstract（CNKI 内部 API 路径）
// 跨代理域名稳定、跨 CSS 改版稳定、SPA hydration 中间态也命中
const SEL_TITLE_LINK = 'a[href*="/kcms2/article/abstract"]';
const SEL_NEXT_PAGE  = '#PageNext';      // id 唯一；最后一页不存在

// ===================== 等待时长（毫秒）=====================
export const WAIT_AFTER_OPEN_DETAIL_MS = 600;    // 打开详情页后等加载
export const WAIT_AFTER_CLOSE_DETAIL_MS = 500;   // 关闭详情页后等结果页稳定
export const WAIT_AFTER_NEXT_PAGE_MS    = 1200;  // 翻页后等新结果页加载

// ===================== 底层 =====================
/**
 * 返回当前结果页所有标题文字（顺序 = 列表从上到下）。
 *
 * @param {import('playwright').Page} page
 * @returns {Promise<string[]>}
 */
export async function getTitleLinks(page) {
  const links = page.locator(SEL_TITLE_LINK);
  const count = await links.count();
  const out = [];
  for (let i = 0; i < count; i++) {
    const t = await links.nth(i).textContent();
    out.push((t ?? '').trim());
  }
  return out;
}

/**
 * 是否还有下一页（用 #PageNext 是否存在判断）。
 *
 * @param {import('playwright').Page} page
 * @returns {Promise<boolean>}
 */
export async function hasNextPage(page) {
  return (await page.locator(SEL_NEXT_PAGE).count()) > 0;
}

/**
 * 访问当前结果页的第 index 个标题（0-based）。
 *
 * @param {import('playwright').Page} page      当前结果页
 * @param {import('playwright').BrowserContext} context
 * @param {number} index   0-based 索引
 * @param {(detailPage: import('playwright').Page, title: string) => Promise<void>|void} [onDetail]
 *   可选回调；访问成功时调用，可读详情页信息
 * @returns {Promise<boolean>} True : 访问成功；False : 当前页没有这个 index（越界）或详情页加载失败
 */
export async function visitOne(page, context, index, onDetail) {
  const links = page.locator(SEL_TITLE_LINK);
  if (index >= (await links.count())) return false;

  const title = ((await links.nth(index).textContent()) ?? '').trim();

  let detailPage;
  try {
    // 标题链接 target="_blank"，点击会开新 tab；用 waitForEvent('page') 抓
    const [newPage] = await Promise.all([
      context.waitForEvent('page'),
      links.nth(index).click(),
    ]);
    detailPage = newPage;

    try {
      await detailPage.waitForLoadState('domcontentloaded', { timeout: 15_000 });
      await page.waitForTimeout(WAIT_AFTER_OPEN_DETAIL_MS);

      if (typeof onDetail === 'function') {
        await onDetail(detailPage, title);
      }
    } finally {
      await detailPage.close();
      await page.waitForTimeout(WAIT_AFTER_CLOSE_DETAIL_MS);
    }
  } catch {
    return false;
  }

  return true;
}

// ===================== 顶层 =====================
/**
 * 从当前结果页开始，访问前 n 个详情，自动翻页直到累计 n 次或没有更多结果。
 *
 * @param {import('playwright').Page} page      当前结果页
 * @param {number} n         要访问的总数
 * @param {(detailPage: import('playwright').Page, title: string) => Promise<void>|void} [onDetail]
 *   可选回调
 * @param {boolean} [verbose=true] 是否打印进度
 * @returns {Promise<number>} 实际访问成功的次数（可能 < n，如果总结果数不够）
 */
export async function visitNPages(page, n, onDetail, verbose = true) {
  if (n <= 0) return 0;

  // 等首个标题出现。href 锚点对 SPA hydration 中间态也命中，10s 已足够
  // （旧的 BUG-001 "30s 兜底轮询" 已删除 —— 根因是 class 抖动，现已用 href 锚点根治，
  //  详见 references/troubleshooting.md#BUG-002）
  await page.locator(SEL_TITLE_LINK).first().waitFor({ state: 'visible', timeout: 10_000 });

  let visited = 0;
  while (visited < n) {
    const links = page.locator(SEL_TITLE_LINK);
    const currentCount = await links.count();

    if (currentCount === 0) {
      if (verbose) console.log('  ⚠ 当前结果页没有可访问的标题，停止。');
      break;
    }

    // 本页要访问的条数
    const toVisit = Math.min(currentCount, n - visited);
    if (verbose) {
      console.log(`  📄 当前结果页共 ${currentCount} 条，本次访问 ${toVisit} 条`);
    }

    for (let i = 0; i < toVisit; i++) {
      // 注意：i 必须用基于"已访问过 + 剩余"的偏移；
      // 但本函数每访问一篇就 count++，下次循环还是从 0 开始（第 i 个 = 第 i+1 篇），
      // 因为详情页开新 tab，不影响结果页的链接顺序。
      const titles = await getTitleLinks(page);
      const titlePreview = (titles[i] ?? '').slice(0, 40);
      if (verbose) {
        console.log(`  · 访问第 ${visited + 1}/${n} 篇: ${titlePreview}…`);
      }
      if (await visitOne(page, page.context(), i, onDetail)) {
        visited++;
      } else {
        if (verbose) console.log(`    ⚠ 第 ${i + 1} 篇访问失败，跳过`);
        // 失败也继续往下
      }

      if (visited >= n) break;
    }

    if (visited >= n) break;

    // 本页访完，看是否需要翻页
    if (!(await hasNextPage(page))) {
      if (verbose) console.log('  📄 已是最后一页，停止翻页。');
      break;
    }

    if (verbose) console.log('  📄 点击「下一页」…');
    await page.locator(SEL_NEXT_PAGE).click();
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(WAIT_AFTER_NEXT_PAGE_MS);
  }

  return visited;
}
