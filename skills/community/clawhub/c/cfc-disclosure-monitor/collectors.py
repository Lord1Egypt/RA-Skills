# collectors.py — 消金信披 Phase-1 采集方法（按架构模式分组）
"""
注册机制：
  所有函数以 collect_<name> 命名，自动注册到 COLLECTORS 字典。
  方法派发：run_company() 根据 companies.json 中的 method 字段查表。

架构分组：
  GROUP_A  — 静态 HTML，滚动即可（无翻页）
  GROUP_B  — 翻页型，通用下一页按钮
  GROUP_C  — 首页滚动（JS动态加载）
  GROUP_D  — 详情页 URL 可枚举（从列表页提取 ID 构造）
  GROUP_E  — Vue / Element UI / 各类 JS 框架
  GROUP_F  — 多 Tab / 多栏
  GROUP_G  — 特殊格式（日期分两行、PDF附件等）
  GROUP_H  — WSL2 受限（需特殊处理）
"""
import asyncio
import json
import re
import uuid
from pathlib import Path
from typing import Callable

from core import extract_from_text, classify, normalize_date

# ─── 注册表 ──────────────────────────────────────────────────────────────────
COLLECTORS: dict[str, Callable] = {}

def collector(name: str) -> Callable:
    """装饰器：注册采集方法"""
    def decor(fn: Callable) -> Callable:
        COLLECTORS[name] = fn
        for alias in name.split("|"):
            COLLECTORS[alias.strip()] = fn
        return fn
    return decor


# ════════════════════════════════════════════════════════════════════════════════
# GROUP_A — 静态 HTML（滚动提取，无翻页）
# ════════════════════════════════════════════════════════════════════════════════

@collector("html_dom")
@collector("html_dom")
async def collect_html_dom(page, url: str) -> list:
    """静态HTML：提取公告详情URL + 正文，同步完成 Phase 1+2。

    改进：从列表页提取 .shtml/.pdf/PXXXXXXXX 等真实详情页URL，
          用真实URL替换列表页URL，让 Phase 2 能正确抓取详情页正文。
    """
    import re
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)

    # ── 提取详情页 URL ───────────────────────────────────────────────
    detail_links = await page.evaluate("""
() => {
    const results = [];
    const baseDomain = window.location.hostname;
    document.querySelectorAll('a[href]').forEach(a => {
        const href = a.href;
        if (!href || href === '#' || href.includes('javascript:')) return;
        // 过滤备案/广告/外部政府链接
        if (href.includes('beian.gov.cn')) return;
        if (href.includes('gov.cn') && !href.match(/cfcnb/i)) return;
        const txt = a.innerText.trim();
        // 过滤导航/版权/产品链接
        if (!txt || txt.length < 3) return;
        const navWords = ['首页','关于我们','联系我们','加入我们','产品介绍','新闻动态','重要公告','公告查询','Copyright','网站地图','人才招聘','商务合作'];
        if (navWords.some(w => txt.includes(w)) && txt.length < 15) return;
        // 匹配详情页：.shtml .html .htm .pdf 或含日期路径
        const isDetail = href.match(/\.(shtml|html|htm|pdf)$/i) ||
                         href.match(/\/\d{8,10}\//) ||
                         href.match(/\/P0\d{10,}/) ||
                         (href.match(/\d{6,}/) && !href.includes('/css/') && !href.includes('/js/') && !href.includes('/images/'));
        if (isDetail) {
            results.push({ href, text: txt.substring(0, 200) });
        }
    });
    // 去重
    const seen = new Set();
    return results.filter(r => {
        if (seen.has(r.href)) return false;
        seen.add(r.href);
        return true;
    });
}
    """)

    # ── 构建公告列表 ───────────────────────────────────────────────
    url_to_info = {}
    for link in (detail_links or []):
        href = link["href"]
        txt = link["text"]
        # 提取日期：优先从URL路径匹配 /YYYYMMDD/ 或 /YYYY-MM-DD/
        date_str = ""
        date_m = re.search(r"/(\d{4})(\d{2})(\d{2})/", href)
        if date_m:
            try:
                date_str = f"{date_m.group(1)}-{date_m.group(2)}-{date_m.group(3)}"
            except Exception:
                pass
        # 也匹配 P0XXXXXXXXXXXXXXXX 格式（日期在文件名中）
        if not date_str:
            date_m2 = re.search(r"/P0(\d{4})(\d{2})(\d{2})\d+", href)
            if date_m2:
                try:
                    date_str = f"{date_m2.group(1)}-{date_m2.group(2)}-{date_m2.group(3)}"
                except Exception:
                    pass
        url_to_info[href] = {"title": txt, "date": date_str or "1970-01-01"}

    # ── 如果找到详情URL ─────────────────────────────────────────────
    if url_to_info:
        items = []
        for detail_url, info in url_to_info.items():
            items.append({
                "title": info["title"],
                "date": info["date"],
                "url": detail_url,
                "category": classify(info["title"]),
            })
        print(f"  html_dom: 提取{len(items)}条真实详情URL", flush=True)
        return items

    # ── 没有详情URL，退化为纯列表提取 ─────────────────────────────
    print("  html_dom: 未找到详情URL，退化为列表提取", flush=True)
    for _ in range(6):
        await page.evaluate("window.scrollBy(0, 600)")
        await asyncio.sleep(0.4)
    text = await page.evaluate("document.body.innerText")
    return extract_from_text(text, url)


@collector("cdp_rpa")
async def collect_cdp_rpa(page, url: str) -> list:
    """大量滚动（15次）用于慢加载页面"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)
    for _ in range(15):
        await page.evaluate("window.scrollBy(0, 400)")
        await asyncio.sleep(0.5)
    text = await page.evaluate("document.body.innerText")
    return extract_from_text(text, url)


# ════════════════════════════════════════════════════════════════════════════════
# GROUP_B — 翻页型
# ════════════════════════════════════════════════════════════════════════════════

@collector("paginated")
async def collect_paginated(page, url: str) -> list:
    """通用翻页：找下一页按钮循环（支持 li.page[data-page=N] 格式）"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)
    all_items, seen = [], set()
    page_num = 0
    while True:
        page_num += 1
        for _ in range(6):
            await page.evaluate("window.scrollBy(0, 600)")
            await asyncio.sleep(0.3)
        text = await page.evaluate("document.body.innerText")
        items = extract_from_text(text, page.url)
        new_count = 0
        for item in items:
            key = f"{item['title'][:30]}|{item['date']}"
            if key not in seen:
                seen.add(key)
                all_items.append(item)
                new_count += 1
        print(f"  第{page_num}页:+{new_count}条 累计{len(all_items)}条", flush=True)
        if new_count == 0:
            break
        clicked = False
        # 马上消费金融：li.page[data-page=N]（共4页）
        for sel in [
            f'li.page[data-page="{page_num}"]',
            f'li.page:has-text("{page_num + 1}")',
            '[aria-label="下一页"]', '.btn-next', 'span.next',
            'text=">"', 'span[class*="next"]',
            'a:has-text(">")', 'a:has-text("›")',
        ]:
            try:
                btn = page.locator(sel).first
                if await btn.count() > 0:
                    disabled = await btn.get_attribute("disabled")
                    if disabled is None or disabled == "false":
                        await btn.click(timeout=2000)
                        clicked = True
                        break
            except Exception:
                pass
        if not clicked:
            break
        await asyncio.sleep(2.5)
    return all_items


@collector("pingan_detail")
async def collect_pingan(page, url: str) -> list:
    """平安消费金融：首页 fullPage.js 滚动，popup关闭按钮触发。
    注意：popup含安全校验图片，无法自动化完全绕过，保守提取可见文本。"""
    import datetime
    today = datetime.date.today().strftime("%Y-%m-%d")
    await page.goto(url, wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(4)

    # 滚动 fullPage sections
    for _ in range(15):
        await page.evaluate("window.scrollBy(0, window.innerHeight)")
        await asyncio.sleep(0.3)

    # 关闭 popup（找关闭按钮）
    for pop_sel in [
        ".notice_popUp [class*=close], .notice_popUp button",
        ".notice_popUp_box [class*=close], .notice_popUp_box button",
        "[class*=popUp] [class*=close], [class*=popUp] button",
    ]:
        try:
            btns = page.locator(pop_sel)
            if await btns.count() > 0:
                await btns.first.click(timeout=1000)
                await asyncio.sleep(1)
        except Exception:
            pass

    text = await page.evaluate("document.body.innerText")
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    items = []
    skip_kw = {"产品服务", "关于我们", "消费者之家", "证照公示", "首页",
               "Copyright", "ICP备案", "公网安", "年化利率", "额度", "定价",
               "400-", "中国平安", "注册地址", "公司名称", "经营范围", "有限公司",
               "minDate", "maxDate", "实际利率", "需要根据", "按照单利", "感谢您"}
    for line in lines:
        if len(line) > 15 and "消费金融" in line and not any(k in line for k in skip_kw):
            items.append({"title": line[:100], "date": today, "url": url, "category": "平安消费金融"})
    seen = set()
    unique = [i for i in items if i["title"][:30] not in seen and not seen.add(i["title"][:30])]
    return unique[:20]


# ════════════════════════════════════════════════════════════════════════════════
# GROUP_D — 详情页 URL 可枚举（从列表页提取 ID 构造详情 URL）
# ════════════════════════════════════════════════════════════════════════════════

@collector("zhongyou_detail")
async def collect_zhongyou(page, url: str) -> list:
    """中邮消费金融：提取 /xxgg/{id}.html 详情URL"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)
    for _ in range(6):
        await page.evaluate("window.scrollBy(0, 500)")
        await asyncio.sleep(0.3)

    blocks = await page.evaluate("""
        () => {
            const results = [];
            document.querySelectorAll('a[href*="/xxgg/"]').forEach(a => {
                const href = a.href;
                if (!href.match(/\\/xxgg\\/\\d+\\.html/)) return;
                const text = a.innerText.trim();
                if (!text || text.length < 5) return;
                let date = '';
                const pt = (a.parentElement || {}).innerText || '';
                const m = pt.match(/(\\d{4}[-/]\\d{2}[-/]\\d{2})/);
                if (m) date = m[1];
                if (!date) {
                    const gp = (a.parentElement || {}).parentElement || {};
                    const m2 = (gp.innerText || '').match(/(\\d{4}[-/]\\d{2}[-/]\\d{2})/);
                    if (m2) date = m2[1];
                }
                if (!date) {
                    const urlDate = href.match(/(\\d{4})(\\d{2})(\\d{2})/);
                    if (urlDate) date = urlDate[1] + '-' + urlDate[2] + '-' + urlDate[3];
                }
                if (text && text.length > 5 && date)
                    results.push({ title: text, date, href });
            });
            const seen = new Set();
            return results.filter(r => { if (seen.has(r.href)) return false; seen.add(r.href); return true; });
        }
    """)
    items, seen = [], set()
    for b in (blocks or []):
        key = f"{b['title'][:30]}|{b['date']}"
        if key not in seen:
            seen.add(key)
            items.append({"title": b["title"][:200], "date": b["date"], "url": b["href"],
                          "category": classify(b["title"])})
    print(f"  中邮消金: {len(items)}条详情页", flush=True)
    return items


@collector("xiaomi_detail")
async def collect_xiaomi(page, url: str) -> list:
    """小米消费金融：提取 /newsDetail?id= 详情URL"""
    await page.goto(url, wait_until="networkidle", timeout=20000)
    await asyncio.sleep(4)
    for _ in range(6):
        await page.evaluate("window.scrollBy(0, 500)")
        await asyncio.sleep(0.3)

    blocks = await page.evaluate("""
        () => {
            const results = [];
            document.querySelectorAll('a[href*="newsDetail"]').forEach(a => {
                const href = a.href;
                const text = a.innerText.trim();
                if (!text || text.length < 6) return;
                if (text.includes('AppStore') || text.includes('Android')) return;
                const container = (a.parentElement || {}).innerText || '';
                let date = '';
                const m = container.match(/(\\d{4})[-/年](\\d{1,2})[-/月](\\d{1,2})/);
                if (m)
                    date = m[1] + '-' + String(m[2]).padStart(2,'0') + '-' + String(m[3]).padStart(2,'0');
                if (!date) date = '2025-01-01';
                results.push({ title: text, date, href });
            });
            const seen = new Set();
            return results.filter(r => { if (seen.has(r.href)) return false; seen.add(r.href); return true; });
        }
    """)
    items, seen = [], set()
    for b in (blocks or []):
        key = f"{b['title'][:30]}|{b['date']}"
        if key not in seen:
            seen.add(key)
            items.append({"title": b["title"][:200], "date": b["date"], "url": b["href"],
                          "category": classify(b["title"])})
    print(f"  小米消金: {len(items)}条详情页", flush=True)
    return items


@collector("jinmixin_detail")
async def collect_jinmixin(page, url: str) -> list:
    """金美信消费金融：提取 /xxpl/{id} 详情URL"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)
    for _ in range(8):
        await page.evaluate("window.scrollBy(0, 500)")
        await asyncio.sleep(0.4)

    blocks = await page.evaluate("""
        () => {
            const results = [];
            document.querySelectorAll('a[href]').forEach(a => {
                const href = a.href;
                if (!href.match(/\\/xxpl\\/\\d+/)) return;
                const text = a.innerText.trim();
                if (!text || text.length < 6) return;
                if (['首页', '关于金美信', '产品服务'].includes(text)) return;
                let date = '';
                const pt = (a.parentElement || {}).innerText || '';
                const m = pt.match(/(\\d{4}-\\d{2}-\\d{2})/);
                if (m) date = m[1];
                if (!date) {
                    const gp = (a.parentElement || {}).parentElement || {};
                    const m2 = (gp.innerText || '').match(/(\\d{4}-\\d{2}-\\d{2})/);
                    if (m2) date = m2[1];
                }
                if (!date) date = '2025-01-01';
                results.push({ title: text, date, href });
            });
            const seen = new Set();
            return results.filter(r => { if (seen.has(r.href)) return false; seen.add(r.href); return true; });
        }
    """)
    items, seen = [], set()
    for b in (blocks or []):
        key = f"{b['title'][:30]}|{b['date']}"
        if key not in seen:
            seen.add(key)
            items.append({"title": b["title"][:200], "date": b["date"], "url": b["href"],
                          "category": classify(b["title"])})
    print(f"  金美信消金: {len(items)}条详情页", flush=True)
    return items


@collector("xingye_detail")
async def collect_xingye(page, url: str) -> list:
    """兴业消费金融：精确 DOM（.new_title + .new_time + 附件）"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)
    await page.evaluate("window.scrollTo(0, 0)")
    await asyncio.sleep(1)

    blocks = await page.evaluate("""
        () => {
            const results = [];
            document.querySelectorAll('.new_title').forEach(titleEl => {
                const parent = titleEl.parentElement;
                const title = titleEl.innerText.trim();
                if (!title || title.length < 10) return;
                let date = '';
                const timeEl = parent.querySelector('.new_time');
                if (timeEl) {
                    const m = timeEl.innerText.match(/(\\d{4}-\\d{2}-\\d{2})/);
                    if (m) date = m[1];
                }
                if (!date) return;
                const links = [];
                parent.querySelectorAll('a[href]').forEach(a => {
                    const h = a.href;
                    if (h && !h.includes('javascript') && h !== '#') links.push(h);
                });
                let sib = parent.nextElementSibling;
                while (sib) {
                    sib.querySelectorAll('a[href]').forEach(a => {
                        const h = a.href;
                        if (h && !h.includes('javascript') && h !== '#') links.push(h);
                    });
                    if (sib.querySelector('.new_title')) break;
                    sib = sib.nextElementSibling;
                }
                const uniqueLinks = [...new Set(links)];
                if (uniqueLinks.length === 0)
                    results.push({ title, date, url: window.location.href });
                else
                    uniqueLinks.forEach(href => results.push({ title, date, url: href }));
            });
            return results;
        }
    """)
    items, seen = [], set()
    for b in (blocks or []):
        key = f"{b['title'][:30]}|{b['date']}|{b['url'][:30]}"
        if key not in seen:
            seen.add(key)
            items.append({"title": b["title"][:200], "date": b["date"], "url": b["url"],
                          "category": classify(b["title"])})
    print(f"  兴业消金: {len(items)}条（含PDF附件）", flush=True)
    return items


@collector("haier_news_detail")
async def collect_haier(page, url: str) -> list:
    """海尔消费金融：Element UI 分页（14页）+ .newsList DOM提取公告图片URL
    注意：._truncated 来自 .contentBox.innerText，是列表页预览文本（含真实公告内容摘要），
    不是 OCR 结果，已移除 500 字限制（2026-04-13 修复）。
    PNG 图片是装饰性标题图（VLM OCR 返回"公告"两字），正文内容在 _truncated 中。"""
    await page.goto(url, wait_until="networkidle", timeout=20000)
    await asyncio.sleep(4)

    all_items, seen = [], set()

    async def extract_page_items():
        blocks = await page.evaluate("""
            () => {
                const results = [];
                document.querySelectorAll(".newsList").forEach(item => {
                    const day = item.querySelector(".day") ? item.querySelector(".day").innerText.trim() : "";
                    const month = item.querySelector(".month") ? item.querySelector(".month").innerText.trim() : "";
                    const titleEl = item.querySelector(".title");
                    const title = titleEl ? titleEl.innerText.trim() : "";
                    const imgEl = item.querySelector(".imgBox img");
                    const imgSrc = imgEl ? imgEl.src : "";
                    const contentEl = item.querySelector(".contentBox");
                    const truncated = contentEl ? contentEl.innerText.trim() : "";
                    if (!title) return;
                    let date = "";
                    if (month && day) {
                        const m2 = month.match(/^(\\d{4})\\/(\\d{2})$/);
                        if (m2) date = m2[1] + "-" + m2[2] + "-" + (day || "01").padStart(2, "0");
                    }
                    if (!date) date = "2026-01-01";
                    results.push({ title, date, imgSrc, truncated });
                });
                return results;
            }
        """)
        return blocks or []

    for b in await extract_page_items():
        key = f"{b['title'][:30]}|{b['date']}"
        if key not in seen:
            seen.add(key)
            all_items.append({"title": b["title"][:200], "date": b["date"],
                             "url": b["imgSrc"], "_truncated": b["truncated"],
                             "category": classify(b["title"])})

    print(f"  海尔第1页: +{len(all_items)}条 累计{len(all_items)}条", flush=True)

    for pg in range(2, 15):
        try:
            btn = page.locator(f'.el-pager li[aria-label="第 {pg} 页"]')
            await btn.click(timeout=3000)
            await asyncio.sleep(2)
            new_count = 0
            for b in await extract_page_items():
                key = f"{b['title'][:30]}|{b['date']}"
                if key not in seen:
                    seen.add(key)
                    all_items.append({"title": b["title"][:200], "date": b["date"],
                                     "url": b["imgSrc"], "_truncated": b["truncated"],
                                     "category": classify(b["title"])})
                    new_count += 1
            print(f"  海尔第{pg}页: +{new_count}条 累计{len(all_items)}条", flush=True)
        except Exception as e:
            print(f"  海尔第{pg}页失败: {str(e)[:50]}", flush=True)
            break

    print(f"  海尔消金: {len(all_items)}条（含图片URL）", flush=True)
    return all_items


@collector("beiyin_marquee")
async def collect_beiyin(page, url: str) -> list:
    """北银消费金融：首页滚动区提取URL → 详情页获取日期"""
    all_items, seen = [], set()
    base = "https://www.bobcfc.com"
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(3)
        for _ in range(6):
            await page.evaluate("window.scrollBy(0, 400)")
            await asyncio.sleep(0.5)
        els = await page.query_selector_all('.dowebok a[href*="/contents/"]')
        urls = []
        for el in els:
            href = await el.get_attribute("href") or ""
            if href and href not in seen:
                seen.add(href)
                t = await el.inner_text()
                t = t.replace("处理个人信息合作机构列表", "").strip()
                if t:
                    urls.append((t, base + href))
        print(f"  北银滚动区: {len(urls)}个公告", flush=True)
        for title, detail_url in urls:
            try:
                await page.goto(detail_url, wait_until="domcontentloaded", timeout=15000)
                await asyncio.sleep(2)
                text = await page.evaluate("document.body.innerText")
                date_str = ""
                for line in text.split("\n"):
                    line = line.strip()
                    if re.search(r"202[4-6]", line) and len(line) < 30:
                        date_str = line
                        break
                if date_str:
                    all_items.append({"title": title[:200], "date": date_str,
                                     "url": detail_url, "category": classify(title)})
            except Exception as e:
                print(f"    北银详情页异常 {detail_url}: {e}", flush=True)
    except Exception as e:
        return [{"title": f"ERROR: {e}", "date": "", "url": url, "category": "错误"}]
    return all_items


@collector("jianxin_dmyy")
async def collect_jianxin(page, url: str) -> list:
    """建信消费金融：Vue SPA，等待网络idle + 充分滚动"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(4)
    for _ in range(6):
        await page.evaluate("window.scrollBy(0, 500)")
        await asyncio.sleep(0.5)
    text = await page.evaluate("document.body.innerText")
    return extract_from_text(text, url)


@collector("suyinkaiji")
async def collect_suyinkaiji(page, url: str) -> list:
    """
    苏银凯基消费金融：Cloudflare WAF + Vue SPA + 详情页点击
    - 首页先触发 Cloudflare challenge
    - 信息页只访问一次，MutationObserver 自动关闭弹窗
    - 每条公告点击进入 inforDetail 页面获取完整正文
    """
    all_items = []

    async def setup_observer():
        """注入 MutationObserver，自动关闭弹窗"""
        try:
            await page.evaluate("""
                () => {
                    if (window.__sykObs) return;
                    window.__sykObs = true;
                    const obs = new MutationObserver(() => {
                        const w = document.querySelector('.el-message-box__wrapper');
                        if (w) {
                            const btn = w.querySelector('.el-message-box__headerbtn') ||
                                        w.querySelector('.el-message-box__btns button');
                            if (btn) { btn.click(); obs.disconnect(); }
                        }
                    });
                    obs.observe(document.body, { childList: true, subtree: true });
                }
            """)
        except Exception:
            pass

    # 主页触发 Cloudflare
    await page.goto("https://www.sykcfc.cn/", wait_until="domcontentloaded", timeout=30000)
    await asyncio.sleep(15)
    await setup_observer()

    # 信息发布页
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await asyncio.sleep(15)
    # 等弹窗自动关闭
    for _ in range(15):
        if await page.locator(".el-message-box__wrapper").count() == 0:
            break
        await asyncio.sleep(1)
    await page.wait_for_load_state("networkidle", timeout=20000)

    # 提取列表页文本和条目 DOM 引用
    text = await page.inner_text("body")

    def parse_list(text: str) -> list:
        items = []
        lines = text.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            m = re.match(r'^(\d{4})\s*-\s*(\d{2})(?:\s*-\s*(\d{2}))?$', line)
            if m:
                y, mo, d = m.group(1), m.group(2), (m.group(3) or "01")
                date_str = f"{y}-{mo}-{d}"
                j = i + 1
                while j < len(lines) and lines[j].strip().isdigit():
                    j += 1
                title = ""
                while j < len(lines):
                    cand = lines[j].strip()
                    if cand and not cand.isdigit() and len(cand) > 5:
                        title = cand
                        break
                    j += 1
                if title and len(title) > 5:
                    items.append({"title": title[:200], "date": date_str})
            i += 1
        return items

    list_items = parse_list(text)
    print(f"  苏银凯基列表: {len(list_items)}条", flush=True)

    # 解析正文：STOP_KEYWORDS 之后的不要
    STOP_KEYWORDS = ['相关信息', '服务及价目公告', '公示信息', '投诉方式', '联系我们',
                      '全国客服', '公司地址', '苏银消金APP', '苏银消金公众号']

    def parse_body(detail_text: str) -> str:
        lines = detail_text.split('\n')
        body_lines = []
        in_body = False
        for line in lines:
            ls = line.strip()
            if re.match(r'^\d{4}\s*年', ls) or (ls.startswith('时间')):
                in_body = True
                continue
            if any(kw in ls for kw in STOP_KEYWORDS) and in_body:
                break
            if in_body and ls and len(ls) > 5:
                body_lines.append(ls)
        return '\n'.join(body_lines)

    # 逐条点击提取详情
    # 在当前页面的 DOM 中获取 .sykj-news_item 元素
    for idx, item in enumerate(list_items):
        try:
            # 刷新列表条目（每次都重新查询 DOM）
            news_items = await page.locator(".sykj-news_item").all()
            if idx >= len(news_items):
                print(f"  [{idx+1}] 条目不存在", flush=True)
                continue

            target = news_items[idx]
            await target.scroll_into_view_if_needed()
            await asyncio.sleep(1)

            # 尝试普通 click（带重试）
            clicked = False
            for attempt in range(3):
                # 确保弹窗关闭
                for _ in range(8):
                    if await page.locator(".el-message-box__wrapper").count() == 0:
                        await asyncio.sleep(0.5)  # 等 overlay 动画结束
                        break
                    await asyncio.sleep(0.5)
                try:
                    await target.click(timeout=8000)
                    clicked = True
                    break
                except Exception:
                    await asyncio.sleep(1)

            # 等待详情页内容
            detail_text = ""
            for _ in range(20):
                await asyncio.sleep(1)
                txt = await page.inner_text("body")
                if '/inforDetail' in page.url and re.search(r'\d{4}\s*年\s*\d+\s*月', txt) and len(txt) < 800:
                    detail_text = txt
                    break
            await page.wait_for_load_state("networkidle", timeout=20000)

            body = parse_body(detail_text)
            print(f"  [{idx+1}] 详情正文: {len(body)}字 | URL: {page.url[-40:]}", flush=True)

            all_items.append({
                "title": item["title"],
                "date": item["date"],
                "url": page.url,
                "text": body[:1000],
                "_content": body[:1000],
                "category": classify(item["title"]),
            })

            # 返回列表页
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(15)
            # 等弹窗自动关闭
            for _ in range(15):
                if await page.locator(".el-message-box__wrapper").count() == 0:
                    break
                await asyncio.sleep(1)
            await page.wait_for_load_state("networkidle", timeout=20000)

        except Exception as e:
            print(f"  [{idx+1}] 异常: {e}", flush=True)
            all_items.append({
                "title": item["title"],
                "date": item["date"],
                "url": url,
                "text": "",
                "_content": "",
                "category": classify(item["title"]),
            })
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(15)
                for _ in range(15):
                    if await page.locator(".el-message-box__wrapper").count() == 0:
                        break
                    await asyncio.sleep(1)
            except Exception:
                pass

    if not all_items:
        for item in parse_list(text):
            all_items.append({
                "title": item["title"],
                "date": item["date"],
                "url": url,
                "text": "",
                "_content": "",
                "category": classify(item["title"]),
            })

    seen, result = set(), []
    for item in all_items:
        key = f"{item['title'][:30]}|{item['date']}"
        if key not in seen:
            seen.add(key)
            result.append(item)

    print(f"  苏银凯基消金: {len(result)}条", flush=True)
    return result
@collector("jinshang_detail")
async def collect_jinshang(page, url: str) -> list:
    """晋商消费金融：双栏（col23 + col22），提取详情URL"""
    all_items, seen = [], set()
    for col_url, col_name in [
        ("https://www.jcfc.cn/col23/list.html", "col23"),
        ("https://www.jcfc.cn/col22/list.html", "col22"),
    ]:
        await page.goto(col_url, wait_until="domcontentloaded", timeout=15000)
        await asyncio.sleep(3)
        page_num = 0
        while True:
            page_num += 1
            for _ in range(4):
                await page.evaluate("window.scrollBy(0, 400)")
                await asyncio.sleep(0.3)

            blocks = await page.evaluate("""
                () => {
                    const results = [];
                    document.querySelectorAll("a[href]").forEach(a => {
                        const href = a.href;
                        if (!href.match(/\\/col23\\/\\d+\\.html|\\/col22\\/\\d+\\.html/)) return;
                        const text = a.innerText.trim();
                        if (!text || text.length < 5) return;
                        let date = '';
                        const pt = (a.parentElement || {}).innerText || '';
                        const dm = pt.match(/(\\d{4}-\\d{2}-\\d{2})/);
                        if (dm) date = dm[1];
                        if (!date) {
                            const gp = (a.parentElement || {}).parentElement || {};
                            const dm2 = (gp.innerText || '').match(/(\\d{4}-\\d{2}-\\d{2})/);
                            if (dm2) date = dm2[1];
                        }
                        if (!date) date = '2025-01-01';
                        results.push({ title: text, date, href });
                    });
                    const seenLocal = new Set();
                    return results.filter(r => {
                        if (seenLocal.has(r.href)) return false;
                        seenLocal.add(r.href); return true;
                    });
                }
            """)
            new_count = 0
            for b in (blocks or []):
                key = f"{b['title'][:30]}|{b['date']}"
                if key not in seen:
                    seen.add(key)
                    all_items.append({"title": b["title"][:200], "date": b["date"],
                                     "url": b["href"], "category": classify(b["title"])})
                    new_count += 1
            print(f"  [{col_name}第{page_num}页]+{new_count}条 累计{len(all_items)}条", flush=True)
            if new_count == 0:
                break
            clicked = False
            for sel in ["text=下一页"]:
                try:
                    btn = page.locator(sel).first
                    if await btn.count() > 0 and not await btn.get_attribute("disabled"):
                        await btn.click(timeout=2000)
                        clicked = True
                except Exception:
                    pass
            if not clicked:
                break
            await asyncio.sleep(2)
    return all_items


@collector("zhongyin_layui")
async def collect_zhongyin(page, url: str) -> list:
    """中银消费金融：layui JS分页，13页，.main_content_body_item"""
    all_items, seen = [], set()
    base = "https://www.boccfc.cn"
    for pg in range(1, 20):
        try:
            if pg == 1:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                await asyncio.sleep(3)
            else:
                clicked = False
                for sel in [f'a[data-page="{pg}"]', f'.layui-laypage a[data-page="{pg}"]']:
                    try:
                        btn = page.locator(sel).first
                        if await btn.count() > 0:
                            await btn.click(timeout=3000)
                            clicked = True
                            break
                    except Exception:
                        pass
                if not clicked:
                    try:
                        next_btn = page.locator('.layui-laypage a.layui-laypage-prev + a').first
                        if await next_btn.count() > 0:
                            await next_btn.click(timeout=3000)
                            clicked = True
                    except Exception:
                        pass
                if not clicked:
                    print(f"    中银第{pg}页找不到按钮，停止", flush=True)
                    break
            await asyncio.sleep(2)

            items = await page.query_selector_all(".main_content_body_item")
            new_count = 0
            for item in items:
                try:
                    href = await item.get_attribute("href") or ""
                    spans = await item.query_selector_all("span")
                    date_str = ""
                    for sp in spans:
                        t = await sp.inner_text()
                        m = re.search(r"(\d{4}[-/]\d{2}[-/]\d{2})", t)
                        if m:
                            date_str = m.group(1).replace("/", "-")
                            break
                    title_els = await item.query_selector_all("a")
                    title = ""
                    for a in title_els:
                        t = await a.inner_text()
                        if t and len(t) > 3:
                            title = t.strip()
                            break
                    if not title:
                        title = "公告"
                    detail_url = base + href if href else url
                    key = f"{detail_url[:40]}|{date_str}"
                    if key not in seen:
                        seen.add(key)
                        all_items.append({"title": title[:200], "date": date_str,
                                         "url": detail_url, "category": classify(title)})
                        new_count += 1
                except Exception:
                    continue
            print(f"  中银第{pg}页:+{new_count}条 累计{len(all_items)}条", flush=True)
            if new_count == 0:
                break
        except Exception as e:
            print(f"  中银第{pg}页异常: {e}", flush=True)
            break
    return all_items


@collector("yangguang_detail")
async def collect_yangguang(page, url: str) -> list:
    """阳光消费金融：DOM列表提取（标题+日期来自URL路径）"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(4)
    all_items, seen = [], set()
    page_num = 0
    while page_num < 10:
        page_num += 1
        for _ in range(2):
            await page.evaluate("window.scrollBy(0, 400)")
            await asyncio.sleep(0.3)
        raw_items = await page.evaluate("""
            () => {
                const result = [];
                const selectors = ['.list-item', '.news-item', '.article-item',
                                   'li[data-id]', '.item', 'ul li', '.newslist li'];
                let containers = [];
                for (const sel of selectors) {
                    containers = document.querySelectorAll(sel);
                    if (containers.length > 0) break;
                }
                if (containers.length === 0) {
                    const links = document.querySelectorAll('a[href*="/xxgg/"]');
                    for (const a of links) {
                        const text = a.innerText.trim();
                        if (text.length > 5 && !text.includes('首页') && !text.includes('关于我们'))
                            result.push({ title: text, href: a.href });
                    }
                } else {
                    for (const container of containers) {
                        const a = container.querySelector('a[href*="/xxgg/"]') || container.querySelector('a');
                        const titleEl = a || container.querySelector('.title, h3, h4, .tit');
                        if (titleEl)
                            result.push({ title: titleEl.innerText.trim().slice(0, 100), href: a ? a.href : '' });
                    }
                }
                return result;
            }
        """)
        new_count = 0
        for raw in raw_items:
            title = raw.get('title', '')
            if len(title) < 4:
                continue
            if any(x in title for x in ["首页", "关于我们", "联系我们", "版权", "客服", "投诉"]):
                continue
            href = raw.get('href', '')
            date_str = ""
            date_m = re.search(r'/(\d{4})(\d{2})(\d{2})\d+/index\.html', href)
            if date_m:
                date_str = f"{date_m.group(1)}-{date_m.group(2)}-{date_m.group(3)}"
            key = f"{title[:30]}|{date_str}"
            if key not in seen and title:
                seen.add(key)
                all_items.append({"title": title[:200], "date": date_str,
                                 "url": href or url, "category": classify(title)})
                new_count += 1
        print(f"  第{page_num}页:+{new_count}条 累计{len(all_items)}条", flush=True)
        if new_count == 0:
            break
        clicked = False
        for sel in ["text=下一页", "[class*=next]", "a:has-text('下一页')", ".next"]:
            try:
                btn = page.locator(sel).first
                if await btn.count() > 0 and "disabled" not in (await btn.get_attribute("class") or ""):
                    await btn.click(timeout=2000)
                    clicked = True
                    break
            except Exception:
                pass
        if not clicked:
            break
        await asyncio.sleep(2)
    return all_items


@collector("zhongyuan")
async def collect_zhongyuan(page, url: str) -> list:
    """中原消费金融：滚动加载，'查看更多'翻页，split-line日期"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)
    all_items, seen = [], set()
    for _ in range(8):
        for _ in range(4):
            await page.evaluate("window.scrollBy(0, 400)")
            await asyncio.sleep(0.3)
        text = await page.evaluate("document.body.innerText")
        items = extract_from_text(text, url)
        for item in items:
            key = f"{item['title'][:30]}|{item['date']}"
            if key not in seen:
                seen.add(key)
                all_items.append(item)
        print(f"  中原:+{len(items)}条 累计{len(all_items)}条", flush=True)
        clicked = False
        for sel in ["text=查看更多", "text=加载更多", "[class*=more]"]:
            try:
                btns = page.locator(sel)
                cnt = await btns.count()
                if cnt > 0:
                    btn = btns.first
                    if not await btn.get_attribute("disabled"):
                        await btn.click(timeout=3000)
                        clicked = True
            except Exception:
                pass
        if not clicked:
            break
        await asyncio.sleep(2)
    skip_prefixes = ("您现在的位置", "新闻公告", "公司动态", "媒体报道", "通知公告",
                     "企业荣誉", "党建活动", "信息披露")
    filtered = [it for it in all_items if not any(it["title"].startswith(p) for p in skip_prefixes)]
    print(f"  中原过滤后:{len(filtered)}条（原始{len(all_items)}条）", flush=True)
    return filtered


@collector("hebei_detail")
async def collect_hebei(page, url: str) -> list:
    """河北幸福消费金融：直接文本提取（DD-MM-YY格式）"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)
    for _ in range(5):
        await page.evaluate("window.scrollBy(0, 600)")
        await asyncio.sleep(0.5)
    text = await page.evaluate("document.body.innerText")
    items = extract_from_text(text, url)
    for item in items:
        item["category"] = "河北幸福消费金融"
    return items


@collector("time_prefix")
async def collect_time_prefix(page, url: str) -> list:
    """盛银消费金融：时间在前标题在后"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)
    for _ in range(4):
        await page.evaluate("window.scrollBy(0, 400)")
        await asyncio.sleep(0.4)
    text = await page.evaluate("document.body.innerText")
    return extract_from_text(text, url)


@collector("shangcheng_news")
async def collect_shangcheng(page, url: str) -> list:
    """尚诚消费金融：新闻列表"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)
    for _ in range(4):
        await page.evaluate("window.scrollBy(0, 400)")
        await asyncio.sleep(0.4)
    text = await page.evaluate("document.body.innerText")
    return extract_from_text(text, url)


@collector("pdf_link|notice_link_parse")
async def collect_pdf_link(page, url: str) -> list:
    """天津京东消费金融 / 锦程消费金融：PDF附件列表"""
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)
    for _ in range(4):
        await page.evaluate("window.scrollBy(0, 400)")
        await asyncio.sleep(0.4)
    text = await page.evaluate("document.body.innerText")
    return extract_from_text(text, url)


# ════════════════════════════════════════════════════════════════════════════════
# GROUP_H — WSL2 受限（CDP专用，或特殊URL）
# ════════════════════════════════════════════════════════════════════════════════

@collector("changyin58_telling")
async def collect_changyin58(page, url: str) -> list:
    """
    长银五八消费金融：telling.html
    Cloudflare 保护站点，尝试 stealth + 长时间等待劫持 API。
    如果 Cloudflare 仍未通过，返回空列表（由 html_dom 兜底）。
    """
    import re as _re

    # 劫持 fetch/XHR，捕获 API 响应
    api_data = []

    async def _capture_response(resp):
        if any(k in resp.url for k in ['news', 'article', 'list', 'telling', 'info']):
            try:
                d = await resp.json()
                records = d.get('data', {}) or d
                if isinstance(records, list) and records:
                    api_data.extend(records)
                elif isinstance(records, dict):
                    for v in records.values():
                        if isinstance(v, list):
                            api_data.extend(v)
            except Exception:
                pass

    page.on('response', _capture_response)

    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=20000)
        await asyncio.sleep(12)  # Cloudflare 验证等待

        # 如果劫持到数据，直接返回
        if api_data:
            items = []
            for rec in api_data:
                title = str(rec.get('title') or rec.get('name', '')).strip()
                date = str(rec.get('date') or rec.get('releaseTime') or rec.get('publishTime') or '')[:10]
                detail_url = str(rec.get('url') or rec.get('link') or rec.get('id', ''))
                if title and len(title) > 3:
                    items.append({
                        'title': title[:200],
                        'date': date,
                        'url': detail_url,
                        'category': classify(title),
                    })
            if items:
                return items

        # 没有 API 数据，尝试 SPA 导航提取列表项
        items = []
        seen_keys = set()

        for _ in range(5):
            await page.evaluate('window.scrollBy(0, 400)')
            await asyncio.sleep(0.5)

            text = await page.evaluate('document.body.innerText')
            blocks = await page.evaluate("""
                () => {
                    const lines = document.body.innerText.split('\n');
                    return lines.map(l => l.trim()).filter(l => l.length > 5);
                }
            """)

            for line in blocks:
                date_m = _re.search(r'(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})', line)
                if date_m and line == date_m.group(0):
                    continue  # 跳过纯日期行
                key = line[:50]
                if key not in seen_keys and len(line) > 10:
                    seen_keys.add(key)
                    items.append({
                        'title': line[:200],
                        'date': date_m.group(1) + '-' + date_m.group(2).zfill(2) + '-' + date_m.group(3).zfill(2) if date_m else '',
                        'url': page.url,
                        'category': classify(line),
                    })

        return items

    except Exception:
        pass

    return []

@collector("shaanxi_changyin")
async def collect_shaanxi_changyin(page, url: str) -> list:
    """
    陕西长银消费金融：m.cycfc.com Vue SPA
    1. 访问列表页，拦截 API 获取第1页（5条）
    2. 点击"公告通知" Tab，获取该 Tab 内容（不同5条）
    3. 对每个 Tab 的每条记录，直接导航到详情页提取正文
    注意：API pageNum=2+ 在 headless 模式下返回"系统内部异常"，故仅采集两 Tab（10条）。
    """
    import re as _re

    all_items = []
    seen_keys = set()
    captured_records = []

    # ── 辅助：提取当前 DOM 可见条目 ───────────────────────────────────────
    # 两 Tab DOM 结构不同：
    #   公司动态 → .item_news 包含日期（首行）和标题
    #   公告通知 → .item 为标题（含时间行），.time 为日期（时间：YYYY年MM月DD日）
    # 返回 dict 列表，每项含 tab/title/date/el（el 仅公告通知有）
    async def _extract_visible_items(tab_label: str = "") -> list:
        items = []
        try:
            # 公告通知: .item(标题+时间行) + .time(日期)
            ann_items = []
            ann_time = await page.locator(".time").all()
            ann_title_els = await page.locator(".item").all()
            if ann_time and ann_title_els:
                for i in range(min(len(ann_time), len(ann_title_els))):
                    try:
                        t_txt = (await ann_time[i].inner_text()).strip()
                        raw_title = (await ann_title_els[i].inner_text()).strip()
                        # 去掉"时间：YYYY年MM月DD日"这一行
                        lines = [l.strip() for l in raw_title.split('\n') if l.strip()]
                        title = '\n'.join(l for l in lines if not _re.match(r'时间：', l))
                        date_m = _re.search(r'(\d{4})年(\d{2})月(\d{2})日', t_txt)
                        date_str = (f"{date_m.group(1)}-{date_m.group(2)}-{date_m.group(3)}"
                                    if date_m else t_txt[3:13] if len(t_txt) > 3 else t_txt[:10])
                        if title and date_str and len(title) > 3:
                            ann_items.append({
                                'tab': tab_label, 'title': title, 'date': date_str,
                                'el': ann_title_els[i]   # 点击元素引用
                            })
                    except Exception:
                        pass

            # 公司动态: .item_news 内部
            dyn_items = []
            dyn_els = await page.locator(".item_news").all()
            for el in dyn_els:
                try:
                    txt = (await el.inner_text()).strip()
                    if not txt or len(txt) <= 5:
                        continue
                    lines = txt.split('\n')
                    date_str, title = "", ""
                    for line in lines:
                        s = line.strip()
                        if not s or s == "加载中...":
                            continue
                        date_m = _re.search(r'(\d{4})[/年](\d{2})[/月](\d{2})', s)
                        if date_m and not date_str:
                            date_str = f"{date_m.group(1)}-{date_m.group(2)}-{date_m.group(3)}"
                        elif s and not title and len(s) > 5:
                            title = s
                    if title and date_str:
                        dyn_items.append({'tab': tab_label, 'title': title, 'date': date_str})
                except Exception:
                    pass

            # 选取非空的
            items = ann_items if len(ann_items) > len(dyn_items) else dyn_items
        except Exception as e:
            print(f"    _extract_visible_items 出错: {e}", flush=True)
        return items

    # ── 辅助：提取详情正文 ───────────────────────────────────────────────
    # 方式1: rec_id → 直接导航到详情页
    # 方式2: 点击 .item (公告通知) 或 .item_news (公司动态) 进入详情
    async def _fetch_detail(rec_id: int = None, click_el=None, return_url: bool = False):
        try:
            if rec_id:
                await page.goto(f"https://m.cycfc.com/#/news/{rec_id}",
                                wait_until='domcontentloaded', timeout=15000)
            elif click_el:
                await click_el.click(timeout=5000)
            else:
                return ("", "") if return_url else ""
            await asyncio.sleep(2.5)
            cur_url = page.url
            text = await page.evaluate("""
                () => {
                    const rm = sel => document.querySelectorAll(sel).forEach(e => e.remove());
                    rm('.header, .footer, .nav, .sidebar, script, style');
                    const el = document.querySelector('.content, .article, #content, main, [class*=detail]');
                    return el ? el.innerText.trim() : document.body.innerText.trim();
                }
            """)
            lines = text.split('\n')
            cleaned = []
            skip = 0
            NAV = {'首页','产品介绍','联系我们','关于我们','加入我们','客服热线',
                   '版权','ICP','公网安','公司动态详情','公告通知详情'}
            for line in lines:
                s = line.strip()
                if not s: continue
                if s in NAV:
                    skip += 1
                    if skip > 3: continue
                    continue
                skip = 0
                cleaned.append(s)
            content = '\n'.join(cleaned).strip()
            if return_url:
                return (content, cur_url)
            return content
        except Exception:
            return ("", "") if return_url else ""

    # ── 第1步：拦截 API ───────────────────────────────────────────────────
    async def _capture(resp):
        if 'getNewsByNum' in resp.url:
            try:
                d = await resp.json()
                captured_records.extend(d.get('data', {}).get('records', []))
            except Exception:
                pass

    page.on('response', _capture)
    await page.goto("https://m.cycfc.com/#/news", wait_until='domcontentloaded', timeout=20000)
    await asyncio.sleep(4)
    page.remove_listener('response', _capture)

    if not captured_records:
        print("  陕西长银: API 未返回数据", flush=True)
        return []

    # ── 第2步：采集公司动态 Tab ──────────────────────────────────────────
    tab1_items = await _extract_visible_items("公司动态")
    print(f"  陕西长银 [公司动态]: {len(tab1_items)}条", flush=True)

    # ── 第3步：点击公告通知 Tab ──────────────────────────────────────────
    tab2_items = []
    try:
        ann_tab = page.locator("text=公告通知").first
        if await ann_tab.is_visible():
            await ann_tab.click(timeout=3000)
            await asyncio.sleep(1.5)
            tab2_items = await _extract_visible_items("公告通知")
            print(f"  陕西长银 [公告通知]: {len(tab2_items)}条", flush=True)
    except Exception as e:
        print(f"  陕西长银: 公告通知 Tab 切换失败 ({e})", flush=True)

    # ── 第4步：逐条提取详情正文 ──────────────────────────────────────────
    # 用索引对应：captured_records[0..4] 对应公司动态，captured_records[5..9] 对应公告通知
    all_tab_items = tab1_items + tab2_items

    for idx, item in enumerate(all_tab_items):
        title = item['title'].strip()
        date_str = item['date']
        tab_label = item['tab']
        key = f"{title[:30]}|{date_str}"
        if key in seen_keys or not title or len(title) <= 3:
            continue
        seen_keys.add(key)

        # 用索引从 captured_records 取 rec_id（仅公司动态有效）
        rec = captured_records[idx] if idx < len(captured_records) else None
        rec_id = rec.get('id') if rec else None
        click_el = item.get('el')  # 公告通知有 .item 元素引用

        # 正文提取：优先用 rec_id 导航，否则点击元素
        content = ""
        detail_url = ""
        if rec_id:
            detail_url = f"https://m.cycfc.com/#/news/{rec_id}"
            content = await _fetch_detail(rec_id=rec_id)
        elif click_el and tab_label == "公告通知":
            content, detail_url = await _fetch_detail(click_el=click_el, return_url=True)

        # 返回列表页并切回对应 Tab
        try:
            await page.goto("https://m.cycfc.com/#/news", wait_until='domcontentloaded', timeout=15000)
            await asyncio.sleep(2)
            if tab_label == "公告通知":
                try:
                    ann_t = page.locator("text=公告通知").first
                    if await ann_t.is_visible():
                        await ann_t.click(timeout=2000)
                        await asyncio.sleep(2)  # 等待公告通知 Tab 内容渲染
                except Exception:
                    pass
        except Exception:
            pass

        if content and len(content) > 50:
            print(f"    [{tab_label}] {date_str} {title[:40]}... ({len(content)}字)", flush=True)
            all_items.append({
                'title': title[:200],
                'date': date_str,
                'url': detail_url if detail_url else f"https://m.cycfc.com/#/news/{rec_id}",
                '_content': content,
                'category': classify(title),
            })
        else:
            all_items.append({
                'title': title[:200],
                'date': date_str,
                'url': detail_url if detail_url else "",
                'category': classify(title),
            })

    print(f"  陕西长银消金: {len(all_items)}条（含正文{sum(1 for x in all_items if x.get('_content'))}条）", flush=True)
    return all_items



# ════════════════════════════════════════════════════════════════════════════════
# BROKEN FIX — SPA详情页导航（替代extract_from_text）
# 原理：列表页本身没有href → 点击"查看更多/详情" → URL出现 → 逐条提取
# ════════════════════════════════════════════════════════════════════════════════

async def _spa_detail_nav(
    page,
    base_url: str,
    btn_locator: str,           # e.g. 'button:has-text("查看详情")'
    max_pages: int = 10,
    max_per_page: int = 20,
    expected_pagination_sel: str = "text=›",  # 哈银用"›"，杭银可能用"下一页"
) -> list:
    """
    通用SPA列表导航：
    1. 访问列表页
    2. 翻页（每页最多max_per_page条）
    3. 点击每条公告的"查看更多/详情" → 获取detail URL
    4. 提取正文内容
    5. 返回 [{title, date, url, full_text}]
    """
    await page.goto(base_url, wait_until="domcontentloaded", timeout=15000)
    await asyncio.sleep(3)
    
    all_items = []
    seen_keys = set()
    
    for page_num in range(1, max_pages + 1):
        # 滚动加载
        for _ in range(5):
            await page.evaluate("window.scrollBy(0, 400)")
            await asyncio.sleep(0.3)
        
        # 找到当前页所有公告按钮
        try:
            btns = page.locator(btn_locator)
            count = btns.count()
        except Exception:
            break
        
        if count == 0:
            # 可能已到尾页
            break
        
        print(f"  第{page_num}页: 发现{count}条, 累计{len(all_items)}条", flush=True)
        
        for i in range(min(count, max_per_page)):
            try:
                # 重新定位（每次点击后索引可能变）
                btns = page.locator(btn_locator)
                btn = btns.nth(i)
                if not await btn.is_visible():
                    await btn.scroll_into_view_if_needed()
                
                # 点击前获取当前可见文本（用于提取标题/日期）
                try:
                    parent = btn.locator("xpath=..")
                    grandparent = parent.locator("xpath=../..")
                    item_text = await parent.inner_text() + await grandparent.inner_text()
                except Exception:
                    item_text = ""
                
                # 提取日期
                import re
                date_m = re.search(r"(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})", item_text)
                date_str = f"{date_m.group(1)}-{int(date_m.group(2)):02d}-{int(date_m.group(3)):02d}" if date_m else ""
                
                # 提取标题（取第一行非日期文字）
                title_lines = []
                for line in item_text.split("\n"):
                    line = line.strip()
                    if not line: continue
                    if re.match(r"^\d{4}[-/年]", line): continue
                    if len(line) > 5 and len(line) < 100:
                        title_lines.append(line)
                title = title_lines[0] if title_lines else ""
                
                # 点击进入详情页
                await btn.click(timeout=3000)
                await page.wait_for_timeout(2500)
                
                detail_url = page.url
                key = f"{detail_url}|{date_str}"
                
                # 提取正文
                body_text = await page.evaluate("document.body.innerText")
                
                # 清洗正文
                lines = body_text.split("\n")
                cleaned = []
                skip = 0
                NAV = {"首页","产品介绍","联系我们","关于我们","加入我们","联系我们","客服热线","版权","ICP","公网安"}
                for line in lines:
                    s = line.strip()
                    if not s: continue
                    if s in NAV:
                        skip += 1
                        if skip > 3: continue
                        continue
                    skip = 0
                    cleaned.append(s)
                content = "\n".join(cleaned).strip()
                
                # 有效内容检查
                is_valid = len(content) > 80 and not content.startswith("首页")
                
                if key not in seen_keys and is_valid:
                    seen_keys.add(key)
                    all_items.append({
                        "title": title[:200],
                        "date": date_str,
                        "url": detail_url,
                        "_content": content,
                        "category": classify(title),
                    })
                
                # 返回列表页
                await page.go_back(timeout=5000)
                await page.wait_for_timeout(1500)
                
            except Exception as e:
                try:
                    await page.go_back(timeout=3000)
                    await page.wait_for_timeout(1000)
                except Exception:
                    pass
                continue
        
        # 翻页
        next_clicked = False
        for sel in [expected_pagination_sel, "text=下一页", "text=>", "[class*=next]"]:
            try:
                btn = page.locator(sel).first
                if await btn.count() > 0 and not await btn.get_attribute("disabled"):
                    await btn.click(timeout=2000)
                    next_clicked = True
                    break
            except Exception:
                pass
        if not next_clicked:
            break
        await asyncio.sleep(2)
    
    return all_items


@collector("hubei_list")
async def collect_hubei(page, url: str) -> list:
    """湖北消费金融：快速列表提取，不进详情页，3个Tab全量采集"""
    import re
    tabs = [
        ("https://www.hubeicfc.com/news-notice.html", "通知公告"),
        ("https://www.hubeicfc.com/news-voice.html", "消保之声"),
        ("https://www.hubeicfc.com/news-enterprise.html", "企业新闻"),
    ]
    all_items = []
    seen_keys = set()

    for tab_url, tab_name in tabs:
        await page.goto(tab_url, wait_until="domcontentloaded", timeout=10000)
        await asyncio.sleep(2)

        page_num = 0
        while page_num < 20:
            page_num += 1
            text = await page.evaluate("document.body.innerText")
            lines = [l.strip() for l in text.split("\n") if l.strip()]

            pending_ym = ""
            page_count = 0

            i = 0
            while i < len(lines):
                line = lines[i]
                # ISO date: 2026-03-27
                iso_m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", line)
                if iso_m:
                    date_str = f"{iso_m.group(1)}-{iso_m.group(2)}-{iso_m.group(3)}"
                    for j in range(i + 1, min(i + 6, len(lines))):
                        t = lines[j]
                        if t and 5 < len(t) < 100:
                            skip = any(s in t for s in ["首页", "关于我们", "查看详情",
                                    "Copyright", "产品介绍", "联系我们", "EN", "首页"])
                            if not skip and not re.match(r"^\d+$", t):
                                key = f"{t[:30]}|{date_str}"
                                if key not in seen_keys:
                                    seen_keys.add(key)
                                    all_items.append({
                                        "title": t[:200], "date": date_str,
                                        "url": tab_url, "category": classify(t)
                                    })
                                    page_count += 1
                                break
                    i += 1
                    continue

                # YYYY-MM
                ym_m = re.match(r"^(\d{4})-(\d{2})$", line)
                if ym_m:
                    pending_ym = f"{ym_m.group(1)}-{ym_m.group(2)}"
                    i += 1
                    continue

                # Day number — 向前看找 YYYY-MM（通知公告格式：day + YYYY-MM + title）
                day_m = re.match(r"^(\d{1,2})$", line)
                if day_m and 1 <= int(day_m.group(1)) <= 31:
                    day = int(day_m.group(1))
                    # 向前找 YYYY-MM（跳过 day 和导航行）
                    ym_found = ""
                    for j in range(i + 1, min(i + 6, len(lines))):
                        ym_t = lines[j].strip()
                        if re.match(r"^\d{4}-\d{2}$", ym_t):
                            ym_found = ym_t
                            break
                        if re.match(r"^\d{1,2}$", ym_t):
                            break  # next day already, stop
                    if ym_found:
                        date_str = f"{ym_found}-{int(day_m.group(1)):02d}"
                        # 找标题：跳过 YYYY-MM 和 duplicate
                        prev_title = ""
                        for k in range(i + 1, min(i + 10, len(lines))):
                            t = lines[k].strip()
                            if not t or len(t) < 5:
                                continue
                            if re.match(r"^\d{4}-\d{2}$", t):
                                continue  # skip YYYY-MM
                            if re.match(r"^\d{1,2}$", t):
                                break  # next day started
                            skip = any(s in t for s in ["首页", "关于我们", "查看详情",
                                    "Copyright", "产品介绍", "联系我们", "EN",
                                    "Copyright ©", "关于我们"])
                            if skip:
                                continue
                            # skip duplicate title (same as prev)
                            if prev_title and t == prev_title:
                                prev_title = t
                                continue
                            key = f"{t[:30]}|{date_str}"
                            if key not in seen_keys:
                                seen_keys.add(key)
                                all_items.append({
                                    "title": t[:200], "date": date_str,
                                    "url": tab_url, "category": classify(t)
                                })
                                page_count += 1
                            break
                    i += 1
                    continue

                i += 1

            print(f"  [{tab_name}] 第{page_num}页:+{page_count}条 累计{len(all_items)}条", flush=True)

            if page_count == 0:
                break

            # 下一页
            next_clicked = False
            for sel in ["text=下一页", "[class*=next]"]:
                if next_clicked:
                    break
                try:
                    btns = await page.locator(sel).all()
                    for btn in btns:
                        dis = await btn.get_attribute("disabled")
                        txt = (await btn.inner_text()).strip()
                        if dis is None and "下一页" in txt:
                            await btn.click(timeout=2000)
                            next_clicked = True
                            break
                except Exception:
                    pass
            if not next_clicked:
                break
            await asyncio.sleep(2)

    print(f"  湖北消金: {len(all_items)}条（3 Tab合计）", flush=True)
    return all_items


@collector("zhaolian_v2")
async def collect_zhaolian(page, url: str) -> list:
    """
    招联消费金融：mgp.api.mucfc.com POST API，GraphQL风格分页
    - sectionId 固定: 202211150853512516748518839263
    - 分页参数: start=0,5,10...  limit=10
    - 总条数: 96条 (notTopTotal)
    """
    import re as _re
    import uuid as _uuid
    from urllib.parse import urlencode

    all_items = []
    seen_keys = set()
    section_id = "202211150853512516748518839263"
    boundary = f"----WebKitFormBoundary{_uuid.uuid4().hex[:16]}"

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Referer": "https://www.mucfc.com/news/?module=module3",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    }

    async def fetch_page(start: int, limit: int = 10) -> dict:
        """POST 获取指定起始位置的数据"""
        data_json = json.dumps({"sectionId": section_id, "start": str(start), "limit": str(limit)})
        body = (f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="data"\r\n\r\n'
                f"{data_json}\r\n"
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="reqEnvParams"\r\n\r\n'
                f'{{"channel":"0OWS","appType":"H5"}}\r\n'
                f"--{boundary}--\r\n")

        resp = await page.request.post(
            "https://mgp.api.mucfc.com/?operationId=mucfc.content.post.query",
            headers=headers,
            data=body,
        )
        try:
            return await resp.json()
        except:
            return {}

    # 获取第1页确定总条数
    page1 = await fetch_page(0)
    total = page1.get("data", {}).get("notTopTotal", 0)
    print(f"  招联: total={total}", flush=True)
    if total == 0:
        return []

    # 逐页采集（start=0,10,20...）
    start = 0
    while start < total:
        data = await fetch_page(start) if start > 0 else page1
        records = data.get("data", {}).get("postInfos", [])
        if not records:
            break

        for rec in records:
            title = rec.get("title", "").strip()
            content = rec.get("postContentGen", "").strip()
            # 时间格式: 1743157657000 (毫秒时间戳) 或 YYYY-MM-DD
            ts = rec.get("updateTime", "") or rec.get("createTime", "")
            if ts and ts.isdigit():
                import datetime
                date_str = datetime.datetime.fromtimestamp(int(ts) / 1000).strftime("%Y-%m-%d")
            else:
                date_str = str(ts)[:10]

            key = f"{title[:30]}|{date_str}"
            if key in seen_keys or not title:
                continue
            seen_keys.add(key)

            # 取正文
            if content and len(content) > 50:
                all_items.append({
                    "title": title[:200],
                    "date": date_str,
                    "url": url,
                    "_content": content[:5000],
                    "category": classify(title),
                })
            else:
                all_items.append({
                    "title": title[:200],
                    "date": date_str,
                    "url": url,
                    "category": classify(title),
                })

        start += len(records)
        await asyncio.sleep(0.5)

    print(f"  招联消金: {len(all_items)}条（含正文{sum(1 for x in all_items if x.get('_content'))}条）", flush=True)
    return all_items


@collector("nyfb_v2")
async def collect_nyfb(page, url: str) -> list:
    """
    南银法巴消费金融：详情URL已直接渲染在HTML，不需要AJAX
    结构: /boncfc/YYYY-MM/article_YYYYMMDDHHMMSS.shtml
    列表页: https://www.boncfc.com/boncfc/xwgg/gsgg/
    分页: > 按钮，onclick=queryArticleByCondition(this, '/boncfc/xwgg/gsgg/hash.shtml')
    """
    import re as _re

    all_items = []
    seen_keys = set()
    base = "https://www.boncfc.com"

    async def extract_page() -> list:
        """从当前DOM提取"""
        items = []
        try:
            # 找所有标题+日期对
            rows = await page.locator("td, .article-item, .news-item, tr").all()
            for row in rows:
                try:
                    text = (await row.inner_text()).strip()
                    if not text or len(text) < 5:
                        continue
                    # 匹配日期格式
                    date_m = _re.search(r"20\d{2}-\d{2}-\d{2}", text)
                    # 匹配详情链接
                    link = row.locator("a[href*=shtml]").first
                    href = await link.get_attribute("href") if await link.count() > 0 else ""
                    title = text.strip()
                    if href and date_m:
                        full_url = (base + href) if href.startswith("/") else href
                        date_str = date_m.group()
                        if title and len(title) > 3:
                            items.append({"title": title[:200], "date": date_str, "url": full_url})
                except Exception:
                    pass
        except Exception:
            pass
        return items

    async def extract_simple() -> list:
        """备用：从 inner_text 直接解析"""
        text = await page.inner_text("body")
        items = []
        # 匹配 "2026-04-07\n南银法巴消费金融有限公司信息披露" 模式
        pattern = r"(20\d{2}-\d{2}-\d{2})\s*\n?\s*([^\n]{5,60}?(?:信息披露|公告|通知))[^\n]{0,100}?(?=\s*(?:20\d{2}-\d{2}-\d{2})|$)"
        matches = _re.findall(pattern, text)
        for date_str, title in matches:
            title = title.strip()
            if title and len(title) > 3:
                # 找对应详情URL
                href = ""
                try:
                    all_links = await page.locator("a[href*=shtml]").all()
                    for link in all_links:
                        link_text = (await link.inner_text()).strip()
                        if title[:10] in link_text or link_text in title:
                            href = await link.get_attribute("href") or ""
                            break
                except Exception:
                    pass
                full_url = (base + href) if href.startswith("/") else href
                items.append({"title": title[:200], "date": date_str, "url": full_url})
        return items

    # 访问列表页
    await page.goto(url, wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(3)

    page1_items = await extract_page()
    if not page1_items:
        page1_items = await extract_simple()

    print(f"  南银法巴 第1页: {len(page1_items)}条", flush=True)
    all_items.extend(page1_items)

    # 翻页（最多20页）
    for pg in range(2, 21):
        try:
            next_btn = page.locator("text=>").first
            if not await next_btn.is_visible():
                break
            await next_btn.click(timeout=3000)
            await asyncio.sleep(3)
            items = await extract_page()
            if not items:
                items = await extract_simple()
            if items:
                print(f"  南银法巴 第{pg}页: +{len(items)}条", flush=True)
                all_items.extend(items)
            else:
                break
        except Exception as e:
            print(f"  南银法巴 第{pg}页失败: {e}", flush=True)
            break

    # 去重
    seen = set()
    deduped = []
    for item in all_items:
        key = f"{item['title'][:30]}|{item['date']}"
        if key not in seen:
            seen.add(key)
            deduped.append(item)

    print(f"  南银法巴消金: {len(deduped)}条", flush=True)
    return deduped


@collector("hangyin_v2")
async def collect_hangyin(page, url: str) -> list:
    """
    杭银消费金融：API返回 list，viewType=2需进详情页
    - API: https://www.51xf.cn/news/?type=1
    - 详情URL: https://www.51xf.cn/news/detail/{newsDetailId}
    - 翻页: API参数 pageNum + pageSize
    """
    import re as _re

    all_items = []
    seen_keys = set()

    async def fetch_page(page_num: int, page_size: int = 10) -> list:
        """直接请求API"""
        api_url = f"https://www.51xf.cn/news/?type=1&pageNum={page_num}&pageSize={page_size}"
        resp = await page.request.get(api_url)
        try:
            d = await resp.json()
            return d.get("data", {}).get("list", [])
        except:
            return []

    # 第1页获取总数
    records = await fetch_page(1)
    if not records:
        return []

    # 从第1页响应找total
    # 尝试 JS 注入获取 total
    total = await page.evaluate("""
        () => {
            const els = document.querySelectorAll('[class*=total], [class*=count], .page-info');
            for (let el of els) {
                const t = el.innerText.trim();
                if (/\\d+/.test(t)) return t;
            }
            return '';
        }
    """)

    print(f"  杭银 第1页: {len(records)}条", flush=True)

    # 提取每条记录的详情URL
    for rec in records:
        title = str(rec.get("newsTitle", "")).strip()
        news_id = rec.get("newsDetailId", "")
        # viewType=2 表示有详情页
        detail_url = f"https://www.51xf.cn/news/detail/{news_id}" if news_id else ""
        date_str = str(rec.get("validStartTime", ""))[:10] if rec.get("validStartTime") else ""
        if not date_str:
            date_str = str(rec.get("newsDate", ""))[:10] if rec.get("newsDate") else ""

        key = f"{title[:30]}|{date_str}"
        if key in seen_keys or not title:
            continue
        seen_keys.add(key)

        all_items.append({
            "title": title[:200],
            "date": date_str,
            "url": detail_url,
            "category": classify(title),
        })

    # 翻页
    total_estimate = len(records) * 20  # 保守估计
    for pg in range(2, 21):
        recs = await fetch_page(pg)
        if not recs:
            break
        print(f"  杭银 第{pg}页: +{len(recs)}条", flush=True)
        for rec in recs:
            title = str(rec.get("newsTitle", "")).strip()
            news_id = rec.get("newsDetailId", "")
            detail_url = f"https://www.51xf.cn/news/detail/{news_id}" if news_id else ""
            date_str = str(rec.get("validStartTime", ""))[:10] if rec.get("validStartTime") else ""
            if not date_str:
                date_str = str(rec.get("newsDate", ""))[:10] if rec.get("newsDate") else ""
            key = f"{title[:30]}|{date_str}"
            if key in seen_keys or not title:
                continue
            seen_keys.add(key)
            all_items.append({
                "title": title[:200],
                "date": date_str,
                "url": detail_url,
                "category": classify(title),
            })
        await asyncio.sleep(0.5)

    print(f"  杭银消金: {len(all_items)}条", flush=True)
    return all_items


