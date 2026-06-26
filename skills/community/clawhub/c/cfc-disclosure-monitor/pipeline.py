"""
cfc-disclosure-monitor Pipeline — 三阶段贯通编排器

Phase 1 → Phase 2 → Phase 3 自动流水线：
  Phase 1 (collect.py)      : 采集公告列表 + 详情页正文/PDF
  Phase 2 (phase2_parse.py) : 解析 PDF/附件，提取合作机构实体
  Phase 3 (phase3_ontology.py): 写入知识图谱 (ontology graph.jsonl)

用法:
  python3 pipeline.py                       # 全量运行三阶段
  python3 pipeline.py --phase 1             # 只跑 Phase 1
  python3 pipeline.py --phase 2 中邮消费金融  # 从 Phase 2 开始，只处理中邮
  python3 pipeline.py --phase 3 --company 中邮消费金融  # 只跑 Phase 3
  python3 pipeline.py --list                 # 列出支持的公司
"""
import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).parent
RAW_DIR = SKILL_DIR.parent.parent / "cfc_raw_data"


def run_phase1(companies: list = None):
    """运行 Phase 1：采集公告列表。"""
    print("\n" + "=" * 60)
    print(f"Phase 1: 采集公告列表 | {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)

    cmd = [sys.executable, str(SKILL_DIR / "collect.py")]
    if companies:
        cmd.extend(["--companies", ",".join(companies)])
        print(f"Target: {companies}")
    else:
        print("Target: ALL 30 companies")

    result = subprocess.run(cmd, cwd=str(SKILL_DIR))
    return result.returncode == 0


def run_phase2(companies: list = None):
    """运行 Phase 2：解析 PDF/附件，提取合作机构。"""
    print("\n" + "=" * 60)
    print(f"Phase 2: 解析 PDF/附件，提取合作机构 | {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)

    cmd = [sys.executable, str(SKILL_DIR / "phase2_parse.py")]
    if companies:
        for co in companies:
            print(f"\n>> {co}")
            r = subprocess.run(cmd + [co], cwd=str(SKILL_DIR))
    else:
        r = subprocess.run(cmd, cwd=str(SKILL_DIR))
    return True


def run_phase3(companies: list = None):
    """运行 Phase 3：写入知识图谱。"""
    print("\n" + "=" * 60)
    print(f"Phase 3: 写入知识图谱 | {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)

    cmd = [sys.executable, str(SKILL_DIR / "phase3_ontology.py")]
    if companies:
        for co in companies:
            print(f"\n>> {co}")
            subprocess.run(cmd + [co], cwd=str(SKILL_DIR))
    else:
        subprocess.run(cmd, cwd=str(SKILL_DIR))
    return True


def list_companies():
    """列出 RAW_DIR 下已采集的公司。"""
    print("已采集的公司:")
    for d in sorted(RAW_DIR.iterdir()):
        if d.is_dir() and d.name != "parsed":
            ann_file = d / "announcements.json"
            count = 0
            if ann_file.exists():
                import json
                try:
                    with open(ann_file) as f:
                        count = len(json.load(f))
                except:
                    pass
            print(f"  {d.name} ({count} announcements)")


def run_full(companies: list = None):
    """完整流水线：P1 → P2 → P3。"""
    ok1 = run_phase1(companies)
    if not ok1:
        print("Phase 1 failed, continuing to Phase 2 anyway...")

    ok2 = run_phase2(companies)
    ok3 = run_phase3(companies)

    print("\n" + "=" * 60)
    print(f"Pipeline 完成 | {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    return ok1 and ok2 and ok3


def main():
    parser = argparse.ArgumentParser(description="cfc-disclosure-monitor Pipeline")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3], help="从哪个阶段开始（默认全部）")
    parser.add_argument("--company", type=str, help="指定公司名称（支持部分匹配）")
    parser.add_argument("--companies", type=str, help="逗号分隔的多个公司名")
    parser.add_argument("--list", action="store_true", help="列出已采集的公司")
    args = parser.parse_args()

    if args.list:
        list_companies()
        return

    companies = None
    if args.company:
        companies = [args.company]
    elif args.companies:
        companies = args.companies.split(",")

    phase = args.phase

    if phase == 1:
        run_phase1(companies)
    elif phase == 2:
        run_phase2(companies)
    elif phase == 3:
        run_phase3(companies)
    else:
        run_full(companies)


if __name__ == "__main__":
    main()
