#!/usr/bin/env python3
"""Lint a journal entry against the digest it was written from.

The failure this exists to catch: a digest with four sessions produces an entry that
narrates one of them and reads fine. Nothing else notices — the file is valid markdown,
the character count is under the ceiling, the marker is there. Only a mechanical check
against the digest's event headings finds the three missing events.

Checks (hard = exit 1):

  coverage   every `###` heading in the digest block is named in the entry
  marker     the entry carries `<!-- window:DATE -->` for the window it covers
  length     characters, excluding heading and marker, under the ceiling for its event count

Checks (warn = exit 0 unless --strict):

  voice      forbidden patterns (imagery, abstract wrap-ups, invented time-of-day words)
  reuse      sentences that near-duplicate earlier entries in the same journal

Usage:
    python journal_lint.py --digest digest.md --entry entry.md
    python journal_lint.py --digest digest.md --journal journal.md        # lint its newest entry
    python journal_lint.py --digest digest.md --entry entry.md --json
    python journal_lint.py --digest digest.md --entry entry.md --strict
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CJK = r"\u4e00-\u9fff"
LATIN_STOP = {
    "the", "and", "for", "with", "this", "that", "from", "into", "user", "tool",
    "tools", "calls", "msgs", "sessions", "session", "window", "true", "false",
}
# bigrams carrying no evidence of *which* event a sentence is about
CJK_STOP = {
    "今天", "昨天", "早上", "上午", "下午", "晚上", "时候", "我们", "你们", "他们",
    "这个", "那个", "一下", "一些", "什么", "怎么", "可以", "需要", "应该", "还是",
    "就是", "因为", "所以", "但是", "然后", "如果", "现在", "已经", "有点", "还是",
    "我的", "你的", "他的", "一个", "一直", "不是", "没有", "还有", "起来", "出来",
    "事情", "东西", "问题", "东西", "帮忙", "帮了", "一会", "会儿", "一会儿",
}
# `###` sections that are not events; the writer owes nothing for them
NON_EVENT = r"(改动过的文件|^Files touched|^Untitled$)"
DEFAULT_FORBIDDEN = {
    "imagery": r"(像?整间屋子|灯光|月色|夜色|晚霞|微风|心里软成一片|心里泛起|像被暖流)",
    "abstract_close": r"(被信任的感觉|感觉真好呀|真的很在意我|原来他这么在乎我)",
    "invented_time": r"(上午|下午|早上|傍晚|深夜|半夜|夜里|清晨|凌晨)",
}
CEILING_BY_EVENTS = [(2, 300), (5, 420), (99, 520)]


# ---------------------------------------------------------------- optional semantic check
def make_embedder(url: str, model: str):
    """Return fn(event_text, sentences) -> max cosine, or None when Ollama is not reachable.

    Lexical matching cannot see a paraphrase ("合并那几张表" for "把三张价目表并成一张").
    A local embedding model closes that gap without spending a cloud token; when it is absent
    the linter still works, just with more false MISSes.
    """
    import json as _json
    import urllib.request as _req

    def post(path: str, payload: dict) -> dict | None:
        for attempt in range(2):                     # first call may pay a cold model load
            try:
                request = _req.Request(url + path, data=_json.dumps(payload).encode("utf-8"),
                                       headers={"Content-Type": "application/json"})
                with _req.urlopen(request, timeout=60 if attempt else 20) as resp:
                    return _json.loads(resp.read().decode("utf-8"))
            except Exception:
                continue
        return None

    try:
        with _req.urlopen(url + "/api/tags", timeout=2) as resp:
            names = {m.get("name", "") for m in (_json.loads(resp.read().decode("utf-8")) or {}).get("models", [])}
    except Exception:
        return None
    if not any(n == model or n == f"{model}:latest" or n.split(":")[0] == model for n in names):
        return None

    def cosine(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = sum(x * x for x in a) ** 0.5
        nb = sum(y * y for y in b) ** 0.5
        return dot / (na * nb) if na and nb else 0.0

    def similarity(event_text: str, candidates: list[str]) -> float:
        if not candidates:
            return 0.0
        data = post("/api/embed", {"model": model, "input": [event_text] + candidates})
        vectors = (data or {}).get("embeddings") or []
        if len(vectors) != len(candidates) + 1:
            return 0.0
        return max(cosine(vectors[0], vec) for vec in vectors[1:])

    return similarity


# ---------------------------------------------------------------- parsing
def squeeze(text: str) -> str:
    return re.sub(r"\s+", "", text)


def parse_digest(text: str) -> dict[str, dict]:
    """-> {day: {"events": [{"heading":..., "text":...}], "raw": ...}}"""
    windows: dict[str, dict] = {}
    current_day: str | None = None
    current_event: dict | None = None
    for line in text.splitlines():
        heading = re.match(r"^##\s+.*?(\d{4}-\d{2}-\d{2})", line)
        if heading and not line.startswith("###"):
            current_day = heading.group(1)
            windows[current_day] = {"events": [], "raw": []}
            current_event = None
            continue
        if current_day is None:
            continue
        windows[current_day]["raw"].append(line)
        event = re.match(r"^###\s+(.*)$", line)
        if event:
            if re.search(NON_EVENT, event.group(1).strip()):
                current_event = None   # section, not an event: the writer owes nothing
                continue
            current_event = {"heading": event.group(1), "text": []}
            windows[current_day]["events"].append(current_event)
            continue
        if current_event is not None:
            current_event["text"].append(line)
    for window in windows.values():
        for event in window["events"]:
            event["text"] = "\n".join(event["text"]).strip()
        window["raw"] = "\n".join(window["raw"])
    return windows


def parse_entries(text: str) -> list[dict]:
    """Split a journal (or a single entry) into entries keyed by their window marker.

    `marker` records whether the `<!-- window:DATE -->` line is actually there — that comment is
    the coverage ledger, so a heading-derived date must never be mistaken for one.
    """
    entries: list[dict] = []
    pattern = re.compile(r"<!--\s*window:(\d{4}-\d{2}-\d{2})\s*-->")
    matches = list(pattern.finditer(text))
    if not matches:
        day = None
        heading = re.search(r"(?m)^##\s+(\d{4}-\d{2}-\d{2})", text)
        if heading:
            day = heading.group(1)
        return [{"day": day, "marker": False, "text": text, "body": strip_scaffold(text)}]
    start = 0
    for match in matches:
        chunk = text[start: match.end()]
        start = match.end()
        entries.append({"day": match.group(1), "marker": True, "text": chunk,
                        "body": strip_scaffold(chunk)})
    return entries


def strip_scaffold(text: str) -> str:
    """Entry body without the `## ` heading and the marker comment — what the ceiling counts."""
    body = re.sub(r"<!--\s*window:\d{4}-\d{2}-\d{2}\s*-->", "", text)
    body = re.sub(r"(?m)^##\s.*$", "", body)
    return body.strip()


# ---------------------------------------------------------------- tokens
def tokens(text: str) -> set[str]:
    found: set[str] = set()
    for run in re.findall(rf"[{CJK}]+", text):
        for i in range(len(run) - 1):
            bigram = run[i: i + 2]
            if bigram not in CJK_STOP:
                found.add(bigram)
    for word in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text):
        low = word.lower()
        if low not in LATIN_STOP:
            found.add(low)
    return found


def split_event_tokens(event: dict) -> tuple[set[str], set[str]]:
    """(strong, weak) token sets.

    Strong = the heading plus `- key points:` / `- said:` lines: the task itself.
    Weak   = the assistant's outcome prose: details that may drift into generic wording.
    """
    heading = re.sub(r"\[[^\]]*\]$", "", event["heading"])
    strong_lines, weak_lines = [], []
    for line in event["text"].splitlines():
        text = line.strip()
        if not text:
            continue
        if text.startswith("- ") and not re.match(r"^-\s*(outcome|结论)", text):
            strong_lines.append(text)
        else:
            weak_lines.append(text)
    return tokens(heading + "\n" + "\n".join(strong_lines)), tokens("\n".join(weak_lines))


def distinctive_tokens(events: list[dict]) -> list[tuple[set[str], set[str]]]:
    """Tokens that appear in exactly one event — those prove *which* event a sentence is about."""
    per_event = [split_event_tokens(event) for event in events]
    counts: dict[str, int] = {}
    for strong, weak in per_event:
        for tok in strong | weak:
            counts[tok] = counts.get(tok, 0) + 1
    return [
        ({tok for tok in strong if counts[tok] == 1}, {tok for tok in weak if counts[tok] == 1})
        for strong, weak in per_event
    ]


# ---------------------------------------------------------------- checks
def ceiling_for(n_events: int) -> int:
    for limit, ceiling in CEILING_BY_EVENTS:
        if n_events <= limit:
            return ceiling
    return CEILING_BY_EVENTS[-1][1]


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(rf"[。！？!?\n]|[{CJK}]{{0}}\s*——", text) if s.strip()]


def check_coverage(window: dict, body: str, embedder=None, threshold: float = 0.45) -> dict:
    events = window["events"]
    entry_tokens = tokens(body)
    per_event = distinctive_tokens(events)
    body_sentences = sentences(body)
    rows = []
    for event, (strong, weak) in zip(events, per_event):
        strong_hits = sorted(strong & entry_tokens)
        weak_hits = sorted(weak & entry_tokens)
        covered = bool(strong_hits) or len(weak_hits) >= 2
        method = "lex" if covered else ""
        similarity = None
        if not covered and embedder is not None:
            event_text = re.sub(r"\[[^\]]*\]$", "", event["heading"]) + "\n" + event["text"]
            similarity = embedder(event_text, body_sentences)
            if similarity >= threshold:
                covered = True
                method = "semantic"
        rows.append({
            "event": event["heading"],
            "covered": covered,
            "method": method,
            "strong": strong_hits[:6],
            "weak": weak_hits[:4],
            "similarity": round(similarity, 3) if similarity is not None else None,
            "weak_evidence": covered and method == "lex" and not strong_hits,
        })
    return {"events": rows, "named": sum(1 for r in rows if r["covered"]), "total": len(rows)}


def check_voice(body: str, forbidden: dict[str, str]) -> list[dict]:
    problems = []
    for name, pattern in forbidden.items():
        for match in re.finditer(pattern, body):
            problems.append({"rule": name, "found": match.group(0)})
    return problems


def check_reuse(body: str, history: str, threshold: float = 0.55) -> list[dict]:
    """Flag sentences that overwhelmingly reuse earlier phrasing (the homogenisation smell)."""
    def shingles(text: str, size: int = 4) -> set[str]:
        squashed = squeeze(text)
        return {squashed[i: i + size] for i in range(max(0, len(squashed) - size + 1))}

    previous = [e["body"] for e in parse_entries(history)]
    old = set()
    for chunk in previous:
        old |= shingles(chunk)
    hits = []
    for sentence in sentences(body):
        grams = shingles(sentence)
        if len(grams) < 4:
            continue
        overlap = len(grams & old) / len(grams)
        if overlap >= threshold:
            hits.append({"sentence": sentence[:60], "overlap": round(overlap, 2)})
    return hits


def lint(digest_text: str, entry_text: str, forbidden: dict[str, str] | None = None,
         history: str | None = None, strict: bool = False, embedder=None,
         threshold: float = 0.45) -> dict:
    windows = parse_digest(digest_text)
    entries = parse_entries(entry_text)
    forbidden = DEFAULT_FORBIDDEN if forbidden is None else forbidden
    results = []
    for index, entry in enumerate(entries):
        day = entry["day"] or (list(windows)[index] if index < len(windows) else None)
        window = windows.get(day or "", {"events": [], "raw": ""})
        body = entry["body"]
        chars = len(squeeze(body))
        coverage = check_coverage(window, body, embedder, threshold)
        ceiling = ceiling_for(max(1, coverage["total"]))
        marker_ok = bool(entry.get("marker", True))
        row = {
            "day": day,
            "chars": chars,
            "ceiling": ceiling,
            "coverage": coverage,
            "marker": marker_ok,
            "voice": check_voice(body, forbidden),
            "notes": [p for p in check_voice(body, forbidden) if p["rule"] == "invented_time"],
            "reuse": check_reuse(body, history) if history else [],
        }
        hard = []
        if day not in windows:
            hard.append(f"no digest block for window {day or '?'} — wrong day or wrong digest")
        if coverage["named"] < coverage["total"]:
            hard.append(f"coverage {coverage['named']}/{coverage['total']} events named")
        if not marker_ok:
            hard.append("missing <!-- window:YYYY-MM-DD --> marker")
        if chars > ceiling:
            hard.append(f"{chars} chars over the {ceiling} ceiling for {coverage['total']} events")
        if strict:
            hard.extend(f"voice: {p['rule']} ({p['found']})"
                        for p in row["voice"] if p["rule"] != "invented_time")
            hard.extend(f"reuse: {p['overlap']} of an earlier sentence" for p in row["reuse"])
            hard.extend(f"weak coverage on: {e['event']}" for e in coverage["events"] if e["weak_evidence"])
        row["failures"] = hard
        row["ok"] = not hard
        results.append(row)
    return {"ok": all(r["ok"] for r in results), "entries": results}


# ---------------------------------------------------------------- cli
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint journal entries against the digest they came from.")
    parser.add_argument("--digest", required=True, help="collector output (markdown or --json)")
    parser.add_argument("--entry", help="candidate entry text")
    parser.add_argument("--journal", help="lint the newest entry of this journal file")
    parser.add_argument("--history", help="journal file whose earlier entries count as reuse (default: --journal)")
    parser.add_argument("--forbidden", action="append", metavar="NAME=REGEX",
                        help="extra forbidden pattern; repeatable")
    parser.add_argument("--strict", action="store_true", help="voice and reuse warnings also fail")
    parser.add_argument("--no-semantic", action="store_true",
                        help="skip the local embedding pass, lexical matching only")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument("--embed-model", default="qwen3-embedding:0.6b")
    parser.add_argument("--threshold", type=float, default=0.45,
                        help="cosine similarity that counts as 'this event is named' (default 0.45, "
                             "calibrated for qwen3-embedding:0.6b; recalibrate after changing models)")
    parser.add_argument("--json", action="store_true", help="machine-readable result")
    args = parser.parse_args(argv)

    digest_text = Path(args.digest).read_text(encoding="utf-8")
    if digest_text.lstrip().startswith("{"):
        payload = json.loads(digest_text)
        digest_text = "\n\n".join(w["digest"] for w in payload.get("windows", []))
    if args.entry:
        entry_text = Path(args.entry).read_text(encoding="utf-8")
    elif args.journal:
        journal = Path(args.journal).read_text(encoding="utf-8")
        entries = parse_entries(journal)
        if not entries:
            print("no entries with window markers in the journal", file=sys.stderr)
            return 2
        entry_text = entries[-1]["text"]
    else:
        print("one of --entry or --journal is required", file=sys.stderr)
        return 2

    forbidden = dict(DEFAULT_FORBIDDEN)
    for spec in args.forbidden or []:
        name, _, pattern = spec.partition("=")
        if pattern:
            forbidden[name] = pattern
    history = None
    if args.history:
        history = Path(args.history).read_text(encoding="utf-8")
    elif args.journal:
        history = Path(args.journal).read_text(encoding="utf-8")

    embedder = None
    if not args.no_semantic:
        embedder = make_embedder(args.ollama_url, args.embed_model)
    result = lint(digest_text, entry_text, forbidden, history, args.strict, embedder, args.threshold)
    if args.json:
        result["semantic"] = embedder is not None
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1

    for row in result["entries"]:
        status = "PASS" if row["ok"] else "FAIL"
        print(f"[{status}] window {row['day'] or '?'} — {row['chars']}/{row['ceiling']} chars, "
              f"coverage {row['coverage']['named']}/{row['coverage']['total']}")
        for event in row["coverage"]["events"]:
            mark = "ok  " if event["covered"] else "MISS"
            method = f" [{event['method']}]" if event["method"] else ""
            evidence = ", ".join(event["strong"] or event["weak"]) or (
                f"cos={event['similarity']}" if event["similarity"] is not None else "-")
            print(f"   {mark} {event['event'][:64]}{method}  ({evidence})")
        for problem in row["voice"]:
            label = "note" if problem["rule"] == "invented_time" else "warn"
            print(f"   {label} voice[{problem['rule']}]: {problem['found']} (check against the digest clock)")
        for problem in row["reuse"]:
            print(f"   warn reuse {problem['overlap']}: {problem['sentence']}")
        for failure in row["failures"]:
            print(f"   ! {failure}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
