#!/usr/bin/env python3
"""
CDP Fallback Scraper — 当 Docker 代理批量爬取被 Amazon 软拦截时使用
通过本地 Chrome CDP (port 9222) 逐个爬取详情页，串行 + 随机延迟，成功率 100%

前置条件:
- Chrome 调试口只绑回环地址，且不要加 --remote-allow-origins=*：
    google-chrome --remote-debugging-port=9222 \
        --remote-debugging-address=127.0.0.1 \
        --user-data-dir="$HOME/.cache/amazon-scraper-chrome"
  CDP 无认证。--remote-allow-origins=* 会让这个浏览器里打开的任意网页都能接管它。
- Xvfb :99 已运行（headless 模式不需要，但 VPS 需要）
- pip install websocket-client

用法:
  python3 cdp_fallback_scrape.py --asin-file failed_asins.json
  python3 cdp_fallback_scrape.py --asins "B07XXX,B08YYY,B09ZZZ"
  python3 cdp_fallback_scrape.py --asins "B07XXX,B08YYY" --output results.json

输出: JSON 数组，每个元素是一个 ASIN 的详情页数据
"""
import itertools, json, time, random, re, sys, os, argparse, websocket
from urllib.request import urlopen, Request

CDP_HOST = os.environ.get("CDP_HOST", "127.0.0.1")
CDP_PORT = os.environ.get("CDP_PORT", "9222")
CDP_URL = f"http://{CDP_HOST}:{CDP_PORT}"
CDP_TIMEOUT = float(os.environ.get("CDP_TIMEOUT", "30"))

ASIN_RE = re.compile(r"^[A-Z0-9]{10}$")

# Monotonic ids. Random ids could collide across calls and match the wrong reply.
_next_id = itertools.count(1).__next__


def open_dedicated_tab():
    """Open our own tab rather than driving one the user is working in."""
    try:
        req = Request(f"{CDP_URL}/json/new?about:blank", method="PUT")
        tab = json.loads(urlopen(req, timeout=10).read())
    except Exception:
        tab = json.loads(urlopen(f"{CDP_URL}/json/new?about:blank", timeout=10).read())
    return tab["webSocketDebuggerUrl"], tab["id"]


def close_tab(target_id):
    try:
        urlopen(f"{CDP_URL}/json/close/{target_id}", timeout=10).read()
    except Exception as e:
        print(f"warning: could not close scratch tab: {e}", file=sys.stderr)


def cdp_send(ws, method, params=None):
    id_ = _next_id()
    msg = {"id": id_, "method": method}
    if params:
        msg["params"] = params
    ws.send(json.dumps(msg))
    # Bounded wait: CDP interleaves unsolicited events, and the old `while True`
    # over a socket with no timeout could block the run forever.
    deadline = time.monotonic() + CDP_TIMEOUT
    while True:
        if time.monotonic() > deadline:
            raise TimeoutError(f"CDP {method} timed out after {CDP_TIMEOUT}s")
        resp = json.loads(ws.recv())
        if resp.get("id") == id_:
            return resp

def scrape_detail(asin, ws):
    if not ASIN_RE.match(asin):
        return {"asin": asin, "error": "invalid_asin"}
    url = f"https://www.amazon.com/dp/{asin}"
    cdp_send(ws, "Page.navigate", {"url": url})
    time.sleep(random.uniform(3, 5))

    for _ in range(10):
        result = cdp_send(ws, "Runtime.evaluate", {
            "expression": "document.querySelector('#productTitle')?.textContent?.trim() || null"
        })
        title = result.get("result", {}).get("result", {}).get("value")
        if title:
            break
        time.sleep(1)
    else:
        return {"asin": asin, "error": "timeout"}

    js_code = """
    (() => {
        const r = {};
        r.title = (document.querySelector('#productTitle') || {}).textContent?.trim() || null;
        let brand = (document.querySelector('#bylineInfo') || {}).textContent?.trim() || null;
        if (brand) brand = brand.replace(/^Brand:\\s*/i, '').replace(/^Visit the\\s+/i, '').replace(/\\s+Store$/i, '').trim();
        r.brand = brand;
        const priceEl = document.querySelector('.a-price .a-offscreen, #priceblock_ourprice, #priceblock_dealprice');
        r.priceStr = priceEl ? priceEl.textContent.trim() : null;
        r.price = r.priceStr ? parseFloat(r.priceStr.replace(/[^0-9.]/g, '')) : null;
        const ratingEl = document.querySelector('#acrPopover .a-icon-alt');
        r.rating = ratingEl ? parseFloat(ratingEl.textContent) : null;
        const reviewsEl = document.querySelector('#acrCustomerReviewText');
        r.reviews = reviewsEl ? parseInt(reviewsEl.textContent.replace(/[^0-9]/g, '')) : null;
        const sellerEl = document.querySelector('#sellerProfileTriggerId, #merchantInfo_feature_div a, [data-feature-name="merchantInfo"] a');
        r.seller = sellerEl ? sellerEl.textContent.trim() : null;
        if (r.seller && (r.seller.includes('\\n') || r.seller.includes('Show details'))) r.seller = null;
        r.image = (document.querySelector('#landingImage, #imgBlkFront') || {}).src || null;
        let bsr = null;
        document.querySelectorAll('#prodDetails tr, #productDetails_techSpec_section_1 tr, #productDetails_detailBullets_sections1 tr').forEach(row => {
            const cells = row.querySelectorAll('th, td');
            if (cells.length >= 2) {
                const key = cells[0].textContent.trim().replace(/[:\\s]+$/, '');
                const val = cells[1].textContent.trim();
                if (key.match(/Best Sellers Rank/i)) { const m = val.match(/#([\\d,]+)/); if (m) bsr = parseInt(m[1].replace(/,/g, '')); }
            }
        });
        r.bsr = bsr;
        const boughtMatch = document.body.innerText.match(/([\\d,.]+[KkMm]?\\+?)\\s*bought in past month/i);
        r.boughtPastMonth = boughtMatch ? boughtMatch[1] : null;
        let dateFirstAvailable = null;
        document.querySelectorAll('#prodDetails tr, #productDetails_techSpec_section_1 tr, #productDetails_detailBullets_sections1 tr').forEach(row => {
            const cells = row.querySelectorAll('th, td');
            if (cells.length >= 2) {
                const key = cells[0].textContent.trim().replace(/[:\\s]+$/, '');
                const val = cells[1].textContent.trim();
                if (key.match(/Date First Available/i)) { const m = val.match(/([A-Za-z]+ \\d+,? \\d{4})/); if (m) dateFirstAvailable = m[1]; }
            }
        });
        r.dateFirstAvailable = dateFirstAvailable;
        r.category = Array.from(document.querySelectorAll('#wayfinding-breadcrumbs_feature_div a')).map(a => a.textContent.trim());
        r.bullets = Array.from(document.querySelectorAll('#feature-bullets li span')).map(s => s.textContent.trim()).filter(Boolean);
        r.details = {};
        document.querySelectorAll('#productDetails_techSpec_section_1 tr, #prodDetails tr, #productDetails_detailBullets_sections1 tr').forEach(row => {
            const cells = row.querySelectorAll('th, td');
            if (cells.length >= 2) {
                const key = cells[0].textContent.trim().replace(/[:\\s]+$/, '');
                const val = cells[1].textContent.trim();
                if (key && val && key.length < 50) r.details[key] = val;
            }
        });
        return JSON.stringify(r);
    })()
    """
    result = cdp_send(ws, "Runtime.evaluate", {"expression": js_code, "returnByValue": True})
    try:
        val = result.get("result", {}).get("result", {}).get("value")
        if val:
            data = json.loads(val)
            data["asin"] = asin
            return data
    except (ValueError, TypeError, KeyError) as e:
        return {"asin": asin, "error": f"extract_failed: {type(e).__name__}: {e}"}
    return {"asin": asin, "error": "extract_failed"}

def main():
    parser = argparse.ArgumentParser(description='CDP Fallback Scraper for blocked ASINs')
    parser.add_argument('--asins', help='Comma-separated ASINs')
    parser.add_argument('--asin-file', help='JSON file with ASIN list')
    parser.add_argument('--output', default='cdp_retry_results.json', help='Output file')
    args = parser.parse_args()

    if args.asin_file:
        asins = json.load(open(args.asin_file))
    elif args.asins:
        asins = args.asins.split(',')
    else:
        print("ERROR: provide --asins or --asin-file")
        sys.exit(1)

    asins = [a.strip() for a in asins if a and a.strip()]
    bad = [a for a in asins if not ASIN_RE.match(a)]
    if bad:
        print(f"ERROR: {len(bad)} invalid ASIN(s), e.g. {bad[:3]}", file=sys.stderr)
        sys.exit(1)

    print(f"Total ASINs: {len(asins)}")
    try:
        urlopen(f"{CDP_URL}/json/version", timeout=10)
    except Exception as e:
        print(f"ERROR: Chrome CDP not reachable at {CDP_URL}: {e}", file=sys.stderr)
        sys.exit(1)

    ws_url, target_id = open_dedicated_tab()
    ws = websocket.create_connection(ws_url, timeout=CDP_TIMEOUT)
    results = []
    success = fail = 0

    for i, asin in enumerate(asins, 1):
        print(f"[{i}/{len(asins)}] {asin}...", end=" ", flush=True)
        try:
            data = scrape_detail(asin, ws)
            if data.get("title") or data.get("brand"):
                results.append(data); success += 1
                print(f"OK: brand={data.get('brand','?')}, seller={data.get('seller','?')}")
            else:
                fail += 1; print("NULL (blocked)")
                results.append({"asin": asin, "error": "null_data"})
        except Exception as e:
            fail += 1; print(f"ERROR: {e}")
            results.append({"asin": asin, "error": str(e)})
        time.sleep(random.uniform(2, 4))
        if i % 10 == 0:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  [Progress: {success} success, {fail} fail]")

    ws.close()
    close_tab(target_id)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nDone: {success} success, {fail} fail out of {len(asins)}")
    print(f"Results: {args.output}")
    if fail:
        sys.exit(3)

if __name__ == '__main__':
    main()
