#!/usr/bin/env python3
"""高德地图 Web 服务 API 命令行工具（零依赖，仅标准库）。

环境变量:
    AMAP_KEY   高德开放平台 Web服务 类型的 Key（lbs.amap.com 免费申请）

子命令:
    geocode <地址> [城市]            地址 → 坐标
    regeo <lng,lat>                  坐标 → 地址
    search <关键词> [城市]           POI 关键词搜索
    around <lng,lat> <关键词> [半径] POI 周边搜索（半径米，默认3000）
    driving <起点lng,lat> <终点lng,lat>   驾车路线
    walking <起点lng,lat> <终点lng,lat>   步行路线
    weather <adcode> [all]           天气（all=预报，默认实况）
    ip [ip地址]                      IP 定位（缺省定位本机出口）
    call <path> k=v [k=v...]         通用调用任意 v3/v5 接口

示例:
    export AMAP_KEY=你的key
    python3 amap.py geocode "北京市朝阳区阜通东大街6号"
    python3 amap.py around 116.481028,39.989643 咖啡 1000
    python3 amap.py weather 110101 all
"""
import json
import os
import sys
import urllib.parse
import urllib.request

BASE = "https://restapi.amap.com"


def die(msg: str) -> None:
    print(f"错误: {msg}", file=sys.stderr)
    sys.exit(1)


def api(path: str, **params) -> dict:
    key = os.environ.get("AMAP_KEY") or die("未设置 AMAP_KEY（lbs.amap.com 申请 Web服务 Key）")
    params["key"] = key
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=20) as resp:
        r = json.loads(resp.read())
    # v3 用 status/info，v5 用 status/infocode；status=0 即失败
    if str(r.get("status")) == "0":
        die(f"API 失败: {r.get('info')} (infocode={r.get('infocode')}，"
            "10001=key无效 10003=日配额超限 10021=并发超限)")
    return r


def out(r: dict) -> None:
    print(json.dumps(r, ensure_ascii=False, indent=1))


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cmd, rest = args[0], args[1:]

    if cmd == "geocode":
        rest or die("用法: geocode <地址> [城市]")
        p = {"address": rest[0]}
        if len(rest) > 1:
            p["city"] = rest[1]
        out(api("/v3/geocode/geo", **p))
    elif cmd == "regeo":
        rest or die("用法: regeo <lng,lat>")
        out(api("/v3/geocode/regeo", location=rest[0], extensions="base"))
    elif cmd == "search":
        rest or die("用法: search <关键词> [城市]")
        p = {"keywords": rest[0], "page_size": 10}
        if len(rest) > 1:
            p["region"] = rest[1]
        out(api("/v5/place/text", **p))
    elif cmd == "around":
        len(rest) >= 2 or die("用法: around <lng,lat> <关键词> [半径米]")
        out(api("/v5/place/around", location=rest[0], keywords=rest[1],
                radius=rest[2] if len(rest) > 2 else 3000, page_size=10))
    elif cmd in ("driving", "walking"):
        len(rest) >= 2 or die(f"用法: {cmd} <起点lng,lat> <终点lng,lat>")
        out(api(f"/v5/direction/{cmd}", origin=rest[0], destination=rest[1],
                show_fields="cost"))
    elif cmd == "weather":
        rest or die("用法: weather <adcode> [all]")
        ext = "all" if len(rest) > 1 and rest[1] == "all" else "base"
        out(api("/v3/weather/weatherInfo", city=rest[0], extensions=ext))
    elif cmd == "ip":
        out(api("/v3/ip", **({"ip": rest[0]} if rest else {})))
    elif cmd == "call":
        rest or die("用法: call <path> k=v [k=v...]")
        params = dict(kv.split("=", 1) for kv in rest[1:])
        out(api(rest[0], **params))
    else:
        die(f"未知子命令: {cmd}（运行不带参数查看帮助）")


if __name__ == "__main__":
    main()
