#!/usr/bin/env python3
"""
install-ecc-bundle.py — 一键安装 ECC Bundle (23 个核心技能)

将本技能包 bundle/ 目录下的 23 个 SKILL.md 写入目标 ~/.agents/skills/<name>/

用法:
  python scripts/install-ecc-bundle.py [OPTIONS]

选项:
  --target DIR    目标 agents skills 目录 (默认: ~/.agents/skills)
  --dry-run       只查看, 不实际写入
  --force         覆盖已存在的同名技能
  --backup        覆盖前先备份(默认 .bak-<timestamp>)
  --uninstall     反向: 删除这 23 个技能

退出码:
  0 - 全部成功
  1 - 部分失败
  2 - 完全失败 (源目录缺失)
"""
import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

BUNDLE_DIR = Path(__file__).resolve().parent.parent / "bundle"
DEFAULT_TARGET = Path.home() / ".agents" / "skills"
SKILLS = [
    "agentic-engineering", "agent-eval", "ai-first-engineering", "autonomous-loops",
    "architecture-decision-records", "codebase-onboarding", "context-budget",
    "continuous-agent-loop", "cost-aware-llm-pipeline", "deployment-patterns",
    "deep-research", "docker-patterns", "git-workflow", "prompt-optimizer",
    "safety-guard", "search-first", "security-review", "security-scan", "skill-comply",
    "token-budget-advisor", "rules-distill", "product-lens", "blueprint",
]


def log(msg: str):
    print(f"[ECC-BUNDLE] {msg}")


def install(target: Path, dry_run: bool = False, force: bool = False, backup: bool = True) -> int:
    if not BUNDLE_DIR.exists():
        log(f"FATAL: bundle 目录不存在: {BUNDLE_DIR}")
        return 2

    if not target.exists():
        log(f"目标目录不存在: {target}")
        log(f"  尝试创建: {target}")
        if not dry_run:
            target.mkdir(parents=True, exist_ok=True)

    log(f"目标: {target}")
    log(f"源: {BUNDLE_DIR}")
    log(f"动作: {'DRY-RUN' if dry_run else 'INSTALL'} (force={force}, backup={backup})")
    log("")

    success = 0
    failed = []

    for skill_name in SKILLS:
        src = BUNDLE_DIR / f"{skill_name}.md"
        dst_dir = target / skill_name
        dst = dst_dir / "SKILL.md"

        if not src.exists():
            log(f"  - {skill_name}: SKIP (源缺失)")
            failed.append(skill_name)
            continue

        if dst.exists() and not force:
            log(f"  - {skill_name}: SKIP (已存在, 用 --force 覆盖)")
            continue

        if dst.exists() and backup and not dry_run:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            bak = dst.with_suffix(f".md.bak-{ts}")
            shutil.copy2(dst, bak)
            log(f"  - {skill_name}: backup → {bak.name}")

        if dry_run:
            log(f"  - {skill_name}: WOULD INSTALL")
            success += 1
            continue

        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        log(f"  - {skill_name}: OK ({src.stat().st_size} bytes)")
        success += 1

    log("")
    log(f"总计: {success}/{len(SKILLS)} 成功, {len(failed)} 失败")
    if failed:
        log(f"失败列表: {', '.join(failed)}")
        return 1
    return 0


def uninstall(target: Path, dry_run: bool = False) -> int:
    log(f"目标: {target}")
    log(f"动作: {'DRY-RUN' if dry_run else 'UNINSTALL'}")
    removed = 0
    for skill_name in SKILLS:
        dst = target / skill_name / "SKILL.md"
        if dst.exists():
            if not dry_run:
                # 删除整个目录
                skill_dir = target / skill_name
                if skill_dir.exists():
                    shutil.rmtree(skill_dir)
                log(f"  - {skill_name}: REMOVED")
            else:
                log(f"  - {skill_name}: WOULD REMOVE")
            removed += 1
        else:
            log(f"  - {skill_name}: NOT INSTALLED")
    log("")
    log(f"总计: {removed}/{len(SKILLS)} 移除")
    return 0


def main():
    parser = argparse.ArgumentParser(description="ECC Bundle 一键安装器")
    parser.add_argument("--target", type=str, default=str(DEFAULT_TARGET),
                        help=f"目标 agents skills 目录 (默认: {DEFAULT_TARGET})")
    parser.add_argument("--dry-run", action="store_true", help="只看, 不实际写入")
    parser.add_argument("--force", action="store_true", help="覆盖已有技能")
    parser.add_argument("--backup", action="store_true", default=True, help="覆盖前备份")
    parser.add_argument("--no-backup", dest="backup", action="store_false", help="不备份")
    parser.add_argument("--uninstall", action="store_true", help="反向卸载")
    args = parser.parse_args()

    target = Path(args.target).expanduser()

    if args.uninstall:
        return uninstall(target, dry_run=args.dry_run)
    return install(target, dry_run=args.dry_run, force=args.force, backup=args.backup)


if __name__ == "__main__":
    sys.exit(main())
