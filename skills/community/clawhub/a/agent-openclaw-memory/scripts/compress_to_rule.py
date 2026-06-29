"""
compress_to_rule.py - 执行轨迹 → 规则/抗体提取

从 Qdrant 中 compress.py 写入的观察数据中提取高频失败/成功模式:
  - 错误模式 → antibodies.json 候选
  - 成功/决策模式 → self-improving/.candidates/ 规则候选

设计原则:
  - 0 token 优先(频率统计 + 规则匹配)
  - LLM 只用于提炼候选文本
  - 走 gateway_client.py 调 Gateway API

用法:
    python scripts/compress_to_rule.py                    # 全流程
    python scripts/compress_to_rule.py --dry-run          # 只预览
    python scripts/compress_to_rule.py --min-freq 3       # 最低频率
"""

import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSPACE   = SCRIPTS_DIR.parent
DATA_DIR    = WORKSPACE / "data"
QDRANT_URL  = "http://127.0.0.1:6333"
KB_COLL     = "knowledge_base"

ANTIBODIES_FILE = DATA_DIR / "antibodies.json"
CANDIDATES_DIR  = Path.home() / "self-improving" / ".candidates"

MIN_FREQ        = 3      # 最少出现次数才算高频
MAX_CANDIDATES  = 5      # 每次最多产出候选数
LOOKBACK_DAYS   = 7      # 回看天数


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  QDRANT SCROLL                                                     ║
# ╚═════════════════════════════════════════════════════════════════════╝

def scroll_compressed(max_points=2000):
    """从 Qdrant 滚动获取 compress.py 产生的观察点。"""
    import requests
    points = []
    offset = None
    while len(points) < max_points:
        payload = {
            "limit": min(500, max_points - len(points)),
            "with_payload": True,
            "with_vector": False,
            "filter": {
                "must": [
                    {"key": "source", "match": {"value": "compress.py"}},
                ]
            },
        }
        if offset:
            payload["offset"] = offset
        try:
            resp = requests.post(
                f"{QDRANT_URL}/collections/{KB_COLL}/points/scroll",
                json=payload, timeout=30,
            )
            if resp.status_code != 200:
                break
            data = resp.json().get("result", {})
            batch = data.get("points", [])
            points.extend(batch)
            offset = data.get("next_page_offset")
            if not batch or offset is None:
                break
        except Exception:
            break
    return points


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  PATTERN EXTRACTION (0 token)                                      ║
# ╚═════════════════════════════════════════════════════════════════════╝

# ── Session log scanning patterns ──────────────────────────────────
ERROR_PATTERNS = [
    r"FAIL", r"Error", r"ERROR", r"Traceback", r"FATAL",
    r"\b[45]\d{2}\b",           # HTTP 4xx/5xx
    r"exception", r"fatal", r"insufficient balance",
    r"API key", r"timeout", r"time out", r"timed out",
    r"Unauthorized", r"Forbidden", r"rate limit", r"quota",
    # Chinese
    r"失败", r"错误", r"超时", r"余额不足",
    r"拒绝", r"无法", r"断开", r"崩溃",
]

DECISION_PATTERNS = [
    r"决定", r"改用", r"不用", r"放弃", r"换成",
    r"切换", r"选择", r"不再用", r"改为", r"改成",
    r"Decision", r"choose", r"switch", r"migrate",
]

DISCOVERY_PATTERNS = [
    r"发现", r"原来", r"其实", r"实际上", r"纠正",
    r"注意的是", r"重要的是", r"注意:", r"Note:",
    r"Correction", r"Actually", r"Turns out",
    r"原来是", r"根本原因是",
]

# ── Concept extraction keywords ────────────────────────────────────
# 按长度降序排列:长词优先匹配(更具体的概念),避免 "api" 盖过 "api.deepseek"
CONCEPT_KEYWORDS_SORTED = sorted([
    # 系统组件(长词优先)
    "maintenance_orchestrator", "build_project_profile", "sync_skills_to_memory",
    "extract_memories", "vault_to_qdrant", "vault_guardian", "vault_maintainer",
    "session_cleaner", "health_scoreboard", "heartbeat_alert", "heartbeat_heavy",
    "lmstudio_guardian", "system_snapshot", "context_snapshot", "auto_link_vault",
    "process_inbox", "sync_vault_memory", "memory_health", "smoke_test",
    "compress_to_rule", "health_check_v2", "elevate_frequent",
    "evolution_engine", "system_health",
    # DeepSeek / 模型
    "deepseek", "deepseek-v4-flash", "deepseek-v4-pro",
    # 核心子系统
    "orchestrator", "embedding", "lmstudio", "qdrant", "pipeline",
    "antibody", "gateway", "compaction", "heartbeat",
    "distill", "observe", "compress", "elevate",
    # 通用技术概念
    "timeout", "config", "session", "memory", "vault",
    "search", "worker", "analyzer", "router", "health",
    "context", "encoding", "watcher", "model",
    "proxy", "token", "fetch", "auth", "cron", "api",
], key=lambda x: -len(x))

# 概念别名归一化(把同义词映射到标准名)
CONCEPT_ALIASES = {
    "deepseek-v4-flash": "deepseek",
    "deepseek-v4-pro": "deepseek",
    "vault_to_qdrant": "vault",
    "vault_guardian": "vault",
    "vault_maintainer": "vault",
    "auto_link_vault": "vault",
    "sync_vault_memory": "vault",
    "session_cleaner": "session",
    "maintenance_orchestrator": "orchestrator",
    "build_project_profile": "pipeline",
    "extract_memories": "memory",
    "compress_to_rule": "compress",
    "health_check_v2": "antibody",
    "health_scoreboard": "health",
    "heartbeat_alert": "heartbeat",
    "heartbeat_heavy": "heartbeat",
    "lmstudio_guardian": "lmstudio",
    "system_snapshot": "health",
    "context_snapshot": "context",
    "process_inbox": "vault",
    "memory_health": "memory",
    "smoke_test": "health",
    "sync_skills_to_memory": "memory",
    "elevate_frequent": "elevate",
    "evolution_engine": "antibody",
    "system_health": "health",
}


def _read_file_safe(path):
    """Read text file with auto encoding detection."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="gbk")
        except Exception:
            return ""
    except Exception:
        return ""


def _extract_concept(line, fname):
    """Extract a concept keyword from a line or filename.

    策略:
    1. 长关键词优先匹配(更具体,避免 "api" 盖过 "api.deepseek")
    2. 聚合同义词(deepseek-v4-flash → deepseek)
    3. 文件名兜底
    """
    lower = line.lower()
    for kw in CONCEPT_KEYWORDS_SORTED:
        if kw in lower:
            # 聚合同义词
            return CONCEPT_ALIASES.get(kw, kw)
    # Fallback: keyword from filename (strip date + category prefix)
    name = Path(fname).stem
    parts = name.split("-")
    for p in parts[2:]:  # Skip date parts
        if len(p) > 3 and not p.isdigit():
            return p[:20]
    return "general"


def _match_patterns(line, patterns):
    """Check if line matches any pattern. Returns True on first match."""
    import re
    for pat in patterns:
        if re.search(pat, line, re.IGNORECASE):
            return True
    return False


def scan_session_logs(log_dir=None, max_files=100, min_freq=MIN_FREQ,
                      max_days=LOOKBACK_DAYS):
    """
    直接从 memory/*.md 会话日志提取执行模式(0 token)。
    绕过 observe→compress→Qdrant 断裂链。

    Returns:
        errors: [(concept, freq, example_line), ...]
        decisions: [(concept, freq, example_line), ...]
        discoveries: [(concept, freq, example_line), ...]
    """
    if log_dir is None:
        log_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    if not Path(log_dir).exists():
        print("  Session log dir not found:", log_dir)
        return [], [], []

    errors = defaultdict(list)
    decisions = defaultdict(list)
    discoveries = defaultdict(list)

    cutoff = time.time() - max_days * 86400
    files = sorted(
        Path(log_dir).glob("*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,  # Newest first (for time-drift correction)
    )[:max_files]

    print(f"  Scanning {len(files)} session log files...")

    for fp in files:
        # Time filter on file mtime
        try:
            if fp.stat().st_mtime < cutoff:
                continue
        except OSError:
            continue

        content = _read_file_safe(fp)
        if not content:
            continue

        fname = fp.name
        lines = content.split("\n")

        for i, line in enumerate(lines):
            line = line.strip()
            if not line or len(line) < 10:
                continue

            concept = _extract_concept(line, fname)

            # Error match
            if _match_patterns(line, ERROR_PATTERNS):
                errors[concept].append((fp.stat().st_mtime, i, line[:200]))

            # Decision match
            if _match_patterns(line, DECISION_PATTERNS):
                decisions[concept].append((fp.stat().st_mtime, i, line[:200]))

            # Discovery/Correction match
            if _match_patterns(line, DISCOVERY_PATTERNS):
                discoveries[concept].append((fp.stat().st_mtime, i, line[:200]))

    # Deduplicate by time: newer overrides older for same concept.
    # Sort each group by (mtime, line_no) descending, keep ALL examples (capped).
    MAX_EXAMPLES_PER_CONCEPT = 50
    def _dedup_time(patterns_dict):
        result = []
        for concept, entries in patterns_dict.items():
            if len(entries) < min_freq:
                continue
            entries.sort(key=lambda x: (-x[0], -x[1]))
            # Keep ALL examples (capped) - not just one
            examples = [e[2] for e in entries[:MAX_EXAMPLES_PER_CONCEPT]]
            result.append((concept, len(entries), examples))
        result.sort(key=lambda x: -x[1])
        return result

    return (
        _dedup_time(errors),
        _dedup_time(decisions),
        _dedup_time(discoveries),
    )


def group_observations(points, min_freq=MIN_FREQ):
    """Qdrant compressed observations → pattern groups (supplementary)."""
    errors = defaultdict(list)
    decisions = defaultdict(list)
    discoveries = defaultdict(list)
    cutoff = time.time() - LOOKBACK_DAYS * 86400

    for pt in points:
        p = pt.get("payload", {})
        compressed_at = p.get("compressedAt", "")
        if compressed_at:
            try:
                dt = datetime.fromisoformat(compressed_at)
                if dt.timestamp() < cutoff:
                    continue
            except (ValueError, OSError):
                pass

        obs_type = p.get("type", "")
        narrative = p.get("narrative", "") or p.get("title", "")
        concepts = p.get("concepts", [])
        if not concepts:
            concepts = ["general"]
        primary_concept = concepts[0] if concepts else "general"

        if obs_type == "error":
            errors[primary_concept].append(narrative)
        elif obs_type == "decision":
            decisions[primary_concept].append(narrative)
        elif obs_type == "discovery":
            discoveries[primary_concept].append(narrative)

    def top(d, mf):
        MAX_EX = 50
        return sorted(
            [(c, len(v), [x[:200] for x in v[:MAX_EX]]) for c, v in d.items() if len(v) >= mf],
            key=lambda x: -x[1],
        )
    return top(errors, min_freq), top(decisions, min_freq), top(discoveries, min_freq)


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  LLM REFINEMENT (via Gateway)                                      ║
# ╚═════════════════════════════════════════════════════════════════════╝

ANTIBODY_PROMPT_TEMPLATE = (
    "You are a failure pattern analyst. A tool has failed {freq} times "
    "in the last {days} days with concept '{concept}'. "
    "Generate an antibody entry. Output JSON only:\n\n"
    '{{"name": "auto-{concept}-N", '
    '"pattern": "error regex pattern", '
    '"fix": "one line fix description", '
    '"auto_fix": "powershell command or null"}}\n\n'
    "Example failure: {example}"
)

RULE_PROMPT_TEMPLATE = (
    "You are a rule distillation engine. The following pattern occurred "
    "{freq} times in the last {days} days with concept '{concept}'. "
    "Extract a reusable behavioral rule. Output JSON only:\n\n"
    '{{"title": "Rule title (<=20 char)", '
    '"rule": "One-line actionable rule", '
    '"why": "Why this matters", '
    '"when": "When to apply", '
    '"confidence": 1-10}}\n\n'
    "Example observation: {example}"
)


def _llm_refine_batch(tasks):
    """批量 LLM 提炼 - N 个模式合并为 1 次 API 调用,直连 DeepSeek(不走 Gateway 会话)。

    tasks: list of (type, concept, freq, example) where type is 'antibody'/'decision'/'discovery'
    Returns: list of dict or None, parallel to tasks
    """
    if not tasks:
        return []

    import requests
    import sys
    SCRIPTS_DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(SCRIPTS_DIR))
    from shared_config import MIMO_KEY as DEEPSEEK_KEY, MIMO_CHAT_URL as DEEPSEEK_CHAT_URL, MIMO_MODEL
  
    MODEL = MIMO_MODEL
    TIMEOUT = 120

    # 构建合并 prompt,每段一个模式,用 JSONL 输出
    sections = []
    for i, (task_type, concept, freq, example) in enumerate(tasks):
        if task_type == "antibody":
            tmpl = ANTIBODY_PROMPT_TEMPLATE
        else:
            tmpl = RULE_PROMPT_TEMPLATE
        prompt = tmpl.format(
            concept=concept, freq=freq, days=LOOKBACK_DAYS, example=example,
        )
        sections.append(f"### Task {i}\n{prompt}")

    combined = (
        "Process each task below independently. "
        "Output exactly one JSON object per task, separated by a blank line. "
        "No markdown fences, no extra commentary.\n\n"
        + "\n\n".join(sections)
        + f"\n\nOutput {len(tasks)} JSON objects, one per line, in task order:"
    )

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": combined}],
        "temperature": 0.1,
        "max_tokens": 400 * len(tasks),
    }

    try:
        resp = requests.post(
            DEEPSEEK_CHAT_URL,
            headers={
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=TIMEOUT,
        )
        if resp.status_code != 200:
            print(f"  [LLM] DeepSeek API error {resp.status_code}: {resp.text[:200]}")
            return [None] * len(tasks)

        data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not content:
            return [None] * len(tasks)

        usage = data.get("usage", {})
        print(f"  [LLM] DeepSeek direct: {usage.get('prompt_tokens', '?')} prompt, "
              f"{usage.get('completion_tokens', '?')} completion, "
              f"{usage.get('total_tokens', '?')} total")
    except Exception as e:
        print(f"  [LLM] DeepSeek API failed: {e}")
        return [None] * len(tasks)

    content = content.strip()
    # Remove markdown fences if any
    if content.startswith("```"):
        import re
        content = re.sub(
            r"^```(?:json)?\s*|\s*```$", "", content, flags=re.MULTILINE
        )

    # Parse each non-empty line as JSON
    results = []
    for line in content.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            results.append(obj)
        except json.JSONDecodeError:
            results.append(None)

    # Pad to match task count
    while len(results) < len(tasks):
        results.append(None)
    return results[:len(tasks)]


def generate_antibody_candidates(error_patterns, dry_run=False):
    """错误模式 → antibodies.json 候选(批量 API 调用)。"""
    if not error_patterns:
        print("  No high-frequency error patterns found.")
        return []

    if dry_run:
        return [{"concept": c, "freq": f, "example": e[:100], "dry": True}
                for c, f, e in error_patterns[:MAX_CANDIDATES]]

    patterns = error_patterns[:MAX_CANDIDATES]
    for concept, freq, _ in patterns:
        print(f"  Error pattern: concept={concept}, freq={freq}")

    print(f"  → Batch refining {len(patterns)} antibody candidates in 1 API call...")
    tasks = [("antibody", c, f, e) for c, f, e in patterns]
    results = _llm_refine_batch(tasks)

    candidates = []
    for (concept, freq, _), r in zip(patterns, results):
        if r:
            candidates.append({**r, "_freq": freq, "_concept": concept})
    return candidates


def generate_rule_candidates(patterns, pattern_type, dry_run=False):
    """成功/决策模式 → .candidates/ 规则候选(批量 API 调用)。"""
    if not patterns:
        print(f"  No high-frequency {pattern_type} patterns found.")
        return []

    if dry_run:
        return [{"concept": c, "freq": f, "type": pattern_type,
                 "example": e[:100], "dry": True}
                for c, f, e in patterns[:MAX_CANDIDATES]]

    patterns_trimmed = patterns[:MAX_CANDIDATES]
    for concept, freq, _ in patterns_trimmed:
        print(f"  {pattern_type} pattern: concept={concept}, freq={freq}")

    print(f"  → Batch refining {len(patterns_trimmed)} {pattern_type} candidates in 1 API call...")
    tasks = [(pattern_type, c, f, e) for c, f, e in patterns_trimmed]
    results = _llm_refine_batch(tasks)

    candidates = []
    for (concept, freq, _), r in zip(patterns_trimmed, results):
        if r:
            r["_freq"] = freq
            r["_concept"] = concept
            r["_type"] = pattern_type
            candidates.append(r)

    return candidates


def _batch_refine_all(antibody_patterns, decision_patterns, discovery_patterns):
    """合并所有模式 → 1 次 API 调用 → 拆分结果。

    模式格式: (concept, freq, examples_list) 其中 examples_list 是全部匹配行
    Returns: (antibody_results, decision_results, discovery_results)
    每个都是 list of (concept, freq, examples_list, result_dict_or_None)
    """
    all_tasks = []  # (type, concept, freq, primary_example)
    all_meta = []   # (category, concept, freq, examples_list)

    for c, f, examples in antibody_patterns[:MAX_CANDIDATES]:
        ex = examples[0] if examples else ""
        all_tasks.append(("antibody", c, f, ex))
        all_meta.append(("antibody", c, f, examples))
    for c, f, examples in decision_patterns[:MAX_CANDIDATES]:
        ex = examples[0] if examples else ""
        all_tasks.append(("decision", c, f, ex))
        all_meta.append(("decision", c, f, examples))
    for c, f, examples in discovery_patterns[:MAX_CANDIDATES]:
        ex = examples[0] if examples else ""
        all_tasks.append(("discovery", c, f, ex))
        all_meta.append(("discovery", c, f, examples))

    if not all_tasks:
        return [], [], []

    print(f"  → Batch refining {len(all_tasks)} patterns in 1 API call (was {len(all_tasks)} calls)...")
    results = _llm_refine_batch(all_tasks)

    ab, de, di = [], [], []
    for meta, r in zip(all_meta, results):
        cat, c, f, examples = meta
        if cat == "antibody":
            ab.append((c, f, examples, r))
        elif cat == "decision":
            de.append((c, f, examples, r))
        else:
            di.append((c, f, examples, r))

    return ab, de, di


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  WRITE                                                             ║
# ╚═════════════════════════════════════════════════════════════════════╝

def write_antibodies(candidates, dry_run=False):
    """追加新抗体到 antibodies.json(去重)。"""
    if not candidates:
        return 0

    existing = {"antibodies": []}
    if ANTIBODIES_FILE.exists():
        try:
            with open(ANTIBODIES_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    existing_names = {a.get("name", "") for a in existing.get("antibodies", [])}
    added = 0

    for c in candidates:
        if c.get("dry"):
            concept = c.get("_concept", c.get("concept", "unknown"))
            print(f"  [DRY] Would add antibody: {concept}")
            continue

        name = c.get("name", f"auto-{c.get('_concept', 'unknown')}")
        if name in existing_names:
            continue

        existing["antibodies"].append({
            "name": name,
            "pattern": c.get("pattern", ""),
            "fix": c.get("fix", ""),
            "auto_fix": c.get("auto_fix"),
            "created": datetime.now().strftime("%Y-%m-%d"),
            "hits": 0,
            "success_rate": 0.0,
        })
        existing_names.add(name)
        added += 1

    if added > 0 and not dry_run:
        ANTIBODIES_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = ANTIBODIES_FILE.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        tmp.replace(ANTIBODIES_FILE)
        print(f"  Added {added} antibodies to {ANTIBODIES_FILE}")

    return added


def write_rule_candidates(candidates, dry_run=False):
    """写规则候选到 .candidates/。"""
    if not candidates:
        return 0

    CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    out_file = CANDIDATES_DIR / f"exec_rules_{today}.json"

    if dry_run:
        for c in candidates:
            concept = c.get("_concept", c.get("concept", "unknown"))
            print(f"  [DRY] Would write rule: {c.get('title', concept)}")
        return 0

    payload = {
        "source": "compress_to_rule.py",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "candidates": candidates,
    }

    tmp = out_file.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    tmp.replace(out_file)

    print(f"  Wrote {len(candidates)} rule candidates to {out_file}")
    return len(candidates)


# ╔═════════════════════════════════════════════════════════════════════╗
# ║  MAIN                                                              ║
# ╚═════════════════════════════════════════════════════════════════════╝

def main():
    dry_run = "--dry-run" in sys.argv
    skip_scan = "--no-scan-logs" in sys.argv
    json_output = None
    min_freq = MIN_FREQ
    for arg in sys.argv:
        if arg.startswith("--json-output="):
            json_output = arg.split("=", 1)[1]
        elif arg.startswith("--min-freq="):
            min_freq = int(arg.split("=")[1])

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
          f"compress_to_rule.py (min_freq={min_freq})")

    # 1. Session log scanning (primary - bypass broken observe→compress)
    errors, decisions, discoveries = [], [], []
    if not skip_scan:
        print("[1] Scanning session logs for execution patterns...")
        errors, decisions, discoveries = scan_session_logs(
            min_freq=min_freq,
        )
        print(f"  Errors: {len(errors)}, Decisions: {len(decisions)}, "
              f"Discoveries: {len(discoveries)}")

    # 2. Qdrant scroll (supplementary - for any existing compressed data)
    print("[2] Scrolling Qdrant for compressed observations...")
    points = scroll_compressed()
    print(f"  Found {len(points)} compressed points (supplementary)")

    # Merge Qdrant patterns into session log results
    if points:
        q_errors, q_decisions, q_discoveries = group_observations(points, min_freq)
        # Merge by concept: sum frequencies, keep best example
        def _merge(existing, new):
            merged = {}
            for c, f, examples in existing:
                merged[c] = (f, examples)
            for c, f, examples in new:
                if c in merged:
                    old_f, old_ex = merged[c]
                    merged[c] = (old_f + f, (old_ex + examples)[:50])
                else:
                    merged[c] = (f, examples)
            return [(c, f, examples) for c, (f, examples) in sorted(
                merged.items(), key=lambda x: -x[1][0]
            )]
        errors = _merge(errors, q_errors)
        decisions = _merge(decisions, q_decisions)
        discoveries = _merge(discoveries, q_discoveries)
        print(f"  Merged: Errors={len(errors)}, Decisions={len(decisions)}, "
              f"Discoveries={len(discoveries)}")

    # JSON output mode: dump patterns for external LLM refinement
    if json_output:
        dump_patterns_json(errors, decisions, discoveries, json_output)
        return

    # 3. Generate candidates (LLM, all patterns → 1 batch API call → 1 session)
    print("[3] Generating candidates (batch)...")
    if dry_run:
        ab_candidates = generate_antibody_candidates(errors, dry_run)
        rule_candidates = (
            generate_rule_candidates(decisions, "decision", dry_run)
            + generate_rule_candidates(discoveries, "discovery", dry_run)
        )
    else:
        # 合并所有模式 → 1 次 API 调用
        ab_raw, de_raw, di_raw = _batch_refine_all(errors, decisions, discoveries)
        # 转回原有格式(保留全部 examples 到 _examples 字段)
        ab_candidates = []
        for c, f, examples, r in ab_raw:
            if r:
                ab_candidates.append({**r, "_freq": f, "_concept": c, "_examples": examples})
        rule_candidates = []
        for c, f, examples, r in de_raw:
            if r:
                r["_freq"] = f; r["_concept"] = c; r["_type"] = "decision"; r["_examples"] = examples
                rule_candidates.append(r)
        for c, f, examples, r in di_raw:
            if r:
                r["_freq"] = f; r["_concept"] = c; r["_type"] = "discovery"; r["_examples"] = examples
                rule_candidates.append(r)

    # 4. Write
    print("[4] Writing...")
    n_ab = write_antibodies(ab_candidates, dry_run)
    n_rule = write_rule_candidates(rule_candidates, dry_run)

    print(f"\n[OK] compress_to_rule.py complete.")
    print(f"  Antibodies added: {n_ab}")
    print(f"  Rule candidates: {n_rule}")


def dump_patterns_json(errors, decisions, discoveries, out_file):
    """Write extracted patterns to JSON for LLM refinement by cron agent."""
    payload = {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "source": "compress_to_rule.py",
        "errors": [{"concept": c, "freq": f, "examples": examples} for c, f, examples in errors],
        "decisions": [{"concept": c, "freq": f, "examples": examples} for c, f, examples in decisions],
        "discoveries": [{"concept": c, "freq": f, "examples": examples} for c, f, examples in discoveries],
        "min_freq": MIN_FREQ,
        "lookback_days": LOOKBACK_DAYS,
    }
    out_path = Path(out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"  Patterns dumped to {out_path}")


if __name__ == "__main__":
    main()
