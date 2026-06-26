#!/usr/bin/env python3
"""
测试门店解析 API：确保 Skill 在解析链接时调用 API 能准确获得门店编号。
用法：
  python test_store_api.py --base-url http://localhost:8888/api/openclaw
  python test_store_api.py --base-url http://localhost:8888/api/openclaw --city 上海 --keyword 嘉定城北 --expect-kfc SHA391
  python test_store_api.py --base-url http://localhost:8888/api/openclaw --mcd-keyword 亚龙 --expect-mcd 1450103
"""
import argparse
import os
import sys

import requests

DEFAULT_BASE = "http://localhost:8888/api/openclaw"


def resolve_base_url(cli: str) -> str:
    cli = (cli or "").strip()
    if cli:
        return cli.rstrip("/")
    return (os.getenv("OPENCLAW_PLATFORM_BASE_URL") or os.getenv("KFC_PLATFORM_BASE_URL") or DEFAULT_BASE).strip().rstrip("/")


def test_kfc_store(base_url: str, city: str, keyword: str, timeout: int = 10) -> str:
    """GET /kfc/store?city=xxx&keyword=xxx，返回 store_code。"""
    url = f"{base_url}/kfc/store"
    resp = requests.get(url, params={"city": city, "keyword": keyword}, timeout=timeout)
    resp.encoding = "utf-8"
    resp.raise_for_status()
    data = resp.json()
    code = (data.get("store_code") or data.get("storeCode") or data.get("store") or "").strip()
    if not code:
        raise RuntimeError(f"KFC 门店接口未返回 store_code，响应: {data}")
    return code


def test_mcd_store(base_url: str, keyword: str, timeout: int = 10) -> str:
    """GET /mcd/store?keyword=xxx，返回 store。"""
    url = f"{base_url}/mcd/store"
    resp = requests.get(url, params={"keyword": keyword}, timeout=timeout)
    resp.encoding = "utf-8"
    resp.raise_for_status()
    data = resp.json()
    store = (data.get("store") or data.get("store_id") or "").strip()
    if not store:
        raise RuntimeError(f"麦当劳门店接口未返回 store，响应: {data}")
    return store


def main() -> int:
    parser = argparse.ArgumentParser(description="测试门店解析 API（KFC / 麦当劳）")
    parser.add_argument("--base-url", type=str, default="", help="后端 base URL，如 http://localhost:8888/api/openclaw")
    parser.add_argument("--city", type=str, default="上海", help="KFC 城市")
    parser.add_argument("--keyword", type=str, default="嘉定城北", help="KFC 门店关键词")
    parser.add_argument("--expect-kfc", type=str, default="", help="期望的 KFC store_code，不填则只打印不断言")
    parser.add_argument("--mcd-keyword", type=str, default="", help="麦当劳门店关键词，不填则只测 KFC")
    parser.add_argument("--expect-mcd", type=str, default="", help="期望的麦当劳 store 编号，不填则只打印不断言")
    parser.add_argument("--timeout", type=int, default=10, help="请求超时秒数")
    args = parser.parse_args()

    base_url = resolve_base_url(args.base_url)
    print(f"base_url: {base_url}")
    print("提示: 请先启动后端 (order-api)，并确保已导入门店数据 (import_stores)。\n")

    failed = 0

    # KFC
    try:
        code = test_kfc_store(base_url, args.city, args.keyword, args.timeout)
        print(f"KFC city={args.city} keyword={args.keyword} -> store_code={code}")
        if args.expect_kfc and code != args.expect_kfc.strip():
            print(f"  FAIL: 期望 store_code={args.expect_kfc}, 实际={code}", file=sys.stderr)
            failed += 1
    except Exception as e:
        print(f"KFC 请求失败: {e}", file=sys.stderr)
        failed += 1

    # McD
    if args.mcd_keyword:
        try:
            store = test_mcd_store(base_url, args.mcd_keyword, args.timeout)
            print(f"McD keyword={args.mcd_keyword} -> store={store}")
            if args.expect_mcd and store != args.expect_mcd.strip():
                print(f"  FAIL: 期望 store={args.expect_mcd}, 实际={store}", file=sys.stderr)
                failed += 1
        except Exception as e:
            print(f"McD 请求失败: {e}", file=sys.stderr)
            failed += 1

    if failed:
        print(f"\n共 {failed} 项失败", file=sys.stderr)
        return 1
    print("\n全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
