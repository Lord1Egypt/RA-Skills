#!/usr/bin/env python3
"""Step 3: 批量抓取房源详情页，补齐交付方式/地址/装修/电话等字段。
关键：详情页必须带 referer（列表页） + 随机延迟 3-6s，否则触发 58 antibot 验证码。
用法: python3 fetch_details.py [--config path/to/config.json]
"""
import asyncio, json, re, time, random, os, pathlib, sys
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
REFERER = (f"https://{CFG['city_pinyin']}.zu.anjuke.com/fangyuan/x1/"
           f"?t=1&comm_exist=on&kw={quote(CFG['keyword'])}")

records = json.load(open(OUT + "final_records.json"))
print(f"总房源: {len(records)}")

async def fetch_detail(page, rec):
    url = rec['full_url'] if rec.get('full_url') else rec['url']
    try:
        await page.goto(url, timeout=40000, wait_until="domcontentloaded",
                        referer=REFERER)
        await asyncio.sleep(3 + random.random() * 3)
    except Exception as e:
        return {'status': 'error', 'msg': str(e)[:60]}
    # 验证码检测
    cur = page.url
    if 'verifycode' in cur or 'antibot' in cur:
        try:
            await page.screenshot(path=OUT + f"verify_{rec['id']}.png")
        except Exception:
            pass
        return {'status': 'verify'}
    body = await page.evaluate("document.body ? document.body.innerText : ''")
    title = await page.title()
    d = {'status': 'ok', 'id': rec['id']}
    # 付款/交付方式
    m = re.search(r'付\d押\d|押\d付\d|付一押一|押一付一|押一付二|押一付三|半年付|年付|季付|月付', body)
    d['pay_way'] = m.group(0) if m else ''
    # 详细字段
    m2 = re.search(r'户型[：:]\s*(\S+)', body)
    d['model_full'] = m2.group(1) if m2 else ''
    m3 = re.search(r'面积[：:]\s*([\d.]+)\s*平方米', body)
    d['area_exact'] = m3.group(1) if m3 else ''
    m4 = re.search(r'楼层[：:]\s*(\S+)', body)
    d['floor_full'] = m4.group(1) if m4 else ''
    m5 = re.search(r'装修[：:]\s*(\S+)', body)
    d['decoration'] = m5.group(1) if m5 else ''
    m6 = re.search(r'类型[：:]\s*(\S+)', body)
    d['house_type'] = m6.group(1) if m6 else ''
    m7 = re.search(r'小区[：:]\s*([\u4e00-\u9fa5A-Za-z0-9·]+)\s*\(([^)]*)\)', body)
    if m7:
        d['community_exact'] = m7.group(1)
        d['district_exact'] = m7.group(2)
    # 完整地址（区-街道-路号 模式）
    m8 = re.search(r'([\u4e00-\u9fa5]{2,6}(?:区|县))[\u4e00-\u9fa5A-Za-z0-9\-·]*(?:路|街|大道|巷|支路)[\u4e00-\u9fa5A-Za-z0-9\-·]*\d+号?', body)
    d['address'] = m8.group(0) if m8 else ''
    # 电话：详情页正文电话（排除房屋编码里的）
    phones = re.findall(r'1[3-9]\d{9}', body)
    code = rec.get('id', '')
    real = [p for p in phones if not (code and p in code)]
    d['phone_detail'] = real[0] if real else (phones[0] if phones else '')
    # 朝向/电梯补充
    m9 = re.search(r'朝向[：:]\s*(\S+)', body)
    d['orientation_full'] = m9.group(1) if m9 else ''
    return d

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

        results = {}
        done_file = OUT + "detail_results.json"
        if os.path.exists(done_file):
            results = json.load(open(done_file))
            print(f"已有进度: {len(results)} 条")

        pending = [r for r in records if r['id'] not in results]
        print(f"待抓: {len(pending)}")

        for i, rec in enumerate(pending):
            r = await fetch_detail(page, rec)
            r['record'] = {k: rec.get(k) for k in ['id', 'title', 'community', 'district',
                                                   'rent_min', 'rent_max', 'contact', 'phone', 'url']}
            results[rec['id']] = r
            st = r['status']
            if st == 'verify':
                print(f"[{i+1}/{len(pending)}] {rec['id']} => 验证码, 跳过")
                try:
                    await page.goto(REFERER, timeout=30000, wait_until="domcontentloaded")
                    await asyncio.sleep(6 + random.random() * 4)
                except Exception:
                    pass
            elif st == 'ok':
                print(f"[{i+1}/{len(pending)}] {rec['id']} OK pay={r.get('pay_way','')} phone={r.get('phone_detail','')}")
            else:
                print(f"[{i+1}/{len(pending)}] {rec['id']} ERR {r.get('msg','')}")
            if (i + 1) % 8 == 0:
                json.dump(results, open(done_file, "w"), ensure_ascii=False, indent=1)
                print(f"  -- 进度保存 {len(results)} 条")
            await asyncio.sleep(2 + random.random() * 3)

        json.dump(results, open(done_file, "w"), ensure_ascii=False, indent=1)
        ok = sum(1 for r in results.values() if r['status'] == 'ok')
        vf = sum(1 for r in results.values() if r['status'] == 'verify')
        print(f"\n完成: 总{len(results)} | OK {ok} | 验证码 {vf} | 错误 {len(results)-ok-vf}")
        await browser.close()

asyncio.run(main())
