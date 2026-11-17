#!/usr/bin/env python3
"""Scan recent OpenClaw memory and sessions for repeated workflow candidates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

from scaffold_skill import scaffold_skill, slugify


STOPWORDS = {
    "this",
    "that",
    "with",
    "from",
    "user",
    "users",
    "workflow",
    "task",
    "tasks",
    "about",
    "into",
    "their",
    "there",
    "then",
    "when",
    "have",
    "will",
    "would",
    "should",
    "could",
    "also",
    "same",
    "need",
    "needs",
    "using",
    "used",
    "make",
    "made",
    "keep",
    "keeps",
    "again",
    "still",
}

NOISY_SIGNATURE_TOKENS = {
    "2026",
    "asia",
    "daily",
    "entities",
    "health",
    "logs",
    "memory",
    "session",
    "type",
    "version",
    "timestamp",
    "cwd",
    "任务来源",
    "最后更新",
    "执行时间",
}

NOISY_LINE_MARKERS = [
    "任务来源",
    "最后更新",
    "执行时间",
    "连续健康运行",
    "详细报告",
    "memory/logs/",
    "health-check",
]

HIGH_SIGNAL_MARKERS = [
    "publish",
    "config",
    "workflow",
    "monitor",
    "article",
    "setup",
    "deploy",
    "report",
    "document",
    "docs",
    "wechat",
    "xiaohongshu",
    "stock",
    "å¾®ä¿¡",
    "å°çº¢ä¹¦",
    "é…ç½®",
    "ç›‘æŽ§",
    "æ–‡æ¡£",
    "å‘å¸ƒ",
]

STRONG_NOISE_MARKERS = [
    "memory/logs/",
    "health-check",
    "entities:",
    "session/",
    "agent session",
    "cron:",
    "memory-daily-merge",
    "合并任务 id",
    "日常记忆文件",
    "ä»»åŠ¡æ¥æº",
    "æœ€åŽæ›´æ–°",
    "æ‰§è¡Œæ—¶é—´",
    "è¿žç»­å¥åº·è¿è¡Œ",
    "è¯¦ç»†æŠ¥å‘Š",
]

def iter_recent_memory_files(workspace_root: Path, days: int) -> list[Path]:
    memory_dir = workspace_root / "memory"
    if not memory_dir.exists():
        return []
    threshold = datetime.now() - timedelta(days=max(1, days))
    results: list[Path] = []
    for path in sorted(memory_dir.glob("*.md")):
        match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})\.md", path.name)
        if not match:
            continue
        stamp = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        if stamp >= threshold:
            results.append(path)
    return results


def iter_recent_session_files(openclaw_root: Path, days: int) -> list[Path]:
    sessions_dir = openclaw_root / "agents"
    if not sessions_dir.exists():
        return []
    threshold = datetime.now() - timedelta(days=max(1, days))
    results: list[Path] = []
    for path in sessions_dir.rglob("*.jsonl"):
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified >= threshold:
            results.append(path)
    return sorted(results)


def extract_candidate_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#") or line.startswith("```"):
            continue
        if line.startswith("{") and '"type"' in line:
            continue
        if line.startswith("|") and line.count("|") >= 3:
            continue
        line = line.lstrip("-*0123456789. ").strip()
        if len(line) < 30 or len(line) > 240:
            continue
        lowered = line.lower()
        if any(
            marker in lowered
            for marker in [
                "session",
                "model_change",
                "thinking_level_change",
                "timestamp",
                "cwd",
                "memory_search",
                "memory_store",
                "连续健康运行",
                "健康检查",
                "详细报告",
            ]
        ):
            continue
        lines.append(line)
    return lines


def signature_for_line(line: str) -> tuple[str, ...]:
    tokens = [
        token
        for token in re.findall(r"[a-z0-9\u4e00-\u9fff]+", line.lower())
        if len(token) >= 4 and token not in STOPWORDS
    ]
    unique: list[str] = []
    for token in tokens:
        if token not in unique:
            unique.append(token)
    return tuple(sorted(unique[:3]))


def infer_goal(signature: tuple[str, ...], evidence: list[str]) -> str:
    if signature:
        return " ".join(signature) + " workflow"
    if evidence:
        return evidence[0][:80]
    return "repeated workflow"


def evidence_text(evidence: list[str]) -> str:
    return " ".join(evidence).lower()


def infer_candidate_name(goal: str, signature: tuple[str, ...], evidence: list[str]) -> str:
    name = slugify(goal)
    if name != "workflow":
        return name

    artifact_tokens: list[str] = []
    for line in evidence:
        for token in re.findall(r"[a-z0-9]+", line.lower()):
            if len(token) < 4 or token in STOPWORDS:
                continue
            if token not in artifact_tokens:
                artifact_tokens.append(token)
    if artifact_tokens:
        return slugify("-".join(artifact_tokens[:4]))

    signature_tokens = [token for token in signature if re.search(r"[a-z0-9]", token)]
    if signature_tokens:
        return slugify("-".join(signature_tokens[:4]))
    return "repeated-workflow"


def score_candidate(signature: tuple[str, ...], evidence: list[str], count: int) -> tuple[int, list[str]]:
    score = count * 10
    reasons: list[str] = [f"repeat_count={count}"]
    evidence_blob = evidence_text(evidence)

    if any(any(ch.isdigit() for ch in token) for token in signature):
        score -= 12
        reasons.append("penalty:numeric_signature")
    if any(token in NOISY_SIGNATURE_TOKENS for token in signature):
        score -= 14
        reasons.append("penalty:noisy_signature")
    if len(signature) >= 2:
        score += 6
        reasons.append("bonus:multi_token_signature")
    if any(marker in evidence_blob for marker in HIGH_SIGNAL_MARKERS):
        score += 10
        reasons.append("bonus:high_signal_marker")
    if any(any(marker in line.lower() for marker in ["publish", "config", "workflow", "monitor", "article", "微信", "小红书", "配置", "监控"]) for line in evidence):
        score += 8
        reasons.append("bonus:actionable_words")
    if any(any(marker in line for marker in NOISY_LINE_MARKERS) for line in evidence):
        score -= 12
        reasons.append("penalty:system_log_pattern")
    if any(marker in evidence_blob for marker in STRONG_NOISE_MARKERS):
        score -= 18
        reasons.append("penalty:strong_noise_pattern")
    if any("`" in line or ".md" in line for line in evidence):
        score += 2
        reasons.append("bonus:artifact_reference")
    if any(token in {"config", "article", "wechat", "xiaohongshu", "docs", "stock"} for token in signature):
        score += 6
        reasons.append("bonus:user_facing_signature")
    return score, reasons


def is_high_signal_candidate(signature: tuple[str, ...], evidence: list[str], score: int) -> bool:
    evidence_blob = evidence_text(evidence)
    has_high_signal = any(marker in evidence_blob for marker in HIGH_SIGNAL_MARKERS)
    if score < 18:
        return False
    if all(token in NOISY_SIGNATURE_TOKENS for token in signature):
        return False
    if any(marker in evidence_blob for marker in STRONG_NOISE_MARKERS):
        if not has_high_signal:
            return False
        if score < 40:
            return False
    if any(any(marker in line for marker in NOISY_LINE_MARKERS) for line in evidence) and score < 28:
        return False
    if not has_high_signal and score < 32:
        return False
    if signature and all(token in {"2026", "daily", "memory", "logs", "entities"} for token in signature):
        return False
    return True


def dedupe_candidates(candidates: list[dict]) -> list[dict]:
    best_by_name: dict[str, dict] = {}
    for candidate in candidates:
        key = candidate["skill_name"]
        existing = best_by_name.get(key)
        if existing is None or candidate["score"] > existing["score"] or (
            candidate["score"] == existing["score"] and candidate["count"] > existing["count"]
        ):
            best_by_name[key] = candidate
    return sorted(best_by_name.values(), key=lambda item: (-item["score"], -item["count"], item["skill_name"]))


def observe_repetition(workspace_root: Path, days: int = 14, min_count: int = 2, create: bool = False, rounds: int = 2) -> dict:
    workspace_root = workspace_root.expanduser().resolve()
    openclaw_root = workspace_root.parent
    memory_files = iter_recent_memory_files(workspace_root, days)
    session_files = iter_recent_session_files(openclaw_root, days)

    buckets: dict[tuple[str, ...], list[str]] = defaultdict(list)
    scanned_files = [*memory_files, *session_files]
    for path in scanned_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line in extract_candidate_lines(text):
            signature = signature_for_line(line)
            if not signature:
                continue
            buckets[signature].append(line)

    raw_candidates: list[dict] = []
    created_skills: list[dict] = []
    for signature, evidence in sorted(buckets.items(), key=lambda item: (-len(item[1]), item[0])):
        if len(evidence) < min_count:
            continue
        goal = infer_goal(signature, evidence)
        score, reasons = score_candidate(signature, evidence, len(evidence))
        candidate = {
            "signature": list(signature),
            "count": len(evidence),
            "goal": goal,
            "skill_name": infer_candidate_name(goal, signature, evidence),
            "evidence": evidence[:5],
            "score": score,
            "score_reasons": reasons,
        }
        raw_candidates.append(candidate)

    ranked_candidates = dedupe_candidates([candidate for candidate in raw_candidates if is_high_signal_candidate(tuple(candidate["signature"]), candidate["evidence"], candidate["score"])])
    shortlist = ranked_candidates[: min(8, len(ranked_candidates))]

    if create:
        for candidate in shortlist:
            report = scaffold_skill(
                workspace_root / "skills",
                goal=candidate["goal"],
                evidence=candidate["evidence"],
                evolve_rounds=rounds,
            )
            created_skills.append(
                {
                    "skill_name": report["skill_name"],
                    "skill_dir": report["skill_dir"],
                    "final_score": report["evolve_report"]["final_audit"]["score"],
                }
            )

    return {
        "workspace_root": str(workspace_root),
        "days": days,
        "min_count": min_count,
        "scanned_file_count": len(scanned_files),
        "raw_candidate_count": len(raw_candidates),
        "candidate_count": len(ranked_candidates),
        "candidates": ranked_candidates,
        "shortlist": shortlist,
        "created_skills": created_skills,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Observe recent OpenClaw memory and sessions for repeated workflow candidates.")
    parser.add_argument("--workspace", default="C:\\Users\\tntwl\\.openclaw\\workspace", help="OpenClaw workspace root")
    parser.add_argument("--days", type=int, default=14, help="Lookback window in days")
    parser.add_argument("--min-count", type=int, default=2, help="Minimum repeated matches to emit a candidate")
    parser.add_argument("--create", action="store_true", help="Create scaffolded skills for emitted candidates")
    parser.add_argument("--rounds", type=int, default=2, help="Evolution rounds when --create is enabled")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    report = observe_repetition(Path(args.workspace), days=args.days, min_count=args.min_count, create=args.create, rounds=args.rounds)
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Candidates: {report['candidate_count']}")
        for candidate in report["candidates"]:
            print(f"- {candidate['skill_name']} ({candidate['count']} hits)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
