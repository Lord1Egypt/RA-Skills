#!/usr/bin/env python3
"""L3#20：榜源自托管镜像构建脚本。

部分海外榜源在受限网络环境下可能不可达，本脚本在可联网环境（CI / 定时任务 / 你本机）
抓取最新排行榜，导出为静态 JSON，供 GitHub Pages 托管为镜像；网络受限环境的用户
可直接拉取镜像，免去自行抓取海外源。

设计：
  - 单源抓取失败会被 fetch_all_leaderboards 内部容错（回退缓存 / 标注），不会整崩；
  - 导出 LEADERBOARD_DATA + model_profiles.json 两份静态文件，前端可直接 fetch；
  - 定时运行（配合 .github/workflows/mirror.yml）即可维持「每日刷新」的镜像。

用法：
  python scripts/mirror_build.py --out mirror/leaderboard.json
  # 国内用户前端改为 fetch('https://<owner>.github.io/<repo>/leaderboard.json')
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # 让 scripts/ 可被 import
import aiweekly.leaderboard as LB  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="构建排行榜自托管镜像静态 JSON")
    ap.add_argument("--out", default="mirror/leaderboard.json",
                    help="导出的排行榜 JSON 路径（默认 mirror/leaderboard.json）")
    ap.add_argument("--profiles-out", default="mirror/model_profiles.json",
                    help="导出的模型档案 JSON 路径")
    ap.add_argument("--top", type=int, default=15, help="抓取条数")
    ap.add_argument("--region", default="global",
                    choices=["auto", "cn", "global"],
                    help="镜像优先国际源（默认 global）")
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        data = LB.fetch_all_leaderboards(args.top, region=args.region)
    except Exception as e:  # noqa: BLE001  整体失败不应静默
        print(f"⚠️ 排行榜抓取失败: {e}", file=sys.stderr)
        sys.exit(1)

    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    prof = LB.SKILL_DIR / "model_profiles.json"
    if prof.exists():
        pout = Path(args.profiles_out)
        pout.parent.mkdir(parents=True, exist_ok=True)
        pout.write_text(prof.read_text(encoding="utf-8"), encoding="utf-8")

    n = sum(
        len((data.get(b, {}) or {}).get(s, {}).get("rows", []) or [])
        for b in ("comprehensive", "open_source")
        for s in ("lmarena", "aa", "ls", "hf")
    )
    print(f"✅ 镜像已写入 {out}（{n} 条排行行）@ {time.strftime('%Y-%m-%dT%H:%M:%S%z')}")
    print(f"   档案：{args.profiles_out}")


if __name__ == "__main__":
    main()
