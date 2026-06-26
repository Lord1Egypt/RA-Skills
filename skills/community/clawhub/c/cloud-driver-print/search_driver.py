from __future__ import annotations

import argparse
import json
import re

from driver_workflow import (
    fetch_driver_candidates,
    print_driver_candidates,
    resolve_and_update_driver_for_ip,
)


def normalize_query(text: str) -> str:
    """归一化用户输入，减少多余空白对匹配效果的影响。"""
    return re.sub(r"\s+", " ", text.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="根据用户输入的型号线索搜索打印机驱动。")
    parser.add_argument("query", nargs="?", help="用户输入的打印机品牌、型号或模糊描述。")
    parser.add_argument("--ip", help="读取该 IP 对应的打印机记录，用其型号或名称搜索并回写驱动。")
    parser.add_argument("--pick", type=int, help="直接指定要回写的驱动序号，从 1 开始。")
    parser.add_argument("--limit", type=int, default=5, help="最多返回多少条候选驱动。")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出搜索结果。")
    args = parser.parse_args()

    if args.ip:
        explicit_query = normalize_query(args.query) if args.query else None
        record, query, guessed, results, chosen = resolve_and_update_driver_for_ip(
            args.ip,
            explicit_query=explicit_query,
            limit=args.limit,
            picked=args.pick,
        )
        payload = {
            "input": query,
            "guessed_model": guessed,
            "results": results,
            "selected_driver": chosen["driver"],
            "printer_ip": record.ip,
            "note": "已完成驱动回写。",
        }
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return
        print_driver_candidates(query, guessed, results)
        print(f"已回写驱动: {chosen['driver']}")
        print(f"目标打印机: {record.name} | {record.ip}")
        return

    if not args.query:
        raise SystemExit("未提供查询词时，必须通过 --ip 指定已保存的打印机。")

    query = normalize_query(args.query)
    guessed, results = fetch_driver_candidates(query, limit=args.limit)
    payload = {
        "input": query,
        "guessed_model": guessed,
        "results": results,
        "note": "已调用驱动搜索适配层。",
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print_driver_candidates(query, guessed, results)


if __name__ == "__main__":
    main()
