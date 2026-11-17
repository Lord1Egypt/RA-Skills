#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run explicitly approved, visible-browser follow batches.

This runner uses a fresh visible session and acts only on the fixed candidate
list supplied for the current batches. Each batch is capped, but a longer fixed
list can be processed as consecutive batches.
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from platforms import get_platform, supported_platform_names
from storage import BloggerDB

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ 未检测到 Playwright 依赖，请在终端运行: pip install playwright && playwright install")
    sys.exit(1)


MAX_BATCH_SIZE = 30
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "batch_results")
PROFILE_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "browser_profiles")


def parse_arguments():
    parser = argparse.ArgumentParser(description="已确认名单的可见浏览器批量关注工具")
    parser.add_argument("-p", "--platform", required=True,
                        help="目标平台: douyin | xiaohongshu | bilibili | x | youtube")
    parser.add_argument("-f", "--file", required=True, help="已审核的候选名单 JSON 文件")
    parser.add_argument("-i", "--industry", default="", help="本批次博主的行业大类（可选）")
    parser.add_argument("--max-follows", type=int, default=MAX_BATCH_SIZE,
                        help=f"本批次最大关注数，范围 1-{MAX_BATCH_SIZE}，默认 {MAX_BATCH_SIZE}")
    parser.add_argument("--profile-dir", default="",
                        help="专用浏览器资料目录；默认使用 data/browser_profiles/<platform>")
    parser.add_argument("--dry-run", action="store_true", help="仅验证并预览名单，不启动浏览器或执行关注")
    return parser.parse_args()


def load_bloggers_data(file_path: str, default_industry: str = "") -> List[Dict]:
    candidates = [file_path, os.path.join(os.getcwd(), file_path)]
    target_file = next((path for path in candidates if os.path.isfile(path)), None)
    if not target_file:
        raise ValueError(f"找不到博主数据文件: {file_path}")

    with open(target_file, "r", encoding="utf-8") as source:
        data = json.load(source)
    if not isinstance(data, list):
        raise ValueError("数据文件格式错误，必须为博主列表 JSON 数组。")

    normalized = []
    seen_names = set()
    for index, item in enumerate(data, 1):
        if not isinstance(item, dict):
            raise ValueError(f"第 {index} 条候选不是对象。")
        name = str(item.get("name", "")).strip()
        if not name:
            raise ValueError(f"第 {index} 条候选缺少 name。")
        key = name.casefold()
        if key in seen_names:
            continue
        seen_names.add(key)
        candidate = dict(item)
        candidate["id"] = candidate.get("id", index)
        candidate["name"] = name
        candidate["industry"] = candidate.get("industry") or default_industry
        candidate["category"] = candidate.get("category") or "默认"
        candidate["fans"] = candidate.get("fans") or ""
        normalized.append(candidate)
    if not normalized:
        raise ValueError("候选名单为空。")
    return normalized


def validate_batch_size(max_follows: int) -> None:
    if not 1 <= max_follows <= MAX_BATCH_SIZE:
        raise ValueError(f"--max-follows 必须在 1 到 {MAX_BATCH_SIZE} 之间。")


def split_batches(bloggers: List[Dict], batch_size: int) -> List[List[Dict]]:
    return [bloggers[start:start + batch_size] for start in range(0, len(bloggers), batch_size)]


def get_profile_dir(platform_name: str, requested_dir: str) -> str:
    """Return an absolute, dedicated browser profile path for this platform."""
    profile_dir = requested_dir.strip() if requested_dir else os.path.join(PROFILE_ROOT, platform_name)
    return os.path.abspath(profile_dir)


def print_batch_preview(target_platform, bloggers: List[Dict], batch_number: int, batch_count: int) -> None:
    print("\n" + "=" * 76)
    print(f"待确认批次 {batch_number}/{batch_count}｜平台：{target_platform.display_name}｜数量：{len(bloggers)}")
    print("=" * 76)
    for index, blogger in enumerate(bloggers, 1):
        category = blogger.get("category", "默认")
        fans = blogger.get("fans", "-")
        print(f"{index:>2}. {blogger['name']}  | 分类：{category} | 粉丝：{fans}")
    print("=" * 76)
    print("执行范围仅限以上固定名单；不会追加候选、跨平台操作或处理验证码。")


def request_batch_approval(target_platform, count: int) -> bool:
    phrase = f"EXECUTE {count}"
    print("\n请在浏览器中确认已登录正确账号。")
    print(f"如确认在 {target_platform.display_name} 对这 {count} 位名单执行关注，请输入：{phrase}")
    return input("确认口令（其他输入将取消）: ").strip() == phrase


def save_results(platform_name: str, results: List[Dict]) -> str:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_path = os.path.join(RESULTS_DIR, f"{platform_name}-{timestamp}.json")
    with open(output_path, "w", encoding="utf-8") as output:
        json.dump(results, output, ensure_ascii=False, indent=2)
    return output_path


def record(item: Dict, platform_name: str, status: str, message: str, meta=None) -> Dict:
    meta = meta or {}
    return {
        "id": item.get("id"), "name": item["name"], "platform": platform_name,
        "profile_url": meta.get("profile_url", ""), "status": status,
        "message": message, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }


def main():
    args = parse_arguments()
    target_platform = get_platform(args.platform)
    if not target_platform:
        print(f"❌ 不支持的平台: {args.platform}")
        print("支持的平台：" + "、".join(supported_platform_names()))
        return 2

    try:
        bloggers = load_bloggers_data(args.file, args.industry)
        validate_batch_size(args.max_follows)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"❌ 无法创建批次: {error}")
        return 2

    batches = split_batches(bloggers, args.max_follows)
    print(f"共 {len(bloggers)} 位候选，将按每批最多 {args.max_follows} 位分为 {len(batches)} 批处理。")
    for batch_number, batch in enumerate(batches, 1):
        print_batch_preview(target_platform, batch, batch_number, len(batches))
    if args.dry_run:
        print("✅ 名单校验通过（dry run，未打开浏览器，未执行关注）。")
        return 0

    db = BloggerDB()
    results = []
    stop_reason = None

    profile_dir = get_profile_dir(target_platform.name, args.profile_dir)
    os.makedirs(profile_dir, exist_ok=True)

    with sync_playwright() as playwright:
        # This is a dedicated profile for the selected platform, never an attachment to a running browser.
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            channel="chrome",
            viewport=None,
        )
        page = context.new_page()
        try:
            page.goto(target_platform.home_url, wait_until="domcontentloaded", timeout=45000)
        except Exception as error:
            print(f"❌ 无法打开平台首页: {error}")
            return 1

        for batch_number, batch in enumerate(batches, 1):
            if not request_batch_approval(target_platform, len(batch)):
                stop_reason = f"batch_{batch_number}_not_approved"
                print(f"已取消：未获得第 {batch_number}/{len(batches)} 批的明确确认。")
                break

            for item_number, item in enumerate(batch, 1):
                print(f"\n[批次 {batch_number}/{len(batches)}｜{item_number}/{len(batch)}] 处理：{item['name']}")
                try:
                    page.goto(target_platform.get_search_url(item["name"]), wait_until="domcontentloaded", timeout=35000)
                except Exception as error:
                    results.append(record(item, target_platform.name, "FAILED", f"页面加载失败: {error}"))
                    continue

                # Platform interventions end all remaining batches; they are never solved or retried by the script.
                if target_platform.check_captcha(page):
                    results.append(record(item, target_platform.name, "STOPPED", "检测到平台验证或风险提示，剩余批次已停止"))
                    stop_reason = "platform_intervention"
                    break

                try:
                    status, message, meta = target_platform.handle_follow(page, item["name"])
                except Exception as error:
                    status, message, meta = "FAILED", str(error), {}

                results.append(record(item, target_platform.name, status, message, meta))
                if status in {"SUCCESS", "ALREADY_FOLLOWED"}:
                    db.upsert_blogger({
                        "name": item["name"], "industry": item.get("industry", ""),
                        "platform": target_platform.name, "profile_url": meta.get("profile_url", ""),
                        "unique_id": meta.get("unique_id", ""), "category": item.get("category", "默认"),
                        "fans": item.get("fans", ""), "bio": meta.get("bio", ""), "status": status,
                    })
            if stop_reason:
                break

        output_path = save_results(target_platform.name, results)
        print("\n" + "=" * 76)
        print(f"批次结束：{stop_reason or 'completed'}")
        print(f"新增关注：{sum(r['status'] == 'SUCCESS' for r in results)}")
        print(f"已关注跳过：{sum(r['status'] == 'ALREADY_FOLLOWED' for r in results)}")
        print(f"结果文件：{output_path}")
        print("=" * 76)
        context.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
