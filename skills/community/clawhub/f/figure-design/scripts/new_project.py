#!/usr/bin/env python3
"""Scaffold a figure-design project folder from the bundled templates.

Creates the seven-stage directory tree, copies the five templates with the
project code / name prefilled, writes a kanban checklist, and drops a
params.json that gate_check.py can consume.

Usage
-----
    python new_project.py --code MOCHI --name "麻糍兔" --out D:/projects \
        --ratio 1/7 --price 899 --height 240

    python new_project.py --code MOCHI --name "麻糍兔" --out . --mold steel --quantity 3000
"""

import argparse
import json
import os
import shutil
import sys
from datetime import date

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
TEMPLATE_DIR = os.path.join(SKILL_ROOT, "assets", "templates")

# destination folder -> template file
LAYOUT = [
    ("00_brief", "01_项目Brief.md", "01_项目Brief.md"),
    ("01_spec", "02_仕様書.md", "02_仕様書.md"),
    ("03_engineer", "03_拆件与工程表.csv", "03_拆件与工程表.csv"),
    ("04_sample", "04_打样验收单.md", "04_打样验收单.md"),
    ("05_production", "05_QC抽检表.csv", "05_QC抽检表.csv"),
]
EMPTY_DIRS = ["02_form", "06_launch"]

PHASES = [
    ("P0 立项", 10, [
        ("W01", "题材筛选", "3 个候选 + 打分表"),
        ("W02", "竞品扫描", "竞品对照表"),
        ("W03", "商业假设", "一页 Brief"),
        ("W04", "立项评审 G0", "Go/No-Go 记录"),
    ]),
    ("P1 设定", 8, [
        ("W05", "人设三问", "设定卡"),
        ("W06", "姿势三方案", "3 套姿势草图"),
        ("W07", "仕様書 v1", "仕様書"),
        ("W08", "授权核对", "送审包 + 排期"),
    ]),
    ("P2 造型", 12, [
        ("W09", "剪影测试", "黑形对比图"),
        ("W10", "三视图与动势", "三视图 v1"),
        ("W11", "表面与材质采样", "细节清单 + 参考照"),
        ("W12", "配色", "配色稿 + 色号"),
        ("W13", "造型评审 G1", "Design Freeze 记录"),
    ]),
    ("P3 建模工程", 18, [
        ("W14", "数字雕刻", "高模"),
        ("W15", "拆件方案", "拆件表"),
        ("W16", "结构工程", "工程模型 + 剖面图"),
        ("W17", "手板打印", "素模 5-10 件"),
        ("W18", "工程评审 G2", "DFM 回写"),
    ]),
    ("P4 打样", 12, [
        ("W19", "涂装打样", "Golden Sample"),
        ("W20", "包装与跌落", "包装打样 + 测试记录"),
        ("W21", "商品评审 G3", "放行单"),
    ]),
    ("P5 量产", 45, [
        ("W22", "开模与试模", "模具验收 + T1 样"),
        ("W23", "量产与 QC", "QC 报告"),
        ("W24", "上市与复盘", "复盘报告"),
    ]),
]

GATES = [
    ("G0", "W04 之后", "四项：一句话定位 / 四数一致 / 三个竞品 / 模具路线"),
    ("G1", "W13 之后", "四项：黑形测试 / 识别点数量 / 三视图 / 配色锁定"),
    ("G2", "W18 之后", "五项：可脱模 / 分模线不进脸 / 壁厚 / 数值间隙 / 工厂书面回签"),
    ("G3", "W21 之后", "四项：样品批准 / 毛利 3x / 包装跌落 / 盲盒合规"),
]


def read_template(name):
    path = os.path.join(TEMPLATE_DIR, name)
    with open(path, encoding="utf-8") as f:
        return f.read()


def build_readme(code, name, ratio, price, height, mold, qty):
    lines = []
    lines.append(f"# {code} | {name}\n")
    lines.append(f"> 由 figure-design 技能生成 · {date.today().isoformat()}\n")
    lines.append("## 基本参数\n")
    lines.append("| 项目 | 值 |")
    lines.append("|---|---|")
    lines.append(f"| 项目代号 | {code} |")
    lines.append(f"| 产品名 | {name} |")
    lines.append(f"| 比例 | {ratio or '待定'} |")
    lines.append(f"| 成品高度 | {height or '待定'} |")
    lines.append(f"| 目标零售价 | {price or '待定'} |")
    lines.append(f"| 模具路线 | {mold} |")
    lines.append(f"| 首批数量 | {qty or '待定'} |")
    lines.append("")
    lines.append("## 看板\n")
    lines.append("每张卡完成后才进入下一张；闸门未通过不得越段。\n")
    total = 0
    for phase, days, tasks in PHASES:
        lines.append(f"### {phase} · {days} 天\n")
        for tid, tname, out in tasks:
            lines.append(f"- [ ] **{tid}** {tname} — 交付：{out}")
            total += 1
        lines.append("")
    lines.append("### 闸门记录\n")
    for gid, when, criteria in GATES:
        lines.append(f"- [ ] **{gid}**（{when}）— {criteria}")
    lines.append("")
    lines.append(f"共 {total} 个任务、4 个闸门。\n")
    lines.append("## 命名规范\n")
    lines.append("`<CODE>_v<NN>_<内容>_<YYYYMMDD>.<ext>`，冻结版加 `FREEZE`，永不覆盖。\n")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="手办设计项目脚手架")
    ap.add_argument("--code", required=True, help="项目代号，例：MOCHI")
    ap.add_argument("--name", required=True, help="产品名，例：麻糍兔")
    ap.add_argument("--out", default=".", help="输出目录（默认当前目录）")
    ap.add_argument("--ratio", default="", help="比例，例：1/7")
    ap.add_argument("--price", default="", help="目标零售价，例：899")
    ap.add_argument("--height", default="", help="成品高度 mm，例：240")
    ap.add_argument("--mold", default="silicone", choices=["silicone", "steel"])
    ap.add_argument("--quantity", default="", help="首批数量")
    ap.add_argument("--force", action="store_true", help="目标目录已存在时覆盖")
    args = ap.parse_args()

    root = os.path.abspath(os.path.join(args.out, args.code))
    if os.path.exists(root) and not args.force:
        print(f"目录已存在：{root}\n如需覆盖请加 --force", file=sys.stderr)
        return 2
    if not os.path.isdir(TEMPLATE_DIR):
        print(f"找不到模板目录：{TEMPLATE_DIR}", file=sys.stderr)
        return 2

    created = []
    for folder, tpl, dest in LAYOUT:
        d = os.path.join(root, folder)
        os.makedirs(d, exist_ok=True)
        text = read_template(tpl)
        text = text.replace("{项目代号}", args.code).replace("{产品名}", args.name)
        with open(os.path.join(d, dest), "w", encoding="utf-8") as f:
            f.write(text)
        created.append(f"{folder}/{dest}")

    for d in EMPTY_DIRS:
        os.makedirs(os.path.join(root, d), exist_ok=True)
        created.append(f"{d}/")

    readme = build_readme(args.code, args.name, args.ratio, args.price,
                          args.height, args.mold, args.quantity)
    with open(os.path.join(root, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)
    created.append("README.md")

    params = {
        "ratio": args.ratio or None,
        "height_mm": float(args.height) if args.height else None,
        "price_cny": float(args.price) if args.price else None,
        "quantity": int(args.quantity) if args.quantity else None,
        "mold": args.mold,
        "material": "pvc" if args.mold == "steel" else "resin",
    }
    with open(os.path.join(root, "_params.json"), "w", encoding="utf-8") as f:
        json.dump(params, f, ensure_ascii=False, indent=2)
    created.append("_params.json")

    print(f"已创建项目：{root}")
    for c in created:
        print(f"  + {c}")
    print("\n下一步：")
    print(f"  1. 填 {root}/00_brief/01_项目Brief.md，跑 G0")
    print(f"  2. 校验参数：python scripts/gate_check.py \"{root}/_params.json\"")
    print("  3. 打开 README.md 当看板用")
    return 0


if __name__ == "__main__":
    sys.exit(main())
