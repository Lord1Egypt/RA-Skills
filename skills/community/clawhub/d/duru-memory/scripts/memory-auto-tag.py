#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import urllib.request
from pathlib import Path

from common import load_config, env_or_cfg

DEFAULT_MODEL = "qwen3.5:2b"
DEFAULT_OLLAMA = "http://127.0.0.1:11434"


def now_iso():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()


def list_md(memory_dir: Path):
    files = []
    for p in memory_dir.rglob("*.md"):
        rel = p.relative_to(memory_dir)
        if str(rel).startswith("archive/"):
            continue
        if str(rel) == "CORE/anti-patterns.md":
            continue
        files.append(p)
    return sorted(files)


def has_complete_labels(meta: dict) -> bool:
    required = ["status", "polarity", "confidence"]
    return all(str(meta.get(k, "")).strip() for k in required)


def split_frontmatter(text: str):
    if text.startswith("---\n"):
        m = re.match(r"^---\n([\s\S]*?)\n---\n?", text)
        if m:
            return m.group(1), text[m.end():]
    return "", text


def parse_simple_yaml(yaml_text: str):
    out = {}
    for line in yaml_text.splitlines():
        m = re.match(r"^\s*([A-Za-z0-9_\-]+)\s*:\s*(.*?)\s*$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def dump_simple_yaml(d: dict):
    keys = [
        "status",
        "polarity",
        "confidence",
        "avoid_reason",
        "do_instead",
        "tagger_model",
        "tagged_at",
    ]
    lines = []
    for k in keys:
        v = d.get(k, "")
        if v is None:
            v = ""
        v = str(v).replace("\n", " ").strip()
        lines.append(f"{k}: \"{v}\"")
    return "\n".join(lines)


def _extract_json_object(raw: str):
    raw = (raw or "").strip()
    if not raw:
        return {}
    # direct parse
    try:
        return json.loads(raw)
    except Exception:
        pass
    # try fenced block or mixed text
    m = re.search(r"\{[\s\S]*\}", raw)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return {}
    return {}


def call_ollama_tag(base_url: str, model: str, content: str, timeout_sec: int = 120):
    prompt = (
        "You are a strict memory tagger. Return ONLY one JSON object with keys: "
        "status,polarity,confidence,avoid_reason,do_instead. "
        "Rules: status in [active,superseded,invalid], polarity in [positive,negative], "
        "confidence in [high,medium,low]. If not negative, avoid_reason can be empty. "
        "If text is about mistakes/pitfalls, set polarity=negative and usually status=invalid.\n\n"
        "TEXT:\n" + content[:1400]
    )
    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 80},
    }
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/generate",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
        obj = json.loads(resp.read().decode("utf-8"))
    raw = obj.get("response", "").strip()
    tag = _extract_json_object(raw)

    status = tag.get("status", "active")
    polarity = tag.get("polarity", "positive")
    confidence = tag.get("confidence", "medium")
    avoid_reason = tag.get("avoid_reason", "")
    do_instead = tag.get("do_instead", "")

    if status not in {"active", "superseded", "invalid"}:
        status = "active"
    if polarity not in {"positive", "negative"}:
        polarity = "positive"
    if confidence not in {"high", "medium", "low"}:
        confidence = "medium"

    return {
        "status": status,
        "polarity": polarity,
        "confidence": confidence,
        "avoid_reason": avoid_reason,
        "do_instead": do_instead,
    }


def load_state(path: Path):
    if not path.exists():
        return {"files": {}, "last_run": None}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"files": {}, "last_run": None}


def save_state(path: Path, state: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Auto-tag markdown memory with local Ollama model")
    ap.add_argument("workspace", nargs="?", default=os.getcwd())
    ap.add_argument("--config", default=None)
    ap.add_argument("--model", default=None)
    ap.add_argument("--ollama", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--mode", choices=["tag", "review"], default="tag")
    ap.add_argument("--files", nargs="*", default=[])
    ap.add_argument("--force", action="store_true", help="re-tag even if file hash unchanged")
    args = ap.parse_args()

    cfg = load_config(args.config)
    args.model = args.model or env_or_cfg("DURU_MEMORY_TAGGER_MODEL", cfg, "models.tagger", DEFAULT_MODEL)
    args.ollama = args.ollama or env_or_cfg("DURU_MEMORY_OLLAMA_URL", cfg, "ollama.base_url", DEFAULT_OLLAMA)

    workspace = Path(args.workspace).resolve()
    memory_dir = workspace / "memory"
    state_path = memory_dir / ".tagger-state.json"
    state = load_state(state_path)

    changed = 0
    tagged = 0
    reviewed = 0
    skipped = 0
    errors = 0
    error_samples = []

    if args.files:
        candidates = []
        for f in args.files:
            p = Path(f)
            if not p.is_absolute():
                p = (workspace / p).resolve()
            if p.exists() and p.suffix == ".md":
                candidates.append(p)
    else:
        candidates = list_md(memory_dir)

    for p in candidates:
        rel = str(p.relative_to(workspace))
        text = p.read_text(encoding="utf-8", errors="ignore")
        h = sha256_text(text)
        prev = state.get("files", {}).get(rel)

        if (not args.force) and prev and prev.get("hash") == h:
            skipped += 1
            continue

        changed += 1
        try:
            fm_text, body = split_frontmatter(text)
            meta = parse_simple_yaml(fm_text)

            # review mode: keep existing complete labels; only backfill missing labels
            if args.mode == "review" and has_complete_labels(meta):
                reviewed += 1
                state.setdefault("files", {})[rel] = {
                    "hash": h,
                    "tagged_at": now_iso(),
                    "model": args.model,
                }
                continue

            tag = call_ollama_tag(args.ollama, args.model, body, timeout_sec=int(args.timeout))

            # Heuristic safety override for obvious pitfall notes
            lowered = body.lower()
            if "avoid:" in lowered or "anti-pattern" in lowered or "do_instead:" in lowered:
                tag["polarity"] = "negative"
                if tag.get("status") == "active":
                    tag["status"] = "invalid"
                if not str(tag.get("avoid_reason","")).strip():
                    m = re.search(r"(?im)^\s*avoid_reason\s*:\s*(.+?)\s*$", body)
                    if m:
                        tag["avoid_reason"] = m.group(1).strip()

            # In review mode, do not overwrite non-empty existing labels.
            if args.mode == "review":
                for k in ("status", "polarity", "confidence", "avoid_reason", "do_instead"):
                    if str(meta.get(k, "")).strip():
                        tag[k] = meta[k]

            meta.update(tag)
            meta["tagger_model"] = args.model
            meta["tagged_at"] = now_iso()

            new_text = f"---\n{dump_simple_yaml(meta)}\n---\n\n{body.lstrip()}"
            if not args.dry_run:
                p.write_text(new_text, encoding="utf-8")

            tagged += 1
            state.setdefault("files", {})[rel] = {
                "hash": sha256_text(new_text if not args.dry_run else text),
                "tagged_at": now_iso(),
                "model": args.model,
            }
        except Exception as e:
            errors += 1
            if len(error_samples) < 5:
                error_samples.append({"file": rel, "error": str(e)})

    state["last_run"] = now_iso()
    if not args.dry_run:
        save_state(state_path, state)

    print(json.dumps({
        "workspace": str(workspace),
        "model": args.model,
        "mode": args.mode,
        "changed": changed,
        "tagged": tagged,
        "reviewed": reviewed,
        "skipped": skipped,
        "errors": errors,
        "dry_run": bool(args.dry_run),
        "files_scope": args.files,
        "error_samples": error_samples,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
