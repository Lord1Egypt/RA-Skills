#!/usr/bin/env python3
"""
flight-price-monitor: 机票价格监控与多平台比价
通过SCF代理查询飞猪/途牛/RG实时机票价格

用法:
  python3 compare.py search --from "北京" --to "上海" --date 2026-07-01
  python3 compare.py compare --from "北京" --to "上海" --date 2026-07-01 --flight-no "CA1234"
  python3 compare.py calendar --from "北京" --to "上海" --start-date 2026-07-01 --days 14
  python3 compare.py monitor --from "北京" --to "三亚" --date 2026-07-01 [--target 800] [--threshold 10]
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta

# HTTP请求（使用标准urllib，TLS证书验证默认开启）
import urllib.request
import urllib.error

# ============================================================
# 配置
# ============================================================

PROXY_TOKEN = "tp_8k2mX9vQ4z"

# 代理地址
SCF_FLIGGY_URL = "https://1439498936-6sysdjjt99.ap-guangzhou.tencentscf.com"
SCF_TUNIU_URL = "https://1439498936-0junm3maxj.ap-guangzhou.tencentscf.com"
SCF_RG_URL = "https://1439498936-460a7b6oqn.ap-guangzhou.tencentscf.com"

HEADERS = {
    "Content-Type": "application/json",
    "X-Proxy-Token": PROXY_TOKEN,
}

# ============================================================
# 航线常识价格区间（经济舱单程，单位：元）
# ============================================================

ROUTE_PRICE_REF = {
    # 北京出发
    "北京-上海": (350, 700, 1500),
    "北京-广州": (400, 800, 1800),
    "北京-深圳": (400, 850, 1800),
    "北京-成都": (350, 750, 1600),
    "北京-重庆": (350, 700, 1500),
    "北京-杭州": (300, 600, 1300),
    "北京-南京": (300, 550, 1200),
    "北京-武汉": (300, 600, 1300),
    "北京-长沙": (300, 600, 1300),
    "北京-西安": (300, 600, 1400),
    "北京-昆明": (400, 850, 1800),
    "北京-三亚": (500, 1100, 2500),
    "北京-厦门": (350, 700, 1600),
    "北京-大连": (250, 500, 1100),
    "北京-青岛": (250, 500, 1100),
    "北京-哈尔滨": (300, 650, 1400),
    # 上海出发
    "上海-广州": (350, 700, 1500),
    "上海-深圳": (350, 700, 1500),
    "上海-成都": (350, 750, 1600),
    "上海-重庆": (350, 700, 1500),
    "上海-武汉": (250, 500, 1100),
    "上海-长沙": (250, 550, 1200),
    "上海-西安": (300, 650, 1400),
    "上海-昆明": (400, 850, 1800),
    "上海-三亚": (450, 1000, 2200),
    "上海-厦门": (250, 500, 1100),
    "上海-青岛": (250, 500, 1100),
    "上海-大连": (250, 550, 1200),
    "上海-哈尔滨": (350, 750, 1600),
    # 广州/深圳出发
    "广州-成都": (300, 650, 1400),
    "广州-重庆": (300, 600, 1300),
    "广州-杭州": (250, 550, 1200),
    "广州-武汉": (250, 500, 1100),
    "广州-昆明": (300, 700, 1500),
    "深圳-成都": (300, 650, 1400),
    "深圳-杭州": (250, 550, 1200),
    "深圳-重庆": (300, 600, 1300),
    # 西南出发
    "成都-昆明": (200, 450, 1000),
    "成都-重庆": (150, 350, 800),
    "成都-西安": (250, 550, 1200),
    "成都-武汉": (250, 550, 1200),
    "重庆-昆明": (200, 450, 1000),
    "重庆-西安": (250, 550, 1200),
    # 其他热门
    "杭州-厦门": (200, 400, 900),
    "杭州-深圳": (250, 550, 1200),
    "武汉-三亚": (350, 750, 1600),
    "西安-昆明": (250, 550, 1200),
}

# 节假日/旺季日期（2026年）
PEAK_DATES = {
    "春运": ("2026-01-25", "2026-02-22"),
    "清明": ("2026-04-03", "2026-04-06"),
    "五一": ("2026-05-01", "2026-05-05"),
    "端午": ("2026-05-30", "2026-06-01"),
    "暑假": ("2026-07-01", "2026-08-31"),
    "中秋": ("2026-09-25", "2026-09-27"),
    "国庆": ("2026-10-01", "2026-10-07"),
    "寒假": ("2026-01-15", "2026-02-22"),
}

# 城市三字码映射
CITY_CODES = {
    "北京": "BJS", "上海": "SHA", "广州": "CAN", "深圳": "SZX",
    "成都": "CTU", "重庆": "CKG", "杭州": "HGH", "南京": "NKG",
    "武汉": "WUH", "长沙": "CSX", "西安": "SIA", "昆明": "KMG",
    "三亚": "SYX", "厦门": "XMN", "大连": "DLC", "青岛": "TAO",
    "哈尔滨": "HRB", "天津": "TSN", "郑州": "CGO", "福州": "FOC",
    "济南": "TNA", "沈阳": "SHE", "长春": "CGQ", "贵阳": "KWE",
    "兰州": "LHW", "乌鲁木齐": "URC", "拉萨": "LXA", "海口": "HAK",
    "宁波": "NGB", "合肥": "HFE", "南昌": "KHN", "太原": "TYN",
}


def get_route_key(from_city, to_city):
    return f"{from_city}-{to_city}"


def get_route_price_range(from_city, to_city):
    key = get_route_key(from_city, to_city)
    if key in ROUTE_PRICE_REF:
        return ROUTE_PRICE_REF[key]
    rev_key = get_route_key(to_city, from_city)
    if rev_key in ROUTE_PRICE_REF:
        return ROUTE_PRICE_REF[rev_key]
    return None


def is_peak_season(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        for name, (start, end) in PEAK_DATES.items():
            if datetime.strptime(start, "%Y-%m-%d") <= d <= datetime.strptime(end, "%Y-%m-%d"):
                return True, name
    except ValueError:
        pass
    return False, None


def get_weekday_weight(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        wd = d.weekday()
        weights = {0: 0.95, 1: 0.88, 2: 0.88, 3: 0.92, 4: 1.05, 5: 1.12, 6: 1.08}
        return weights.get(wd, 1.0)
    except ValueError:
        return 1.0


# ============================================================
# 价格监控分析引擎
# ============================================================

def analyze_price_status(price, from_city, to_city, dep_date, all_prices=None, target_price=None, last_price=None):
    """
    价格状态分析引擎（监控视角）
    返回: {status, reasons[], alert, savings}
    status: "low" / "fair" / "high" / "expensive"
    """
    reasons = []
    status_scores = []

    # 1. 航线常识价格分位
    price_range = get_route_price_range(from_city, to_city)
    percentile = None
    if price_range:
        low, avg, high = price_range
        percentile = (price - low) / (high - low) if high > low else 0.5
        percentile = max(0, min(1, percentile))

        if percentile <= 0.2:
            reasons.append(f"¥{price}处于该航线极低价区间（{int(percentile*100)}%分位），低于均价¥{avg}")
            status_scores.append(-3)  # 负数=价格低=好消息
        elif percentile <= 0.4:
            reasons.append(f"¥{price}低于该航线均价¥{avg}（{int(percentile*100)}%分位），价格合理")
            status_scores.append(-1)
        elif percentile <= 0.6:
            reasons.append(f"¥{price}接近该航线均价¥{avg}（{int(percentile*100)}%分位），中等水平")
            status_scores.append(0)
        elif percentile <= 0.8:
            reasons.append(f"¥{price}高于该航线均价¥{avg}（{int(percentile*100)}%分位），偏贵")
            status_scores.append(2)
        else:
            reasons.append(f"¥{price}远高于该航线均价¥{avg}（{int(percentile*100)}%分位），很贵")
            status_scores.append(4)
    else:
        reasons.append("该航线暂无参考价格区间")
        status_scores.append(0)

    # 2. 距出发天数
    try:
        dep_dt = datetime.strptime(dep_date, "%Y-%m-%d")
        days_left = (dep_dt - datetime.now()).days

        if days_left < 3:
            reasons.append(f"距出发仅{days_left}天，临期价格大概率维持高位或继续上涨")
            status_scores.append(3)
        elif days_left < 7:
            reasons.append(f"距出发{days_left}天，已进入涨价区间")
            status_scores.append(2)
        elif days_left <= 21:
            reasons.append(f"距出发{days_left}天，处于国内航线价格相对稳定期")
            status_scores.append(0)
        elif days_left <= 45:
            reasons.append(f"距出发{days_left}天，处于提前购票优惠期，仍有降价空间")
            status_scores.append(-1)
        else:
            reasons.append(f"距出发{days_left}天，航司尚未放出低价舱位，后续可能更低")
            status_scores.append(-2)
    except ValueError:
        days_left = None

    # 3. 旺季判断
    is_peak, peak_name = is_peak_season(dep_date)
    if is_peak:
        reasons.append(f"出发日处于{peak_name}旺季，价格易涨难跌")
        status_scores.append(3)

    # 4. 多源价差
    if all_prices and len(all_prices) >= 2:
        valid_prices = [p for p in all_prices if p and p > 0]
        if len(valid_prices) >= 2:
            min_p = min(valid_prices)
            max_p = max(valid_prices)
            spread = (max_p - min_p) / min_p * 100 if min_p > 0 else 0
            if spread > 20:
                reasons.append(f"多平台价差{spread:.0f}%（¥{min_p}~¥{max_p}），最低价可能不持续太久")
                status_scores.append(1)
            elif spread > 10:
                reasons.append(f"多平台价差{spread:.0f}%，有一定选择空间")
                status_scores.append(0)
            else:
                reasons.append(f"多平台价差仅{spread:.0f}%，价格趋于一致")
                status_scores.append(0)

    # 5. 星期效应
    wd_weight = get_weekday_weight(dep_date)
    try:
        dep_dt = datetime.strptime(dep_date, "%Y-%m-%d")
        weekdays_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        wd_name = weekdays_cn[dep_dt.weekday()]
        if wd_weight <= 0.9:
            reasons.append(f"出发日{wd_name}，属于低价出行日")
            status_scores.append(-1)
        elif wd_weight >= 1.05:
            reasons.append(f"出发日{wd_name}，属于高价出行日")
            status_scores.append(1)
    except ValueError:
        pass

    # 6. 目标价对比（监控专用）
    if target_price and target_price > 0:
        if price <= target_price:
            reasons.append(f"✅ 已达到目标价¥{target_price}！当前¥{price}，低于目标¥{target_price - price}")
            status_scores.append(-5)
        else:
            gap = price - target_price
            gap_pct = gap / target_price * 100
            reasons.append(f"距目标价¥{target_price}还差¥{gap}（{gap_pct:.0f}%）")
            status_scores.append(1)

    # 7. 价格变动（上次对比）
    if last_price and last_price > 0:
        change = price - last_price
        change_pct = change / last_price * 100
        if change < 0:
            reasons.append(f"📉 较上次查询降价¥{abs(change)}（{abs(change_pct):.0f}%）")
            status_scores.append(-2)
        elif change > 0:
            reasons.append(f"📈 较上次查询涨价¥{change}（{change_pct:.0f}%）")
            status_scores.append(2)
        else:
            reasons.append("价格与上次查询持平")

    # 综合判断
    total = sum(status_scores)

    if total <= -3:
        status = "low"
        status_emoji = "🟢"
        status_text = "价格较低"
        alert = True
    elif total <= 0:
        status = "fair"
        status_emoji = "🟡"
        status_text = "价格适中"
        alert = False
    elif total <= 3:
        status = "high"
        status_emoji = "🟠"
        status_text = "价格偏高"
        alert = False
    else:
        status = "expensive"
        status_emoji = "🔴"
        status_text = "价格很高"
        alert = False

    # 如果达到目标价，强制alert
    if target_price and target_price > 0 and price <= target_price:
        alert = True

    # 计算潜在节省（与最高价对比）
    savings = None
    if all_prices and len(all_prices) >= 2:
        valid = [p for p in all_prices if p and p > 0]
        if len(valid) >= 2:
            savings = max(valid) - min(valid)

    # 购票时机建议
    timing = "观望"
    if total <= -3:
        timing = "建议尽快入手"
    elif total <= 0:
        timing = "可以入手，也可再等等"
    elif total <= 3 and is_peak:
        timing = "旺季价格偏高但易涨难跌"
    elif total <= 3:
        timing = "建议继续观望"

    return {
        "status": status,
        "status_emoji": status_emoji,
        "status_text": status_text,
        "alert": alert,
        "timing": timing,
        "reasons": reasons,
        "price_percentile": int(percentile * 100) if percentile is not None else None,
        "route_price_range": {"low": price_range[0], "avg": price_range[1], "high": price_range[2]} if price_range else None,
        "savings": savings,
        "is_peak": is_peak,
        "peak_name": peak_name if is_peak else None,
        "days_left": days_left if 'days_left' in dir() else None,
        "target_hit": bool(target_price and target_price > 0 and price <= target_price),
    }


# ============================================================
# HTTP请求
# ============================================================

def http_post(url, body, timeout=25):
    """发送POST请求到代理服务，返回JSON结果。数据流向：用户查询参数 → 代理服务 → 旅游平台 → 结果返回。"""
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "detail": e.read().decode("utf-8", errors="replace")}


# ============================================================
# 数据源查询
# ============================================================

def search_fliggy_flights(from_city, to_city, dep_date):
    """飞猪机票搜索"""
    try:
        resp = http_post(SCF_FLIGGY_URL, {
            "type": "search_flight",
            "params": {
                "origin": from_city,
                "destination": to_city,
                "depDate": dep_date,
                "journeyType": 1,
                "adultCount": 1,
            },
        })

        data = resp.get("data", {})
        items = data.get("itemList", [])

        flights = []
        for item in items:
            journeys = item.get("journeys", [])
            if not journeys:
                continue
            journey = journeys[0]
            segments = journey.get("segments", [])
            if not segments:
                continue

            seg = segments[0]
            price_str = item.get("ticketPrice", "0")
            try:
                price = float(price_str)
            except (ValueError, TypeError):
                price = 0

            airline_name = seg.get("marketingTransportName", "")
            if "|" in airline_name:
                airline_name = airline_name.split("|")[-1]

            flight = {
                "source": "飞猪",
                "flight_no": seg.get("marketingTransportNo", ""),
                "airline": airline_name,
                "price": price,
                "dep_time": seg.get("depDateTime", "")[11:16] if seg.get("depDateTime") else "",
                "arr_time": seg.get("arrDateTime", "")[11:16] if seg.get("arrDateTime") else "",
                "dep_airport": seg.get("depStationShortName", seg.get("depStationName", "")),
                "arr_airport": seg.get("arrStationShortName", seg.get("arrStationName", "")),
                "duration": journey.get("totalDuration", ""),
                "url": item.get("jumpUrl", ""),
                "cabin": seg.get("seatClassName", "经济舱"),
            }
            flights.append(flight)

        return {"source": "飞猪", "flights": flights, "error": None}
    except Exception as e:
        return {"source": "飞猪", "flights": [], "error": str(e)}


def search_tuniu_flights(from_city, to_city, dep_date):
    """途牛机票搜索"""
    try:
        resp = http_post(SCF_TUNIU_URL, {
            "type": "tuniu_flight_search",
            "params": {
                "departureCityName": from_city,
                "arrivalCityName": to_city,
                "departureDate": dep_date,
            },
        })

        data = resp.get("data", {})
        if isinstance(data, dict) and data.get("error"):
            return {"source": "途牛", "flights": [], "error": data["error"]}

        flight_list = data.get("data", []) if isinstance(data, dict) else data
        if not isinstance(flight_list, list):
            flight_list = []

        flights = []
        for f in flight_list:
            try:
                price = float(f.get("basePrice", 0))
            except (ValueError, TypeError):
                price = 0

            dep_time_full = f.get("departureTime", "")
            arr_time_full = f.get("arrivalTime", "")
            dep_time = dep_time_full.split(" ")[-1][:5] if dep_time_full else ""
            arr_time = arr_time_full.split(" ")[-1][:5] if arr_time_full else ""

            flight = {
                "source": "途牛",
                "flight_no": f.get("flightNumber", ""),
                "airline": f.get("airlineCompany", ""),
                "price": price,
                "dep_time": dep_time,
                "arr_time": arr_time,
                "dep_airport": f.get("departureAirport", ""),
                "arr_airport": f.get("arrivalAirport", ""),
                "duration": f.get("totalDuration", f.get("flyTime", "")),
                "remaining_seats": f.get("remainingSeats", ""),
                "cabin": f.get("cabinClass", "经济舱"),
            }
            flights.append(flight)

        return {"source": "途牛", "flights": flights, "error": None}
    except Exception as e:
        return {"source": "途牛", "flights": [], "error": str(e)}


def search_rg_flights(from_city, to_city, dep_date):
    """RG机票搜索（备用）"""
    try:
        from_code = CITY_CODES.get(from_city, from_city)
        to_code = CITY_CODES.get(to_city, to_city)

        resp = http_post(SCF_RG_URL, {
            "type": "flight",
            "params": {
                "from_city": from_code,
                "to_city": to_code,
                "from_date": dep_date,
                "trip_type": "ONE_WAY",
                "adult_number": 1,
                "cabin_grade": "ECONOMY",
            },
        })

        data = resp.get("data", {})
        flight_list = data.get("flightInformationList", [])

        if not flight_list:
            return {"source": "RG", "flights": [], "error": "无结果（API可能暂时不可用）"}

        flights = []
        for f in flight_list:
            try:
                price = float(f.get("price", 0))
            except (ValueError, TypeError):
                price = 0

            flight = {
                "source": "RG",
                "flight_no": f.get("flightNo", ""),
                "airline": f.get("airline", ""),
                "price": price,
                "dep_time": f.get("departureTime", ""),
                "arr_time": f.get("arrivalTime", ""),
                "dep_airport": f.get("departureAirport", ""),
                "arr_airport": f.get("arrivalAirport", ""),
                "duration": f.get("duration", ""),
                "url": f.get("bookingUrl", ""),
                "cabin": "经济舱",
            }
            flights.append(flight)

        return {"source": "RG", "flights": flights, "error": None}
    except Exception as e:
        return {"source": "RG", "flights": [], "error": str(e)}


# ============================================================
# 航班跨平台匹配
# ============================================================

def match_flight_cross_platform(flight_no, candidates):
    """按航班号匹配跨平台航班"""
    if not flight_no:
        return []
    fn = flight_no.strip().upper()
    matched = []
    for c in candidates:
        c_fn = c.get("flight_no", "").strip().upper()
        if c_fn == fn:
            matched.append(c)
    return matched


# ============================================================
# 主命令
# ============================================================

def cmd_search(args):
    """搜索航班（多源合并+价格状态分析）"""
    from_city = args.from_city
    to_city = args.to_city
    dep_date = args.dep_date

    # 并行查询
    fliggy_result = search_fliggy_flights(from_city, to_city, dep_date)
    tuniu_result = search_tuniu_flights(from_city, to_city, dep_date)
    rg_result = search_rg_flights(from_city, to_city, dep_date)

    # 合并航班
    all_flights = []

    if fliggy_result.get("flights"):
        all_flights.extend(fliggy_result["flights"])

    # 途牛去重
    if tuniu_result.get("flights"):
        existing_fns = {f["flight_no"].upper() for f in all_flights if f.get("flight_no")}
        for tf in tuniu_result["flights"]:
            fn = tf.get("flight_no", "").upper()
            if fn and fn in existing_fns:
                for af in all_flights:
                    if af.get("flight_no", "").upper() == fn:
                        af["tuniu_price"] = tf.get("price", 0)
                        break
            else:
                all_flights.append(tf)
                existing_fns.add(fn)

    # 按价格排序（佣金优先级：RG>飞猪>途牛）
    commission_order = {"RG": 0, "飞猪": 1, "途牛": 2}
    all_flights.sort(key=lambda x: (x.get("price", 99999) if x.get("price", 0) > 0 else 99999, commission_order.get(x.get("source", ""), 9)))

    # 取最低价生成价格状态分析
    lowest = None
    for f in all_flights:
        if f.get("price", 0) > 0:
            lowest = f
            break

    price_analysis = None
    if lowest:
        all_prices = [f["price"] for f in all_flights if f.get("price", 0) > 0]
        price_analysis = analyze_price_status(lowest["price"], from_city, to_city, dep_date, all_prices, target_price=getattr(args, 'target', None))

    output = {
        "success": True,
        "action": "search",
        "from": from_city,
        "to": to_city,
        "date": dep_date,
        "flights_count": len(all_flights),
        "flights": all_flights[:20],
        "sources": {
            "飞猪": {"count": len(fliggy_result.get("flights", [])), "error": fliggy_result.get("error")},
            "途牛": {"count": len(tuniu_result.get("flights", [])), "error": tuniu_result.get("error")},
            "RG": {"count": len(rg_result.get("flights", [])), "error": rg_result.get("error")},
        },
        "lowest_price": lowest["price"] if lowest else None,
        "lowest_flight": lowest["flight_no"] if lowest else None,
        "lowest_source": lowest["source"] if lowest else None,
        "price_analysis": price_analysis,
        "tip": "选定航班后告诉我航班号，可以多平台精确比价！" if all_flights else "该航线暂无航班数据",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_compare(args):
    """指定航班号多平台精确比价"""
    from_city = args.from_city
    to_city = args.to_city
    dep_date = args.dep_date
    flight_no = args.flight_no.strip().upper()

    # 查所有平台
    fliggy_result = search_fliggy_flights(from_city, to_city, dep_date)
    tuniu_result = search_tuniu_flights(from_city, to_city, dep_date)
    rg_result = search_rg_flights(from_city, to_city, dep_date)

    # 按航班号匹配
    results = []

    # 飞猪匹配
    fg_matched = match_flight_cross_platform(flight_no, fliggy_result.get("flights", []))
    if fg_matched:
        best = fg_matched[0]
        results.append({
            "source": "飞猪",
            "matched": True,
            "flight_no": best["flight_no"],
            "airline": best["airline"],
            "price": best["price"],
            "dep_time": best["dep_time"],
            "arr_time": best["arr_time"],
            "dep_airport": best["dep_airport"],
            "arr_airport": best["arr_airport"],
            "duration": best["duration"],
            "url": best.get("url", ""),
            "cabin": best["cabin"],
        })
    else:
        results.append({"source": "飞猪", "matched": False, "error": "未找到该航班"})

    # 途牛匹配
    tn_matched = match_flight_cross_platform(flight_no, tuniu_result.get("flights", []))
    if tn_matched:
        best = tn_matched[0]
        results.append({
            "source": "途牛",
            "matched": True,
            "flight_no": best["flight_no"],
            "airline": best["airline"],
            "price": best["price"],
            "dep_time": best["dep_time"],
            "arr_time": best["arr_time"],
            "dep_airport": best["dep_airport"],
            "arr_airport": best["arr_airport"],
            "duration": best["duration"],
            "cabin": best["cabin"],
        })
    else:
        results.append({"source": "途牛", "matched": False, "error": "未找到该航班"})

    # RG匹配
    rg_matched = match_flight_cross_platform(flight_no, rg_result.get("flights", []))
    if rg_matched:
        best = rg_matched[0]
        results.append({
            "source": "RG",
            "matched": True,
            "flight_no": best["flight_no"],
            "airline": best["airline"],
            "price": best["price"],
            "dep_time": best["dep_time"],
            "arr_time": best["arr_time"],
            "dep_airport": best["dep_airport"],
            "arr_airport": best["arr_airport"],
            "duration": best["duration"],
            "url": best.get("url", ""),
            "cabin": best["cabin"],
        })
    else:
        results.append({"source": "RG", "matched": False, "error": "未找到该航班"})

    # 按价格排序（佣金优先级同价时RG排前）
    priced = [r for r in results if r.get("matched") and r.get("price") and isinstance(r["price"], (int, float)) and r["price"] > 0]
    unpriced = [r for r in results if r not in priced]
    commission_order = {"RG": 0, "飞猪": 1, "途牛": 2}
    priced.sort(key=lambda x: (x["price"], commission_order.get(x.get("source", ""), 9)))

    all_sorted = priced + unpriced

    # 价格分析
    all_prices = [r["price"] for r in priced]
    price_analysis = None
    if priced:
        price_analysis = analyze_price_status(
            priced[0]["price"], from_city, to_city, dep_date, all_prices,
            target_price=getattr(args, 'target', None),
            last_price=getattr(args, 'last_price', None),
        )

    output = {
        "success": True,
        "action": "compare",
        "flight_no": flight_no,
        "from": from_city,
        "to": to_city,
        "date": dep_date,
        "platforms": all_sorted,
        "lowest_price": priced[0]["price"] if priced else None,
        "lowest_platform": priced[0]["source"] if priced else None,
        "lowest_url": priced[0].get("url") if priced else None,
        "price_analysis": price_analysis,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_calendar(args):
    """低价日历（扫描多日价格）"""
    from_city = args.from_city
    to_city = args.to_city
    start_date = args.start_date
    days = min(args.days, 30)

    calendar = []

    for i in range(days):
        try:
            d = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
            date_str = d.strftime("%Y-%m-%d")
        except ValueError:
            continue

        # 查飞猪（速度快，数据全）
        result = search_fliggy_flights(from_city, to_city, date_str)
        flights = result.get("flights", [])

        if flights:
            prices = [f["price"] for f in flights if f.get("price", 0) > 0]
            lowest = min(prices) if prices else None
            calendar.append({
                "date": date_str,
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][d.weekday()],
                "lowest_price": lowest,
                "flight_count": len(flights),
                "cheapest_flight": flights[0]["flight_no"] if flights else None,
                "url": flights[0].get("url", "") if flights else "",
            })
        else:
            calendar.append({
                "date": date_str,
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][d.weekday()],
                "lowest_price": None,
                "flight_count": 0,
                "cheapest_flight": None,
                "url": "",
            })

        time.sleep(0.3)

    # 标注价格标签
    priced_days = [d for d in calendar if d.get("lowest_price")]
    if priced_days:
        min_price = min(d["lowest_price"] for d in priced_days)
        avg_price = sum(d["lowest_price"] for d in priced_days) / len(priced_days)

        for d in calendar:
            p = d.get("lowest_price")
            if p:
                if p <= min_price * 1.05:
                    d["tag"] = "🟢 低价"
                elif p <= avg_price:
                    d["tag"] = "🟡 适中"
                else:
                    d["tag"] = "🔴 偏贵"
            else:
                d["tag"] = "— 无数据"

        # 最便宜日期的价格状态
        cheapest = min(priced_days, key=lambda x: x["lowest_price"])
        price_analysis = analyze_price_status(cheapest["lowest_price"], from_city, to_city, cheapest["date"])
    else:
        price_analysis = None
        min_price = None
        avg_price = None

    output = {
        "success": True,
        "action": "calendar",
        "from": from_city,
        "to": to_city,
        "start_date": start_date,
        "days": days,
        "calendar": calendar,
        "min_price": min_price,
        "avg_price": int(avg_price) if avg_price else None,
        "cheapest_date": cheapest["date"] if priced_days else None,
        "price_analysis": price_analysis,
        "tip": "🟢标记的日期是价格洼地，适合入手" if priced_days else "暂无数据",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_monitor(args):
    """生成降价监控任务（供宿主Agent定时执行）"""
    from_city = args.from_city
    to_city = args.to_city
    dep_date = args.dep_date
    target = args.target
    threshold = args.threshold or 10

    # 先查一次当前价格
    fliggy_result = search_fliggy_flights(from_city, to_city, dep_date)
    tuniu_result = search_tuniu_flights(from_city, to_city, dep_date)
    rg_result = search_rg_flights(from_city, to_city, dep_date)

    all_flights = []
    for r in [fliggy_result, tuniu_result, rg_result]:
        if r.get("flights"):
            all_flights.extend(r["flights"])

    all_prices = [f["price"] for f in all_flights if f.get("price", 0) > 0]
    current_lowest = min(all_prices) if all_prices else None

    # 价格分析
    price_analysis = None
    if current_lowest:
        price_analysis = analyze_price_status(current_lowest, from_city, to_city, dep_date, all_prices, target_price=target)

    # 航线常识价
    route_range = get_route_price_range(from_city, to_city)
    suggested_target = None
    if route_range and current_lowest:
        # 建议目标价=均价*0.85（比均价低15%算好价）
        suggested_target = int(route_range[1] * 0.85)
    elif current_lowest:
        suggested_target = int(current_lowest * 0.85)

    monitor = {
        "success": True,
        "action": "monitor",
        "route": f"{from_city}→{to_city}",
        "from": from_city,
        "to": to_city,
        "date": dep_date,
        "current_lowest": current_lowest,
        "target_price": target or suggested_target,
        "suggested_target": suggested_target,
        "threshold_percent": threshold,
        "price_analysis": price_analysis,
        "check_command": f"python3 scripts/compare.py search --from \"{from_city}\" --to \"{to_city}\" --date {dep_date}",
        "frequency": "daily",
        "created_at": datetime.now().isoformat(),
        "status": "active",
        "tip": f"当前最低¥{current_lowest}，建议设目标价¥{suggested_target}（航线均价85折）" if suggested_target and current_lowest else "已创建监控任务",
    }
    print(json.dumps(monitor, ensure_ascii=False, indent=2))


# ============================================================
# CLI入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="机票价格监控与多平台比价")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # search
    search_p = subparsers.add_parser("search", help="搜索航班+价格状态分析")
    search_p.add_argument("--from", dest="from_city", required=True, help="出发城市")
    search_p.add_argument("--to", dest="to_city", required=True, help="到达城市")
    search_p.add_argument("--date", dest="dep_date", required=True, help="出发日期 YYYY-MM-DD")
    search_p.add_argument("--target", type=int, default=None, help="目标价格（可选）")

    # compare
    compare_p = subparsers.add_parser("compare", help="指定航班号多平台精确比价")
    compare_p.add_argument("--from", dest="from_city", required=True, help="出发城市")
    compare_p.add_argument("--to", dest="to_city", required=True, help="到达城市")
    compare_p.add_argument("--date", dest="dep_date", required=True, help="出发日期 YYYY-MM-DD")
    compare_p.add_argument("--flight-no", dest="flight_no", required=True, help="航班号，如 CA1234")
    compare_p.add_argument("--target", type=int, default=None, help="目标价格")
    compare_p.add_argument("--last-price", type=int, default=None, help="上次查询价格（用于对比变动）")

    # calendar
    cal_p = subparsers.add_parser("calendar", help="低价日历")
    cal_p.add_argument("--from", dest="from_city", required=True, help="出发城市")
    cal_p.add_argument("--to", dest="to_city", required=True, help="到达城市")
    cal_p.add_argument("--start-date", dest="start_date", required=True, help="起始日期 YYYY-MM-DD")
    cal_p.add_argument("--days", type=int, default=14, help="扫描天数（最多30）")

    # monitor
    mon_p = subparsers.add_parser("monitor", help="生成降价监控任务")
    mon_p.add_argument("--from", dest="from_city", required=True, help="出发城市")
    mon_p.add_argument("--to", dest="to_city", required=True, help="到达城市")
    mon_p.add_argument("--date", dest="dep_date", required=True, help="出发日期 YYYY-MM-DD")
    mon_p.add_argument("--target", type=int, default=None, help="目标价格")
    mon_p.add_argument("--threshold", type=int, default=10, help="降价提醒阈值百分比")

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args)
    elif args.command == "compare":
        cmd_compare(args)
    elif args.command == "calendar":
        cmd_calendar(args)
    elif args.command == "monitor":
        cmd_monitor(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
