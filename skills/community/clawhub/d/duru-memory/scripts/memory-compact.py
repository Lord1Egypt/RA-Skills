#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import urllib.request
from collections import defaultdict
from pathlib import Path

from common import load_config, env_or_cfg

DEFAULT_MODEL = "qwen3.5:2b"
DEFAULT_OLLAMA = "http://127.0.0.1:11434"


def now_iso():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def split_frontmatter(text: str):
    if text.startswith("---\n"):
        m = re.match(r"^---\n([\s\S]*?)\n---\n?", text)
        if m:
            return m.group(1), text[m.end():]
    return "", text


def parse_yaml_simple(y: str):
    out = {}
    for line in y.splitlines():
        m = re.match(r"^\s*([A-Za-z0-9_\-]+)\s*:\s*(.*?)\s*$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def dump_yaml_simple(d: dict):
    keys = ["status", "polarity", "confidence", "tagger_model", "tagged_at"]
    return "\n".join([f'{k}: "{str(d.get(k, "")).replace(chr(10)," ")}"' for k in keys])


def call_ollama_summary(base_url: str, model: str, text: str):
    prompt = (
        "Summarize weekly memory logs. Output ONLY JSON with keys: "
        "decisions (array), commitments (array), blockers (array), pitfalls (array), carry_over_todos (array). "
        "Keep each bullet short.\n\nLOGS:\n" + text[:7000]
    )
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/generate",
        data=json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.1, "num_predict": 400}}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = json.loads(resp.read().decode()).get("response", "")
    m = re.search(r"\{[\s\S]*\}", raw)
    if not m:
        return {"decisions": [], "commitments": [], "blockers": [], "pitfalls": [], "carry_over_todos": []}
    try:
        obj = json.loads(m.group(0))
    except Exception:
        obj = {}
    for k in ["decisions", "commitments", "blockers", "pitfalls", "carry_over_todos"]:
        v = obj.get(k, [])
        if not isinstance(v, list):
            v = [str(v)] if v else []
        obj[k] = [str(x).strip() for x in v if str(x).strip()]
    return obj


def week_key(d: dt.date):
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def main():
    ap = argparse.ArgumentParser(description="Compact daily memory into weekly summaries")
    ap.add_argument("workspace", nargs="?", default=os.getcwd())
    ap.add_argument("--config", default=None)
    ap.add_argument("--model", default=None)
    ap.add_argument("--ollama", default=None)
    ap.add_argument("--hot-days", type=int, default=7)
    ap.add_argument("--warm-days", type=int, default=30)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = load_config(args.config)
    args.model = args.model or env_or_cfg("DURU_MEMORY_COMPACT_MODEL", cfg, "models.compact", DEFAULT_MODEL)
    args.ollama = args.ollama or env_or_cfg("DURU_MEMORY_OLLAMA_URL", cfg, "ollama.base_url", DEFAULT_OLLAMA)

    ws = Path(args.workspace).resolve()
    daily_dir = ws / "memory" / "daily"
    sum_dir = ws / "memory" / "summaries"
    sum_dir.mkdir(parents=True, exist_ok=True)

    today = dt.date.today()
    groups = defaultdict(list)
    stale_marked = 0

    for p in sorted(daily_dir.glob("*.md")):
        m = re.match(r"(\d{4}-\d{2}-\d{2})", p.name)
        if not m:
            continue
        d = dt.date.fromisoformat(m.group(1))
        age = (today - d).days
        if age <= args.hot_days or age > args.warm_days:
            continue

        text = p.read_text(encoding="utf-8", errors="ignore")
        fm, body = split_frontmatter(text)
        meta = parse_yaml_simple(fm)
        if meta.get("status", "active") in ("invalid", "superseded"):
            continue

        groups[week_key(d)].append((p, body))

        # mark stale (no deletion)
        meta["status"] = "stale"
        meta.setdefault("polarity", "positive")
        meta.setdefault("confidence", "medium")
        meta["tagger_model"] = args.model
        meta["tagged_at"] = now_iso()
        if not args.dry_run:
            p.write_text(f"---\n{dump_yaml_simple(meta)}\n---\n\n{body.lstrip()}", encoding="utf-8")
        stale_marked += 1

    summaries_written = 0
    for wk, items in groups.items():
        merged = "\n\n".join([f"## {p.name}\n{b[:1800]}" for p, b in items])
        data = call_ollama_summary(args.ollama, args.model, merged)

        out = [f"# Weekly Summary - {wk}", "", f"_generated_at: {now_iso()}_", "", "## Decisions"]
        out += [f"- {x}" for x in data.get("decisions", [])] or ["- (none)"]
        out += ["", "## Commitments"]
        out += [f"- {x}" for x in data.get("commitments", [])] or ["- (none)"]
        out += ["", "## Blockers"]
        out += [f"- {x}" for x in data.get("blockers", [])] or ["- (none)"]
        out += ["", "## Pitfalls (Avoid)"]
        out += [f"- {x}" for x in data.get("pitfalls", [])] or ["- (none)"]
        out += ["", "## Carry-over TODOs"]
        out += [f"- [ ] {x}" for x in data.get("carry_over_todos", [])] or ["- [ ] (none)"]
        out += ["", "## Source Files"]
        out += [f"- {str(p.relative_to(ws))}" for p, _ in items]

        target = sum_dir / f"{wk}.md"
        if not args.dry_run:
            target.write_text("\n".join(out) + "\n", encoding="utf-8")
        summaries_written += 1

    # re-sync semantic index after compaction changes
    if not args.dry_run:
        sem = ws / "skills" / "duru-memory" / "scripts" / "memory-semantic-search.py"
        if sem.exists():
            subprocess.run(["uv", "run", "python", str(sem), "warmup", str(ws), "--build-only"], check=False, cwd=str(ws / "skills" / "duru-memory"))

    print(json.dumps({
        "workspace": str(ws),
        "model": args.model,
        "hot_days": args.hot_days,
        "warm_days": args.warm_days,
        "stale_marked": stale_marked,
        "weekly_groups": len(groups),
        "summaries_written": summaries_written,
        "dry_run": bool(args.dry_run),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
