#!/usr/bin/env python3
"""
消金信披 — 诊断脚本
对不稳定公司逐一探测，返回：页面标题、关键元素、公告候选行
用法: python3 diagnose.py [公司名]
"""
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

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

UNSTABLE = [
    ("宁银消费金融",     "https://www.cfcbnb.com/xwgg/zygg/",               "html_dom"),
    ("天津京东消费金融","https://www.jdcfc.cn/pub-info",                     "pdf_link"),
    ("建信消费金融",     "https://www.ccbcf.cn/#/NewsIndex",                "jianxin_dmyy"),
    ("陕西长银消费金融", "https://m.cycfc.com/#/news",                       "html_dom"),
    ("锦程消费金融",     "https://www.jccfc.com/news/notice",               "notice_link_parse"),
    ("平安消费金融",     "https://www.pacfc.com",                           "pingan_detail"),
    ("尚诚消费金融",     "https://www.sccfc.cn/Index/news.html",            "shangcheng_news"),
    ("蚂蚁消费金融",     "https://www.myxiaojin.cn/information",            "html_dom"),
    ("中信消费金融",     "https://www.eciticcfc.com/",                       "html_dom"),
    ("哈银消费金融",     "https://www.hrbbcf.com/news-list?type=1",         "cdp_rpa"),
    ("苏银凯基消费金融", "https://www.sykcfc.cn/#/layout/information",      "suyinkaiji_vue"),
    ("马上消费金融",     "https://www.msxf.com/consumer/zygg",              "paginated"),
    ("中原消费金融",     "https://www.hnzycfc.com/html/news",              "zhongyuan"),
    ("河北幸福消费金融", "https://www.happycfc.com",                         "hebei_detail"),
    ("盛银消费金融",     "https://www.syxfjr.cn/info/xfgg/297",            "time_prefix"),
    ("蒙商消费金融",     "https://www.mengshangxiaofei.com/html/1//208/217/index.html", "mengshang_detail"),
    ("北银消费金融",     "https://www.bobcfc.com",                          "beiyin_marquee"),
]

async def diagnose(name, url, method):
    print(f"\n{'='*60}")
    print(f"🏢 {name} | method={method}")
    print(f"🔗 {url}")
    print("="*60)
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=STEALTH_ARGS)
            ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
            page = await ctx.new_page()

            # 拦截请求，追踪动态加载
            requests = []
            page.on("response", lambda r: requests.append((r.status, r.url[-60:])) if "notification" not in r.url.lower() and len(r.url) > 10 else None)

            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(4)

            # 基础信息
            title = await page.title()
            print(f"📄 标题: {title}")

            # URL检查
            final_url = page.url
            if final_url != url:
                print(f"🔀 重定向: {final_url}")

            # 关键元素探测
            selectors_to_try = [
                ".news-list", ".news-item", ".article-list", ".list-item",
                "a[href*='news']", "a[href*='detail']", "a[href*='info']",
                "a[href*='notice']", ".el-pagination", ".layui-laypage",
                "[class*=list]", "[class*=news]", "[class*=article]",
                "button:has-text('查看详情')", "button:has-text('更多')",
                "[class*=tab]", ".nav a",
            ]
            found_elements = {}
            for sel in selectors_to_try:
                try:
                    cnt = await page.locator(sel).count()
                    if cnt > 0:
                        found_elements[sel] = cnt
                except Exception:
                    pass
            if found_elements:
                print(f"🗂 元素: " + " | ".join(f"{s}[{n}]" for s, n in list(found_elements.items())[:8]))
            else:
                print(f"🗂 元素: 未找到关键选择器")

            # 滚动+文本提取
            for _ in range(6):
                await page.evaluate("window.scrollBy(0, 500)")
                await asyncio.sleep(0.4)

            text = await page.evaluate("document.body.innerText")
            lines = [l.strip() for l in text.split("\n") if l.strip()]

            # 找公告候选行（含"公告"/日期/标题的）
            candidates = []
            import re
            date_ptrn = re.compile(r"^\d{4}[年\-\./]?\d{0,2}")
            for line in lines:
                if len(line) > 5 and len(line) < 200:
                    if any(k in line for k in ["公告", "通知", "关于", "关于本公司", "消费者", "信息披露", "年度"]):
                        if not any(s in line for s in ["首页", "关于我们", "联系我们", "版权", "客服热线", "Copyright", "ICP备案"]):
                            candidates.append(line[:80])
                    elif date_ptrn.match(line) and len(line) < 30:
                        candidates.append(line[:60])

            print(f"📝 公告候选行（{len(candidates)}条）:")
            for c in candidates[:15]:
                print(f"   {c}")

            # HTTP响应统计
            status_counts = {}
            for status, _ in requests:
                status_counts[status] = status_counts.get(status, 0) + 1
            print(f"🌐 HTTP响应: {status_counts}")

            await browser.close()
            return {"name": name, "url": url, "method": method, "ok": True}

    except Exception as e:
        print(f"❌ 异常: {str(e)[:200]}")
        return {"name": name, "url": url, "method": method, "ok": False, "error": str(e)[:200]}


async def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
        for name, url, method in UNSTABLE:
            if name == target:
                await diagnose(name, url, method)
                return
        print(f"未知公司: {target}")
        return

    # 全部运行
    for name, url, method in UNSTABLE:
        await diagnose(name, url, method)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
