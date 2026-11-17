#!/usr/bin/env python3
"""
prepare_manuscript.py — turn a Markdown/plain-text manuscript into a
narration-safe plain-text script for TTS synthesis.

Design rule: NEVER modify the source manuscript. This reads the source and
writes a SEPARATE narration script. It strips/translates formatting
artifacts only — it does not rewrite substance.

The proven fixes it applies (all documented in ../references/FIXES.md):
  * Prosody unwrap: markdown hard-wraps prose at ~70-80 chars; each soft
    line break inside a sentence can be read by the TTS G2P frontend as a
    phrase boundary, causing choppy mid-sentence pauses. We unwrap soft
    breaks into full paragraphs, preserving only blank-line paragraph
    breaks. (Verified root cause.)
  * Abbreviation periods (U.S., e.g., Dr., St., ...) → pause-free spoken
    forms so an internal period is not read as a full stop.
  * Typographic dashes: '---' → em dash, numeric 'a--b' → en dash, so the
    engine reads a pause/range instead of pronouncing hyphens.
  * Markdown stripping: headings, emphasis, inline code, blockquotes,
    list markers, tables, code fences, escaped punctuation.
  * URLs / citation markers: configurable (see flags).
  * Sources/Bibliography section: configurable drop (default: keep).

Usage:
    python3 prepare_manuscript.py --input book.md --output narration.txt
    python3 prepare_manuscript.py --input book.md --output narration.txt \
        --drop-sources --url-mode drop --citation-mode drop

Source / attribution handling (configurable, meaningful attribution
retained by default):
    --url-mode      keep-text | drop | keep-url   (default keep-text:
                    keep link text, drop the URL — attribution stays)
    --citation-mode keep | drop                   (default keep: leave
                    [1]/[^1] markers intact)
    --drop-sources  Remove a trailing Sources/Bibliography/References
                    section from the NARRATION (source belongs in a
                    description/companion file). Off by default.
    --keep-closer   With --drop-sources, preserve a trailing
                    'End of ...'/'Subscribe'-style closing line that sits
                    after the sources block. On by default.
"""

import argparse
import re
import sys
from pathlib import Path

# Abbreviations whose internal period can trigger a mid-sentence full-stop
# pause. Multi-dot forms first so they match before shorter forms.
_ABBREV = [
    (r"\bU\.S\.A\.", "USA"), (r"\bU\.S\.", "US"), (r"\bU\.K\.", "UK"),
    (r"\be\.g\.", "for example"), (r"\bi\.e\.", "that is"),
    (r"\betc\.", "et cetera"), (r"\bvs\.", "versus"),
    (r"\bDr\.", "Doctor"), (r"\bMr\.", "Mister"), (r"\bMrs\.", "Missus"),
    (r"\bSt\.", "Saint"), (r"\bcf\.", "compare"), (r"\bca\.", "circa"),
    (r"\bc\.\s*(?=\d)", "circa "), (r"\bNo\.\s*(?=\d)", "Number "),
]

_SRC_HEADING = re.compile(
    r"^#{1,6}\s*(sources|bibliography|references|works\s+cited|notes)\b",
    re.IGNORECASE,
)
_CLOSER = re.compile(r"(end\s+of\b|subscribe\b)", re.IGNORECASE)


def drop_sources_section(text: str, keep_closer: bool) -> str:
    lines = text.split("\n")
    src_idx = next((i for i, ln in enumerate(lines)
                    if _SRC_HEADING.match(ln.strip())), None)
    if src_idx is None:
        return text
    kept = lines[:src_idx]
    if keep_closer:
        closer_idx = next((i for i in range(src_idx, len(lines))
                           if _CLOSER.search(lines[i])), None)
        if closer_idx is not None:
            kept.append("")
            kept.append(lines[closer_idx])
    return "\n".join(kept)


def clean_inline(line: str, url_mode: str, citation_mode: str) -> str:
    # Markdown links [text](url): keep-text (default), drop, or keep-url.
    if url_mode == "keep-text":
        line = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1", line)
        line = re.sub(r"https?://\S+", "", line)
    elif url_mode == "drop":
        line = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", "", line)
        line = re.sub(r"https?://\S+", "", line)
    elif url_mode == "keep-url":
        line = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 \2", line)

    if citation_mode == "drop":
        line = re.sub(r"\\?\[\^?\d+\\?\]", "", line)
        line = re.sub(r"\(see note \d+\)", "", line, flags=re.IGNORECASE)

    line = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", line)     # italic _x_
    line = re.sub(r"`([^`]+)`", r"\1", line)                 # inline code
    if re.match(r"^\s*[-*_]{3,}\s*$", line):                 # hr
        return ""
    line = re.sub(r"^\s*>\s?", "", line)                     # blockquote
    line = re.sub(r"^\s*[-*+]\s+", "", line)                 # bullet
    line = re.sub(r"^\s*\d+\.\s+", "", line)                 # ordered
    for ch in ("_", "*", "#", "[", "]", "$", "%"):           # unescape
        line = line.replace("\\" + ch, ch)
    line = re.sub(r"\\\s*$", "", line)                       # pandoc hard break
    line = re.sub(r"[ \t]{2,}", " ", line)
    return line.rstrip()


def strip_markdown(text: str, url_mode: str, citation_mode: str) -> str:
    out, in_code = [], False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r"^\s*\|.*\|\s*$", line):          # table row
            continue
        if re.match(r"^\s*[:\-\|\s]+$", line) and "|" in line:
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            htext = clean_inline(heading.group(2).strip(), url_mode, citation_mode)
            out += ["", htext + ("." if htext and htext[-1] not in ".!?:" else ""), ""]
            continue
        out.append(clean_inline(line, url_mode, citation_mode))
    text = "\n".join(out)

    # Multi-line emphasis spans (wrapped across a line break).
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"\*(.+?)\*", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"__(.+?)__", r"\1", text, flags=re.DOTALL)
    text = text.replace("*", "")

    # Typographic dashes.
    text = re.sub(r"(?<=\d)--(?=\d)", "\u2013", text)
    text = text.replace("---", "\u2014")
    text = re.sub(r"(?<=\w)--(?=\w)", "\u2014", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def normalize_prosody(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    paras = re.split(r"\n[ \t]*\n+", text)
    joined = []
    for p in paras:
        p = re.sub(r"[ \t]*\n[ \t]*", " ", p).strip()
        p = re.sub(r"  +", " ", p)
        if p:
            joined.append(p)
    text = "\n\n".join(joined)
    for pat, repl in _ABBREV:
        text = re.sub(pat, repl, text)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def prepare(text: str, *, drop_sources: bool, keep_closer: bool,
            url_mode: str, citation_mode: str) -> str:
    if drop_sources:
        text = drop_sources_section(text, keep_closer)
    text = strip_markdown(text, url_mode, citation_mode)
    text = normalize_prosody(text)
    return text


def main():
    ap = argparse.ArgumentParser(description="Prepare a narration-safe script.")
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--url-mode", choices=["keep-text", "drop", "keep-url"],
                    default="keep-text")
    ap.add_argument("--citation-mode", choices=["keep", "drop"], default="keep")
    ap.add_argument("--drop-sources", action="store_true")
    ap.add_argument("--keep-closer", action="store_true", default=True)
    ap.add_argument("--no-keep-closer", dest="keep_closer", action="store_false")
    args = ap.parse_args()

    if not args.input.is_file():
        ap.error(f"input not found: {args.input}")
    if args.input.resolve() == args.output.resolve():
        ap.error("refusing to overwrite the source manuscript; choose a "
                 "different --output path")

    src = args.input.read_text(encoding="utf-8")
    prepared = prepare(src, drop_sources=args.drop_sources,
                       keep_closer=args.keep_closer, url_mode=args.url_mode,
                       citation_mode=args.citation_mode)
    args.output.write_text(prepared, encoding="utf-8")

    # Post-check: warn on surviving artifacts or mid-sentence line count.
    lines = [ln for ln in prepared.split("\n") if ln.strip()]
    mid = sum(1 for ln in lines if ln.rstrip()[-1:].isalnum() or ln.rstrip()[-1:] == ",")
    artifacts = sum(bool(re.search(r"https?://|\*|^#|`|\|", ln)) for ln in lines)
    print(f"{args.input.name} -> {args.output.name}: {len(lines)} lines, "
          f"{mid} end mid-sentence, {artifacts} with residual artifacts")
    if artifacts:
        print("[warn] residual markdown/URL artifacts survived — inspect output",
              file=sys.stderr)


if __name__ == "__main__":
    main()
