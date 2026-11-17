#!/usr/bin/env python
"""parse_tasks 命令行入口"""

import argparse
import json

from _errors import SkillError
from _output import print_output, print_error, configure_windows_stdio

from capabilities.parse_tasks import service


COMMAND_NAME = "parse_tasks"
COMMAND_DESC = "解析主 Agent 已结构化的批量任务，写入台账并输出任务确认参数"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cli.py parse_tasks",
        description="解析批量任务并写入台账（1688-item-batch-opt-apply/tasks.json；开新批次时旧台账自动归档）",
    )
    p.add_argument("--tasks", required=True,
                   help="结构化任务 JSON 数组；商品任务 {item_id, op, requirements, item_title}，素材任务 {op, input_images, ...}；op 取值见 SKILL.md。任意输入（Excel/文件夹等）均由主 Agent 自行读取结构化后传入，脚本不解析文件")
    p.add_argument("--replace", action="store_true", default=False,
                   help="清空现有台账后重建（默认追加，重复任务跳过）；开新批次时旧台账自动归档为 tasks_<店铺前缀>_<旧批次ID>.json")
    p.add_argument("--store_name", default=None,
                   help="当前操作店铺展示名（可选；主 Agent 从宿主店铺上下文/选店结果取得）。仅用于台账元数据与归档/导出产物文件名前缀（如 批量任务结果_<店铺>_<批次ID>.xlsx），避免多店铺同会话运行时产物文件名重叠；不参与鉴权，未传时产物命名不带店铺前缀")
    p.add_argument("--base_dir", default=None,
                   help="台账根目录（默认当前工作目录；一般不需要显式传）")
    return p


def main():
    configure_windows_stdio()
    args = build_parser().parse_args()

    try:
        result = service.parse_tasks(
            tasks_json=args.tasks,
            replace=args.replace,
            base_dir=args.base_dir,
            store_name=args.store_name,
        )
    except SkillError as e:
        print_error(e)
        return
    except Exception as e:
        print_error(e)
        return

    md_lines = []
    if result["new_count"] > 0:
        md_lines.append("✅ 已解析 {} 个新任务（批次 {}），已写入台账。".format(
            result["new_count"], result["batch_id"]))
    else:
        md_lines.append("本次没有新增任务（重复任务已跳过 {} 个）。".format(
            result["skip_duplicates"]))
    if result["skip_duplicates"] > 0 and result["new_count"] > 0:
        md_lines.append("重复任务已跳过 {} 个。".format(result["skip_duplicates"]))
    if result["warnings"]:
        md_lines.append("")
        md_lines.append("⚠️ 解析提示：")
        for w in result["warnings"][:10]:
            md_lines.append("- {}".format(w))
    md_lines.append("")
    md_lines.append("下一步：按 SKILL.md 规则3 进入任务确认——当前主路径用 ask_user（mode=form）"
                    "多选题让用户勾选要执行的任务；data.confirm_card 暂存备用，"
                    "batch-task-confirm 组件上线放量后才弹 offer_select_card。")

    print_output(True, "\n".join(md_lines), result)


if __name__ == "__main__":
    main()
