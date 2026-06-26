#!/usr/bin/env python3
"""
消金信披采集 — 统一入口（Phase 1+2 合并版）
═══════════════════════════════════════════════════════════════════
Phase 1+2: 列表采集 → 详情页正文/图片/PDF 同步完成
    输出: announcements.json（含完整text字段）
         content/{id}/fulltext.txt + attachments/

执行:
    python3 collect.py                          # 全量（30家，3次重试）
    python3 collect.py --company "湖北消费金融"   # 指定公司
    python3 collect.py --date 2026-04-15        # 指定日期目录
    python3 collect.py --resume                 # 增量（保留历史数据）
    python3 collect.py --retry 1 --delay 0      # 快速测试
    python3 collect.py --check                   # 检查浏览器状态
    python3 collect.py --no-detail              # 仅列表，不抓详情（快速验证）
    python3 collect.py --workers 3               # 并发浏览器数（默认3）
"""
import argparse
import asyncio
import hashlib
import json
import re
import shutil
import sys
import time
from datetime import date
from pathlib import Path

# ── 路径设置 ─────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
OUT_BASE = ROOT.parent.parent / "cfc_raw_data"
TODAY = str(date.today())

# ── 核心模块 ─────────────────────────────────────────────────────────────────
sys.path.insert(0, str(ROOT))
from core import extract_from_text, classify
from collectors import COLLECTORS

# ── Playwright 参数（WSL2 已验证）──────────────────────────────────────────────
STEALTH_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-blink-features=AutomationControlled",
    "--disable-web-security",
    "--enable-webgl",
    "--ignore-certificate-errors",
    "--allow-running-insecure-content",
    "--headless=new",
]

# ── 常量 ─────────────────────────────────────────────────────────────────────
MIN_TEXT_LEN_FOR_DETAIL_SKIP = 150   # title/正文超过此长度则跳过详情页抓取


# ═══════════════════════════════════════════════════════════════════════════════
# 浏览器管理
# ═══════════════════════════════════════════════════════════════════════════════
class Browser:
    """统一浏览器生命周期。每个公司独立 ctx/page。"""

    def __init__(self):
        self._pw = None
        self._browser = None
        self._extra_args = []

    def set_extra_args(self, args):
        self._extra_args = args

    async def launch(self):
        if self._browser:
            return self._browser
        from playwright.async_api import async_playwright
        self._pw = await async_playwright().start()
        launch_args = list(STEALTH_ARGS)
        for a in self._extra_args:
            if a not in launch_args:
                launch_args.append(a)
        self._browser = await self._pw.chromium.launch(
            headless=True,
            args=launch_args,
        )
        return self._browser

    async def new_page(self) -> "page":
        browser = await self.launch()
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            no_viewport=True,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        return await ctx.new_page()

    async def close(self):
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._pw:
            await self._pw.stop()
            self._pw = None


# ═══════════════════════════════════════════════════════════════════════════════
# Phase 2 — 详情页处理器（按优先级匹配）
# ═══════════════════════════════════════════════════════════════════════════════

def _content_id(url: str) -> str:
    """从URL生成稳定的内容ID"""
    return hashlib.md5(url.encode()).hexdigest()[:8]


async def _fetch_html_detail(page, url: str) -> tuple[str, list]:
    """
    通用HTML详情页抓取。
    返回: (fulltext, attachments[])
    attachments: [{"filename": "...", "path": "...", "type": "pdf|image"}]
    """
    import trafilatura
    attachments = []

    try:
        # 方法1: trafilatura（快速，适合静态页）
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            if text and len(text) > 50:
                return text.strip(), attachments
    except Exception:
        pass

    # 方法2: Playwright 直接提取（JS渲染页）
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        await asyncio.sleep(3)

        # 提取正文
        text = await page.evaluate("""
() => {
    // 移除干扰元素
    const remove = sel => document.querySelectorAll(sel).forEach(e => e.remove());
    remove('.header, .footer, .nav, .sidebar, .breadcrumb, .ad, script, style');

    // 找主要内容区
    const candidates = [
        '.content', '.article', '.main', '#content', '#main',
        '[class*=content]', '[class*=article]', '[class*=detail]'
    ];
    for (const sel of candidates) {
        const el = document.querySelector(sel);
        if (el && el.innerText.length > 200) {
            return el.innerText.trim();
        }
    }
    return document.body.innerText.trim();
}
        """)

        if text and len(text) > 50:
            # 下载页面中的图片和PDF
            atts = await _extract_attachments(page, url)
            return text.strip(), atts

    except Exception:
        pass

    return "", attachments


async def _extract_attachments(page, base_url: str) -> list:
    """从页面提取并下载 PDF/图片附件"""
    attachments = []
    try:
        links = await page.evaluate("""
() => {
    const links = document.querySelectorAll('a[href], img[src]');
    const results = [];
    for (const el of links) {
        const url = el.href || el.src;
        if (!url || url.startsWith('javascript') || url === '#') continue;
        const fname = (el.href ? el.getAttribute('download') : null) ||
                      url.split('/').pop().split('?')[0];
        if (fname && (fname.endsWith('.pdf') || fname.match(/\\.(png|jpg|jpeg|gif|webp)$/i))) {
            if (fname.length < 200) {
                results.push({url, fname, type: fname.endsWith('.pdf') ? 'pdf' : 'image'});
            }
        }
    }
    return results;
}
        """)
        for att in links:
            try:
                att_path = await _download_attachment(att, page)
                if att_path:
                    attachments.append({
                        "filename": att["fname"],
                        "path": str(att_path),
                        "type": att["type"],
                    })
            except Exception:
                pass
    except Exception:
        pass
    return attachments


async def _download_attachment(att: dict, page) -> Path:
    """下载单个附件到 content/{id}/attachments/"""
    import urllib.request
    content_dir = Path(sys.argv[0]).parent  # will be overridden by caller
    att_dir = content_dir / "attachments"
    att_dir.mkdir(parents=True, exist_ok=True)

    fname = att["fname"]
    url = att["url"]

    # 如果是相对路径，拼成绝对路径
    if not url.startswith("http"):
        from urllib.parse import urljoin
        url = urljoin(page.url, url)

    filepath = att_dir / fname
    if filepath.exists():
        return filepath

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            with open(filepath, "wb") as f:
                f.write(r.read())
        return filepath
    except Exception:
        return None


async def _fetch_pdf_detail(page, url: str) -> tuple[str, list]:
    """PDF 详情页：下载 PDF + pdfplumber 解析文本。
    
    改进：先探测 Content-Type，若为 HTML 则改用 HTML 处理器（处理.shtml实为HTML的情况）。"""
    attachments = []
    text = ""

    # 先探测 Content-Type
    ct = ""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            ct = r.headers.get("Content-Type", "")
            # 如果是 HTML，说明 URL 不是 PDF，改用 HTML 处理器
            if "text/html" in ct:
                html_text, html_atts = await _fetch_html_detail(page, url)
                return html_text, html_atts
    except Exception:
        pass

    # 下载 PDF
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
            filepath = Path("/tmp") / url.split("/")[-1]
            if not filepath.suffix or filepath.suffix == ".pdf" and not data[:4] == b"%PDF":
                # 探测实际文件类型
                if data[:4] == b"%PDF":
                    filepath = filepath.with_suffix(".pdf")
                elif data[:2] in (b"PK", b"PK\r"):
                    filepath = filepath.with_suffix(".zip")
                else:
                    filepath = filepath.with_suffix(".html")
            with open(filepath, "wb") as f:
                f.write(data)

        attachments.append({
            "filename": filepath.name,
            "path": str(filepath),
            "type": "pdf",
        })

        # 解析 PDF
        if filepath.suffix == ".pdf":
            try:
                import pdfplumber
                with pdfplumber.open(filepath) as pdf:
                    for pg in pdf.pages:
                        t = pg.extract_text() or ""
                        text += t + "\n"
            except Exception:
                pass

    except Exception:
        pass

    return text.strip(), attachments


async def _fetch_image_detail(page, url: str, ann: dict = None, item_dir: Path = None) -> tuple[str, list]:
    """
    图片正文页：优先用列表页 _truncated 文本（海尔等），
    否则下载图片到 content/{id}/，Phase 2 做 VLM OCR。
    """
    attachments = []

    # 优先用 _truncated（列表页预览文本，已含真实内容）
    if ann and ann.get("_truncated"):
        return ann["_truncated"], []

    # 下载图片到 content/{id}/image.png
    if item_dir:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            img_ext = Path(url).suffix or ".png"
            img_path = item_dir / f"image{img_ext}"
            with urllib.request.urlopen(req, timeout=15) as r:
                with open(img_path, "wb") as f:
                    f.write(r.read())
            attachments.append({
                "filename": img_path.name,
                "path": str(img_path),
                "type": "image",
            })
        except Exception:
            pass

    return "", attachments




async def _fetch_vue_detail(page, url: str) -> tuple[str, list]:
    """Vue SPA 详情页：等待JS渲染后提取正文"""
    attachments = []

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        await asyncio.sleep(5)

        text = await page.evaluate("""
() => {
    const remove = sel => document.querySelectorAll(sel).forEach(e => e.remove());
    remove('.header, .footer, .nav, .sidebar, .breadcrumb, script, style');
    const el = document.querySelector('.content, .article, #content, main, [class*=detail]');
    return el ? el.innerText.trim() : document.body.innerText.trim();
}
        """)
        if text and len(text) > 50:
            atts = await _extract_attachments(page, url)
            attachments.extend(atts)
            return text.strip(), attachments
    except Exception:
        pass

    return "", attachments


async def _fetch_cloudflare_detail(page, url: str) -> tuple[str, list]:
    """Cloudflare 保护页：用 Playwright stealth 模式"""
    attachments = []

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(5)  # 等待 Cloudflare 验证通过

        text = await page.evaluate("""
() => {
    const remove = sel => document.querySelectorAll(sel).forEach(e => e.remove());
    remove('.header, .footer, .nav, .sidebar, script, style');
    const el = document.querySelector('.content, .article, #content, main');
    return el ? el.innerText.trim() : document.body.innerText.trim();
}
        """)

        if text and len(text) > 50:
            atts = await _extract_attachments(page, url)
            attachments.extend(atts)
            return text.strip(), attachments

    except Exception:
        pass

    return "", attachments


def _select_detail_handler(url: str) -> str:
    """
    根据URL选择详情页处理器。
    返回处理器名: html | pdf | image | vue | cloudflare
    """
    url_lower = url.lower()

    # Cloudflare 保护域名
    if any(domain in url_lower for domain in [
        "boccfc.cn", "sykcfc.cn", "hncy58.com",
    ]):
        return "cloudflare"

    # PDF URL（部分消金PDF链接不带.pdf扩展名，如 /P0XXXXXXXXXXXXXXX/）
    if ".pdf" in url_lower or "pdf" in url_lower:
        return "pdf"
    # P0XXXXXXXXXXXXXXXX 格式（常见于消金债权转让PDF）
    if re.search(r"/P0\d{10,}[^/]*$", url_lower):
        return "pdf"

    # 图片URL
    if any(ext in url_lower for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp", "/img", "/image"]):
        return "image"

    # Vue SPA
    if "#" in url or any(pat in url_lower for pat in ["vue", "mpvue", "/m/", "/h5/"]):
        return "vue"

    return "html"


async def fetch_detail_for_announcement(
    page,
    ann: dict,
    content_dir: Path,
) -> dict:
    """
    为单条公告抓取详情页正文。
    - 如果列表页已有长正文（>MIN_TEXT_LEN），直接使用，跳过详情页
    - 否则根据URL类型选择处理器
    - 下载附件到 content/{id}/attachments/
    - 图片下载后返回空文本（OCR 在 Phase 2 执行）
    返回更新后的 ann（含 text, _content_type, _attachments）
    """
    url = ann.get("url", "")
    title = ann.get("title", "")

    # 内容目录
    cid = _content_id(url)
    item_dir = content_dir / cid
    item_dir.mkdir(parents=True, exist_ok=True)
    att_dir = item_dir / "attachments"
    att_dir.mkdir(parents=True, exist_ok=True)

    ann["_content_id"] = cid

    # 如果列表页已有长正文（title 或 _truncated），直接使用
    list_text = ann.get("_truncated", "") or title
    if len(list_text) > MIN_TEXT_LEN_FOR_DETAIL_SKIP:
        ann["text"] = list_text
        ann["_content_type"] = "list_page"
        ann["_attachments"] = []

        # 保存到 fulltext.txt
        (item_dir / "fulltext.txt").write_text(list_text, encoding="utf-8")

        print(f"    [skip detail] {cid} 列表页正文 {len(list_text)}字", flush=True)
        return ann

    # 没有 URL，无法抓详情
    if not url or url == "#":
        ann["text"] = title
        ann["_content_type"] = "no_url"
        ann["_attachments"] = []
        print(f"    [skip] {cid} 无URL", flush=True)
        return ann

    # 选择处理器
    handler_name = _select_detail_handler(url)
    ann["_content_type"] = handler_name

    print(f"    [fetch {handler_name}] {cid} {url[:60]}", flush=True)

    try:
        if handler_name == "pdf":
            text, attachments = await _fetch_pdf_detail(page, url)
        elif handler_name == "image":
            text, attachments = await _fetch_image_detail(page, url, ann=ann, item_dir=item_dir)
        elif handler_name == "cloudflare":
            text, attachments = await _fetch_cloudflare_detail(page, url)
        elif handler_name == "vue":
            text, attachments = await _fetch_vue_detail(page, url)
        else:
            text, attachments = await _fetch_html_detail(page, url)

        ann["text"] = text or title  # 保底用列表页标题
        ann["_attachments"] = attachments

        # 保存 fulltext.txt
        (item_dir / "fulltext.txt").write_text(ann["text"], encoding="utf-8")

        if text:
            print(f"      -> 正文 {len(text)}字, 附件 {len(attachments)}个", flush=True)
        else:
            print(f"      -> 详情页无内容，保底使用列表标题 {len(title)}字", flush=True)

    except Exception as e:
        ann["text"] = title
        ann["_attachments"] = []
        ann["_fetch_error"] = str(e)[:100]
        print(f"      -> 抓取失败: {e}", flush=True)

    return ann


# ═══════════════════════════════════════════════════════════════════════════════
# Phase 1+2 合并采集
# ═══════════════════════════════════════════════════════════════════════════════

async def run_company(
    name: str,
    url: str,
    method: str,
    out_dir: Path,
    retry: int = 3,
    since_date: str = None,
    no_detail: bool = False,
) -> dict:
    """
    Phase 1+2 合并采集：
    1. 列表页采集（复用 COLLECTORS 方法）
    2. 详情页抓取（对每条URL调用 fetch_detail_for_announcement）
    3. 保存 announcements.json（含 text 字段）+ content/{id}/

    返回 dict: {"company", "method", "count", "status", "errors", "with_text", "without_text"}
    """
    import datetime
    # suyinkaiji 需要特殊参数绕过 Cloudflare
    SUYIN_ARGS = [
        "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
        "--disable-blink-features=AutomationControlled",
        "--disable-web-security", "--enable-webgl",
        "--allow-running-insecure-content", "--headless=new",
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    ]
    browser = Browser()
    if "suyinkaiji" in method:
        browser.set_extra_args(SUYIN_ARGS)
    result = {
        "company": name,
        "method": method,
        "count": 0,
        "status": "error",
        "errors": [],
        "with_text": 0,    # 有详情正文的条数
        "without_text": 0,  # 只有列表标题的条数
    }
    valid = []

    # ── 增量合并：加载已有数据 ───────────────────────────────────────
    company_dir = out_dir / name
    existing = []
    if company_dir.exists():
        existing_file = company_dir / "announcements.json"
        if existing_file.exists():
            try:
                existing = json.loads(existing_file.read_text(encoding="utf-8"))
            except Exception:
                existing = []

    # 去重 key
    existing_keys = {f"{it.get('title','')[:30]}|{it.get('date','')}" for it in existing}

    for attempt in range(1, retry + 1):
        try:
            page = await browser.new_page()
            collector = COLLECTORS.get(method) or COLLECTORS.get("html_dom")

            print(f"\n▶ {name} ({method}){' [仅列表]' if no_detail else ''}", flush=True)
            items = await collector(page, url)
            await page.close()

            errors = [i for i in items if i.get("title", "").startswith("ERROR:")]
            fetched = [
                i for i in items
                if not i.get("title", "").startswith("ERROR:") and i.get("date")
            ]

            # ── 增量日期过滤 ─────────────────────────────────────────
            if since_date:
                try:
                    since_dt = datetime.datetime.strptime(since_date, "%Y-%m-%d").date()
                    fetched = [
                        i for i in fetched
                        if datetime.datetime.strptime(i["date"][:10], "%Y-%m-%d").date()
                        >= since_dt
                    ]
                except Exception:
                    pass

            # ── 与历史合并（去重）────────────────────────────────────
            merged = list(existing)
            for it in fetched:
                key = f"{it['title'][:30]}|{it['date']}"
                if key not in existing_keys:
                    merged.append(it)
                    existing_keys.add(key)

            valid = merged
            print(f"  列表采集: +{len(fetched)}条 / 合并后 {len(valid)}条", flush=True)

            # ── Phase 2: 详情页抓取（跳过 no_detail 模式）──────────
            if not no_detail:
                print(f"  Phase 2 详情页抓取 ({len(valid)}条)...", flush=True)
                detail_page = await browser.new_page()

                with_text = 0
                without_text = 0

                for ann in valid:
                    # 已有 text 字段且长度足够，跳过
                    if ann.get("text") and len(ann.get("text", "")) > MIN_TEXT_LEN_FOR_DETAIL_SKIP:
                        with_text += 1
                        continue

                    ann = await fetch_detail_for_announcement(
                        detail_page, ann, company_dir
                    )
                    if ann.get("text") and len(ann.get("text", "")) > MIN_TEXT_LEN_FOR_DETAIL_SKIP:
                        with_text += 1
                    else:
                        without_text += 1

                    # 进度输出（每10条）
                    idx = valid.index(ann)
                    if (idx + 1) % 10 == 0:
                        print(f"    详情页进度: {idx+1}/{len(valid)}", flush=True)

                await detail_page.close()
                result["with_text"] = with_text
                result["without_text"] = without_text
                print(f"  Phase 2 完成: 有正文 {with_text}条 / 仅标题 {without_text}条", flush=True)

            result["count"] = len(valid)
            result["status"] = "ok"
            result["errors"] = [e["title"] for e in errors]
            break

        except Exception as e:
            err_str = str(e)[:200]
            print(f"  ❌ {name} 异常 (attempt {attempt}): {err_str}", flush=True)
            result["errors"].append(f"ERROR: {err_str}")
            if attempt < retry:
                await asyncio.sleep(2 ** (attempt - 1))
        finally:
            try:
                await browser.close()
            except Exception:
                pass

    # ── 写文件 ─────────────────────────────────────────────────────
    out_dir.mkdir(parents=True, exist_ok=True)
    company_dir.mkdir(parents=True, exist_ok=True)

    with open(company_dir / "announcements.json", "w", encoding="utf-8") as f:
        json.dump(valid, f, ensure_ascii=False, indent=2)

    # 索引文件
    categories = {}
    for it in valid:
        cat = it.get("category", "其他")
        categories[cat] = categories.get(cat, 0) + 1

    with open(company_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump({
            "company": name,
            "url": url,
            "method": method,
            "collect_date": TODAY,
            "status": result["status"],
            "count": result["count"],
            "retry": result["retry"] if "retry" in result else 1,
            "with_text": result.get("with_text", 0),
            "without_text": result.get("without_text", 0),
            "categories": categories,
            "errors": result["errors"][:5],
        }, f, ensure_ascii=False, indent=2)

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def parse_args():
    p = argparse.ArgumentParser(
        description="消费金融官网信披采集 Phase 1+2 合并",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 collect.py                          # 全量
  python3 collect.py --company "湖北消费金融"   # 指定公司
  python3 collect.py --resume                  # 增量（保留历史）
  python3 collect.py --no-detail               # 仅列表，快速验证
  python3 collect.py --workers 3                # 并发浏览器数
        """,
    )
    p.add_argument("--resume", action="store_true", help="增量模式（保留历史数据）")
    p.add_argument("--retry", type=int, default=3, help="单家公司最大重试次数（默认3）")
    p.add_argument("--delay", type=float, default=2.0, help="公司间延迟秒数（默认2）")
    p.add_argument("--company", default=None, help="指定公司（逗号分隔）")
    p.add_argument("--date", default=None, help="采集日期（默认今天）")
    p.add_argument("--check", action="store_true", help="检查浏览器状态")
    p.add_argument("--since", default=None, help="增量起始日期（YYYY-MM-DD）")
    p.add_argument("--incremental", action="store_true", help="自动推断增量起始日期")
    p.add_argument("--no-detail", action="store_true", help="仅列表采集，不抓详情页（快速验证模式）")
    return p.parse_args()


async def cmd_check():
    from playwright.async_api import async_playwright

    print("检查 Playwright Chromium...")
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True, args=STEALTH_ARGS)
            print("✅ Chromium 可用")
            await browser.close()
        except Exception as e:
            print(f"❌ Chromium 启动失败: {e}")


async def cmd_collect(args):
    collect_date = args.date or TODAY
    out_dir = Path(OUT_BASE) / collect_date

    # ── 确定 since_date（增量起始日期）───────────────────────────────
    since_date = None
    if args.incremental or args.since:
        if args.since:
            since_date = args.since
            since_label = f"指定日期 {since_date} 起"
        else:
            date_dirs = sorted(
                [d for d in OUT_BASE.iterdir() if d.is_dir() and d.name.startswith("20")],
                reverse=True,
            )
            latest_dir = date_dirs[0] if date_dirs else None
            if latest_dir and (latest_dir / "_summary.json").exists():
                try:
                    prev = json.loads((latest_dir / "_summary.json").read_text())
                    since_date = prev.get("last_run_date") or latest_dir.name
                    since_label = f"上次采集 {since_date} 起（自动推断）"
                except Exception:
                    since_date = latest_dir.name
                    since_label = f"最新目录 {since_date} 起（自动推断）"
            else:
                since_date = None
                since_label = "无法推断，执行全量"

    # ── 清理或保留输出目录 ───────────────────────────────────────────
    if not args.resume:
        shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── 加载公司配置 ───────────────────────────────────────────────
    cfg_file = ROOT / "companies.json"
    cfg = json.loads(cfg_file.read_text(encoding="utf-8"))
    companies = cfg["companies"]

    if args.company:
        names = {n.strip() for n in args.company.split(",")}
        companies = [c for c in companies if c["name"] in names]
        print(f"已筛选 {len(companies)} 家公司: {names}", flush=True)

    print(f"""
╔══════════════════════════════════════════════════════╗
║  消金信披采集 Phase 1+2  {collect_date}                    ║
║  公司: {len(companies)}家  重试:{args.retry}次  延迟:{args.delay}秒            ║
║  详情: {'是' if not args.no_detail else '否（仅列表）'}        ║
║  输出: {str(out_dir)[:46]}  ║""", flush=True)
    if since_date:
        print(f"║  增量: {since_label}          ║")
    print(f"╚══════════════════════════════════════════════════════╝", flush=True)

    results = []
    for c in companies:
        r = await run_company(
            name=c["name"],
            url=c["url"],
            method=c["method"],
            out_dir=out_dir,
            retry=args.retry,
            since_date=since_date,
            no_detail=args.no_detail,
        )
        results.append(r)

        status = "✅" if r["status"] == "ok" else "❌"
        print(
            f"{status} {r['company']}: {r['count']}条 "
            f"(有正文{r.get('with_text',0)} / 仅标题{r.get('without_text',0)})",
            flush=True,
        )

        if args.delay > 0:
            await asyncio.sleep(args.delay)

    # ── 汇总 ────────────────────────────────────────────────────────
    total = sum(r["count"] for r in results)
    ok_count = sum(1 for r in results if r["status"] == "ok")
    total_with_text = sum(r.get("with_text", 0) for r in results)
    total_without_text = sum(r.get("without_text", 0) for r in results)

    print(f"\n{'='*60}")
    print(f"采集完成: {ok_count}/{len(results)}家公司成功")
    print(f"总条数: {total}条 (有正文 {total_with_text} / 仅标题 {total_without_text})")
    print(f"输出: {out_dir}")

    # 写入汇总
    summary = {
        "collect_date": collect_date,
        "last_run_date": TODAY,
        "total_companies": len(results),
        "total": total,
        "ok": ok_count,
        "with_text": total_with_text,
        "without_text": total_without_text,
        "results": [
            {
                "company": r["company"],
                "method": r["method"],
                "count": r["count"],
                "status": r["status"],
                "with_text": r.get("with_text", 0),
                "without_text": r.get("without_text", 0),
            }
            for r in results
        ],
    }
    with open(out_dir / "_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


def main():
    args = parse_args()

    if args.check:
        asyncio.run(cmd_check())
    else:
        asyncio.run(cmd_collect(args))


if __name__ == "__main__":
    main()
