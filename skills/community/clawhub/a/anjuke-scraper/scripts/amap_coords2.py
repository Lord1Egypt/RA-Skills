#!/usr/bin/env python3
"""Step 4: 高德 poiInfo 批量获取小区坐标 + 计算距目标地点距离 → coords.json
关键：在 amap.com 页面上下文内 fetch（带登录 cookie + Referer），免 API key。
用法: python3 amap_coords2.py [--config path/to/config.json]
"""
import asyncio, json, os, pathlib, sys
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
CITY = CFG.get("city", "重庆")
TARGET_PLACES = CFG.get("target_places", [])
assert TARGET_PLACES, "config.json 需要 target_places（目标地点搜索词列表）"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = await ctx.new_page()
        await page.goto("https://www.amap.com/", timeout=45000, wait_until="domcontentloaded")
        await asyncio.sleep(4)

        async def poi_search(kw):
            try:
                return await page.evaluate("""
                async (kw) => {
                    const url = 'https://www.amap.com/service/poiInfo?query_type=TQUERY&pagesize=5&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&city=' + encodeURIComponent(CITY) + '&keywords=' + encodeURIComponent(kw);
                    const resp = await fetch(url, {headers: {'Referer': 'https://www.amap.com/'}});
                    return await resp.text();
                }
                """.replace("CITY", json.dumps(CITY)), kw)
            except Exception as e:
                return 'ERR:' + str(e)[:60]

        def extract(body):
            try:
                j = json.loads(body)
                pl = j.get('data', {}).get('poi_list', [])
                return [{'name': x.get('disp_name') or x.get('name', ''),
                         'lng': x.get('longitude'), 'lat': x.get('latitude'),
                         'address': x.get('address', ''), 'id': x.get('id', '')}
                        for x in pl if x.get('longitude')]
            except Exception:
                return []

        # 1. 目标地点（公司/学校等）：依次尝试搜索词
        print("== 目标地点定位 ==")
        company = None
        for q in TARGET_PLACES:
            body = await poi_search(q)
            pois = extract(body)
            for po in pois:
                print(f"  候选: {po['name']} | {po['address']} | {po['lng']},{po['lat']}")
            if pois:
                company = pois[0]
                break
        if company is None:
            print("!! 未找到目标地点，请在 config.json 调整 target_places")
            return
        print("目标地点选用:", json.dumps(company, ensure_ascii=False))

        # 2. 小区坐标
        records = json.load(open(OUT + "final_records.json"))
        communities = []
        for r in records:
            c = r.get('community', '')
            if c and c not in communities:
                communities.append(c)
        print(f"\n去重小区: {len(communities)}")

        results = {}
        for i, c in enumerate(communities):
            body = await poi_search(c + " " + CITY)
            pois = extract(body)
            best = None
            for po in pois:
                if po['name'] == c or (c[:3] and c[:3] in po['name']) or (po['name'][:3] and po['name'][:3] == c[:3]):
                    best = po
                    break
            if not best and pois:
                best = pois[0]
            results[c] = best
            if best:
                print(f"[{i+1}/{len(communities)}] ✓ {c} => {best['name']} ({best['lng']},{best['lat']})")
            else:
                print(f"[{i+1}/{len(communities)}] ✗ {c} 无结果")
            await asyncio.sleep(0.5)

        with open(OUT + "coords.json", "w") as f:
            json.dump({'company': company, 'communities': results}, f, ensure_ascii=False, indent=1)
        ok = sum(1 for v in results.values() if v)
        print(f"\n完成: {ok}/{len(communities)} 小区有坐标")
        await page.close()
        await browser.close()

asyncio.run(main())
