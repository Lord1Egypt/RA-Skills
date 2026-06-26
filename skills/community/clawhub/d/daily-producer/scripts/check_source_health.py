#!/usr/bin/env python3
"""
扫描来源信号历史，判断哪些来源触发了健康阈值，生成待审查的变更建议。

规则：
- stale：某 sources.direct URL 在最近 stale_threshold_days 天内每天命中为 0 → 建议移除
- emerging：非 sources.direct 的新来源在最近 add_threshold_runs 天中均有命中 → 建议新增

结果写入 data/source_review_pending.json。
若该文件已存在且 reviewed: false，则跳过（不覆盖未完成的审查）。

用法：
    python3 scripts/check_source_health.py
    python3 scripts/check_source_health.py --window 14 --stale-threshold 10 --add-threshold 4
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def resolve_root_dir() -> Path:
    env_root = os.environ.get("DAILY_ROOT") or os.environ.get("AI_DAILY_ROOT")
    candidates = []
    if env_root:
        candidates.append(Path(env_root).expanduser())

    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    script_dir = Path(__file__).resolve().parent
    candidates.extend([script_dir, *script_dir.parents])

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / "SKILL.md").exists() and (candidate / "config").is_dir():
            return candidate

    return script_dir.parent


def load_profile(root: Path) -> dict:
    config_path = root / "config" / "profile.yaml"
    if not config_path.exists():
        print(f"ERROR: {config_path} 不存在，请先运行 /daily-init", file=sys.stderr)
        sys.exit(1)

    try:
        import yaml
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        pass

    result: dict = {"sources": {"direct": []}}
    text = config_path.read_text(encoding="utf-8")
    in_direct = False

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if " #" in stripped:
            stripped = stripped[: stripped.index(" #")].rstrip()
        indent = len(line) - len(line.lstrip())

        if stripped == "direct:":
            in_direct = True
        elif stripped == "search_seeds:":
            in_direct = False
        elif in_direct and stripped.startswith("- ") and indent >= 4:
            result["sources"].setdefault("direct", []).append(
                stripped[2:].strip().strip("'\"")
            )
        elif indent < 4 and not stripped.startswith("-") and in_direct:
            in_direct = False

    return result


def load_signals(signals_dir: Path, dates: list[str]) -> dict[str, dict]:
    """加载指定日期列表的信号文件，返回 {date: signal} 字典。"""
    result = {}
    for date in dates:
        path = signals_dir / f"{date}.json"
        if path.exists():
            try:
                result[date] = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
    return result


def get_date_range(window: int) -> list[str]:
    """返回最近 window 天的日期列表（不含今天），格式 YYYY-MM-DD。"""
    today = datetime.now().date()
    return [
        (today - timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(1, window + 1)
    ]


def check_stale(
    direct_urls: list[str],
    signals: dict[str, dict],
    dates: list[str],
    stale_threshold: int,
) -> list[dict]:
    """
    检查 stale 条件：某 direct URL 在最近 stale_threshold 天内每天命中为 0。
    只统计实际有信号记录的天数（raw_missing=false 的天）。
    """
    candidates = []
    for url in direct_urls:
        hit_counts = []
        for date in dates:
            signal = signals.get(date)
            if signal is None:
                continue
            if signal.get("raw_missing"):
                continue
            url_signal = signal.get("sources_direct", {}).get(url)
            if url_signal is not None:
                hit_counts.append(url_signal.get("hit_count", 0))

        if len(hit_counts) < stale_threshold:
            continue

        # 只取最近 stale_threshold 天的有效记录
        recent = hit_counts[:stale_threshold]
        if all(c == 0 for c in recent):
            candidates.append({
                "url": url,
                "action": "remove_suggestion",
                "reason_auto": f"过去 {stale_threshold} 个有效采集日命中均为 0",
                "hit_counts": recent,
                "confirmed": None,
                "reason_model": None,
                "replacement_url": None,
            })

    return candidates


def check_emerging(
    direct_urls: list[str],
    signals: dict[str, dict],
    dates: list[str],
    add_threshold: int,
) -> list[dict]:
    """
    检查 emerging 条件：非 sources.direct 的新来源域名，
    在最近 add_threshold 个有效采集日中均有命中。
    """
    direct_domains = set()
    for url in direct_urls:
        import re
        domain = re.sub(r"https?://(www\.)?", "", url.lower()).split("/")[0]
        direct_domains.add(domain)

    # 统计每个新来源域名在各天的命中情况
    domain_hits: dict[str, list[int]] = {}
    valid_days = 0

    for date in dates:
        signal = signals.get(date)
        if signal is None:
            continue
        if signal.get("raw_missing"):
            continue
        valid_days += 1
        for domain, info in signal.get("new_sources", {}).items():
            if domain in direct_domains:
                continue
            if domain not in domain_hits:
                domain_hits[domain] = []
            domain_hits[domain].append(info.get("hit_count", 0))

    if valid_days < add_threshold:
        return []

    candidates = []
    for domain, hits in domain_hits.items():
        if len(hits) < add_threshold:
            continue
        recent = hits[:add_threshold]
        if all(c > 0 for c in recent):
            # 找一个 sample_url
            sample_url = ""
            for date in dates:
                signal = signals.get(date)
                if signal and not signal.get("raw_missing"):
                    info = signal.get("new_sources", {}).get(domain)
                    if info:
                        sample_url = info.get("sample_url", "")
                        break

            candidates.append({
                "domain": domain,
                "sample_url": sample_url,
                "action": "add_suggestion",
                "reason_auto": f"过去 {add_threshold} 个有效采集日均有命中",
                "hit_counts": recent,
                "confirmed": None,
                "reason_model": None,
                "add_url": None,  # 模型审查后填入建议加入的完整 URL
            })

    return candidates


def main() -> int:
    parser = argparse.ArgumentParser(description="检查来源健康状态，生成变更建议")
    parser.add_argument(
        "--window",
        type=int,
        default=14,
        help="扫描最近几天的信号（默认 14）",
    )
    parser.add_argument(
        "--stale-threshold",
        type=int,
        default=7,
        help="连续几个有效采集日命中为 0 视为 stale（默认 7）",
    )
    parser.add_argument(
        "--add-threshold",
        type=int,
        default=3,
        help="新来源连续几个有效采集日有命中视为 emerging（默认 3）",
    )
    args = parser.parse_args()

    root = resolve_root_dir()

    # 检查是否存在未完成的 pending
    pending_path = root / "data" / "source_review_pending.json"
    if pending_path.exists():
        try:
            existing = json.loads(pending_path.read_text(encoding="utf-8"))
            if not existing.get("reviewed", True):
                print(
                    "INFO: 已存在未完成的来源审查 (reviewed: false)，跳过本次检查。"
                    f"\n      文件: {pending_path}",
                    file=sys.stderr,
                )
                return 0
        except (json.JSONDecodeError, OSError):
            pass

    profile = load_profile(root)
    direct_urls: list[str] = (profile.get("sources") or {}).get("direct") or []

    signals_dir = root / "data" / "source_signals"
    if not signals_dir.exists():
        print("INFO: data/source_signals/ 不存在，尚无信号数据，跳过。", file=sys.stderr)
        return 0

    dates = get_date_range(args.window)
    signals = load_signals(signals_dir, dates)
    actual_days = sum(
        1 for d in dates
        if d in signals and not signals[d].get("raw_missing")
    )

    if actual_days == 0:
        print("INFO: 窗口内无有效信号数据，跳过。", file=sys.stderr)
        return 0

    stale = check_stale(direct_urls, signals, dates, args.stale_threshold)
    emerging = check_emerging(direct_urls, signals, dates, args.add_threshold)

    changes = stale + emerging
    if not changes:
        print("INFO: 无触发阈值的来源变更，跳过写入。")
        return 0

    pending = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "reviewed": False,
        "window_days": args.window,
        "actual_valid_days": actual_days,
        "stale_threshold_days": args.stale_threshold,
        "add_threshold_runs": args.add_threshold,
        "changes": changes,
    }

    pending_path.parent.mkdir(parents=True, exist_ok=True)
    pending_path.write_text(
        json.dumps(pending, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"已生成来源变更建议: {pending_path}\n"
        f"  stale 建议移除: {len(stale)} 条\n"
        f"  emerging 建议新增: {len(emerging)} 条"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
