"""CLI `--health-check`：网络与榜源可达性诊断（只探测，不抓取、不生成）。

为什么独立成模块：
  * 主入口 generate_site.py 有「≤500 行」硬守卫（validate_report.py 的
    source_module_size），探针清单 + 并发逻辑体积不小；
  * 它是「只探测不生成」的独立子命令，与生成流程无耦合，独立出来也便于单测。

设计要点：
  * 探针并发执行——串行 7 个目标 × 6s 超时最坏要 40 秒以上，并发后降到单次超时量级；
  * 只回答「通不通」，不做真实抓取（真实抓取 + 指数退避会让检查卡数分钟）；
  * 同一 URL 只探一次——探针成本是网络往返，重复项不提供额外信息。
"""
from __future__ import annotations

import concurrent.futures

from aiweekly.translate import ollama_health
from aiweekly.utils import _detect_region, _probe

# 基线组用于判定运行环境；榜单组在 --no-live-ranking 时跳过
BASELINE_PROBES: list[tuple[str, str]] = [
    ("百度（国内哨兵）", "https://www.baidu.com"),
    ("OpenCompass（国内榜源）", "https://rank.opencompass.org.cn/leaderboard-llm"),
    ("LMArena（国外综合榜）", "https://lmarena.ai/leaderboard"),
    ("Hugging Face（国外榜源）", "https://huggingface.co"),
]
RANKING_PROBES: list[tuple[str, str]] = [
    ("排行榜·AA", "https://artificialanalysis.ai/"),
    ("排行榜·LLM-Stats", "https://llm-stats.com/leaderboards/open-llm-leaderboard"),
    ("排行榜·HuggingFace", "https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard"),
]
PROBE_TIMEOUT = 6  # 秒


def probe_all(targets) -> dict:
    """并发探测一批 URL，返回 ``{url: 是否可达}``。"""
    urls = [url for _, url in targets]
    if not urls:
        return {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as pool:
        results = list(pool.map(lambda u: _probe(u, timeout=PROBE_TIMEOUT), urls))
    return dict(zip(urls, results))


def _print_probe(name: str, url: str, reachable: dict) -> None:
    ok = reachable.get(url, False)
    print(f"  {'✅' if ok else '❌'} {name}: {'可达' if ok else '不可达'}", flush=True)


def run_health_check(no_live_ranking: bool = False, translate_model: str | None = None) -> None:
    """打印网络 / 榜源 / 本地 Ollama 可达性诊断（只探测，不生成报告）。

    输入：no_live_ranking — 跳过榜单源探测（与生成时的同名开关语义一致）；
          translate_model  — 一并探测本地 Ollama 上该模型是否就绪（None 时只看服务）。
    输出：无（结果直接打印）；异常：不抛——所有探测失败只体现为「不可达」。
    """
    print("🧪 健康检查（只探测，不生成报告）", flush=True)
    print(f"  🌐 网络环境判定：{_detect_region()}", flush=True)

    ranking_probes = [] if no_live_ranking else RANKING_PROBES
    reachable = probe_all(list(BASELINE_PROBES) + list(ranking_probes))
    for name, url in BASELINE_PROBES:
        _print_probe(name, url, reachable)
    if no_live_ranking:
        print("  ⏭️ 已跳过排行榜探测（--no-live-ranking）", flush=True)
    else:
        for name, url in RANKING_PROBES:
            _print_probe(name, url, reachable)
        print("  ℹ️ 生成时会按多源池自动回退快照/缓存，单项不可达不阻断。", flush=True)

    ok, detail = ollama_health(timeout=3.0, model=translate_model)
    print(f"  {'✅' if ok else '⏭️'} 本地 Ollama（--translate-en 依赖）: {detail}", flush=True)
    if not ok:
        print("     ↳ 不影响报告生成：未开启 --translate-en 时无关；开启时英文报道保留原文。",
              flush=True)
    print("🧪 健康检查结束。", flush=True)


__all__ = ["BASELINE_PROBES", "RANKING_PROBES", "PROBE_TIMEOUT", "probe_all", "run_health_check"]
