#!/usr/bin/env python3
"""携程国内机票查询 API — 支持城市/省份查询及多机场比价"""

import json, sys, re, ssl, uuid, hashlib, random, time
import urllib.request, urllib.error
from datetime import datetime, timedelta
from pathlib import Path

try:
    import quickjs
except ImportError:
    sys.exit("缺少依赖: pip install quickjs")

SCRIPT_DIR = Path(__file__).parent
COOKIE_CACHE = SCRIPT_DIR / ".cookie_cache.json"
CSIGN_JS = SCRIPT_DIR / "_extract" / "c-sign.js"

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# ============ 城市 & 省份 ============
CITY_INFO = {
    "北京": {"code": "BJS", "id": 1, "prov": 1},
    "上海": {"code": "SHA", "id": 2, "prov": 2},
    "广州": {"code": "CAN", "id": 32, "prov": 7},
    "深圳": {"code": "SZX", "id": 30, "prov": 7},
    "珠海": {"code": "ZUH", "id": 33, "prov": 7},
    "成都": {"code": "CTU", "id": 104, "prov": 21},
    "杭州": {"code": "HGH", "id": 17, "prov": 11},
    "温州": {"code": "WNZ", "id": 21, "prov": 11},
    "宁波": {"code": "NGB", "id": 13, "prov": 11},
    "武汉": {"code": "WUH", "id": 477, "prov": 8},
    "西安": {"code": "SIA", "id": 7, "prov": 24},
    "重庆": {"code": "CKG", "id": 158, "prov": 22},
    "南京": {"code": "NKG", "id": 12, "prov": 10},
    "天津": {"code": "TSN", "id": 154, "prov": 3},
    "长沙": {"code": "CSX", "id": 148, "prov": 9},
    "三亚": {"code": "SYX", "id": 43, "prov": 26},
    "海口": {"code": "HAK", "id": 37, "prov": 26},
    "昆明": {"code": "KMG", "id": 100, "prov": 25},
    "丽江": {"code": "LJG", "id": 311, "prov": 25},
    "西双版纳": {"code": "JHG", "id": 109, "prov": 25},
    "厦门": {"code": "XMN", "id": 25, "prov": 13},
    "福州": {"code": "FOC", "id": 26, "prov": 13},
    "大连": {"code": "DLC", "id": 39, "prov": 4},
    "沈阳": {"code": "SHE", "id": 58, "prov": 4},
    "青岛": {"code": "TAO", "id": 5, "prov": 15},
    "济南": {"code": "TNA", "id": 3, "prov": 15},
    "哈尔滨": {"code": "HRB", "id": 151, "prov": 5},
    "长春": {"code": "CGQ", "id": 152, "prov": 5},
    "郑州": {"code": "CGO", "id": 180, "prov": 6},
    "贵阳": {"code": "KWE", "id": 99, "prov": 23},
    "太原": {"code": "TYN", "id": 163, "prov": 14},
    "兰州": {"code": "LHW", "id": 184, "prov": 28},
    "乌鲁木齐": {"code": "URC", "id": 171, "prov": 31},
    "南宁": {"code": "NNG", "id": 168, "prov": 20},
    "桂林": {"code": "KWL", "id": 28, "prov": 20},
    "合肥": {"code": "HFE", "id": 16, "prov": 12},
    "南昌": {"code": "KHN", "id": 146, "prov": 16},
}

PROVINCE_CITIES = {
    "广东": ["广州", "深圳", "珠海"],
    "浙江": ["杭州", "温州", "宁波"],
    "福建": ["厦门", "福州"],
    "山东": ["青岛", "济南"],
    "辽宁": ["大连", "沈阳"],
    "海南": ["三亚", "海口"],
    "云南": ["昆明", "丽江", "西双版纳"],
    "广西": ["南宁", "桂林"],
    "黑龙江": ["哈尔滨"],
    "吉林": ["长春"],
    "河南": ["郑州"],
    "湖北": ["武汉"],
    "湖南": ["长沙"],
    "江苏": ["南京"],
    "江西": ["南昌"],
    "安徽": ["合肥"],
    "陕西": ["西安"],
    "四川": ["成都"],
    "贵州": ["贵阳"],
    "山西": ["太原"],
    "甘肃": ["兰州"],
    "新疆": ["乌鲁木齐"],
    "天津": ["天津"],
    "重庆": ["重庆"],
    "北京": ["北京"],
    "上海": ["上海"],
}


def resolve_location(name: str) -> list[str]:
    """
    解析地点名称，返回城市列表。
    支持城市名、三字码、省份名。省份会展开为该省所有有机场的城市。
    """
    name = name.strip()
    if name in PROVINCE_CITIES:
        return PROVINCE_CITIES[name]
    if name in CITY_INFO:
        return [name]
    for c, info in CITY_INFO.items():
        if info["code"] == name.upper():
            return [c]
    raise ValueError(f"'{name}' 无法识别。支持城市: {', '.join(sorted(CITY_INFO.keys()))}；"
                     f"省份: {', '.join(sorted(PROVINCE_CITIES.keys()))}")


def get_city(name: str) -> dict:
    """获取单个城市信息"""
    name = name.strip()
    for c, info in CITY_INFO.items():
        if info["code"] == name.upper():
            return {**info, "name": c}
    if name in CITY_INFO:
        return {**CITY_INFO[name], "name": name}
    raise ValueError(f"城市 '{name}' 不支持")


# ============ 签名引擎 ============
_JS_MOCK = """
var window = globalThis; var self = globalThis;
var document = { cookie:'', createElement:function(){return{getContext:function(){return null},toDataURL:function(){return ''},width:0,height:0,style:{}}}, body:{appendChild:function(){},removeChild:function(){}}, head:{appendChild:function(){}}, getElementById:function(){return null}, getElementsByTagName:function(){return []}, addEventListener:function(){}, characterSet:'UTF-8' };
var navigator = { userAgent:'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', platform:'MacIntel', language:'en-US', languages:['en-US'], hardwareConcurrency:8, cookieEnabled:true, plugins:{length:5,refresh:function(){},item:function(){return null}}, maxTouchPoints:0, webdriver:false };
var screen = {width:1920,height:1080,colorDepth:24,pixelDepth:24,availWidth:1920,availHeight:1080};
var location = {hostname:'flights.ctrip.com',href:'https://flights.ctrip.com/',protocol:'https:'};
var history = {length:2}; var chrome = {runtime:{}};
var OfflineAudioContext=undefined; var AudioContext=undefined;
var HTMLCanvasElement={prototype:{toDataURL:function(){},getContext:function(){}}}; var HTMLElement={prototype:{offsetHeight:0}};
var CanvasRenderingContext2D={prototype:{getImageData:function(){},toBlob:function(){}}}; var WebGLRenderingContext=undefined; var WebGL2RenderingContext=undefined;
var Request=function(){}; Request.prototype={credentials:true};
var module = {exports:{}};
"""
_csign_ctx = None

def _get_csign_ctx():
    global _csign_ctx
    if _csign_ctx is None:
        _csign_ctx = quickjs.Context()
        _csign_ctx.eval(_JS_MOCK)
        _csign_ctx.eval(CSIGN_JS.read_text())
    return _csign_ctx

def compute_w_payload(body_str: str) -> str:
    return _get_csign_ctx().eval(f'module.exports.cSign("{hashlib.md5(body_str.encode()).hexdigest()}")')

def compute_sign(tid: str, segments: list) -> str:
    raw = tid + "".join(s["departureCityCode"] + s["arrivalCityCode"] + s["departureDate"] for s in segments)
    return hashlib.md5(raw.encode()).hexdigest()


# ============ Cookie ============
def _fetch_fvp(dep_code="BJS", arr_code="SHA"):
    dep_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    url = f"https://flights.ctrip.com/online/list/oneway-{dep_code}-{arr_code}?depdate={dep_date}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"}), timeout=15, context=SSL_CTX) as resp:
            m = re.search(r"FVP=([^;\"'\s]+)", resp.read(10000).decode("utf-8", errors="ignore"))
            return m.group(1) if m else ""
    except Exception:
        return ""

def get_cookies() -> dict:
    if COOKIE_CACHE.exists():
        try:
            d = json.loads(COOKIE_CACHE.read_text())
            if time.time() - d.get("ts", 0) < 86400:
                return d
        except Exception:
            pass
    vid = f"{int(time.time()*1000)}.{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=12))}"
    fvp = _fetch_fvp()
    parts = ([f"FVP={fvp}"] if fvp else []) + [f"UBT_VID={vid}", f"GUID={uuid.uuid4().hex[:20]}", f"_RGUID={uuid.uuid4()}"]
    d = {"cookie": "; ".join(parts), "vid": vid, "ts": time.time()}
    COOKIE_CACHE.write_text(json.dumps(d))
    return d


# ============ API ============
SEARCH_URL = "https://flights.ctrip.com/international/search/api/search/batchSearch"
LOWPRICE_URL = "https://m.ctrip.com/restapi/soa2/15380/bjjson/FlightIntlAndInlandLowestPriceSearch"

def _post(url, headers, body):
    try:
        with urllib.request.urlopen(urllib.request.Request(f"{url}?v={random.random()}", data=body, headers=headers, method="POST"), timeout=15, context=SSL_CTX) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def search_flights(dep_city: str, arr_city: str, dep_date: str, cabin: str = "Y") -> dict:
    """查询单条航线的航班。返回携程 API 原始 JSON。"""
    dep, arr = get_city(dep_city), get_city(arr_city)
    cabin = cabin.upper()
    cd = get_cookies()
    tid = uuid.uuid4().hex
    segments = [{
        "departureCityCode": dep["code"], "arrivalCityCode": arr["code"],
        "departureCityName": dep["name"], "arrivalCityName": arr["name"],
        "departureDate": dep_date,
        "departureCountryId": 1, "departureCountryName": "中国", "departureCountryCode": "CN",
        "departureProvinceId": dep["prov"], "departureCityId": dep["id"],
        "arrivalCountryId": 1, "arrivalCountryName": "中国", "arrivalCountryCode": "CN",
        "arrivalProvinceId": arr["prov"], "arrivalCityId": arr["id"],
        "departureCityTimeZone": 480, "arrivalCityTimeZone": 480, "timeZone": 480,
    }]
    payload = {
        "adultCount": 1, "childCount": 0, "infantCount": 0,
        "flightWay": "S", "cabin": cabin, "scope": "d", "segmentNo": 1,
        "transactionID": tid, "flightSegments": segments,
        "directFlight": False,
        "extGlobalSwitches": {"useAllRecommendSwitch": True, "unfoldPriceListSwitch": True},
        "noRecommend": False,
        "extensionAttributes": {"LoggingSampling": False, "isFlightIntlNewUser": False},
    }
    body_str = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    headers = {
        "Accept": "application/json", "Content-Type": "application/json;charset=utf-8",
        "Cache-Control": "no-cache", "Origin": "https://flights.ctrip.com",
        "Referer": f"https://flights.ctrip.com/online/list/oneway-{dep['code']}-{arr['code']}?depdate={dep_date}&cabin={cabin.lower()}&adult=1&child=0&infant=0",
        "User-Agent": UA, "cookieOrigin": "https://flights.ctrip.com",
        "scope": "d", "Sessionid": "1", "transactionID": tid,
        "sign": compute_sign(tid, segments), "w-payload-source": compute_w_payload(body_str),
        "x-ctx-ubt-vid": cd.get("vid", ""), "x-ctx-ubt-pageid": "10320673302",
        "x-ctx-ubt-pvid": "1", "x-ctx-ubt-sid": "1", "Cookie": cd["cookie"],
    }
    data = _post(SEARCH_URL, headers, body_str.encode())
    if not data.get("data", {}).get("flightItineraryList") and data.get("data", {}).get("needUserLogin"):
        COOKIE_CACHE.unlink(missing_ok=True)
        cd = get_cookies()
        headers["Cookie"] = cd["cookie"]
        headers["w-payload-source"] = compute_w_payload(body_str)
        data = _post(SEARCH_URL, headers, body_str.encode())
    return data

def get_low_prices(dep_city: str, arr_city: str, dep_date: str) -> list:
    dep, arr = get_city(dep_city), get_city(arr_city)
    body = json.dumps({"departCityCode": dep["code"], "arriveCityCode": arr["code"], "departDate": dep_date, "cabinClass": 0, "travelType": 0, "searchType": 1, "caller": "domestic"}).encode()
    return _post(LOWPRICE_URL, {"Content-Type": "application/json", "User-Agent": UA}, body).get("priceList", [])


# ============ 解析 ============
def _dur(m): return f"{m//60}h{m%60:02d}m"
def _pdate(s):
    m = re.search(r"/Date\((\d+)", s)
    return datetime.fromtimestamp(int(m.group(1))/1000).strftime("%Y-%m-%d") if m else s

def parse_flights(data: dict, route_tag: str = "") -> list[dict]:
    """解析 API 原始数据。route_tag 标记航线（如'→广州'）"""
    raw = data.get("data", {}).get("flightItineraryList", [])
    flights = []
    for item in raw:
        seg = item.get("flightSegments", [{}])[0]
        fl = seg.get("flightList", [{}])[0]
        prices = item.get("priceList", [])
        lowest = min((p["adultPrice"] for p in prices if "adultPrice" in p), default=0) if prices else 0
        disc = ""
        if prices:
            best = min(prices, key=lambda x: x.get("adultPrice", 99999))
            for u in best.get("priceUnitList", [{}]):
                for s in u.get("flightSeatList", []):
                    r = s.get("discountRate", 0)
                    if r > 0: disc = f"{r:.1f}折"; break
        f = {
            "airline": seg.get("airlineName", ""), "flightNo": fl.get("flightNo", ""),
            "aircraft": fl.get("aircraftName", ""),
            "depTime": fl.get("departureDateTime", "")[11:16], "arrTime": fl.get("arrivalDateTime", "")[11:16],
            "depAirport": fl.get("departureAirportShortName", "") + (fl.get("departureTerminal") or ""),
            "arrAirport": fl.get("arrivalAirportShortName", "") + (fl.get("arrivalTerminal") or ""),
            "arrCity": seg.get("flightList", [{}])[0].get("arrivalCityName", ""),
            "duration": _dur(seg.get("duration", 0)), "transfer": seg.get("transferCount", 0),
            "price": lowest, "discount": disc, "crossDays": seg.get("crossDays", 0),
        }
        if route_tag:
            f["route"] = route_tag
        flights.append(f)
    return flights

def parse_low_prices(price_list: list) -> list[dict]:
    return sorted([{"date": _pdate(p.get("departDate","")), "price": p["price"], "totalPrice": p.get("totalPrice",0)}
                   for p in price_list if p.get("price",0) > 0], key=lambda x: x["price"])


# ============ 多城市比价 ============
def search_to_region(dep: str, arr: str, dep_date: str, cabin: str = "Y") -> dict:
    """
    查询 dep → arr 的航班。arr 可以是城市名或省份名。
    省份会自动展开为该省所有机场城市，逐一查询后汇总比较。
    返回结构化结果 dict。
    """
    dep_cities = resolve_location(dep)
    arr_cities = resolve_location(arr)

    is_multi_dep = len(dep_cities) > 1
    is_multi_arr = len(arr_cities) > 1
    is_multi = is_multi_dep or is_multi_arr

    all_flights = []
    route_summaries = []

    for dc in dep_cities:
        for ac in arr_cities:
            route = f"{dc}→{ac}"
            data = search_flights(dc, ac, dep_date, cabin)
            flights = parse_flights(data, route_tag=route)
            direct = [f for f in flights if f["transfer"] == 0]
            dp = [f["price"] for f in direct if f["price"] > 0]
            all_flights.extend(flights)
            if dp:
                cheapest = min(direct, key=lambda x: x["price"] if x["price"] > 0 else 99999)
                route_summaries.append({
                    "route": route,
                    "directCount": len(direct),
                    "lowestPrice": min(dp),
                    "avgPrice": sum(dp) // len(dp),
                    "cheapestFlight": cheapest,
                })
            else:
                route_summaries.append({"route": route, "directCount": 0, "lowestPrice": None, "avgPrice": None, "cheapestFlight": None})

    # 找全局最优
    valid_routes = [r for r in route_summaries if r["lowestPrice"] is not None]
    best_route = min(valid_routes, key=lambda x: x["lowestPrice"]) if valid_routes else None

    return {
        "query": {"from": dep, "to": arr, "date": dep_date, "cabin": cabin,
                  "isMultiRoute": is_multi,
                  "depCities": dep_cities, "arrCities": arr_cities},
        "routeSummaries": route_summaries,
        "bestRoute": best_route,
        "allFlights": all_flights,
    }


# ============ 输出格式化 ============
def to_json(result: dict, low_prices: dict = None) -> str:
    """输出 JSON"""
    if low_prices:
        result["lowPriceCalendar"] = low_prices
    return json.dumps(result, ensure_ascii=False, indent=2)


def to_markdown(result: dict, low_prices: dict = None) -> str:
    """输出 Markdown"""
    q = result["query"]
    lines = [f"## {q['from']} → {q['to']} 机票查询（{q['date']}）\n"]

    # 多航线比价汇总
    if q["isMultiRoute"]:
        lines.append(f"查询范围: 出发 {', '.join(q['depCities'])} | 到达 {', '.join(q['arrCities'])}\n")
        lines.append("### 各航线比价\n")
        lines.append("| 航线 | 直飞数 | 最低价 | 均价 | 最便宜航班 |")
        lines.append("|------|--------|--------|------|-----------|")
        for r in result["routeSummaries"]:
            if r["lowestPrice"] is not None:
                cf = r["cheapestFlight"]
                lines.append(f"| {r['route']} | {r['directCount']} | **¥{r['lowestPrice']}** | ¥{r['avgPrice']} "
                             f"| {cf['airline']} {cf['flightNo']} {cf['depTime']}-{cf['arrTime']} |")
            else:
                lines.append(f"| {r['route']} | 0 | - | - | 无直飞 |")

        best = result.get("bestRoute")
        if best:
            bf = best["cheapestFlight"]
            lines.append(f"\n**最优路线: {best['route']}，最低 ¥{best['lowestPrice']}**"
                         f" — {bf['airline']} {bf['flightNo']} {bf['depTime']}-{bf['arrTime']}"
                         f" {bf['depAirport']}→{bf['arrAirport']}\n")

    # 低价日历
    if low_prices:
        for route, lp in low_prices.items():
            if lp:
                lines.append(f"### 低价日历 {route}\n")
                lines.append("| 日期 | 票价 | 含税价 |")
                lines.append("|------|------|--------|")
                for p in lp[:5]:
                    lines.append(f"| {p['date']} | ¥{p['price']:.0f} | ¥{p['totalPrice']:.0f} |")
                lines.append("")

    # 航班详情
    all_flights = result["allFlights"]
    direct = [f for f in all_flights if f["transfer"] == 0]
    xfer = [f for f in all_flights if f["transfer"] > 0]

    if not q["isMultiRoute"]:
        dp = [f["price"] for f in direct if f["price"] > 0]
        if dp:
            cheapest = min(direct, key=lambda x: x["price"] if x["price"] > 0 else 99999)
            lines.append(f"- **航班数量**: {len(direct)} 直飞, {len(xfer)} 中转")
            lines.append(f"- **直飞最低价**: ¥{min(dp)}")
            lines.append(f"- **直飞均价**: ¥{sum(dp)//len(dp)}")
            lines.append(f"- **最便宜航班**: {cheapest['airline']} {cheapest['flightNo']}"
                         f" {cheapest['depTime']}-{cheapest['arrTime']}"
                         f" {cheapest['depAirport']}→{cheapest['arrAirport']} **¥{cheapest['price']}**\n")

    has_route_col = q["isMultiRoute"]
    if has_route_col:
        lines.append("### 全部直飞航班\n")
        lines.append("| 航线 | 航司 | 航班号 | 起飞 | 到达 | 时长 | 出发 | 到达 | 价格 | 折扣 |")
        lines.append("|------|------|--------|------|------|------|------|------|------|------|")
        for f in sorted(direct, key=lambda x: x["price"] if x["price"] > 0 else 99999):
            cross = f" +{f['crossDays']}天" if f["crossDays"] > 0 else ""
            lines.append(f"| {f.get('route','')} | {f['airline']} | {f['flightNo']} "
                         f"| {f['depTime']} | {f['arrTime']}{cross} | {f['duration']} "
                         f"| {f['depAirport']} | {f['arrAirport']} | ¥{f['price']} | {f['discount']} |")
    else:
        lines.append("### 直飞航班\n")
        lines.append("| 航司 | 航班号 | 机型 | 起飞 | 到达 | 时长 | 出发 | 到达 | 价格 | 折扣 |")
        lines.append("|------|--------|------|------|------|------|------|------|------|------|")
        for f in direct:
            cross = f" +{f['crossDays']}天" if f["crossDays"] > 0 else ""
            lines.append(f"| {f['airline']} | {f['flightNo']} | {f['aircraft']} "
                         f"| {f['depTime']} | {f['arrTime']}{cross} | {f['duration']} "
                         f"| {f['depAirport']} | {f['arrAirport']} | ¥{f['price']} | {f['discount']} |")

    if xfer:
        lines.append(f"\n### 中转航班（{len(xfer)}个）\n")
        lines.append("| 航线 | 航司 | 航班号 | 起飞 | 到达 | 价格 |" if has_route_col else "| 航司 | 航班号 | 起飞 | 到达 | 价格 |")
        lines.append("|------|------|--------|------|------|------|" if has_route_col else "|------|--------|------|------|------|")
        for f in xfer:
            prefix = f"| {f.get('route','')} " if has_route_col else ""
            lines.append(f"{prefix}| {f['airline']} | {f['flightNo']} | {f['depTime']} | {f['arrTime']} | ¥{f['price']} |")

    return "\n".join(lines)


# ============ CLI ============
def main():
    if len(sys.argv) < 4:
        print(f"用法: python3 {Path(__file__).name} 出发 到达 日期 [舱位Y/C/F] [--json|--md]", file=sys.stderr)
        print(f"示例: python3 {Path(__file__).name} 北京 广东 2026-04-02", file=sys.stderr)
        print(f"      python3 {Path(__file__).name} 北京 上海 2026-04-02 --json", file=sys.stderr)
        sys.exit(1)

    dep, arr, date = sys.argv[1], sys.argv[2], sys.argv[3]
    cabin, fmt = "Y", "md"
    for arg in sys.argv[4:]:
        if arg.upper() in ("Y", "C", "F"): cabin = arg.upper()
        elif arg in ("--json", "-j"): fmt = "json"
        elif arg in ("--md", "--markdown", "-m"): fmt = "md"

    result = search_to_region(dep, arr, date, cabin)

    # 低价日历: 每条航线取一个
    lp = {}
    for dc in result["query"]["depCities"]:
        for ac in result["query"]["arrCities"]:
            route = f"{dc}→{ac}"
            lp[route] = parse_low_prices(get_low_prices(dc, ac, date))

    if fmt == "json":
        print(to_json(result, lp))
    else:
        print(to_markdown(result, lp))


if __name__ == "__main__":
    main()
