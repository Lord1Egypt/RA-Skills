#!/usr/bin/env python3
"""install_scheduler.py — 注册「系统级每日 09:00 刷新排行榜」兜底任务（R4 修复）。

背景：
  ai-weekly 的实时排行榜刷新原先完全依赖 WorkBuddy automation（每日 09:00）。
  但 automation 仅在 WorkBuddy 会话存活时触发；会话未开（如电脑睡眠 / 未启动客户端）
  则不刷新，排行榜可能多日不更新。本脚本把同一刷新逻辑注册为**操作系统级调度**
  （Windows 任务计划程序 / Linux cron），确保会话不在线也能刷新。
  WorkBuddy automation 仍保留作即时触发；系统调度仅作兜底。

用法：
  python install_scheduler.py            # 安装（按当前 OS 自动选 Windows 任务计划 / cron）
  python install_scheduler.py --uninstall
  python install_scheduler.py --dry-run  # 仅打印将要执行的命令，不落盘
  python install_scheduler.py --time 08:30   # 自定义触发时间（默认 09:00）
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
VENV_PY = (SKILL_DIR / ".." / ".." / "binaries" / "python" / "envs" / "aiweekly" /
           "Scripts" / "python.exe")
if not VENV_PY.exists():
    VENV_PY = Path(sys.executable)

TASK_NAME = "ai-weekly-refresh"
REFRESH = SKILL_DIR / "scripts" / "refresh_deploy.py"
NEWS_JSON = SKILL_DIR / "workspace" / "news.json"
OUTPUT_HTML = SKILL_DIR / "workspace" / "AI_News_live.html"
LOG_FILE = SKILL_DIR / "workspace" / "refresh_deploy.log"


def _is_windows() -> bool:
    return os.name == "nt" or sys.platform.startswith("win")


def _build_inner(enable_push: bool = False) -> str:
    """刷新命令本体（路径带空格已加引号）。
    安全默认：定时任务仅刷新本地数据，不推送 gh-pages；
    仅当 enable_push=True（用户显式 --enable-push）才允许定时自动推送。"""
    push_flag = "--push " if enable_push else ""
    return (f'"{VENV_PY}" "{REFRESH}" --api-json "{NEWS_JSON}" '
            f'--output "{OUTPUT_HTML}" {push_flag}>> "{LOG_FILE}" 2>&1')


def _install_windows(time: str, dry: bool, enable_push: bool = False) -> int:
    if not shutil.which("schtasks"):
        print("  ❌ 未找到 schtasks（仅 Windows 可用）。", flush=True)
        return 1
    # cmd /c "<inner>" —— 外层引号包裹整条命令，内层引号保护带空格路径（Windows 经典转义）
    tr = f'cmd /c "{_build_inner(enable_push)}"'
    cmd = ["schtasks", "/create", "/tn", TASK_NAME, "/tr", tr,
           "/sc", "daily", "/st", time, "/f"]
    print("  ▶ 注册 Windows 任务计划：", " ".join(cmd), flush=True)
    if dry:
        return 0
    rc = subprocess.call(cmd)
    if rc == 0:
        print(f"  ✅ 已注册系统任务「{TASK_NAME}」（每日 {time} 自动刷新排行榜）。", flush=True)
    else:
        print(f"  ⚠️ schtasks 返回 {rc}；如提示权限不足请以管理员身份运行。", flush=True)
    return rc


def _uninstall_windows(dry: bool) -> int:
    cmd = ["schtasks", "/delete", "/tn", TASK_NAME, "/f"]
    print("  ▶ 删除 Windows 任务计划：", " ".join(cmd), flush=True)
    if dry:
        return 0
    return subprocess.call(cmd)


def _install_linux(time: str, dry: bool, enable_push: bool = False) -> int:
    hh, mm = time.split(":")
    push_flag = "--push " if enable_push else ""
    line = (f"{mm} {hh} * * * cd \"{SKILL_DIR}\" && \"{VENV_PY}\" \"{REFRESH}\" "
            f'--api-json "{NEWS_JSON}" --output "{OUTPUT_HTML}" '
            f'{push_flag}>> "{LOG_FILE}" 2>&1  # {TASK_NAME}\n')
    existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    cur = existing.stdout if existing.returncode == 0 else ""
    if TASK_NAME in cur:
        print("  ⏭️ cron 任务已存在，跳过（如需重置请先 --uninstall）。", flush=True)
        return 0
    new = cur + line
    print("  ▶ 追加 cron 任务：", line.strip(), flush=True)
    if dry:
        return 0
    p = subprocess.run(["crontab", "-"], input=new, text=True)
    if p.returncode == 0:
        print(f"  ✅ 已注册 cron 任务（每日 {time} 自动刷新排行榜）。", flush=True)
    return p.returncode


def _uninstall_linux(dry: bool) -> int:
    existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if existing.returncode != 0:
        print("  ⏭️ 无 crontab，无需删除。", flush=True)
        return 0
    new = "\n".join(l for l in existing.stdout.splitlines()
                    if TASK_NAME not in l)
    if new.strip() == existing.stdout.strip():
        print("  ⏭️ crontab 中无本任务，无需删除。", flush=True)
        return 0
    print("  ▶ 从 crontab 移除 ai-weekly-refresh 任务。", flush=True)
    if dry:
        return 0
    p = subprocess.run(["crontab", "-"], input=new + "\n", text=True)
    return p.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="注册/卸载系统级排行榜刷新兜底任务")
    ap.add_argument("--uninstall", action="store_true", help="卸载而非安装")
    ap.add_argument("--dry-run", action="store_true", help="仅打印命令不落盘")
    ap.add_argument("--time", default="09:00", help="每日触发时间 HH:MM（默认 09:00）")
    ap.add_argument("--enable-push", action="store_true",
                    help="允许定时任务自动推送 gh-pages（默认关闭：定时任务仅本地刷新、不推送）")
    args = ap.parse_args()

    # 预检：news.json 必须存在，否则调度任务必然失败
    if not args.uninstall and not NEWS_JSON.exists():
        print(f"  ❌ 未找到 {NEWS_JSON}，请先生成周报（含 workspace/news.json）再安装调度。",
              flush=True)
        return 2

    if args.uninstall:
        rc = _uninstall_windows(args.dry_run) if _is_windows() else _uninstall_linux(args.dry_run)
    else:
        rc = (_install_windows(args.time, args.dry_run, args.enable_push)
              if _is_windows()
              else _install_linux(args.time, args.dry_run, args.enable_push))
    if rc == 0 and not args.uninstall and not args.dry_run:
        print("  💡 系统调度为兜底；WorkBuddy automation 仍可作即时触发。", flush=True)
        if args.enable_push:
            print("  ⚠️ 已启用 --enable-push：定时任务将自动推送 gh-pages，"
                  "依赖环境内可用的 GITHUB_TOKEN/GH_TOKEN 或 git 凭据。", flush=True)
        else:
            print("  🔒 定时任务默认仅本地刷新、不推送（安全默认）。"
                  "如需自动推送，重装时加 --enable-push。", flush=True)
        print(f"     运行日志见：{LOG_FILE}", flush=True)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
