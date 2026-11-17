#!/usr/bin/env python3
"""refresh_deploy.py — 一键「实时刷新排行榜 + 重新部署」编排器（ai-weekly 实时化核心）。

背景：
  原先周报生成时排行榜走 --ranking-json 静态快照，部署后便不再变化。
  实测本环境（2026-09 起）已可直连 LMArena / Artificial Analysis / LLM-Stats /
  HuggingFace / OpenCompass / SuperCLUE / ModelScope，四榜均可实时抓取
  （fetch_all_leaderboards 默认即 live fetch，无需 --ranking-json）。
  因此「排行榜实时更新」= 周期性用 live fetch 重新生成并部署即可。

本脚本把三步合为一：
  1) generate_site.py  —— 实时抓取四榜（默认 live，不传 --ranking-json）+ 复用固定周次新闻
  2) deploy_ghpages.py --no-push —— 把新 HTML 提交到本地 gh-pages worktree
  3) （可选）git push origin gh-pages —— 需显式 --push 才推送；默认仅本地、不推送

用法：
  # 手动刷新（默认仅本地生成+提交，不推送）
  python refresh_deploy.py --api-json ../workspace/news.json \
      --output ../workspace/AI_News_2026-08-31.html

  # 仅本地生成+提交、不推送（离线/调试，等同于默认行为）
  python refresh_deploy.py --api-json news.json --output out.html

  # 显式推送 gh-pages
  python refresh_deploy.py --api-json news.json --output out.html --push

设计要点：
  * 新闻用固定 --api-json（周次不变），只有排行榜随每次 live fetch 刷新 ——
    既保证「实时榜」，又不打乱周刊的新闻内容。
  * 推送复用 git-credential-wincred 取回的 PAT（仅命令内存，不写 config、不落盘）。
  * 推送失败显式非零退出：本地 gh-pages 已提交，但返回非零码并告警，避免自动化误判「实时榜已部署」；多策略回退（$GITHUB_TOKEN / Windows 凭据），凭据经 GIT_CONFIG_* 环境变量注入、不进 argv。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
VENV_PY = (SKILL_DIR / ".." / ".." / "binaries" / "python" / "envs" / "aiweekly" /
           "Scripts" / "python.exe")
# 回退：若 venv 不存在则用当前解释器
if not VENV_PY.exists():
    VENV_PY = Path(sys.executable)


def _run(cmd: list[str], **kw) -> int:
    print("▶", " ".join(cmd), flush=True)
    return subprocess.call(cmd, **kw)


def _git_push_with_creds(creds: str) -> bool:
    """用 insteadOf + GIT_CONFIG_* 注入凭据推送（凭据在环境变量，不进 argv）。"""
    env = dict(os.environ, MSYS_NO_PATHCONV="1")
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "url.https://github.com/.insteadOf"
    env["GIT_CONFIG_VALUE_0"] = f"https://{creds}@github.com/"
    rc = subprocess.call(
        ["git", "push", "origin", "gh-pages"],
        env=env, cwd=SKILL_DIR,
    )
    return rc == 0


def git_push_ghpages() -> bool:
    """推送 gh-pages 到远端。多策略回退，凭据不进 argv（用 GIT_CONFIG_* 环境变量）。

    策略1：$GITHUB_TOKEN / $GH_TOKEN（CI/托管环境）
    策略2：本机 Windows 凭据管理器（git-credential-wincred）
    任一成功即返回 True。
    """
    # 策略1：CI/托管环境常用 GITHUB_TOKEN（细粒度或 classic PAT）
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        print("  ▶ 用 $GITHUB_TOKEN 推送 gh-pages", flush=True)
        if _git_push_with_creds(f"x-access-token:{token}"):
            return True
        print("  ⚠️ $GITHUB_TOKEN 推送失败，尝试 Windows 凭据管理器", flush=True)

    # 策略2：本机 Windows 凭据管理器
    try:
        cred = subprocess.run(
            ["git-credential-wincred", "get"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True, text=True,
        ).stdout
        user = ""
        t = ""
        for line in cred.splitlines():
            if line.startswith("username="):
                user = line[len("username="):].strip()
            elif line.startswith("password="):
                t = line[len("password="):].strip()
        if t:
            print("  ▶ 用 Windows 凭据管理器推送 gh-pages", flush=True)
            if _git_push_with_creds(f"{user}:{t}"):
                return True
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠️ 读取 Windows 凭据失败：{exc}", flush=True)
    return False


def _report_date(api_json: Path, output: Path) -> str | None:
    """推导报告周期截止日（--date），确保「文件名日期 == 报告周期」。

    坑（2026-09-08 实测）：generate_site.py 不传 --date 时取「当天」，于是
    每天刷新都会把历史周报的标题/周期改写成「今天-7 ~ 今天」，
    出现 AI_News_2026-08-31.html 里装的却是 9/1-9/8 周内容的事故。

    优先级：
      1) 新闻 JSON 的 date_end（新闻抓取时的周期截止日，最权威）
      2) 输出文件名里的日期 AI_News_YYYY-MM-DD.html（兜底）
      3) None（交给 generate_site 自己决定）
    """
    try:
        data = json.loads(Path(api_json).read_text(encoding="utf-8"))
        end = (data or {}).get("date_end")
        if isinstance(end, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", end):
            return end
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠️ 读取 {api_json} 的 date_end 失败：{exc}", flush=True)
    m = re.search(r"(\d{4}-\d{2}-\d{2})", Path(output).name)
    return m.group(1) if m else None


def _generate_with_retry(gen: Path, api_json: Path, output: Path,
                         region: str, ranking_top: int,
                         report_date: str | None = None) -> int:
    """实时生成站点（默认 live fetch 排行榜）。网络抖动时自动重试 1 次。

    等价于：generate_site.py --api-json ... --output ... --region ... --ranking-top ...
            [--date YYYY-MM-DD]
    不传 --ranking-json / --no-live-ranking，从而每次都走实时抓取。
    --date 必须显式传：否则报告周期会漂移到「当天」，与文件名/新闻周次不符。
    """
    cmd = [
        str(VENV_PY), str(gen),
        "--api-json", str(api_json),
        "--output", str(output),
        "--region", region,
        "--ranking-top", str(ranking_top),
    ]
    if report_date:
        cmd += ["--date", report_date]
    rc = _run(cmd)
    if rc == 0:
        return 0
    print("  ⚠️ generate_site.py 首次失败，重试 1 次（网络抖动常见）…", flush=True)
    return _run(cmd)


def main() -> int:
    ap = argparse.ArgumentParser(description="实时刷新排行榜并（可选）重部署到 gh-pages（默认仅本地，不推送）")
    ap.add_argument("--api-json", required=True, help="固定周次新闻 JSON（--api-json）")
    ap.add_argument("--output", required=True, help="生成的 HTML 输出路径")
    ap.add_argument("--push", action="store_true",
                    help="推送 gh-pages（默认不推送，仅本地生成+提交）")
    ap.add_argument("--region", default="auto",
                    help="排行榜抓取区域（auto/cn/global），默认 auto")
    ap.add_argument("--ranking-top", type=int, default=15,
                    help="每榜取前 N 条，默认 15")
    args = ap.parse_args()

    gen = SKILL_DIR / "scripts" / "generate_site.py"
    deploy = SKILL_DIR / "scripts" / "deploy_ghpages.py"

    # R4：缺省参数自动落位，便于系统级调度（cron/任务计划）无参调用
    api_json = Path(args.api_json) if args.api_json else (SKILL_DIR / "workspace" / "news.json")
    if not api_json.exists():
        print(f"  ❌ 找不到新闻 JSON：{api_json}（请用 --api-json 指定，"
              f"或放置 workspace/news.json）", flush=True)
        return 2
    output = Path(args.output) if args.output else (SKILL_DIR / "workspace" / "AI_News_live.html")

    # 关键：报告周期 --date 必须显式推导（见 _report_date 注释）。
    # 新闻 JSON 的周期截止日与输出文件名不一致时，以新闻周期为准并改写文件名，
    # 避免「文件名 8-31、内容 9/1-9/8」这类周次错位再次进 gh-pages 存档。
    report_date = _report_date(api_json, output)
    m_out = re.search(r"(\d{4}-\d{2}-\d{2})", output.name)
    if report_date and m_out and m_out.group(1) != report_date:
        print(f"  ⚠️ 输出文件名日期 {m_out.group(1)} 与新闻周期截止日 "
              f"{report_date} 不一致，以新闻周期为准：改用 "
              f"AI_News_{report_date}.html", flush=True)
        output = output.parent / f"AI_News_{report_date}.html"
    print(f"  🗓️ 报告周期截止日：{report_date or '(未指定，取当天)'}", flush=True)

    # 1) 实时生成（默认 live fetch，不传 --ranking-json / --no-live-ranking）
    #    R4：生成失败自动重试 1 次（网络抖动常见），避免单次失败即放弃整轮刷新
    rc = _generate_with_retry(gen, api_json, output, args.region,
                              args.ranking_top, report_date)
    if rc != 0:
        print("  ❌ generate_site.py 连续重试仍失败，中止。", flush=True)
        return rc

    # 2) 本地提交到 gh-pages
    rc = _run([
        str(VENV_PY), str(deploy),
        "--html", str(output),
    ])
    if rc != 0:
        print("  ❌ deploy_ghpages.py 失败，中止。", flush=True)
        return rc

    # 3) 推送（默认不推送，需显式 --push）
    if not args.push:
        print("  ⏭️ 未指定 --push：跳过推送。待需要时手动："
              "git push origin gh-pages", flush=True)
        return 0

    if git_push_ghpages():
        print("  ✅ 已推送 gh-pages（排行榜已实时更新）。", flush=True)
        return 0

    # R4：推送失败必须显式非零退出，避免调度/自动化误以为「实时榜已部署」
    print("  ❌❌ 自动推送失败：本地 gh-pages 已提交，但未能推到远端！", flush=True)
    print(f"     请手动执行： cd {SKILL_DIR} && git push origin gh-pages", flush=True)
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
