#!/usr/bin/env python3
"""leaderboard_diagnose.py — 排行榜源可达性诊断（P0-3 配套工具）。

探测每个榜源的主 URL 与其国内镜像候选，打印可达性 / 延迟，并给出
「当前网络环境下哪些源能实时抓、哪些会回退快照」的判断。用于排查
「国内网抓不到海外源」问题，也便于验证 URL_REWRITES 镜像是否生效。

用法：
  python leaderboard_diagnose.py
  python leaderboard_diagnose.py --verbose     # 打印每个候选 URL 的探测结果
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from aiweekly import leaderboard_sources as S  # noqa: E402
from aiweekly.utils import _probe, _detect_region  # noqa: E402


def _mirror_of(url: str) -> list[str]:
    out = []
    for orig, mirror in S.URL_REWRITES.items():
        if url.startswith(orig):
            out.append(mirror + url[len(orig):])
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="排行榜源可达性诊断（P0-3）")
    ap.add_argument("--verbose", action="store_true", help="打印每个候选 URL 的探测结果")
    args = ap.parse_args()

    print("🔍 排行榜源可达性诊断\n")

    # 区域探测
    region = _detect_region()
    print(f"🌐 当前区域判定：{region}\n")

    # 海外源（需要镜像的主源）单独诊断主+镜像
    overseas = {
        "LMArena": S.LM_ARENA_URL,
        "Artificial Analysis": S.AA_URL,
        "HuggingFace Open LLM": S.HF_DS_API,
    }
    print("— 海外源（主源 + 国内镜像候选）—")
    for label, url in overseas.items():
        mirrors = _mirror_of(url)
        cand_map = {"主源": url, **{f"镜像{i+1}": m for i, m in enumerate(mirrors)}}
        reachable_any = False
        for cname, curl in cand_map.items():
            t0 = time.monotonic()
            ok = _probe(curl, timeout=8)
            lat = int((time.monotonic() - t0) * 1000)
            flag = "✅" if ok else "❌"
            if ok:
                reachable_any = True
            if args.verbose or cname == "主源":
                print(f"  {flag} {label} · {cname}: {curl}  ({lat}ms)")
            elif ok:
                print(f"  {flag} {label} · {cname}: {curl}  ({lat}ms)")
        status = "实时可达（含镜像）" if reachable_any else "⚠️ 主源与镜像均不可达 → 将回退快照"
        print(f"  → {label}：{status}\n")

    # 国内源
    cn = {
        "OpenCompass 司南": S.OC_LLM_URL,
        "SuperCLUE": S.SV_GENERAL_URL,
        "ModelScope 魔搭": S.MS_MODELS_URL,
        "LLM-Stats": S.LLMSTATS_URL,
        "DataLearner": S.DATALARNER_URL,
    }
    print("— 国内 / 全球源（主源直连）—")
    for label, url in cn.items():
        t0 = time.monotonic()
        ok = _probe(url, timeout=8)
        lat = int((time.monotonic() - t0) * 1000)
        flag = "✅" if ok else "❌"
        print(f"  {flag} {label}: {url}  ({lat}ms)")

    print("\n💡 说明：标 ❌ 的源将走 best-effort 回退（缓存 / 国内快照 cn_leaderboard_snapshot.json），"
          "不影响周报生成；海外源若主源 ❌ 但镜像 ✅，会自动改用镜像实时抓取。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
