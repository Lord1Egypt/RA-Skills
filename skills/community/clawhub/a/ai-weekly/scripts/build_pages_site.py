#!/usr/bin/env python3
"""L3#21: 在 CI 内生成 AI 周报站并发布到 GitHub Pages。

同时产出「在线 demo（HTML）」与「往周数据源（结构化 JSON）」两份产物，
全部落在一个目录（默认 public/）下，由 mirror.yml 作为 Pages artifact 上传部署。

部署后站点结构（假设仓库 elisabeth15501/ai-weekly）：
  /leaderboard.json              排行榜镜像（网络受限环境下可直接拉取）
  /model_profiles.json           模型档案镜像
  /index.html                    最新一期周报（根路径直达，在线 demo）
  /reports/index.json            所有已发布周次的清单（往周数据源索引）
  /reports/<iso_week>/index.html 该周 HTML
  /reports/<iso_week>/news.json  该周结构化新闻（机器可读，往周数据源主体）

往周数据源说明：
  RSS 仅保留约 1 周，无法回抓旧闻；但本脚本每次运行都会把「当周已生成的结构化报告」
  发布到 Pages 并累加入 reports/index.json。未来的周报增强（如跨周趋势、WoW 对比）
  即可直接 fetch Pages 上的历史 news.json，无需重新抓取原始 RSS。

翻译说明：
  CI 环境无本地 Ollama，故不传 --translate-en；英文新闻将以原文呈现。
  若需公开站点也带中文总结，请在本地生成后另行推送（见 README）。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def iso_week_key(d: date | None = None) -> str:
    """返回 ISO 周标签，如 2026-W33。"""
    d = d or date.today()
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def run(cmd: list[str], fatal: bool = True) -> int:
    print("▶", " ".join(cmd), flush=True)
    rc = subprocess.run(cmd, cwd=str(REPO_ROOT)).returncode
    if rc != 0 and fatal:
        raise RuntimeError(f"命令失败 (exit={rc}): {' '.join(cmd)}")
    return rc


def derive_pages_base() -> str:
    """由 CI 环境变量推导已部署 Pages 站点基址，用于累加历史索引。"""
    ghr = os.environ.get("GITHUB_REPOSITORY", "")
    if "/" in ghr:
        owner, repo = ghr.split("/", 1)
        return f"https://{owner}.github.io/{repo}/"
    return ""


def fetch_existing_index(pages_base: str) -> dict:
    """best-effort 拉取已部署站点的历史索引；失败则视为空索引。"""
    if not pages_base:
        return {}
    url = pages_base.rstrip("/") + "/reports/index.json"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20) as resp:
                if resp.status == 200:
                    return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001  best-effort，失败则视为空索引
            print(f"  (获取现有 reports/index.json 失败，第{attempt + 1}次: {exc})", flush=True)
            time.sleep(2)
    return {}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="构建 Pages 站点（排行榜镜像 + 周报 HTML + 往周数据源 JSON）")
    ap.add_argument("--out-dir", default="public", help="站点根目录（默认 public）")
    ap.add_argument("--pages-base", default="",
                    help="已部署 Pages 站点基址，用于累加历史索引；缺省由 GITHUB_REPOSITORY 推导")
    ap.add_argument("--top", type=int, default=15, help="排行榜抓取条数")
    ap.add_argument("--week", default=None,
                    help="指定 ISO 周（如 2026-W33）；留空=本周。注意 RSS 仅保留约 1 周")
    args = ap.parse_args()

    py = sys.executable
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    reports = out / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    # 1) 排行榜镜像（best-effort：失败不阻断周报生成，报告将显示「暂无实时数据」）
    print("🏆 构建排行榜镜像…", flush=True)
    run([py, "scripts/mirror_build.py",
         "--out", str(out / "leaderboard.json"),
         "--profiles-out", str(out / "model_profiles.json"),
         "--top", str(args.top)], fatal=False)

    week = args.week or iso_week_key()
    week_dir = reports / week
    week_dir.mkdir(parents=True, exist_ok=True)

    # 2) 抓取新闻（CI 无 Ollama，跳过中文翻译；缺省为最近 7 天滚动窗口）
    print(f"📰 抓取新闻（{week}）…", flush=True)
    news_json = week_dir / "news.json"
    fetch_cmd = [py, "scripts/fetch_ai_news.py", "--output", str(news_json)]
    if args.week:
        fetch_cmd += ["--week", args.week]
    # 退出码语义：0=全成功 / 2=降级(部分源不可达或新闻偏少，但已产出可用数据) / 1=全失败。
    # 降级(2)在 CI 上很常见（GitHub 美国 runner 拉不到部分国内源），只要 news.json 非空即可继续渲染；
    # 仅当 news.json 真正为空（exit=1）时才判失败，避免无谓中断整段构建。
    rc = run(fetch_cmd, fatal=False)
    has_items = False
    if news_json.exists():
        try:
            has_items = bool(json.loads(news_json.read_text(encoding="utf-8")).get("items"))
        except Exception:  # noqa: BLE001
            has_items = False
    if rc == 1 or not has_items:
        raise RuntimeError(f"新闻抓取失败（exit={rc}，有数据={has_items}），无可用数据，终止构建")

    # 3) 生成 HTML（用镜像排行榜，避免 CI 直接抓取海外源；无 insights 时相关板块留空）
    print("🖥️ 生成周报 HTML…", flush=True)
    html = week_dir / "index.html"
    gen_cmd = [py, "scripts/generate_site.py",
               "--api-json", str(news_json),
               "--output", str(html)]
    if (out / "leaderboard.json").exists():
        gen_cmd += ["--ranking-json", str(out / "leaderboard.json"),
                    "--profiles-json", str(out / "model_profiles.json")]
    run(gen_cmd)

    # 4) 根路径直达最新一期（在线 demo 落地页）
    shutil.copyfile(html, out / "index.html")

    # 5) 累加往周数据源索引
    try:
        news = json.loads(news_json.read_text(encoding="utf-8"))
        news_count = len(news.get("items", []))
    except Exception:  # noqa: BLE001
        news_count = 0

    pages_base = args.pages_base or derive_pages_base()
    existing = fetch_existing_index(pages_base)
    weeks = [w for w in existing.get("weeks", []) if w.get("week") != week]
    weeks.append({
        "week": week,
        "html": f"reports/{week}/index.html",
        "data": f"reports/{week}/news.json",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "news_count": news_count,
    })
    weeks.sort(key=lambda w: w["week"])
    index = {
        "latest": week,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "weeks": weeks,
        "leaderboard": "leaderboard.json",
        "model_profiles": "model_profiles.json",
    }
    (reports / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Pages 站点已构建于 {out}：最新周 {week}，累计 {len(weeks)} 周", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
