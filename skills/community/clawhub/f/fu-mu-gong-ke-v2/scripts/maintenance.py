#!/usr/bin/env python3
"""
父母的功课 - 技能维护脚本 (v1.0.0)
自动检查更新、提交、推送和发布。

用法:
    python3 scripts/maintenance.py          # 检查+提交+推送+发布
    python3 scripts/maintenance.py --check  # 仅检查是否有变更
    python3 scripts/maintenance.py --dry    # 模拟运行，不实际操作

定时任务建议：
    # 每周日早8点自动同步
    0 8 * * 0 cd /path/to/skill && python3 scripts/maintenance.py --dry

环境变量:
    ALLOW_AUTO_PUSH — 设为1允许自动推送到GitHub
    ALLOW_AUTO_PUBLISH — 设为1允许自动发布到ClawHub
"""

import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
VERSION_FILE = SKILL_DIR / "VERSION"


def run(cmd: list, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=SKILL_DIR, check=check)


def get_version() -> str:
    return VERSION_FILE.read_text().strip()


def has_changes() -> bool:
    """检查是否有未提交的变更"""
    r = run(["git", "status", "--porcelain"], check=False)
    return bool(r.stdout.strip())


def staged_count() -> int:
    r = run(["git", "diff", "--cached", "--stat"], check=False)
    return len(r.stdout.strip().splitlines()) if r.stdout.strip() else 0


def auto_commit() -> bool:
    """自动提交所有变更"""
    if not has_changes():
        print("✅ 无变更，跳过提交")
        return False
    
    version = get_version()
    summary = f"auto: v{version} 定时维护"

    run(["git", "add", "-A"])
    run(["git", "commit", "-m", summary, "--allow-empty"])
    print(f"📦 已提交: {summary}")
    return True


def auto_push() -> bool:
    """推送到 GitHub"""
    if not os.environ.get("ALLOW_AUTO_PUSH"):
        print("⏭️  跳过推送 (设置 ALLOW_AUTO_PUSH=1 以启用)")
        return False
    
    r = run(["git", "push", "origin", "master", "--no-verify"], check=False)
    if r.returncode == 0:
        print(f"🚀 已推送到 GitHub")
        return True
    else:
        print(f"⚠️  推送失败: {r.stderr[:200]}")
        return False


def auto_publish():
    """发布到 ClawHub"""
    if not os.environ.get("ALLOW_AUTO_PUBLISH"):
        print("⏭️  跳过 ClawHub 发布 (设置 ALLOW_AUTO_PUBLISH=1 以启用)")
        return False
    
    version = get_version()
    today = datetime.now().strftime("%Y-%m-%d")
    
    r = run(["clawhub", "publish", ".", "--slug", "fu-mu-gong-ke",
             "--name", "父母的功课", "--version", version,
             "--changelog", f"auto: v{version} ({today})"],
            check=False)
    
    if r.returncode == 0:
        print(f"✅ 已发布到 ClawHub: v{version}")
        return True
    elif "Version already exists" in r.stderr:
        print(f"ℹ️  ClawHub v{version} 已存在，跳过")
        return True
    else:
        print(f"⚠️  ClawHub 发布失败: {r.stderr[:200]}")
        return False


def main():
    dry_run = "--dry" in sys.argv
    
    print(f"🔍 父母的功课 技能维��")
    print(f"   技能目录: {SKILL_DIR}")
    print(f"   当前版本: {get_version()}")
    
    if "--check" in sys.argv:
        if has_changes():
            print("📝 有未提交的变更:")
            run(["git", "status", "--short"])
        else:
            print("✅ 无变更")
        return
    
    print(f"\n{'='*40}")
    
    if not has_changes():
        print("✅ 无变更，无需维护")
        return
    
    print("📝 变更文件:")
    run(["git", "status", "--short"])
    
    if dry_run:
        print("\n⏭️  Dry run 模式，不执行实际操作")
        print("   git add -A")
        print("   git commit -m 'auto: v{version} 定时维护'")
        print("   git push (需 ALLOW_AUTO_PUSH=1)")
        print("   clawhub publish (需 ALLOW_AUTO_PUBLISH=1)")
        return
    
    committed = auto_commit()
    if not committed:
        return
    
    auto_push()
    auto_publish()
    print("\n✅ 维护完成")


if __name__ == "__main__":
    main()
