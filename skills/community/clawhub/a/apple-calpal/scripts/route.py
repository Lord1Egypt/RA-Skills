# -*- coding: utf-8 -*-
"""
route.py —— 「路上要多久」。有高德 key 时给精确值（含实时路况），是「几点出门」的决定因素。

用法:
    route.py driving  起点lat 起点lon 终点lat 终点lon
    route.py transit  起点lat 起点lon 终点lat 终点lon [--city1 010] [--city2 010]

没配 amap_key 时直接退出并说明 —— 这时由 agent 根据距离自行保守估算，
并明确告诉用户"这是估算，没查实时路况"。宁可少一个功能，不可装作精确。

为什么不能全靠模型估：实测 agent 凭常识把 39 分钟的路估成 90 分钟，
差一倍意味着白早起一小时或者迟到。有 key 就用 key。
坐标是 GCJ-02（高德系），geocode 的 amap 源给的就是它，直接喂即可。
"""

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://restapi.amap.com/v5/direction"
TIMEOUT = 20
PROFILE_PATH = Path(__file__).resolve().parent.parent / "data" / "profile.json"


def die(msg, hint=""):
    print("[错误] " + msg, file=sys.stderr)
    if hint:
        print("       " + hint, file=sys.stderr)
    sys.exit(1)


def load_profile():
    try:
        with open(PROFILE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        die("找不到 %s" % PROFILE_PATH)


def http_json(url, params):
    q = urllib.parse.urlencode(params)
    r = urllib.request.Request(url + "?" + q,
                               headers={"User-Agent": "apple-calpal/1.0"})
    with urllib.request.urlopen(r, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _ll(lat, lon):
    """高德要「经度,纬度」顺序，写反会算到地球另一边。"""
    return "%.6f,%.6f" % (lon, lat)


def driving(o_lat, o_lon, d_lat, d_lon, key):
    d = http_json(BASE + "/driving", {
        "origin": _ll(o_lat, o_lon), "destination": _ll(d_lat, d_lon),
        "key": key, "strategy": 32,          # 32 = 高德推荐
        "show_fields": "cost",
    })
    if d.get("status") != "1":
        return {"error": "高德驾车规划失败：%s（%s）" % (d.get("info"), d.get("infocode"))}
    path = (d.get("route", {}).get("paths") or [{}])[0]
    cost = path.get("cost", {})
    return {"mode": "driving",
            "distance_km": round(int(path.get("distance", 0)) / 1000.0, 1),
            "duration_minutes": int(round(int(cost.get("duration", 0)) / 60.0)),
            "taxi_cost": d["route"].get("taxi_cost"), "tolls": cost.get("tolls"),
            "note": "耗时基于高德实时路况。若是未来日期出发，路况可能不同，高峰要往上加。"}


def transit(o_lat, o_lon, d_lat, d_lon, key, city1, city2):
    d = http_json(BASE + "/transit/integrated", {
        "origin": _ll(o_lat, o_lon), "destination": _ll(d_lat, d_lon),
        "city1": city1, "city2": city2, "key": key, "show_fields": "cost",
    })
    if d.get("status") != "1":
        return {"error": "高德公交规划失败：%s（%s）" % (d.get("info"), d.get("infocode"))}
    plans = []
    for t in (d.get("route", {}).get("transits") or [])[:3]:
        lines = []
        for seg in (t.get("segments") or []):
            for bl in (seg.get("bus", {}).get("buslines") or [])[:1]:
                if bl.get("name"):
                    lines.append(bl["name"].split("(")[0])
        plans.append({"duration_minutes": int(round(int(t["cost"]["duration"]) / 60.0)),
                      "walking_meters": int(t.get("walking_distance") or 0),
                      "fare": t["cost"].get("transit_fee"), "lines": lines})
    plans.sort(key=lambda p: p["duration_minutes"])
    return {"mode": "transit", "plans": plans,
            "note": "已含等车和换乘。步行超过 1.5 公里的方案要提醒用户。"}


def main():
    a = sys.argv[1:]
    if not a or a[0] not in ("driving", "transit") or len(a) < 5:
        print(__doc__)
        return
    prof = load_profile()
    key = prof.get("amap_key")
    if not key:
        die("profile.json 没配 amap_key，route 不可用",
            "由 agent 按距离保守估算路程并声明是估算；要精确路况就去 lbs.amap.com 申请（服务平台选「Web服务」）")
    try:
        o_lat, o_lon, d_lat, d_lon = (float(x) for x in a[1:5])
        if a[0] == "driving":
            out = driving(o_lat, o_lon, d_lat, d_lon, key)
        else:
            opts = dict(zip(a[5::2], a[6::2]))
            out = transit(o_lat, o_lon, d_lat, d_lon, key,
                          opts.get("--city1", prof.get("city_code") or "010"),
                          opts.get("--city2", prof.get("city_code") or "010"))
    except (ValueError, IndexError):
        die("参数要四个数字：起点lat 起点lon 终点lat 终点lon")
    except OSError as e:
        die("高德连不上：%s" % e)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
