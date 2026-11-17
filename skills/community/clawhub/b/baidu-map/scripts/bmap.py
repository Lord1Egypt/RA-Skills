#!/usr/bin/env python3
"""百度地图 Web 服务 API 命令行工具（零依赖，仅标准库）。

环境变量:
    BMAP_AK   百度地图开放平台 AK（lbsyun.baidu.com 免费申请，应用类型选 服务端）

子命令:
    geocode <地址> [城市]             地址 → 坐标（返回 BD-09）
    regeo <lat,lng>                   坐标 → 地址（注意百度是 纬度,经度 顺序）
    search <关键词> <城市>            POI 检索
    around <lat,lng> <关键词> [半径]  周边检索（半径米，默认3000）
    driving <起点lat,lng> <终点lat,lng>   驾车路线（directionlite）
    walking <起点lat,lng> <终点lat,lng>   步行路线
    convert <lng,lat> <from> <to>     坐标转换 1=WGS84 3=GCJ-02 5=BD-09
    call <path> k=v [k=v...]          通用调用任意接口

示例:
    export BMAP_AK=你的ak
    python3 bmap.py geocode "北京市海淀区上地十街10号"
    python3 bmap.py convert 116.404,39.915 1 5
"""
import json
import os
import sys
import urllib.parse
import urllib.request

BASE = "https://api.map.baidu.com"


def die(msg: str) -> None:
    print(f"错误: {msg}", file=sys.stderr)
    sys.exit(1)


def api(path: str, **params) -> dict:
    ak = os.environ.get("BMAP_AK") or die("未设置 BMAP_AK（lbsyun.baidu.com 申请服务端 AK）")
    params.update(ak=ak, output="json")
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=20) as resp:
        r = json.loads(resp.read())
    if r.get("status") != 0:
        die(f"API 失败: status={r.get('status')} {r.get('message', r.get('msg', ''))} "
            "(200=AK不存在 210=AK无效/IP校验失败 302=配额超限 401=并发超限)")
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
        out(api("/geocoding/v3/", **p))
    elif cmd == "regeo":
        rest or die("用法: regeo <lat,lng>")
        out(api("/reverse_geocoding/v3/", location=rest[0]))
    elif cmd == "search":
        len(rest) >= 2 or die("用法: search <关键词> <城市>")
        out(api("/place/v2/search", query=rest[0], region=rest[1], page_size=10))
    elif cmd == "around":
        len(rest) >= 2 or die("用法: around <lat,lng> <关键词> [半径米]")
        out(api("/place/v2/search", query=rest[1], location=rest[0],
                radius=rest[2] if len(rest) > 2 else 3000, page_size=10))
    elif cmd in ("driving", "walking"):
        len(rest) >= 2 or die(f"用法: {cmd} <起点lat,lng> <终点lat,lng>")
        out(api(f"/directionlite/v1/{cmd}",
                origin=rest[0], destination=rest[1]))
    elif cmd == "convert":
        len(rest) >= 3 or die("用法: convert <lng,lat> <from> <to> (1=WGS84 3=GCJ02 5=BD09)")
        out(api("/geoconv/v1/", coords=rest[0],
                **{"from": rest[1], "to": rest[2]}))
    elif cmd == "call":
        rest or die("用法: call <path> k=v [k=v...]")
        params = dict(kv.split("=", 1) for kv in rest[1:])
        out(api(rest[0], **params))
    else:
        die(f"未知子命令: {cmd}（运行不带参数查看帮助）")


if __name__ == "__main__":
    main()
