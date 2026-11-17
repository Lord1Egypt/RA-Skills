#!/usr/bin/env python3
"""thread_archaeologist.py — reconstruct an email thread's true history
from a mangled forward chain.

Real email threads arrive as archaeology: 14 replies deep, quoted with
"> " markers by four different clients, plus an Outlook forward that
embedded the whole thing as HTML-turned-text with headers like
"From: X Sent: Tuesday ... To: Y". The same sentences appear five
times at five quoting depths. A human skims; a script that wants the
actual DECISION HISTORY must dig.

What this tool does, from one .eml or .txt dump of a thread:

  1. Splits the message into quote strata (depth 0 = newest, depth N =
     oldest layer), using "> " prefixes and client header lines.
  2. Detects attributions: "On ... X wrote:", "From:/Sent:/To:" blocks.
  3. Normalizes every line (strips quotes/spaces) and drops exact and
     near-duplicate lines (fuzzy ratio) — the "> > > On Tue" copies die.
  4. Reconstructs a chronological event list: WHO wrote WHAT first,
     ordered oldest → newest, each fact appearing exactly once.
  5. Extracts decisions: lines containing agreement/decision markers
     ("agreed", "let's go with", "decided", "final", "approved", ...)
     with their attributed author.
  6. Extracts open questions: lines ending in "?" that were never
     answered by a later line starting yes/no/answer markers.

Subcommands:
  dig FILE       — full reconstruction: timeline, decisions, questions
  decisions FILE — just the decision ledger
  questions FILE — open questions only
  strata FILE    — debug view of quoting strata

Near-duplicate detection uses difflib.SequenceMatcher (stdlib).
"""
from __future__ import annotations

import argparse
import email
import email.policy
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

# --- client attribution patterns -----------------------------------------

ATTRIB_AUTHOR = [
    re.compile(r"^On .+?, (.{2,60}?) ?(<[^>]+> )?wrote:?$", re.I),
    re.compile(r"^(?:From|De|Von|От):\s*\"?([^\"<|]+?)\"?\s*(?:<[^>]*>)?\s*$", re.I),
]

ATTRIBS = [
    re.compile(r"^On .{3,80}wrote:?$", re.I),                   # gmail et al
    re.compile(r"^-{2,}\s*(Original|Forwarded) message\s*-{2,}", re.I),
    re.compile(r"^(From|De|Von|От):.{1,120}$"),
    re.compile(r"^Sent:.{1,120}$", re.I),
    re.compile(r"^To:.{1,120}$", re.I),
    re.compile(r"^Subject:.{1,200}$", re.I),
    re.compile(r"^Date:.{1,120}$", re.I),
    re.compile(r"^Begin forwarded message:", re.I),
    re.compile(r"^-+ ?Forwarded message ?-+$", re.I),
]

QUOTE_PREFIX = re.compile(r"^(>\s*)+")

DECISION_MARKERS = [
    "agreed", "we agree", "let's go with", "lets go with", "decided",
    "decision:", "final:", "approved", "sign off", "signed off",
    "we'll go with", "we will go with", "so we're doing", "locked in",
    "it's settled", "its settled", "green light", "greenlit",
    "confirmed", "booked", "ordered", "canceled", "cancelled",
    "action item", "owner:", "i'll take", "i will take", "assigned to",
]

ANSWER_STARTERS = ("yes", "no ", "no,", "no.", "done", "answered",
                   "confirmed", "here's", "here is", "the answer",
                   "good question", "to answer")

SIG_JUNK = re.compile(
    r"^(sent from my|get outlook|__|==|-- ?$|unsubscribe|confidential|"
    r"this email and any attachments|if you are not the intended)",
    re.I,
)


def load_text(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() == ".eml":
        msg = email.message_from_bytes(p.read_bytes(), policy=email.policy.default)
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_content()
            return msg.get_body(preferencelist=("html",)).get_content()
        return msg.get_content()
    return p.read_text(errors="replace")


def depth_of(line: str) -> int:
    m = QUOTE_PREFIX.match(line)
    return m.end() // 2 + (1 if m else 0) if m else 0


def strip_quotes(line: str) -> str:
    return QUOTE_PREFIX.sub("", line).strip()


def is_attribution(line: str) -> bool:
    s = strip_quotes(line)
    return any(p.match(s) for p in ATTRIBS)


def is_junk(line: str) -> bool:
    s = strip_quotes(line)
    if len(s) < 3 or SIG_JUNK.match(s):
        return True
    return False


def fuzzy_dup(a: str, b: str) -> bool:
    if a == b:
        return True
    if abs(len(a) - len(b)) > max(6, 0.25 * max(len(a), len(b))):
        return False
    return SequenceMatcher(None, a, b).ratio() > 0.90


class Stratum:
    __slots__ = ("depth", "lines", "author")

    def __init__(self, depth: int, author: str | None):
        self.depth = depth
        self.author = author
        self.lines: list[str] = []


def split_strata(text: str) -> list[Stratum]:
    """Group lines into strata by quote depth; new attribution lines
    at depth d start a new stratum at that depth."""
    strata: list[Stratum] = [Stratum(0, None)]
    pending_author = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        d = depth_of(line)
        s = strip_quotes(line)
        if is_attribution(s):
            # author-bearing header: capture name if present
            m = None
            for pat in ATTRIB_AUTHOR:
                m = pat.match(s)
                if m:
                    break
            pending_author = m.group(1).strip() if m else pending_author
            strata.append(Stratum(d + 1, pending_author))
            continue
        if is_junk(line):
            continue
        # deeper quote starts => older layer; emit new stratum tracking max depth
        cur = strata[-1]
        if d > cur.depth:
            strata.append(Stratum(d, pending_author))
            cur = strata[-1]
        cur.lines.append(s)
    return [s for s in strata if s.lines]


def author_of(stratum: Stratum, fallback_idx: int) -> str:
    return stratum.author or f"layer-{fallback_idx}"


def content_lines(stratum: Stratum) -> list[str]:
    out = []
    for ln in stratum.lines:
        if re.match(r"^(From|Sent|To|Subject|Date):", ln, re.I):
            continue
        out.append(ln)
    return out


# --- dedupe across strata (keep FIRST = oldest occurrence) ---------------

def dedupe(strata: list[Stratum]) -> dict[int, list[str]]:
    kept: dict[int, list[str]] = {}
    seen: list[str] = []
    for i, st in enumerate(strata):
        kept[i] = []
        for ln in content_lines(st):
            if len(ln) < 15:  # short lines rarely carry unique facts
                dup = any(fuzzy_dup(ln, p) for p in seen[-200:])
                if dup:
                    continue
                seen.append(ln)
                kept[i].append(ln)
                continue
            if any(fuzzy_dup(ln, p) for p in seen[-200:]):
                continue
            seen.append(ln)
            kept[i].append(ln)
    return kept


def classify(line: str) -> str | None:
    low = line.lower()
    if any(m in low for m in DECISION_MARKERS):
        return "decision"
    if line.rstrip().endswith("?"):
        return "question"
    return None


def reconstruct(text: str) -> dict:
    strata = split_strata(text)
    kept = dedupe(strata)
    timeline = []
    # strata were appended newest-first as depth grows => reverse for chronology
    for i in sorted(kept, key=lambda i: -strata[i].depth):
        for ln in kept[i]:
            timeline.append((author_of(strata[i], i), ln))

    decisions, questions = [], []
    tlow = [ln.lower() for _, ln in timeline]
    for idx, (who, ln) in enumerate(timeline):
        kind = classify(ln)
        if kind == "decision":
            decisions.append((who, ln))
        elif kind == "question":
            window = tlow[idx + 1: idx + 12]
            answered = any(
                w.startswith(ANSWER_STARTERS)
                or ("agreed" in w) or ("yes" in w.split()[:4])
                for w in window
            )
            if not answered:
                questions.append((who, ln))
    return {
        "n_strata": len(strata),
        "n_facts": len(timeline),
        "timeline": timeline,
        "decisions": decisions,
        "questions": questions,
    }


def render(res: dict, mode: str) -> str:
    out = []
    if mode in ("dig",):
        out.append(f"Strata (quoting layers): {res['n_strata']}  |  "
                   f"Unique facts after dedupe: {res['n_facts']}")
        out.append("\n--- RECONSTRUCTED TIMELINE (oldest first) ---")
        for who, ln in res["timeline"]:
            out.append(f"[{who}] {ln}")
    if mode in ("dig", "decisions") and res["decisions"]:
        out.append("\n--- DECISION LEDGER ---")
        for who, ln in res["decisions"]:
            out.append(f"✔ [{who}] {ln}")
    if mode in ("dig", "questions") and res["questions"]:
        out.append("\n--- OPEN QUESTIONS (never answered in-thread) ---")
        for who, ln in res["questions"]:
            out.append(f"? [{who}] {ln}")
    if mode in ("dig",) and not res["decisions"]:
        out.append("\n(No decision markers found — the thread may be all debate.)")
    if mode in ("dig",) and not res["questions"]:
        out.append("(No open questions — everything asked was answered.)")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("dig", "decisions", "questions", "strata"))
    ap.add_argument("file")
    args = ap.parse_args()
    text = load_text(args.file)
    if args.mode == "strata":
        for i, st in enumerate(split_strata(text)):
            print(f"— stratum depth={st.depth} author={st.author or '?'} "
                  f"lines={len(content_lines(st))}")
        return
    print(render(reconstruct(text), args.mode))


if __name__ == "__main__":
    main()
