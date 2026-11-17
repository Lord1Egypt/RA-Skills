#!/usr/bin/env python3
"""Step 1: 抓取安居客租房列表页卡片（文本+HTML），保存供离线精解析。
用法: python3 grab_full.py [--config path/to/config.json]
"""
import asyncio, json, re, random, os, pathlib, sys
from urllib.parse import quote
from playwright.async_api import async_playwright

BASE = pathlib.Path(__file__).resolve().parent

def load_config():
    """查找 config.json：--config 参数 > 当前目录 > 脚本目录 > skill 根目录"""
    cfg_path = None
    if len(sys.argv) >= 3 and sys.argv[1] == "--config":
        cfg_path = pathlib.Path(sys.argv[2])
    else:
        for cand in [pathlib.Path.cwd() / "config.json",
                     BASE / "config.json",
                     BASE.parent / "config.json"]:
            if cand.exists():
                cfg_path = cand
                break
    if cfg_path is None:
        sys.exit("未找到 config.json：请复制 config.example.json 为 config.json 后重试，或用 --config 指定路径")
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    cfg.setdefault("output_dir", str(cfg_path.parent / "output"))
    os.makedirs(cfg["output_dir"], exist_ok=True)
    return cfg

CFG = load_config()
OUT = CFG["output_dir"].rstrip("/") + "/"
CDP = f"http://127.0.0.1:{CFG.get('cdp_port', 9222)}"

def build_urls(cfg):
    """按城市拼音 + 关键词 + 最大页数生成列表页 URL"""
    kw = quote(cfg["keyword"])
    pinyin = cfg["city_pinyin"]
    p1 = f"https://{pinyin}.zu.anjuke.com/fangyuan/x1/?t=1&comm_exist=on&kw={kw}"
    pages = cfg.get("max_pages", 8)
    return [p1] + [f"https://{pinyin}.zu.anjuke.com/fangyuan/x1-p{i}/?t=1&comm_exist=on&kw={kw}"
                   for i in range(2, pages + 1)]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = None
        for pg in ctx.pages:
            if "anjuke" in pg.url:
                page = pg
                break
        if page is None:
            page = await ctx.new_page()
        await page.bring_to_front()

        all_cards = []
        for i, url in enumerate(build_urls(CFG)):
            await page.goto(url, timeout=45000, wait_until="domcontentloaded")
            await asyncio.sleep(3 + random.random() * 2)
            cards = await page.evaluate("""
            () => [...document.querySelectorAll('.zu-itemmod')].map(it => ({
                text: (it.innerText||'').replace(/\\n+/g,' | ').trim(),
                href: (it.querySelector('a[href*="/fangyuan/"], a[href*="/zufang/"]')||{}).href || '',
                html: it.outerHTML
            }))
            """)
            print(f"页{i+1}: {len(cards)} 卡")
            all_cards.extend(cards)
            await asyncio.sleep(1.5)

        # 去重（按 href 的房源ID）
        seen, uniq = set(), []
        for c in all_cards:
            m = re.search(r'/fangyuan/(\d+)', c['href'])
            key = m.group(1) if m else c['href']
            if key not in seen:
                seen.add(key)
                uniq.append(c)
        print(f"去重后: {len(uniq)}")
        with open(OUT + "cards_full.json", "w") as f:
            json.dump(uniq, f, ensure_ascii=False, indent=1)
        with open(OUT + "all_pages.html", "w") as f:
            f.write("\n\n".join(c['html'] for c in uniq))
        print("已存 cards_full.json + all_pages.html")
        await browser.close()

asyncio.run(main())
