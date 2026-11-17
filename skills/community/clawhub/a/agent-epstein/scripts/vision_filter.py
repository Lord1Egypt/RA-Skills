"""vision_filter.py — verify what an image ACTUALLY contains.

Booru tags are reliable, so this is unnecessary there. On X and Pixiv they
are not: a search for "yuri" returns solo portraits, group shots, memes and
unrelated art. The only dependable check is to look at the image.

Four backends, because the right one depends on the environment:

  worklist   (default) emit a JSON worklist for the AGENT to process with
             its own vision tool, then `--apply` the verdicts it returns.
             No API key, no extra service, and the strongest option when
             the agent model is vision-capable.
  openai     call a vision model over HTTPS with OPENAI_API_KEY.
  ollama     call a local VLM (llava / qwen2-vl) at OLLAMA_HOST.
  mock       testing only; deterministic verdicts, contacts nothing.

Verdict per image:
    {"female_characters": int, "romantically_paired": bool,
     "confidence": float, "notes": str}

Keep rule: at least `--min-females` female-presenting characters AND
`romantically_paired` true (unless --ignore-pairing).

    python vision_filter.py --dataset ./ds --backend worklist
    # agent looks at each path in worklist.json, then:
    python vision_filter.py --dataset ./ds --apply verdicts.json --drop
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from normalize import load_jsonl, write_jsonl                     # noqa: E402

# Sources whose tagging cannot be trusted for "is this yuri".
LOOSE_TAGGING = {"twitter", "pixiv"}

PROMPT = (
    "You are classifying an illustration for a dataset. Answer with STRICT "
    "JSON only, no prose:\n"
    '{"female_characters": <integer count of distinct female-presenting '
    'characters clearly visible>, "romantically_paired": <true if at least '
    'two of them are depicted as a couple, in an intimate or romantic way>, '
    '"confidence": <0.0-1.0>, "notes": "<short reason>"}\n'
    "Count only characters you can actually see. A solo portrait is "
    "female_characters=1. If the image is not a drawn illustration, set "
    "female_characters=0 and explain in notes."
)


# ==========================================================================
# Backends
# ==========================================================================
def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def judge_openai(path: Path, model: str) -> dict:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    body = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/png;base64,{b64(path)}"}},
            ],
        }],
        "max_tokens": 200,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        obj = json.loads(r.read().decode())
    return parse_verdict(obj["choices"][0]["message"]["content"])


def judge_ollama(path: Path, model: str) -> dict:
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    body = {"model": model, "prompt": PROMPT, "images": [b64(path)],
            "stream": False, "format": "json"}
    req = urllib.request.Request(
        f"{host.rstrip('/')}/api/generate",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        obj = json.loads(r.read().decode())
    return parse_verdict(obj.get("response", "{}"))


def judge_mock(path: Path, model: str) -> dict:
    """Testing only. Deterministic, so the plumbing can be verified."""
    h = sum(path.read_bytes()[:64]) if path.exists() else 0
    n = 2 if h % 3 else 1
    return {"female_characters": n, "romantically_paired": n >= 2,
            "confidence": 0.9, "notes": "mock"}


def parse_verdict(raw) -> dict:
    if isinstance(raw, dict):
        return raw
    text = str(raw).strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        text = text[4:] if text.lower().startswith("json") else text
    i, j = text.find("{"), text.rfind("}")
    if i >= 0 and j > i:
        text = text[i:j + 1]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"female_characters": 0, "romantically_paired": False,
                "confidence": 0.0, "notes": f"unparseable: {text[:80]}"}


BACKENDS = {
    "openai": judge_openai,
    "ollama": judge_ollama,
    "mock": judge_mock,
}


def keep_it(v: dict, min_females: int, require_pairing: bool) -> tuple[bool, str]:
    try:
        n = int(v.get("female_characters", 0))
    except (TypeError, ValueError):
        n = 0
    paired = bool(v.get("romantically_paired"))
    if n < min_females:
        return False, f"vision:only-{n}-female"
    if require_pairing and not paired:
        return False, "vision:not-paired"
    return True, ""


# ==========================================================================
# Main
# ==========================================================================
def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Vision-verify harvested images.")
    p.add_argument("--dataset", required=True)
    p.add_argument("--backend", default="worklist",
                   choices=["worklist", "openai", "ollama", "mock"])
    p.add_argument("--model", default="",
                   help="openai: gpt-4o-mini (default) | ollama: llava")
    p.add_argument("--sources", default="",
                   help="only check these sources (default: loose-tagging ones)")
    p.add_argument("--all", action="store_true", help="check every row")
    p.add_argument("--min-females", type=int, default=2)
    p.add_argument("--ignore-pairing", action="store_true")
    p.add_argument("--limit", type=int, default=0, help="cap rows checked")
    p.add_argument("--apply", default="",
                   help="path to verdicts JSON emitted by the agent")
    p.add_argument("--drop", action="store_true",
                   help="move failures to rejected.jsonl")
    args = p.parse_args(argv)

    ds = Path(args.dataset).resolve()
    rows = load_jsonl(ds / "metadata.jsonl")
    if not rows:
        print(f"no metadata.jsonl rows in {ds}", file=sys.stderr)
        return 1

    targets = [s.strip() for s in args.sources.split(",") if s.strip()]
    if not targets and not args.all:
        targets = sorted(LOOSE_TAGGING)

    def selected(r: dict) -> bool:
        return args.all or r.get("source") in targets

    todo = [r for r in rows if selected(r)]
    if args.limit:
        todo = todo[:args.limit]

    # ---- apply verdicts produced elsewhere (agent or manual) ------------
    if args.apply:
        verdicts = json.loads(Path(args.apply).read_text(encoding="utf-8"))
        if isinstance(verdicts, list):
            verdicts = {(v.get("source"), str(v.get("source_id"))): v
                        for v in verdicts}
        by_key = {f"{r.get('source')}:{r.get('source_id')}": r for r in rows}
        applied = 0
        for key, v in verdicts.items():
            if isinstance(key, str) and ":" in key:
                rec = by_key.get(key)
            else:
                rec = by_key.get(f"{v.get('source')}:{v.get('source_id')}")
            if rec is None:
                continue
            rec["vision"] = v
            ok, why = keep_it(v, args.min_females, not args.ignore_pairing)
            rec["vision_pass"] = ok
            if not ok:
                rec["reject_reason"] = why
            applied += 1

        kept, failed = [], []
        for r in rows:
            passed = r.get("vision_pass")
            bad = r.get("reject_reason", "").startswith("vision:")
            if bad and args.drop:
                failed.append(r)
            elif passed is False and args.drop:
                failed.append(r)
            else:
                kept.append(r)

        write_jsonl(ds / "metadata.jsonl", kept)
        if args.drop and failed:
            prev = load_jsonl(ds / "rejected.jsonl")
            write_jsonl(ds / "rejected.jsonl", prev + failed)
        print(f"applied {applied} verdict(s)")
        print(f"kept {len(kept)}  dropped {len(failed)}"
              f"{'' if args.drop else '  (--drop not set, nothing removed)'}")
        return 0

    # ---- worklist mode: hand the images to the agent's own vision -------
    if args.backend == "worklist":
        wl = [{
            "source": r.get("source"),
            "source_id": r.get("source_id"),
            # Prefer a local file; fall back to the remote URL so a
            # vision-gated (not-yet-downloaded) dataset can be reviewed.
            "image": (str(ds / r["file_name"])
                      if r.get("file_name") and (ds / r["file_name"]).exists()
                      else r.get("file_url", "")),
            "page_url": r.get("page_url", ""),
            "caption": (r.get("caption") or "")[:200],
            "question": PROMPT,
        } for r in todo
            if (r.get("file_name") and (ds / r["file_name"]).exists())
            or r.get("file_url")]
        out = ds / "vision_worklist.json"
        out.write_text(json.dumps(wl, indent=2), encoding="utf-8")
        print(f"{len(wl)} image(s) queued -> {out}")
        print("\nNext: look at each 'image' path with your vision tool, then "
              "write verdicts and run:")
        print(f"  vision_filter.py --dataset {ds} --apply verdicts.json --drop")
        print('\nverdicts.json shape: [{"source":"twitter","source_id":"123",'
              '"female_characters":2,"romantically_paired":true,'
              '"confidence":0.8,"notes":"..."}]')
        return 0

    # ---- direct backend loop -------------------------------------------
    fn = BACKENDS[args.backend]
    model = args.model or ("gpt-4o-mini" if args.backend == "openai" else "llava")
    kept = [r for r in rows if not selected(r)]
    failed = []
    for i, r in enumerate(todo, 1):
        fp = ds / (r.get("file_name") or "")
        if not fp.exists():
            kept.append(r)
            continue
        try:
            v = fn(fp, model)
        except Exception as e:                                # noqa: BLE001
            print(f"  [{i}/{len(todo)}] {r['source']}:{r['source_id']} ERROR {e}")
            kept.append(r)
            continue
        r["vision"] = v
        ok, why = keep_it(v, args.min_females, not args.ignore_pairing)
        r["vision_pass"] = ok
        print(f"  [{i}/{len(todo)}] {r['source']}:{r['source_id']} "
              f"females={v.get('female_characters')} "
              f"paired={v.get('romantically_paired')} -> "
              f"{'KEEP' if ok else 'DROP ' + why}")
        if ok or not args.drop:
            kept.append(r)
        else:
            r["reject_reason"] = why
            failed.append(r)

    write_jsonl(ds / "metadata.jsonl", kept)
    if args.drop and failed:
        prev = load_jsonl(ds / "rejected.jsonl")
        write_jsonl(ds / "rejected.jsonl", prev + failed)
    print(f"\nkept {len(kept)}  dropped {len(failed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
