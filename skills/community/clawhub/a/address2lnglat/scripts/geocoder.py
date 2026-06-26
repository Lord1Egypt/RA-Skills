#!/usr/bin/env python3
"""
address2lnglat - 百度地图地理编码工具 v4
通过百度地图开放平台 API 将地名批量转换为 BD-09 经纬度坐标（百度坐标）
百度地图 API 直接返回 BD-09 坐标系，无需额外转换

使用方法：
  python geocoder.py [关键词]

流程：
  1. 输入搜索关键词（如：天津赏花地点）
  2. 自动搜索相关地点列表
  3. 输入百度地图 AK
  4. 自动批量获取经纬度（BD-09，百度坐标系）
  5. 输出结果（控制台 + CSV + JSON 文件）
"""

import requests
import json
import time
import math
import csv
import sys
from typing import List, Dict, Any


# ──────────────────────────────────────────────
#  工具函数
# ──────────────────────────────────────────────

def input_ak() -> str:
    """获取百度地图 AK"""
    ak = input("\n🔑 请输入您的百度地图 AK：").strip()
    if not ak:
        print("⚠️  AK 不能为空！")
        sys.exit(1)
    return ak


def input_city_limit() -> bool:
    """询问是否限制城市"""
    ans = input("🔍 是否限制在城市内搜索？(y/n，默认为是)：").strip().lower()
    return ans != "n"


def search_baidu_places(keyword: str, region: str = "", ak: str = "", city_limit: bool = True) -> List[Dict]:
    """使用百度地图 Place API 搜索地点（坐标直接为 BD-09）"""
    if not ak:
        ak = input_ak()
        city_limit = input_city_limit()

    print(f"\n🌐 正在搜索「{keyword}」相关地点...\n")

    url = "https://api.map.baidu.com/place/v2/search"
    results = []
    page_num = 0

    while True:
        params = {
            "query": keyword,
            "region": region,
            "output": "json",
            "ak": ak,
            "page_size": 20,
            "page_num": page_num,
            "city_limit": str(city_limit).lower(),
            "scope": 2,
        }

        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
        except Exception as e:
            print(f"  ⚠️  第 {page_num + 1} 页请求失败：{e}")
            break

        if data.get("status") != 0:
            print(f"  ⚠️  API 错误：{data.get('message', '未知错误')}")
            if page_num == 0:
                sys.exit(1)
            break

        items = data.get("results", [])
        results.extend(items)

        if not items or len(items) < 20:
            break

        page_num += 1
        time.sleep(0.3)

    print(f"  ✅ 共找到 {len(results)} 个候选地点")
    return results


def deduplicate_addresses(baidu_results: List[Dict]) -> List[Dict]:
    """从百度搜索结果中提取并去重，保留完整信息"""
    seen = set()
    unique = []

    for item in baidu_results:
        name = item.get("name", "").strip()
        addr = item.get("address", "").strip()
        city = item.get("city", "").strip()

        key = addr if addr else (f"{city}{name}" if city else name)
        if not key or key in seen:
            continue

        seen.add(key)
        unique.append({
            "name": name,
            "address": addr,
            "location": item.get("location", {}),
        })

    return unique


def geocode_addresses(place_list: List[Dict], ak: str) -> List[Dict[str, Any]]:
    """
    批量获取 BD-09 经纬度
    百度 Place API 返回的坐标直接是 BD-09 坐标系
    """
    print(f"\n📍 开始获取 BD-09 坐标，共 {len(place_list)} 个地点...\n")

    results = []
    success = 0
    fail = 0

    for i, item in enumerate(place_list, 1):
        name = item.get("name", "")
        address = item.get("address", "")
        loc = item.get("location", {})

        # 优先使用 place 搜索返回的 BD-09 坐标
        if loc.get("lng") is not None and loc.get("lat") is not None:
            bd_lng = round(loc["lng"], 6)
            bd_lat = round(loc["lat"], 6)
            source = "place_api"

            print(f"  [{i:02d}/{len(place_list)}] {name}")
            print(f"           ✅ BD-09：{bd_lng}, {bd_lat}  (来源：Place API)")
            results.append({
                "name": name,
                "address": address,
                "lng": bd_lng,
                "lat": bd_lat,
                "source": source,
                "status": "success",
            })
            success += 1
        else:
            # fallback：调用地理编码 API
            geo_url = "https://api.map.baidu.com/geocoding/v3/"
            geo_params = {"address": address or name, "output": "json", "ak": ak}
            try:
                resp = requests.get(geo_url, params=geo_params, timeout=10)
                geo_data = resp.json()
            except Exception as e:
                print(f"  [{i:02d}/{len(place_list)}] {name}")
                print(f"           ❌ 请求失败：{e}")
                results.append({"name": name, "address": address, "lng": None, "lat": None, "source": "error", "status": "error", "error": str(e)})
                fail += 1
                time.sleep(0.3)
                continue

            if geo_data.get("status") == 0:
                r = geo_data["result"]
                bd_lng = round(r["location"]["lng"], 6)
                bd_lat = round(r["location"]["lat"], 6)
                conf = r.get("confidence", "")
                level = r.get("level", "")
                fmt_addr = r.get("formatted_address", "")
                print(f"  [{i:02d}/{len(place_list)}] {name}")
                print(f"           ✅ BD-09：{bd_lng}, {bd_lat}  (来源：Geocoding API)")
                results.append({
                    "name": name,
                    "address": fmt_addr or address,
                    "lng": bd_lng,
                    "lat": bd_lat,
                    "level": level,
                    "confidence": conf,
                    "source": "geocoding_api",
                    "status": "success",
                })
                success += 1
            else:
                print(f"  [{i:02d}/{len(place_list)}] {name}")
                print(f"           ❌ {geo_data.get('message', '未知错误')}")
                results.append({"name": name, "address": address, "lng": None, "lat": None, "source": "error", "status": "error", "error": geo_data.get("message", "")})
                fail += 1

        time.sleep(0.3)

    print(f"\n  📊 成功 {success} 个，失败 {fail} 个")
    return results


def save_csv_and_json(results: List[Dict], keyword: str) -> tuple:
    """保存为 CSV 和 JSON 文件"""
    safe = keyword.replace(" ", "_").replace("/", "_")
    csv_file = f"lnglat_{safe}.csv"
    json_file = f"lnglat_{safe}.json"

    # CSV
    with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "序号", "名称", "详细地址", "BD-09经度", "BD-09纬度", "坐标来源", "类型", "置信度", "状态"
        ])
        writer.writeheader()
        for i, r in enumerate(results, 1):
            writer.writerow({
                "序号": i,
                "名称": r.get("name", ""),
                "详细地址": r.get("address", ""),
                "BD-09经度": r.get("lng", ""),
                "BD-09纬度": r.get("lat", ""),
                "坐标来源": r.get("source", ""),
                "类型": r.get("level", ""),
                "置信度": r.get("confidence", ""),
                "状态": "成功" if r["status"] == "success" else f"失败:{r.get('error','')}",
            })

    # JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return csv_file, json_file


def print_results(results: List[Dict], keyword: str) -> None:
    """控制台打印结果"""
    print("\n" + "=" * 70)
    print(f"  「{keyword}」BD-09 坐标查询结果（百度坐标系）")
    print("=" * 70)

    for r in results:
        if r["status"] == "success":
            print(f"\n  ✅ {r['name']}")
            print(f"     📌 BD-09：{r['lng']}, {r['lat']}")
            print(f"     🏠 地址：{r.get('address', 'N/A')}")
        else:
            print(f"\n  ❌ {r['name']} — {r.get('error', '未知错误')}")

    print("\n" + "=" * 70)
    success_count = sum(1 for r in results if r["status"] == "success")
    print(f"  合计：{success_count}/{len(results)} 个成功")
    print("=" * 70)


# ──────────────────────────────────────────────
#  主程序
# ──────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  🌐 address2lnglat v4 - 百度地图 BD-09 批量获取工具")
    print("=" * 60)

    # 步骤1：输入关键词
    if len(sys.argv) > 1:
        keyword = " ".join(sys.argv[1:])
    else:
        keyword = input("\n📋 请输入搜索关键词（如：天津赏花地点）：").strip()

    if not keyword:
        print("⚠️ 关键词不能为空！")
        sys.exit(1)

    # 步骤2：输入 AK 和城市限制
    ak = input_ak()
    city_limit = input_city_limit()

    # 步骤3：搜索地点
    baidu_results = search_baidu_places(keyword, ak=ak, city_limit=city_limit)
    if not baidu_results:
        print("\n❌ 未找到任何相关地点！")
        sys.exit(1)

    # 步骤4：去重
    place_list = deduplicate_addresses(baidu_results)
    print(f"\n🔄 去重后共 {len(place_list)} 个唯一地点")

    # 步骤5：批量获取 BD-09 坐标
    geo_results = geocode_addresses(place_list, ak)

    # 步骤6：保存并打印
    print_results(geo_results, keyword)
    csv_file, json_file = save_csv_and_json(geo_results, keyword)
    print(f"\n  💾 CSV 已保存：{csv_file}")
    print(f"  💾 JSON 已保存：{json_file}")


if __name__ == "__main__":
    main()
