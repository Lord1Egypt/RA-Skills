#!/usr/bin/env python3
"""
search_transit.py
盲人辅助 Skill — 公交/地铁换乘路线规划（高德 transit/integrated API）
返回语音友好的换乘摘要
"""
import json
import os
from utils.gaode_client import GaodeClient


def search_transit(destination: str, city: str = "") -> str:
    """
    Args:
        destination: 目的地名称或地址，如"厦门火车站"
        city:         当前城市，优先从 USER_CITY 或逆地理反推，可不传
    Returns:
        JSON str，含 success/results/voice_summary
    """
    client = GaodeClient()

    # ---- 1. 获取用户当前位置 ----
    lat = os.environ.get("USER_LAT")
    lng = os.environ.get("USER_LNG")
    if not lat or not lng:
        return json.dumps(
            {"success": False, "message": "需要位置信息，请授权定位"},
            ensure_ascii=False
        )

    # ---- 2. 推断城市（优先参数 > 环境变量 > 逆地理） ----
    if not city:
        city = os.environ.get("USER_CITY", "")
    if not city:
        try:
            rgc = client.reverse_geocode(float(lat), float(lng))
            city = rgc.get("regeocode", {}).get("addressComponent", {}).get("city", "北京")
        except Exception:
            city = "北京"

    origin_coord = f"{lng},{lat}"

    # ---- 3. 地理编码目的地 ----
    try:
        geo = client.geocode(destination, city=city)
        if not geo.get("geocodes"):
            return json.dumps(
                {"success": False, "message": f"找不到目的地：{destination}"},
                ensure_ascii=False
            )
        dest_coord = geo["geocodes"][0]["location"]
        dest_addr  = geo["geocodes"][0].get("formatted_address", destination)
    except Exception as e:
        return json.dumps(
            {"success": False, "message": f"地理编码失败：{e}"},
            ensure_ascii=False
        )

    # ---- 4. 调高德公交综合换乘规划 API ----
    try:
        route_data = client.plan_transit(origin_coord, dest_coord, city)
    except Exception as e:
        return json.dumps(
            {"success": False, "message": f"公交路线规划失败：{e}"},
            ensure_ascii=False
        )

    transits = route_data.get("route", {}).get("transits", [])
    if not transits:
        return json.dumps(
            {"success": False, "message": f"未找到到「{dest_addr}」的公交/地铁路线"},
            ensure_ascii=False
        )

    # ---- 5. 提取首条方案（最适合盲人听） ----
    t = transits[0]
    segments = t.get("segments", [])
    parts = []

    for seg in segments:
        # 步行段
        if seg.get("walking"):
            dist = seg["walking"].get("distance", "0")
            parts.append(f"步行{dist}米")
        # 公交段
        if seg.get("bus"):
            bus_lines = seg["bus"].get("buslines", [])
            if bus_lines:
                bl = bus_lines[0]
                name = bl.get("name", "公交车")
                parts.append(f"乘坐{name}")
        # 地铁段（高德也归入buslines，name含"地铁"）
        if seg.get("railway"):
            rl = seg["railway"].get("name", "地铁")
            parts.append(f"乘坐{rl}")

    duration_min = int(t.get("duration", 0)) // 60
    cost_yuan   = t.get("cost", "0")

    voice_summary = (
        f"推荐公交方案到{dest_addr}："
        + "，".join(parts)
        + f"，全程约{duration_min}分钟，票价约{cost_yuan}元"
    )

    result = {
        "success": True,
        "destination": dest_addr,
        "total_duration_min": duration_min,
        "cost_yuan": cost_yuan,
        "segments_desc": parts,
        "alternative_count": len(transits) - 1,
        "voice_summary": voice_summary,
        "tip": "如需查看其他换乘方案请告诉我"
    }

    return json.dumps(result, ensure_ascii=False)