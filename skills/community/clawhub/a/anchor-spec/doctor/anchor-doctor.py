#!/usr/bin/env python3
"""
anchor-doctor.py — 锚点生命周期自动化脚本

四种职责：
1. 腐烂治理（冷藏横幅 + 90天归档）
2. 任务锚点转制（14天+完成 → 蒸馏候选）
3. 孤儿检测（有产出无锚点）
4. 双轨与漂移巡检

三种模式：survey（只读盘点）/ doctor（周维护，dry-run默认）/ --json 输出
"""

import os
import sys
import json
import re
import shutil
import argparse
import datetime
from pathlib import Path


# ─────────────────────────────────────────────
# Root configuration (no hardcoded personal paths)
#   priority: CLI --root > env ANCHOR_ROOT > ./anchors
# ─────────────────────────────────────────────
ROOT = Path(os.environ.get("ANCHOR_ROOT", "./anchors"))
# ─────────────────────────────────────────────
# 阈值常量（便于调参）
# ─────────────────────────────────────────────
COLD_DAYS      = 30   # 冷藏线（天）
ARCHIVE_DAYS   = 90   # 归档线（天）
TASK_DONE_DAYS = 14   # 任务锚点完成判定（天）
README_MAX_LINES = 150  # README 硬上限行数

# 分类白名单
CLASSIFICATION_WHITELIST = {"projects", "research", "notes", "misc"}  # customize to your categories
# 排除目录（不扫描）
# 功能性子目录名：项目内部结构，永不判定为孤儿
FUNC_DIR_NAMES = {"src", "data", "assets", "backup", "outbox", "ref"}  # never treated as orphan projects  # never treated as orphan projects
EXCLUDE_DIRS = {".", "..", "archive", "temp", "_shared", "node_modules", "venv"}  # never scanned  # never scanned
# 不参与锚点体系的根目录
EXTRA_ROOT_EXCLUDE = {"INDEX.md", "_shared", "workflows", "anchor-survey"}
# 任务锚点类型值
TASK_TYPE_FINAL = "final"
# 冷藏横幅模板
COLD_BANNER_TEMPLATE = "> ⚠️ 冷藏（{date}）：{days}天+未动，可能过期，恢复时先验证关键事实"
# 日期格式
DATE_FMT = "%Y-%m-%d"

# 全局统计收集
_stats = {
    "projects": {"active": 0, "semi": 0, "rotting": 0, "deep_rotting": 0, "done": 0, "orphan": 0},
    "task_anchors": {"candidate": 0},
    "drift_dirs": [],
    "dual_rail": {"context_md": [], "readme_long": [], "docs_index": False},
    "orphan_dirs": [],
    "doctor_actions": [],
}

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def today():
    return datetime.date.today()

def days_ago(n):
    return (datetime.date.today() - datetime.timedelta(days=n))

def mtime_date(p: Path) -> datetime.date:
    """返回文件/目录的 mtime（date 粒度）"""
    return datetime.date.fromtimestamp(os.path.getmtime(p))

def scan_dir_top(p: Path):
    """返回目录下所有直接子项（不递归）"""
    try:
        return [e for e in p.iterdir() if e.name not in EXCLUDE_DIRS and not e.name.startswith(".")]
    except PermissionError:
        return []

def is_data_symlink(p: Path) -> bool:
    """判断是否为 data 软链（不扫描软链目标）"""
    return p.is_symlink() and p.name == "data"

def read_frontmatter(text: str) -> dict:
    """从 markdown 文本提取 YAML frontmatter（--- 块）"""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---\n", 3)
    if end == -1:
        return {}
    fm_text = text[4:end]
    result = {}
    for line in fm_text.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        result[key.strip()] = val.strip().strip('"').strip("'")
    return result

def read_banner_date(text: str) -> str | None:
    """从已有冷藏横幅提取日期字符串"""
    m = re.search(r"冷藏（(\d{4}-\d{2}-\d{2})）", text)
    return m.group(1) if m else None

def needs_cold_banner(anchor_path: Path) -> tuple[bool, str]:
    """
    判断某锚点文件是否需要插入冷藏横幅。
    返回 (needs, reason)
    """
    text = anchor_path.read_text(errors="replace")
    # 已有横幅 → 不需要
    if "冷藏（" in text and "⚠️" in text:
        return False, "已有横幅"
    # 检查 mtime
    mdate = mtime_date(anchor_path)
    age = (today() - mdate).days
    if age >= COLD_DAYS:
        return True, f"年龄{age}天"
    return False, f"年龄{age}天，未达冷藏线"

def check_readme_done(text: str) -> bool:
    """从 README 文本判断是否明确完结（✅/完成/归档）"""
    first_lines = "\n".join(text.splitlines()[:20])
    return bool(
        re.search(r"[✅📦🏁]|\b完成\b|\b归档\b|\bdone\b|\bfinished\b|\bclosed\b", first_lines, re.IGNORECASE)
    )

def get_last_active(project_dir: Path) -> datetime.date:
    """项目最后活跃时间 = 锚点文件与目录内所有文件的 max mtime"""
    mtimes = []
    for root, dirs, files in os.walk(project_dir):
        # 排除子目录 tasks（任务锚点单独管）
        dirs[:] = [d for d in dirs if d != "tasks"]
        for fname in files:
            if fname.startswith("."):
                continue
            fpath = Path(root) / fname
            if is_data_symlink(fpath):
                continue
            try:
                mtimes.append(os.path.getmtime(fpath))
            except OSError:
                pass
    if not mtimes:
        return today()
    return datetime.date.fromtimestamp(max(mtimes))

def classify_project(project_dir: Path, anchor_path: Path | None, last_active: datetime.date) -> str:
    """分类项目状态桶"""
    if anchor_path is None:
        return "orphan"
    text = anchor_path.read_text(errors="replace")
    if check_readme_done(text):
        return "done"
    age = (today() - last_active).days
    if age < 14:
        return "active"
    elif age < 30:
        return "semi"
    elif age < 90:
        return "rotting"
    else:
        return "deep_rotting"

def ensure_archive_dir() -> Path:
    """确保归档目录存在"""
    archive_root = ROOT / "archive" / "anchors"
    archive_root.mkdir(parents=True, exist_ok=True)
    return archive_root

def archive_project(project_dir: Path, archive_root: Path):
    """
    将项目目录归档到 archive/anchors/，
    冲突处理：同名加 -2 / -3 后缀
    """
    target = archive_root / project_dir.name
    counter = 2
    while target.exists():
        target = archive_root / f"{project_dir.name}-{counter}"
        counter += 1
    shutil.copytree(project_dir, target, symlinks=True)  # 保留软链结构
    return target

# ─────────────────────────────────────────────
# Survey 模式
# ─────────────────────────────────────────────

def survey_docs_root():
    """检测 docs/ 根下的漂移目录 + docs/INDEX.md 存在性"""
    docs = ROOT
    for item in docs.iterdir():
        if item.name in EXCLUDE_DIRS or item.name.startswith("."):
            continue
        if item.is_dir():
            if item.name not in CLASSIFICATION_WHITELIST:
                _stats["drift_dirs"].append(str(item))
        elif item.is_file() and item.name == "INDEX.md":
            _stats["dual_rail"]["docs_index"] = True

def scan_projects():
    """扫描所有分类项目"""
    docs = ROOT
    for cat in CLASSIFICATION_WHITELIST:
        cat_dir = docs / cat
        if not cat_dir.is_dir():
            continue
        for item in cat_dir.iterdir():
            if item.name.startswith("."):
                continue
            if not item.is_dir():
                continue
            scan_single_project(item, cat, docs)

def scan_single_project(project_dir: Path, cat: str, docs: Path):
    """扫描单个项目目录"""
    seed = project_dir / "SEED.md"
    readme = project_dir / "README.md"

    # 锚点文件存在性
    anchor_path = None
    if readme.is_file():
        anchor_path = readme
    elif seed.is_file():
        anchor_path = seed

    # 最后活跃时间
    last_active = get_last_active(project_dir)

    # 分类桶
    bucket = classify_project(project_dir, anchor_path, last_active)
    _stats["projects"][bucket] += 1

    # 双轨检测：CONTEXT.md
    ctx = project_dir / "CONTEXT.md"
    if ctx.is_file():
        _stats["dual_rail"]["context_md"].append(str(ctx.relative_to(docs.parent)))

    # 双轨检测：README 超 150 行
    if readme.is_file():
        line_count = sum(1 for _ in readme.open(errors="replace"))
        if line_count > README_MAX_LINES:
            _stats["dual_rail"]["readme_long"].append(
                f"{project_dir.name} ({line_count}行)"
            )

    # 孤儿目录检测（无锚点 + 有产出文件）
    if anchor_path is None:
        # 容器目录跳过：直接子目录中有带锚点的（本目录是项目群/中间层，非孤儿）
        child_has_anchor = any(
            (child / "README.md").is_file() or (child / "SEED.md").is_file()
            for child in project_dir.iterdir() if child.is_dir()
        )
        # 功能性子目录跳过：这些名字是项目内部结构（出稿/资料/源码等），不是独立项目
        if project_dir.name.lower() in FUNC_DIR_NAMES:
            child_has_anchor = True
        has_output = any(
            f.is_file() and not f.name.startswith(".") and f.suffix in (".md", ".py", ".sh", ".json", ".csv", ".txt", ".xlsx")
            for f in project_dir.rglob("*")
            if f.is_file()
        )
        if has_output and not child_has_anchor:
            age = (today() - last_active).days
            # 排除：文件数≤1 且 6个月+未动（一次性产出，放过）
            file_count = sum(1 for _ in project_dir.rglob("*") if _.is_file() and not _.name.startswith("."))
            if file_count > 1 or age <= 180:
                _stats["orphan_dirs"].append(
                    f"{project_dir.name} (文件数={file_count}, 未动{age}天)"
                )

def scan_task_anchors():
    """扫描所有 tasks/ 目录下的任务锚点"""
    docs = ROOT
    for root, dirs, files in os.walk(docs):
        # 只进 tasks 子目录
        if Path(root).name != "tasks":
            continue
        for fname in files:
            if not fname.endswith(".md") or fname.startswith("."):
                continue
            fpath = Path(root) / fname
            if is_data_symlink(fpath):
                continue
            try:
                text = fpath.read_text(errors="replace")
            except Exception:
                continue
            fm = read_frontmatter(text)
            task_type = fm.get("type", "")
            mdate = mtime_date(fpath)
            age = (today() - mdate).days

            # type=final 且 age > TASK_DONE_DAYS → 候选
            if task_type == TASK_TYPE_FINAL and age > TASK_DONE_DAYS:
                _stats["task_anchors"]["candidate"] += 1
            elif not task_type and age > TASK_DONE_DAYS:
                # type 缺失，按 mtime 推断
                _stats["task_anchors"]["candidate"] += 1

def build_survey_report() -> str:
    """构建 survey markdown 报告"""
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    p = _stats["projects"]
    lines = [
        f"# 锚点体检报告（{date_str}）",
        "",
        "## 项目锚点分类概览",
        "",
        "| 桶 | 数量 | 说明 |",
        "|---|---:|---|",
        f"| 🟢 活跃（<14天） | {p['active']} | 正常运行 |",
        f"| 🟠 半死（14-30天） | {p['semi']} | 轻微关注 |",
        f"| 🟡 腐烂（30-90天） | {p['rotting']} | 需冷藏 |",
        f"| 🔴 深腐烂（>90天） | {p['deep_rotting']} | 建议归档 |",
        f"| ✅ 明确完结 | {p['done']} | 已收尾 |",
        f"| 👻 孤儿（无锚点） | {p['orphan']} | 需补锚点 |",
        "",
        f"**合计项目数**：{sum(p.values())}",
        "",
    ]

    if _stats["drift_dirs"]:
        lines += [
            "## 漂移目录（docs/ 根下未分类）",
            "",
        ]
        for d in _stats["drift_dirs"]:
            lines.append(f"- `{d}`")
        lines.append("")

    dr = _stats["dual_rail"]
    if dr["context_md"] or dr["readme_long"] or dr["docs_index"]:
        lines += ["## 双轨检测", ""]
        if dr["context_md"]:
            lines.append(f"**CONTEXT.md 存量**（应已废除）：{len(dr['context_md'])} 个")
            for c in dr["context_md"][:10]:
                lines.append(f"  - `{c}`")
            if len(dr["context_md"]) > 10:
                lines.append(f"  _...还有 {len(dr['context_md'])-10} 个_")
            lines.append("")
        if dr["readme_long"]:
            lines.append(f"**README 超过{README_MAX_LINES}行**（违规）：{len(dr['readme_long'])} 个")
            for r in dr["readme_long"]:
                lines.append(f"  - {r}")
            lines.append("")
        if dr["docs_index"]:
            lines.append(f"⚠️ **docs/INDEX.md 存在**（应只有 `_shared/INDEX.md`）")
            lines.append("")

    if _stats["orphan_dirs"]:
        lines += [
            "## 孤儿目录（无锚点有产出）",
            "",
        ]
        for o in _stats["orphan_dirs"]:
            lines.append(f"- `{o}`")
        lines.append("")

    lines += [
        f"## 任务锚点候选（type=final 且 >{TASK_DONE_DAYS}天未动）",
        "",
        f"**{_stats['task_anchors']['candidate']}** 个",
        "",
        "_详细清单需 doctor 模式输出_",
        "",
        f"---\n*由 anchor-doctor.py survey 生成 | {date_str}*",
    ]
    return "\n".join(lines)

def run_survey():
    """执行 survey 模式"""
    survey_docs_root()
    scan_projects()
    scan_task_anchors()

    report = build_survey_report()

    # 写报告文件
    out_dir = ROOT / "temp"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"anchor-survey-{datetime.date.today().strftime('%Y%m%d')}.md"
    out_file.write_text(report)

    # stdout 摘要
    p = _stats["projects"]
    print("=== anchor-doctor survey ===")
    print(f"项目锚点：🟢{p['active']}  🟠{p['semi']}  🟡{p['rotting']}  🔴{p['deep_rotting']}  ✅{p['done']}  👻{p['orphan']}")
    print(f"任务锚点候选：{_stats['task_anchors']['candidate']} 个")
    print(f"漂移目录：{len(_stats['drift_dirs'])} 个")
    print(f"CONTEXT.md存量：{len(_stats['dual_rail']['context_md'])} 个")
    print(f"README超行：{len(_stats['dual_rail']['readme_long'])} 个")
    print(f"孤儿目录：{len(_stats['orphan_dirs'])} 个")
    print(f"docs/INDEX.md存在：{_stats['dual_rail']['docs_index']}")
    print(f"\n报告已写：{out_file}")

    return report, out_file

# ─────────────────────────────────────────────
# Doctor 模式
# ─────────────────────────────────────────────

def doctor_projects(execute: bool = False):
    """执行 doctor 模式：冷藏横幅 + 90天归档"""
    docs = ROOT
    archive_root = ensure_archive_dir()
    today_str = datetime.date.today().strftime(DATE_FMT)

    for cat in CLASSIFICATION_WHITELIST:
        cat_dir = docs / cat
        if not cat_dir.is_dir():
            continue
        for item in cat_dir.iterdir():
            if not item.is_dir() or item.name.startswith("."):
                continue
            doctor_single_project(item, cat, archive_root, today_str, execute)

def doctor_single_project(project_dir: Path, cat: str, archive_root: Path, today_str: str, execute: bool):
    """处理单个项目：冷藏 / 归档 / 摘横幅"""
    readme = project_dir / "README.md"
    seed = project_dir / "SEED.md"
    anchor_path = readme if readme.is_file() else seed if seed.is_file() else None

    if anchor_path is None:
        # 孤儿 → 跳过（不动手）
        return

    last_active = get_last_active(project_dir)
    age = (today() - last_active).days

    # 已有横幅：检查是否需要摘除
    text = anchor_path.read_text(errors="replace")
    banner_date_str = read_banner_date(text)

    if banner_date_str and "冷藏（" in text:
        # 横幅在场且文件 mtime 晚于横幅日期 → 复活摘横幅
        try:
            banner_date = datetime.datetime.strptime(banner_date_str, DATE_FMT).date()
        except ValueError:
            banner_date = None

        if banner_date and last_active > banner_date:
            lines = text.splitlines()
            new_lines = []
            skip_banner = False
            for i, line in enumerate(lines):
                if "冷藏（" in line and "⚠️" in line:
                    skip_banner = True
                    continue
                new_lines.append(line)
            if skip_banner:
                new_text = "\n".join(new_lines).rstrip() + "\n"
                if execute:
                    anchor_path.write_text(new_text)
                _stats["doctor_actions"].append(
                    f"{'✅' if execute else '[DRY]'} 摘冷藏横幅：{project_dir.name}"
                )
        return  # 有横幅不管归档

    # 无横幅：判断是否需要插横幅或归档
    if age >= ARCHIVE_DAYS:
        target = archive_project(project_dir, archive_root)
        _stats["doctor_actions"].append(
            f"{'📦' if execute else '[DRY]'} 归档{age}天项目：{project_dir.name} → {target.name}"
        )
    elif age >= COLD_DAYS:
        # 插入冷藏横幅（在第一个 # 标题后）
        lines = text.splitlines()
        insert_after = None
        for i, line in enumerate(lines):
            if line.startswith("# "):
                insert_after = i
                break

        banner = COLD_BANNER_TEMPLATE.format(date=today_str, days=age)
        if insert_after is not None:
            new_lines = lines[:insert_after+1] + ["", banner] + lines[insert_after+1:]
        else:
            new_lines = [banner, ""] + lines

        new_text = "\n".join(new_lines) + "\n"
        if new_text != text:
            if execute:
                anchor_path.write_text(new_text)
            _stats["doctor_actions"].append(
                f"{'⚠️' if execute else '[DRY]'} 插冷藏横幅（{age}天）：{project_dir.name}"
            )

def doctor_task_anchors(execute: bool = False):
    """doctor：任务锚点候选清单（只报告，不动手）"""
    docs = ROOT
    candidates = []

    for root, dirs, files in os.walk(docs):
        if Path(root).name != "tasks":
            continue
        for fname in files:
            if not fname.endswith(".md") or fname.startswith("."):
                continue
            fpath = Path(root) / fname
            try:
                text = fpath.read_text(errors="replace")
            except Exception:
                continue
            fm = read_frontmatter(text)
            mdate = mtime_date(fpath)
            age = (today() - mdate).days
            task_type = fm.get("type", "")
            if (task_type == TASK_TYPE_FINAL or not task_type) and age > TASK_DONE_DAYS:
                candidates.append((fpath, task_type, age))

    if candidates:
        _stats["doctor_actions"].append(
            f"[INFO] 任务锚点蒸馏候选：{len(candidates)} 个（需AI蒸馏流程处理，不自动删除）"
        )

def run_doctor(execute: bool = False):
    """执行 doctor 模式"""
    doctor_projects(execute)
    doctor_task_anchors(execute)

    print("=== anchor-doctor doctor ===")
    print(f"模式：{'EXECUTE（真执行）' if execute else 'DRY-RUN（只打印计划）'}")
    if _stats["doctor_actions"]:
        for a in _stats["doctor_actions"]:
            print(f"  {a}")
    else:
        print("  （无动作）")
    print(f"\n任务锚点候选：{_stats['task_anchors']['candidate']} 个（doctor 不自动处理）")

# ─────────────────────────────────────────────
# JSON 输出
# ─────────────────────────────────────────────

def stats_to_json() -> dict:
    return {
        "date": datetime.date.today().strftime(DATE_FMT),
        "projects": _stats["projects"],
        "task_anchors": _stats["task_anchors"],
        "drift_dirs": _stats["drift_dirs"],
        "dual_rail": _stats["dual_rail"],
        "orphan_dirs": _stats["orphan_dirs"],
        "doctor_actions": _stats["doctor_actions"],
    }

# ─────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="anchor-doctor: 锚点生命周期自动化")
    parser.add_argument("mode", choices=["survey", "doctor"], help="survey=只读盘点 / doctor=周维护")
    parser.add_argument("--execute", action="store_true", help="doctor 模式：真执行（默认 dry-run）")
    parser.add_argument("--json", action="store_true", help="输出 JSON（与 markdown 并存）")

    args = parser.parse_args()

    if args.mode == "survey":
        run_survey()
        if args.json:
            print("\n--- JSON ---")
            print(json.dumps(stats_to_json(), ensure_ascii=False, indent=2))
    else:
        run_doctor(execute=args.execute)
        if args.json:
            print("\n--- JSON ---")
            print(json.dumps(stats_to_json(), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
