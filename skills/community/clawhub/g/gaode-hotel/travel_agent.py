#!/usr/bin/env python3
"""高德 POI × 飞猪酒店联动：一句话定位 + 查真实库存 + 出预订链接。

高德负责把任意地名解析成坐标并验证该地点真实存在（飞猪 --poi-name 只锚得住头部景区），
飞猪负责实时房价、房态和可点击的预订链接。
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

GAODE_BASE = os.environ.get("GAODE_POI_BASE", "").rstrip("/")

# 作为"目的地"优先的非住宿类目；住宿服务是我们要订的对象，不该当目的地
DEST_CATS = {
    "科教文化服务", "体育休闲服务", "风景名胜", "购物服务",
    "餐饮服务", "交通设施服务", "生活服务",
}

# 自然语言解析用的城市表，按长度降序匹配，避免"哈尔滨"被"哈"截断
CITY_LIST = sorted([
    "北京", "上海", "广州", "深圳", "成都", "重庆", "杭州", "南京",
    "武汉", "西安", "天津", "苏州", "长沙", "厦门", "青岛", "大连",
    "昆明", "郑州", "济南", "福州", "泉州", "合肥", "南通", "东莞",
    "烟台", "南昌", "汕头", "宁波", "无锡", "佛山", "沈阳", "哈尔滨",
    "长春", "贵阳", "南宁", "太原", "石家庄", "兰州", "银川", "西宁",
    "海口", "三亚", "拉萨", "乌鲁木齐", "呼和浩特", "珠海", "中山",
    "惠州", "温州", "金华", "徐州", "唐山", "临沂", "潍坊", "绍兴",
    "台州", "威海", "桂林", "丽江", "大理",
], key=len, reverse=True)

WEEKDAYS = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6, "天": 6}
CN_NUMS = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
           "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def parse_natural_query(text):
    """从整句话里提取 city/place/check-in/check-out。
    支持：明天/后天/下周X/这周末/下周末/YYYY-MM-DD + 住N晚/N天。
    返回 (city, place, checkin_str, checkout_str)，缺失项返回 None。
    """
    today = datetime.date.today()
    raw = text

    # 1. 城市
    city = None
    for c in CITY_LIST:
        if c in raw:
            city = c
            raw = raw.replace(c, " ", 1)
            break

    # 2. 住几晚
    nights = 1
    m = re.search(r'住\s*([一两三四五六七八九十\d]+)\s*[晚夜天]', raw)
    if m:
        n = m.group(1)
        nights = CN_NUMS.get(n) or int(n)
        raw = raw[:m.start()] + raw[m.end():]

    # 3. 入住日期
    checkin = None
    _date_subs = [
        (r'大后天', lambda: today + datetime.timedelta(days=3)),
        (r'后天',   lambda: today + datetime.timedelta(days=2)),
        (r'明天',   lambda: today + datetime.timedelta(days=1)),
        (r'下[个]?周末|下个周末', lambda: today + datetime.timedelta(
            days=(5 - today.weekday()) % 7 or 7) + datetime.timedelta(days=7)),
        (r'(这|本)?周末', lambda: today + datetime.timedelta(
            days=(5 - today.weekday()) % 7 or 7)),
    ]
    for pat, fn in _date_subs:
        m2 = re.search(pat, raw)
        if m2:
            checkin = fn()
            raw = raw[:m2.start()] + raw[m2.end():]
            break

    if checkin is None:
        m3 = re.search(r'下[个]?周([一二三四五六日天])', raw)
        if m3:
            wd = WEEKDAYS[m3.group(1)]
            checkin = today + datetime.timedelta(days=(wd - today.weekday()) % 7 + 7 or 7)
            raw = raw[:m3.start()] + raw[m3.end():]

    if checkin is None:
        m4 = re.search(r'(这|本)?周([一二三四五六日天])', raw)
        if m4:
            wd = WEEKDAYS[m4.group(2)]
            checkin = today + datetime.timedelta(days=(wd - today.weekday()) % 7 or 7)
            raw = raw[:m4.start()] + raw[m4.end():]

    if checkin is None:
        m5 = re.search(r'(\d{4}-\d{2}-\d{2})', raw)
        if m5:
            checkin = datetime.date.fromisoformat(m5.group(1))
            raw = raw[:m5.start()] + raw[m5.end():]

    if checkin is None:
        m5b = re.search(r'(\d{1,2})月(\d{1,2})[日号]', raw)
        if m5b:
            month, day = int(m5b.group(1)), int(m5b.group(2))
            year = today.year if (month, day) >= (today.month, today.day) else today.year + 1
            checkin = datetime.date(year, month, day)
            raw = raw[:m5b.start()] + raw[m5b.end():]

    if checkin is None:
        m6 = re.search(r'下[个]?周', raw)
        if m6:
            checkin = today + datetime.timedelta(days=(0 - today.weekday()) % 7 + 7 or 7)
            raw = raw[:m6.start()] + raw[m6.end():]

    if checkin is None:
        checkin = today + datetime.timedelta(days=1)

    checkout = checkin + datetime.timedelta(days=nights)

    # 4. 地点：去掉噪音词后取最长剩余 token
    noise = r'[我去在到想要准备打算订找出差旅游旅行玩住宿附近周边，。,.\s]+'
    place_text = re.sub(noise, ' ', raw).strip()
    tokens = [t for t in re.split(r'\s+', place_text) if len(t) >= 2]
    place = max(tokens, key=len) if tokens else None

    return city, place, checkin.isoformat(), checkout.isoformat()


def gaode_get(path, params, key):
    url = GAODE_BASE + path + "?" + urllib.parse.urlencode(params)
    # explicit UA avoids proxy interception on macOS
    req = urllib.request.Request(url, headers={
        "X-API-Key": key,
        "User-Agent": "Mozilla/5.0 (compatible; gaode-hotel/1.0)",
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def gaode_search(q, city, key, page_size=10):
    return gaode_get("/search", {"q": q, "city": city, "page_size": page_size}, key)


def gaode_nearby(lng, lat, key, radius_m=1000, category="餐饮服务", page_size=5):
    return gaode_get("/nearby", {
        "lng": lng, "lat": lat, "radius_m": radius_m,
        "category": category, "page_size": page_size,
    }, key)


def flyai_search_hotel(dest, keywords, checkin, checkout,
                       stars=None, max_price=None, sort="distance_asc",
                       anchor="key-words"):
    """anchor: 'key-words' 用 --key-words（通用），'poi-name' 用 --poi-name（头部景区锚定更准）"""
    flag = "--key-words" if anchor == "key-words" else "--poi-name"
    cmd = ["flyai", "search-hotel", "--dest-name", dest,
           flag, keywords,
           "--check-in-date", checkin, "--check-out-date", checkout,
           "--sort", sort]
    if stars:
        cmd += ["--hotel-stars", stars]
    if max_price:
        cmd += ["--max-price", str(max_price)]
    # up to 3 retries on timeout
    for attempt in range(3):
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if res.returncode != 0:
            if attempt < 2:
                time.sleep(2)
                continue
            sys.stderr.write(res.stderr)
            sys.exit(res.returncode)
        data = json.loads(res.stdout)
        # flyai sometimes returns data: null for obscure keywords
        if data.get("data") is None and attempt < 2:
            time.sleep(2)
            continue
        return data
    return json.loads(res.stdout)


def pick_destination(items, query=""):
    """从高德候选里挑出真正的目的地，避开同名酒店。

    优先级：名称包含查询词的非住宿 POI > 任意非住宿 DEST_CATS > 任意非住宿 > 兜底首条
    """
    if not items:
        return None
    q = query.strip()
    # 1. 名称匹配 + 目的地类目（防止商场内的小店名覆盖商场本身）
    if q:
        for it in items:
            if q in it.get("name", "") and it.get("cat") in DEST_CATS:
                return it
        # 名称匹配但类目不限
        for it in items:
            if q in it.get("name", "") and it.get("cat") != "住宿服务":
                return it
    # 2. 无名称匹配时走原有逻辑
    for it in items:
        if it.get("cat") in DEST_CATS:
            return it
    for it in items:
        if it.get("cat") != "住宿服务":
            return it
    return items[0]


def fmt_hotel_card(h):
    lines = []
    pic = h.get("mainPic")
    if pic:
        lines.append(f"![]({pic})")
    name = h.get("name", "")
    price = h.get("price", "")
    star = h.get("star", "")
    score = h.get("rate", "")
    poi = h.get("interestsPoi", "")
    lines.append(f"### {name}")
    meta = [x for x in [star, f"{score}分" if score and score != "0" else None,
                        price, poi] if x]
    lines.append(" · ".join(meta))
    detail = h.get("detailUrl")
    if detail:
        lines.append(f"[点击预订]({detail})")
    return "\n\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="高德×飞猪一句话订酒店")
    ap.add_argument("--query", default=None,
                    help="自然语言整句，如 '我下周去成都宽窄巷子住两晚'（自动解析城市/地点/日期）")
    ap.add_argument("--city", default=None, help="城市，如 北京")
    ap.add_argument("--place", default=None, help="目的地/景点名，如 798艺术区")
    ap.add_argument("--check-in", default=None, dest="check_in", help="入住日期 YYYY-MM-DD")
    ap.add_argument("--check-out", default=None, dest="check_out", help="退房日期 YYYY-MM-DD")
    ap.add_argument("--stars", default=None, help="星级，如 4,5")
    ap.add_argument("--max-price", type=int, default=None, help="每晚最高价")
    ap.add_argument("--sort", default="distance_asc",
                    help="排序：distance_asc/rate_desc/price_asc/price_desc")
    ap.add_argument("--enrich-nearby", action="store_true",
                    help="附上目的地周边餐饮（高德富化）")
    ap.add_argument("--top", type=int, default=5, help="展示酒店数")
    args = ap.parse_args()

    # 自然语言解析：--query 填补空缺的 city/place/日期
    if args.query:
        q_city, q_place, q_checkin, q_checkout = parse_natural_query(args.query)
        if not args.city:
            args.city = q_city
        if not args.place:
            args.place = q_place
        if not args.check_in:
            args.check_in = q_checkin
        if not args.check_out:
            args.check_out = q_checkout

    missing = [f for f, v in [("--city", args.city), ("--place", args.place),
                               ("--check-in", args.check_in), ("--check-out", args.check_out)] if not v]
    if missing:
        sys.stderr.write(f"缺少必填参数：{' '.join(missing)}（或通过 --query 整句输入）\n")
        sys.exit(2)

    key = os.environ.get("GAODE_POI_KEY")
    if not key:
        sys.stderr.write("缺少环境变量 GAODE_POI_KEY（高德 POI REST key）\n")
        sys.exit(2)

    if not GAODE_BASE:
        sys.stderr.write("缺少环境变量 GAODE_POI_BASE（高德 POI 服务地址，不含末尾斜杠）\n")
        sys.exit(2)

    # 1. 高德解析目的地：验证存在 + 拿坐标 + 拿规范名
    sr = gaode_search(args.place, args.city, key)
    dest = pick_destination(sr.get("items", []), query=args.place)
    if not dest:
        print(f"# 未在{args.city}找到「{args.place}」\n\n高德返回 {sr.get('total', 0)} 条，无可用目的地候选。")
        sys.exit(1)

    # 用规范名喂飞猪；若高德只找到住宿类 POI 说明是泛名词（如"西湖"），
    # 回退用用户原始输入 + poi-name 模式，飞猪对头部景区用 --poi-name 锚更准
    if dest.get("cat") == "住宿服务":
        keyword = args.place
        anchor = "poi-name"
    else:
        keyword = dest["name"]
        anchor = "key-words"

    display_name = args.place if anchor == "poi-name" else dest["name"]
    print(f"# {args.city} · {display_name} 附近酒店\n")
    print(f"基于高德 POI 定位：{dest['name']}（{dest.get('cat','')}）"
          f"坐标 {dest['lng']},{dest['lat']}，{dest.get('address','')}\n")

    # 2. 飞猪查真实库存
    hj = flyai_search_hotel(args.city, keyword,
                            args.check_in, args.check_out,
                            stars=args.stars, max_price=args.max_price,
                            sort=args.sort, anchor=anchor)
    hotels = hj.get("data", {}).get("itemList", [])[:args.top]
    if not hotels:
        print("飞猪暂无匹配库存，换个关键词或扩大星级/价格范围再试。")
        if hj.get("systemMessage"):
            print(f"\n{hj['systemMessage']}")
        return

    print(f"## 飞猪实时库存（{args.check_in} → {args.check_out}）\n")
    for h in hotels:
        print(fmt_hotel_card(h))
        print("\n---\n")

    # 3. 高德富化：目的地周边餐饮
    if args.enrich_nearby:
        try:
            nb = gaode_nearby(dest["lng"], dest["lat"], key)
            items = nb.get("items", [])
            if items:
                print("## 周边餐饮（高德，1km 内）\n")
                for it in items[:5]:
                    r = it.get("rating")
                    rs = f"{r}分" if r else "暂无评分"
                    print(f"- **{it['name']}** · {it.get('cat','')} · {rs} · {it.get('address','')}")
        except Exception as e:
            sys.stderr.write(f"周边富化失败：{e}\n")

    if hj.get("systemMessage"):
        print(f"\n{hj['systemMessage']}")


if __name__ == "__main__":
    main()
