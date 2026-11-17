#!/usr/bin/env python
"""save_result 命令行入口"""

import argparse

from _errors import SkillError
from _output import print_output, print_error, configure_windows_stdio

from capabilities.save_result import service


COMMAND_NAME = "save_result"
COMMAND_DESC = "落账任务执行/应用结果（每处理一个任务都必须存储）"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cli.py save_result",
        description="把单条任务的执行/应用结果写入台账",
    )
    p.add_argument("--task_id", default=None, help="任务 ID（T001…；优先用它定位）")
    p.add_argument("--item_id", default=None, help="商品 ID（与 --op 联合唯一定位）")
    p.add_argument("--op", default=None, help="优化项 op（与 --item_id 联合唯一定位）")
    p.add_argument("--status", default=None,
                   choices=("confirmed", "skipped", "running", "success", "failed", "cancelled"),
                   help="执行状态更新")
    p.add_argument("--result_summary", default=None, help="执行结果一句话摘要")
    p.add_argument("--result_images", default=None, nargs="+",
                   help="执行产物图（完整覆盖式更新：https:// 链接或 media-output 本地产物路径）")
    p.add_argument("--apply_status", default=None,
                   choices=("requested", "applied", "failed", "unknown", "cancelled"),
                   help="应用状态更新（写入回执到达后）")
    p.add_argument("--apply_detail", default=None, help="应用回执自然语言摘要")
    p.add_argument("--error", default=None, help="失败原因（自然语言，面向用户可读）")
    p.add_argument("--base_dir", default=None, help="台账根目录（默认当前工作目录）")
    return p


def main():
    configure_windows_stdio()
    args = build_parser().parse_args()

    try:
        result = service.save_result(
            task_id=args.task_id,
            item_id=args.item_id,
            op=args.op,
            status=args.status,
            result_summary=args.result_summary,
            result_images=args.result_images,
            apply_status=args.apply_status,
            apply_detail=args.apply_detail,
            error=args.error,
            base_dir=args.base_dir,
        )
    except SkillError as e:
        print_error(e)
        raise SystemExit(1)
    except Exception as e:
        print_error(e)
        raise SystemExit(1)

    md = "✅ 已落账任务 {}（商品 {} · {}）：status={}".format(
        result["task_id"], result["item_id"], result["op"], result["status"])
    if result.get("apply_status"):
        md += "，apply_status={}".format(result["apply_status"])
    stats = result.get("batch_stats") or {}
    md += "\n批次进度：{}/{} 已完成。".format(stats.get("done", 0), stats.get("total", 0))

    print_output(True, md, result)


if __name__ == "__main__":
    main()
