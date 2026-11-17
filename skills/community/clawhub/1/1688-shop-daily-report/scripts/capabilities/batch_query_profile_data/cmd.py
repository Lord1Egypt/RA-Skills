#!/usr/bin/env python3
"""
Profile 补充数据批量并发查询 CLI 入口

一次调用完成所有店铺 × 所有查询类型的并发请求，
避免 Agent 逐条顺序调用带来的性能问题。

Usage（两种入参方式，二选一）:
    # 方式一：内联 JSON 字符串（bash / zsh 正常；Windows cmd.exe 会因单引号/双引号转义失败）
    python3 cli.py batch_query_profile_data \
        --queries '[{"label":"商品动销率","data_source":"SYCM","api_path":"portal/core/overview","params":{"dataType":"RECENT_1"}}]' \
        --shop_login_ids '["丹阳百世芬眼镜厂","丹阳光学眼镜"]'

    # 方式二（跨平台兜底，推荐）：把入参写进文件再传路径，彻底绕开 shell 引号转义
    # 文件内容为 JSON 对象：{"queries": [...], "shop_login_ids": [...], "max_workers": 5}
    python3 cli.py batch_query_profile_data --input_file .tmp/batch_query.json
"""

import os
import sys
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.query_shop_data.service import query_shop_data

COMMAND_NAME = "batch_query_profile_data"
COMMAND_DESC = "Profile 补充数据批量并发查询（多店铺×多查询类型，一次调用）"

# 并发上限，避免触发网关限流
MAX_WORKERS = 5


def _execute_single_query(label: str, data_source: str, api_path: str,
                          params: dict, login_id: str) -> dict:
    """执行单个查询，返回结构化结果（不抛异常）"""
    try:
        data = query_shop_data(data_source, api_path, params, login_id=login_id)
        return {
            "label": label,
            "login_id": login_id,
            "success": True,
            "data": data,
        }
    except Exception as e:
        return {
            "label": label,
            "login_id": login_id,
            "success": False,
            "error": str(e),
        }


def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--queries", "-q", required=False,
                        help='查询规格 JSON 数组，每项含 label/data_source/api_path/params')
    parser.add_argument("--shop_login_ids", "-ids", required=False,
                        help='店铺 loginId JSON 数组')
    parser.add_argument("--input_file", "-f", required=False,
                        help='入参文件路径（跨平台兜底，推荐）：JSON 对象，含 queries / shop_login_ids [/ max_workers]')
    parser.add_argument("--max_workers", type=int, default=MAX_WORKERS,
                        help=f'最大并发数（默认 {MAX_WORKERS}）')
    args = parser.parse_args()

    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法执行批量查询。\n\n请补充有效 AK 或检查鉴权配置后重试",
                     {"data": {}})
        return

    # 解析参数：优先文件入参（彻底绕开 shell 引号转义，Windows cmd.exe 兜底），否则用内联字符串
    queries = None
    shop_login_ids = None
    max_workers_override = None
    if args.input_file:
        try:
            with open(args.input_file, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print_output(False, f"入参文件读取/解析失败：{e}", {"data": {}})
            return
        if not isinstance(payload, dict):
            print_output(False, "入参文件内容必须为 JSON 对象（含 queries / shop_login_ids）", {"data": {}})
            return
        queries = payload.get("queries")
        shop_login_ids = payload.get("shop_login_ids")
        if payload.get("max_workers"):
            max_workers_override = payload.get("max_workers")
    else:
        if not args.queries or not args.shop_login_ids:
            print_output(False,
                         "缺少入参：需同时提供 --queries 与 --shop_login_ids，或改用 --input_file 传入文件路径",
                         {"data": {}})
            return
        try:
            queries = json.loads(args.queries)
        except json.JSONDecodeError as e:
            print_output(False, f"queries JSON 解析失败：{e}（Windows cmd.exe 请改用 --input_file 文件入参）", {"data": {}})
            return
        try:
            shop_login_ids = json.loads(args.shop_login_ids)
        except json.JSONDecodeError as e:
            print_output(False, f"shop_login_ids JSON 解析失败：{e}（Windows cmd.exe 请改用 --input_file 文件入参）", {"data": {}})
            return

    # 统一校验
    if not isinstance(queries, list) or not queries:
        print_output(False, "queries 必须为非空 JSON 数组", {"data": {}})
        return
    if not isinstance(shop_login_ids, list) or not shop_login_ids:
        print_output(False, "shop_login_ids 必须为非空 JSON 数组", {"data": {}})
        return

    # 构建任务列表：shops × queries
    tasks = []
    for login_id in shop_login_ids:
        for q in queries:
            label = q.get("label", q.get("api_path", "unknown"))
            data_source = q.get("data_source", "")
            api_path = q.get("api_path", "")
            params = q.get("params", {})
            if not data_source or not api_path:
                continue
            tasks.append((label, data_source, api_path, params, login_id))

    if not tasks:
        print_output(False, "无有效查询任务（请检查 queries 格式）", {"data": {}})
        return

    # 并发执行
    results_by_shop = {}
    total = len(tasks)
    success_count = 0
    failed_count = 0

    max_workers = min(max_workers_override or args.max_workers, total)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(_execute_single_query, *task): task
            for task in tasks
        }

        for future in as_completed(future_map):
            result = future.result()
            login_id = result["login_id"]
            label = result["label"]

            if login_id not in results_by_shop:
                results_by_shop[login_id] = {}

            if result["success"]:
                results_by_shop[login_id][label] = result["data"]
                success_count += 1
            else:
                results_by_shop[login_id][label] = {"_error": result["error"]}
                failed_count += 1

    # 输出
    summary = {
        "total": total,
        "success": success_count,
        "failed": failed_count,
        "shops": len(shop_login_ids),
        "query_types": len(queries),
    }

    markdown_parts = [
        f"批量查询完成：{len(shop_login_ids)} 店铺 × {len(queries)} 查询类型 = {total} 次调用",
        f"成功 {success_count} / 失败 {failed_count}",
    ]

    print_output(True, "，".join(markdown_parts), {
        "results": results_by_shop,
        "summary": summary,
    })


if __name__ == "__main__":
    main()
