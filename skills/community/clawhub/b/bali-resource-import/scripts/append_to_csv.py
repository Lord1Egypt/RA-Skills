#!/usr/bin/env python3
"""
巴厘岛旅游资源 CSV 入库脚本
用法: python append_to_csv.py --type TYPE --input DATA --target CSV_PATH [--template TMPL]

示例:
  python append_to_csv.py --type hotel --input data.csv --target C:\\output\\hotel.csv
  python append_to_csv.py --type activity --input bounty.csv --target C:\\output\\activity.csv --template C:\\templates\\activity_template.csv

支持的 TYPE: hotel, car, attraction, activity, spa, club, restaurant, tea
"""

import argparse
import csv
import os
import sys

# ── 8类资源 CSV 文件名映射 ────────────────────────────────────────────────
CSV_FILES = {
    "hotel":      "巴厘岛酒店资源库_2026标准版_V4_FINAL.csv",
    "car":        "巴厘岛车费成本表-成本_2.10.csv",
    "attraction": "景点标准化完整版_含人群标签与特色标签_V4.csv",
    "activity":   "活动标准化完整版_含人群标签与特色标签_V4.csv",
    "spa":        "SPA标准化完整版_含人群标签与特色标签_V4.csv",
    "club":       "俱乐部标准化完整版_含人群标签与特色标签_V4.csv",
    "restaurant": "餐厅标准化完整版_含人群标签与特色标签_V4.csv",
    "tea":        "下午茶标准化完整版_含人群标签与特色标签_V4.csv",
}

# ── 默认生产库（仅用于退而求其次的默认值）──────────────────────────────
_DEFAULT_BASE = os.path.join(os.path.expanduser("~"), ".openclaw", "csv")


def resolve_target_path(target_arg, resource_type):
    """
    将 --target 参数转为完整 CSV 路径。
    规则：
      - target 是完整 .csv 路径 → 直接使用
      - target 是目录路径   → 拼接 CSV_FILES[resource_type]
      - target 省略         → 使用默认生产库 + 默认文件名
    """
    if target_arg.endswith(".csv"):
        return os.path.normpath(target_arg)

    # target 是目录或为空
    base = target_arg.strip() if target_arg.strip() else _DEFAULT_BASE
    fname = CSV_FILES.get(resource_type, "output.csv")
    return os.path.normpath(os.path.join(base, fname))


def resolve_template_path(template_arg, resource_type):
    """
    查找模板文件路径。

    顺序（HIGH to LOW）：
      1. --template CLI 参数（用户提供的自定义模板，必须存在）
      2. 生产库目录下的同名 CSV（references 无 CSV 时退回）
    """
    fname = CSV_FILES.get(resource_type)

    if template_arg:
        # 用户明确指定 → 必须存在
        if os.path.exists(template_arg):
            return os.path.normpath(template_arg)
        print(f"[ERROR] 用户指定模板不存在: {template_arg}")
        sys.exit(1)

    # 退回到生产库
    fallback = os.path.join(_DEFAULT_BASE, fname)
    if os.path.exists(fallback):
        return os.path.normpath(fallback)

    # skill 内置 references 目录
    skill_ref = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", fname)
    )
    if os.path.exists(skill_ref):
        return skill_ref

    print(f"[ERROR] 找不到资源类型 '{resource_type}' 的模板文件：")
    print(f"   生产库: {fallback} {'存在' if os.path.exists(fallback) else '不存在'}")
    print(f"   skill:  {skill_ref} {'存在' if os.path.exists(skill_ref) else '不存在'}")
    sys.exit(1)


def append_to_csv(csv_path, new_rows):
    """
    追加记录到指定 CSV 路径
    """
    rows = []
    headers = None

    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            rows = list(reader)
    else:
        # 文件不存在，从 new_rows 提取 headers
        if new_rows:
            headers = list(new_rows[0].keys())
        else:
            print("[WARN] 新文件且无数据")
            return csv_path

    if not headers:
        headers = list(new_rows[0].keys()) if new_rows else []

    rows.extend(new_rows)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    return csv_path


def validate_rows(resource_type, rows):
    """验证必填字段，返回告警列表"""
    required_map = {
        "hotel":      ["英文名称", "Zone ID", "星级"],
        "car":        ["编号", "车型", "全天 (Full Day)"],
        "attraction": ["编号", "景点英文名", "Zone ID"],
        "activity":   ["contract_id (合同编号)", "activitynameen (活动英文名)", "Zone ID"],
        "spa":        ["编号", "活动英文名", "Zone ID"],
        "club":       ["俱乐部名称", "Zone ID", "入场/门票费用"],
        "restaurant": ["编号", "餐厅名称", "Zone ID"],
        "tea":        ["编号", "餐厅名称", "Zone ID"],
    }
    required = required_map.get(resource_type, [])
    alerts = []
    for i, row in enumerate(rows):
        name = (row.get("英文名称") or row.get("景点英文名")
                or row.get("餐厅名称") or row.get("俱乐部名称")
                or row.get("活动英文名", "unknown"))
        missing = [f for f in required if not row.get(f)]
        if missing:
            alerts.append({"row": i + 1, "resource": name, "missing": missing})
    return alerts


def main():
    parser = argparse.ArgumentParser(
        description="巴厘岛旅游资源 CSV 入库脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--type", "-t", required=True,
                        choices=list(CSV_FILES.keys()),
                        help="资源类型")
    parser.add_argument("--input", "-i", required=True,
                        help="输入 CSV 文件路径（包含待入库数据）")
    parser.add_argument("--target", "-o",
                        help="目标 CSV 路径（完整文件路径或目录路径）；省略则使用默认生产库")
    parser.add_argument("--template", "-m",
                        help="模板文件路径（用户自定义模板，文件不存在则报错）")
    parser.add_argument("--dry-run", action="store_true",
                        help="模拟运行，不实际写入")

    args = parser.parse_args()

    # ── 确定目标路径 ───────────────────────────────────────────────
    target_path = resolve_target_path(args.target, args.type)
    print(f"[OK] 目标路径: {target_path}")

    # ── 确定模板路径 ───────────────────────────────────────────────
    template_path = resolve_template_path(args.template, args.type)
    print(f"[OK] 使用模板: {template_path}")

    # ── 读取输入数据 ────────────────────────────────────────────────
    if not os.path.exists(args.input):
        print(f"[ERROR] 输入文件不存在: {args.input}")
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8-sig", errors="replace") as f:
        new_rows = list(csv.DictReader(f))

    if not new_rows:
        print("[WARN] 输入文件没有数据")
        sys.exit(0)

    print(f"[OK] 待入库记录数: {len(new_rows)}")

    # ── 验证必填字段 ───────────────────────────────────────────────
    alerts = validate_rows(args.type, new_rows)
    if alerts:
        print(f"[WARN] {len(alerts)} 条数据缺少必填字段:")
        for a in alerts[:5]:
            print(f"   行{a['row']}: {a['resource']} - 缺失 {a['missing']}")

    # ── 写入 CSV ────────────────────────────────────────────────────
    if args.dry_run:
        print("[WARN] 模拟运行模式，未实际写入")
    else:
        path = append_to_csv(target_path, new_rows)
        print(f"[OK] 入库完成: {path}")


if __name__ == "__main__":
    main()