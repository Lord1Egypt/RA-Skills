#!/usr/bin/env python3
"""
Amazon Reviews 瀑布流抓取脚本（CDP page WS 版）

依赖：已启动的 Chrome + 已登录 Amazon。启动时必须把调试口绑在回环地址上，
并且不要加 --remote-allow-origins=*：

  google-chrome --remote-debugging-port=9222 \
      --remote-debugging-address=127.0.0.1 \
      --user-data-dir="$HOME/.cache/amazon-scraper-chrome"

CDP 没有任何认证，谁能连上 9222 就能用你的登录态下单、改地址、导出 cookie。

用法：
  python3 scrape_reviews.py ASIN [TARGET] [DB_PATH] [--reset]

  --reset  删除该 ASIN 的历史评论后重新抓（默认是追加，不删历史）

输出：
  - SQLite DB (reviews 表)
  - JSON 文件 ./reviews_{ASIN}.json（可用 REVIEWS_OUT_DIR 覆盖目录）
"""
import json, urllib.request, websockets, asyncio, sqlite3, time, sys, os
from pathlib import Path

CDP_HOST = os.environ.get("CDP_HOST", "127.0.0.1")
CDP_PORT = os.environ.get("CDP_PORT", "9222")
CDP_BASE = f"http://{CDP_HOST}:{CDP_PORT}"
CDP_TIMEOUT = float(os.environ.get("CDP_TIMEOUT", "30"))


def open_dedicated_tab():
    """Open our own tab instead of driving whatever the user happens to have focused.

    The previous version grabbed the first tab matching 'amazon' and navigated it
    away, which silently destroyed whatever the user was doing in that tab.
    Returns (ws_url, target_id).
    """
    req = urllib.request.Request(f"{CDP_BASE}/json/new?about:blank", method="PUT")
    try:
        tab = json.loads(urllib.request.urlopen(req, timeout=10).read())
    except Exception:
        # Older Chrome builds still accept GET on /json/new.
        tab = json.loads(urllib.request.urlopen(f"{CDP_BASE}/json/new?about:blank", timeout=10).read())
    return tab["webSocketDebuggerUrl"], tab["id"]


def close_tab(target_id):
    try:
        urllib.request.urlopen(f"{CDP_BASE}/json/close/{target_id}", timeout=10).read()
    except Exception as e:
        print(f"warning: could not close scratch tab {target_id}: {e}", file=sys.stderr)


async def scrape(asin, target=100, db_path='amazon_reviews.db', reset=False):
    ws_url, target_id = open_dedicated_tab()

    try:
        async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
            await _scrape_in_tab(ws, asin, target, db_path, reset)
    finally:
        close_tab(target_id)


async def _scrape_in_tab(ws, asin, target, db_path, reset):
        mid = 0
        async def cdp(method, params={}):
            nonlocal mid
            mid += 1
            await ws.send(json.dumps({"id": mid, "method": method, "params": params}))
            # Bounded: CDP streams unsolicited events, so an unmatched id used to
            # block this coroutine forever.
            deadline = time.monotonic() + CDP_TIMEOUT
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"CDP {method} timed out after {CDP_TIMEOUT}s")
                resp = json.loads(await asyncio.wait_for(ws.recv(), timeout=remaining))
                if resp.get("id") == mid:
                    if "error" in resp:
                        raise RuntimeError(f"CDP {method} failed: {resp['error']}")
                    return resp.get("result", {})
        async def eval_js(expr):
            r = await cdp("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
            return r.get("result", {}).get("value")

        # 建库
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asin TEXT, batch INTEGER, review_index INTEGER,
            rating TEXT, title TEXT, body TEXT,
            review_date TEXT, helpful TEXT, verified INTEGER,
            body_length INTEGER, scraped_at TEXT
        )''')
        # Opt-in only. This used to run unconditionally, so a run interrupted by a
        # CAPTCHA left you with neither the old reviews nor the new ones.
        if reset:
            c.execute("DELETE FROM reviews WHERE asin=?", (asin,))
        conn.commit()

        # 导航到 portal 评论页（瀑布流）
        print(f"导航到评论页 ASIN={asin}...")
        await cdp("Page.navigate", {"url": f"https://www.amazon.com/portal/customer-reviews/{asin}"})
        await asyncio.sleep(5)

        all_reviews = []
        click_count = 0
        no_new_streak = 0

        while len(all_reviews) < target:
            # 滚到底部
            await eval_js("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1)

            # 全量提取评论
            reviews = await eval_js("""
                (function() {
                    const items = document.querySelectorAll('[data-hook="review"]');
                    return Array.from(items).map(r => {
                        const bodyEl = r.querySelector('[data-hook="review-body"] span') || r.querySelector('[data-hook="review-body"]');
                        return {
                            rating: r.querySelector('[data-hook="review-star-rating"]')?.innerText?.trim() || '',
                            title: r.querySelector('[data-hook="review-title"]')?.innerText?.trim() || '',
                            body: bodyEl?.innerText?.trim() || '',
                            date: r.querySelector('[data-hook="review-date"]')?.innerText?.trim() || '',
                            helpful: r.querySelector('[data-hook="helpful-vote-statement"]')?.innerText?.trim() || '',
                            verified: !!r.querySelector('[data-hook="avp-badge"]')
                        };
                    });
                })()
            """) or []

            # 去重
            existing = {(r['title'], r['date']) for r in all_reviews}
            new = [r for r in reviews if (r['title'], r['date']) not in existing]

            if new:
                all_reviews.extend(new)
                for r in new:
                    idx = len(all_reviews)
                    c.execute("INSERT INTO reviews (asin,batch,review_index,rating,title,body,review_date,helpful,verified,body_length,scraped_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                        (asin, click_count+1, idx, r['rating'], r['title'], r['body'], r['date'], r['helpful'], int(r['verified']), len(r['body']), time.strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
                print(f"[点击{click_count}后] 新增 {len(new)} 条, 累计 {len(all_reviews)} 条")
                no_new_streak = 0
            else:
                no_new_streak += 1

            if len(all_reviews) >= target:
                break
            if no_new_streak >= 5:
                print("⚠️ 连续 5 次无新增，退出")
                break

            # 点击 "Show 10 more reviews" — 必须用精确 selector
            clicked = await eval_js("""
                (function() {
                    const a = document.querySelector('.cm-cr-show-more a');
                    if (a) { a.click(); return true; }
                    return false;
                })()
            """)
            if not clicked:
                # The old fallback exec'd /tmp/jev-ultrafast/.venv/bin/python, a path any
                # local user can create. Running an interpreter out of a world-writable
                # directory is arbitrary code execution; there is no safe version of it.
                print("❌ 按钮消失或 selector 失效，没有更多评论")
                break

            click_count += 1
            await asyncio.sleep(2)  # AJAX 1 秒就加载完，2 秒足够

        all_reviews = all_reviews[:target]

        # 统计
        print(f"\n{'='*60}")
        print(f"总计: {len(all_reviews)} 条评论 (点击 {click_count} 次)")
        total_chars = sum(len(r['body']) for r in all_reviews)
        avg_len = total_chars // len(all_reviews) if all_reviews else 0
        verified_count = sum(1 for r in all_reviews if r['verified'])
        ratings = {}
        for r in all_reviews:
            k = r['rating'].split('out')[0].strip()
            ratings[k] = ratings.get(k, 0) + 1
        print(f"总字符: {total_chars}, 平均: {avg_len} 字符/条")
        print(f"已验证购买: {verified_count}/{len(all_reviews)}")
        print(f"评分分布: {dict(sorted(ratings.items(), reverse=True))}")

        c.execute("SELECT COUNT(*) FROM reviews WHERE asin=?", (asin,))
        print(f"DB: {db_path} ({c.fetchone()[0]} 条)")
        conn.close()

        # Review text is third-party personal data; /tmp is world-readable.
        out_dir = Path(os.environ.get('REVIEWS_OUT_DIR', '.'))
        out_dir.mkdir(parents=True, exist_ok=True)
        json_path = out_dir / f'reviews_{asin}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(all_reviews, f, ensure_ascii=False, indent=2)
        os.chmod(json_path, 0o600)
        print(f"JSON: {json_path}")

        return all_reviews

if __name__ == '__main__':
    argv = [a for a in sys.argv[1:] if a != '--reset']
    reset = '--reset' in sys.argv
    if not argv:
        print(__doc__)
        sys.exit(1)
    asin = argv[0]
    target = int(argv[1]) if len(argv) > 1 else 100
    db = argv[2] if len(argv) > 2 else 'amazon_reviews.db'
    asyncio.run(scrape(asin, target, db, reset=reset))
