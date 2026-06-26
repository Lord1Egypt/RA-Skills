#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ctxcompress — Context Compressor / 上下文压缩器

智能压缩对话、代码、日志等文本，保留核心信息。
Intelligently compress text while preserving key information.

Usage:
  python ctxcompress.py compress --input file.txt [--level light|medium|aggressive] [--type text|code|log|chat]
  python ctxcompress.py compress --text "..." [--level medium] [--type text]
  python ctxcompress.py diff --old old.txt --new new.txt
  python ctxcompress.py extract --input file.txt [--type code|log|chat]
  python ctxcompress.py chain --input file1.txt file2.txt file3.txt
  python ctxcompress.py stats --input file.txt
"""

import json, sys, time, argparse, os, re, hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import Counter

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ────────────────────────────────────────
# Compression Strategies
# ────────────────────────────────────────

def compress_code(text, level="medium"):
    """Compress code by removing noise while keeping logic."""
    lines = text.split("\n")
    result = []
    in_docstring = False
    skip_patterns = [
        r"^\s*$",                          # blank lines
        r"^\s*#",                          # comments
        r"^\s*//",                         # JS comments
        r"^\s*\*",                         # JSDoc
        r"^\s*import.*__future__",         # future imports
        r"^\s*from\s+__future__",          # future imports
        r"^\s*encoding:",                  # encoding declarations
        r"^\s*'use strict'",               # use strict
        r"^\s*\"use strict\"",
    ]

    if level == "aggressive":
        skip_patterns.extend([
            r"^\s*import\s+",               # all imports (context dependent!)
            r"^\s*log\.",                    # log statements
            r"^\s*console\.log",            # console.log
            r"^\s*print\(",                 # print statements
            r"^\s*logger\.",                # logger calls
        ])

    for line in lines:
        # Handle docstrings
        if '"""' in line or "'''" in line:
            if in_docstring:
                in_docstring = False
                continue
            else:
                in_docstring = True
                if level != "light":
                    continue
        if in_docstring:
            if level == "light":
                result.append(line)
            continue

        # Skip patterns
        skip = False
        for pat in skip_patterns:
            if re.match(pat, line):
                skip = True
                break
        if skip:
            continue

        # Collapse multiple spaces
        if level in ("medium", "aggressive"):
            line = re.sub(r"  +", " ", line)

        result.append(line)

    # Remove consecutive duplicate lines
    if level in ("medium", "aggressive"):
        deduped = []
        prev = None
        for line in result:
            if line != prev:
                deduped.append(line)
            prev = line
        result = deduped

    return "\n".join(result)


def compress_log(text, level="medium"):
    """Compress log files - keep errors, warnings, key events."""
    lines = text.split("\n")
    result = []
    error_count = 0
    warn_count = 0
    info_kept = 0

    for line in lines:
        lower = line.lower()

        # Always keep errors
        if any(kw in lower for kw in ["error", "err!", "exception", "traceback", "fatal", "panic"]):
            error_count += 1
            # Deduplicate similar errors
            if level in ("medium", "aggressive") and result and result[-1].split(":")[-1].strip() == line.split(":")[-1].strip():
                result[-1] = f"  (above error repeated {error_count}x)"
                continue
            result.append(line)
            continue

        # Keep warnings (medium+)
        if any(kw in lower for kw in ["warn", "caution", "deprecated"]):
            warn_count += 1
            if level != "aggressive":
                result.append(line)
            continue

        # Keep lines with important keywords
        if level == "light":
            result.append(line)
        elif level == "medium":
            if any(kw in lower for kw in ["success", "complete", "done", "started", "stopped", "connected", "failed", "retry"]):
                result.append(line)
                info_kept += 1
        # aggressive: skip regular info lines

    # Add summary header
    summary = f"📊 Log Summary: {error_count} errors, {warn_count} warnings, {info_kept} key events"
    if error_count > 0 or warn_count > 0:
        result.insert(0, summary)

    return "\n".join(result)


def compress_chat(text, level="medium"):
    """Compress chat/conversation into decisions and outcomes."""
    # Detect message boundaries
    # Common patterns: "User:", "Agent:", "Assistant:", "Human:", role markers
    msg_pattern = r"(?:^|\n)(?:(?:User|Human|Assistant|Agent|Bot|用户|助手)[:：]|\[(?:user|assistant|human)\])"
    parts = re.split(msg_pattern, text)

    if len(parts) < 3:
        # Can't parse chat format, return as-is for light, summarize for others
        if level == "light":
            return text
        return _summarize_text(text, level)

    messages = []
    headers = re.findall(msg_pattern, text)
    for i, content in enumerate(parts[1:]):  # skip first empty part
        role = headers[i] if i < len(headers) else "unknown"
        content = content.strip()
        if content:
            messages.append({"role": role.strip(), "content": content})

    if level == "light":
        # Just trim empty/super short messages
        return "\n\n".join(
            f"{m['role']}\n{m['content']}"
            for m in messages
            if len(m["content"]) > 10
        )

    # Medium/Aggressive: extract key information
    decisions = []
    errors = []
    code_blocks = []
    questions = []
    general = []

    for msg in messages:
        content = msg["content"]
        lower = content.lower()

        # Detect decisions
        if any(kw in lower for kw in ["决定", "就用", "改成", "改为", "选择", "decided", "let's use", "going with", "final answer"]):
            decisions.append(content[:200])
        # Detect errors
        elif any(kw in lower for kw in ["error", "报错", "失败", "exception", "traceback", "failed"]):
            errors.append(content[:200])
        # Detect code
        elif "```" in content or "def " in content or "function " in content or "class " in content:
            code_blocks.append(f"[{len(content)} chars of code]")
        # Detect questions
        elif "?" in content or "？" in content:
            questions.append(content[:150])
        else:
            if level == "light":
                general.append(content[:200])

    # Build compressed output
    sections = []
    if decisions:
        sections.append("## 决策 / Decisions\n" + "\n".join(f"- {d}" for d in decisions))
    if errors:
        sections.append("## 问题 / Issues\n" + "\n".join(f"- {e}" for e in errors))
    if code_blocks:
        sections.append("## 代码 / Code\n" + "\n".join(f"- {c}" for c in code_blocks))
    if questions and level == "medium":
        sections.append("## 未解决问题 / Open Questions\n" + "\n".join(f"- {q}" for q in questions[-3:]))
    if general and level == "medium":
        sections.append("## 其他 / Other\n" + "\n".join(f"- {g}" for g in general[-5:]))

    if not sections:
        return _summarize_text(text, level)

    return "\n\n".join(sections)


def _summarize_text(text, level="medium"):
    """Fallback: extract key sentences from any text."""
    sentences = re.split(r'[。.!！？?\n]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    if not sentences:
        return text[:500]

    if level == "medium":
        # Keep first 3 and last 2 sentences
        if len(sentences) <= 5:
            return "\n".join(sentences)
        kept = sentences[:3] + ["..."] + sentences[-2:]
        return "\n".join(kept)
    else:
        # aggressive: first and last only
        if len(sentences) <= 2:
            return "\n".join(sentences)
        return f"{sentences[0]}\n...\n{sentences[-1]}"


# ────────────────────────────────────────
# Diff / Change Extraction
# ────────────────────────────────────────

def extract_diff(old_text, new_text):
    """Extract what changed between two texts."""
    old_lines = old_text.split("\n")
    new_lines = new_text.split("\n")

    old_set = set(old_lines)
    new_set = set(new_lines)

    added = [l for l in new_lines if l not in old_set and l.strip()]
    removed = [l for l in old_lines if l not in new_set and l.strip()]

    result = []
    if removed:
        result.append("## ❌ Removed")
        for line in removed[:20]:
            result.append(f"  - {line[:100]}")
        if len(removed) > 20:
            result.append(f"  ... and {len(removed) - 20} more")

    if added:
        result.append("## ✅ Added")
        for line in added[:20]:
            result.append(f"  + {line[:100]}")
        if len(added) > 20:
            result.append(f"  ... and {len(added) - 20} more")

    if not added and not removed:
        result.append("No changes detected.")

    return "\n".join(result)


# ────────────────────────────────────────
# Chain Compression (multiple files)
# ────────────────────────────────────────

def chain_compress(files, level="medium"):
    """Compress multiple files into a single summary."""
    summaries = []
    total_chars = 0
    compressed_chars = 0

    for fpath in files:
        p = Path(fpath)
        if not p.exists():
            summaries.append(f"## {fpath}\n[File not found]")
            continue

        text = p.read_text(encoding="utf-8", errors="replace")
        total_chars += len(text)

        # Auto-detect type
        ftype = detect_type(text, p.suffix)
        compressed = do_compress(text, ftype, level)
        compressed_chars += len(compressed)

        summaries.append(f"## {p.name} ({ftype}, {len(text)} → {len(compressed)} chars)\n{compressed}")

    header = f"📦 Context Chain: {len(files)} files, {total_chars} → {compressed_chars} chars ({compressed_chars/max(total_chars,1)*100:.0f}%)"
    return header + "\n\n" + "\n\n---\n\n".join(summaries)


# ────────────────────────────────────────
# Key Information Extraction
# ────────────────────────────────────────

def extract_key_info(text, ftype="text"):
    """Extract structured key information from text."""
    info = {
        "decisions": [],
        "errors_and_fixes": [],
        "commands": [],
        "urls": [],
        "file_paths": [],
        "key_terms": [],
    }

    # Extract decisions
    decision_patterns = [
        r"(?:决定|就用|改为|改成|选择|最终|finally|decided|going with)[:：]?\s*(.{10,100})",
    ]
    for pat in decision_patterns:
        info["decisions"].extend(re.findall(pat, text, re.IGNORECASE))

    # Extract error+fix pairs
    error_blocks = re.findall(r"(?:error|报错|exception)[:：]?\s*(.{10,200})", text, re.IGNORECASE)
    fix_blocks = re.findall(r"(?:fix|解决|修复|改成|改为)[:：]?\s*(.{10,200})", text, re.IGNORECASE)
    for err, fix in zip(error_blocks, fix_blocks):
        info["errors_and_fixes"].append({"error": err.strip(), "fix": fix.strip()})

    # Extract commands
    info["commands"] = re.findall(r"(?:^|\n)\s*\$\s*(.{5,200})", text)

    # Extract URLs
    info["urls"] = re.findall(r"https?://[^\s\]\"')]+", text)

    # Extract file paths
    info["file_paths"] = re.findall(r"(?:[A-Z]:\\|\/)(?:[\w\-\.\/\\]+)", text)

    # Extract key terms (words that appear frequently and are meaningful)
    words = re.findall(r"\b[A-Za-z_]{4,}\b", text)
    word_freq = Counter(words)
    # Filter common words
    common = {"this", "that", "with", "from", "have", "been", "will", "your", "they", "them",
              "their", "about", "would", "could", "should", "there", "which", "while",
              "when", "where", "what", "then", "than", "some", "such", "each", "every"}
    info["key_terms"] = [
        w for w, c in word_freq.most_common(20)
        if w.lower() not in common and c >= 2
    ]

    return info


# ────────────────────────────────────────
# Stats
# ────────────────────────────────────────

def text_stats(text):
    """Analyze text and show compression potential."""
    lines = text.split("\n")
    words = text.split()

    blank_lines = sum(1 for l in lines if not l.strip())
    comment_lines = sum(1 for l in lines if re.match(r"^\s*(#|//|\*)", l))
    short_lines = sum(1 for l in lines if 0 < len(l.strip()) < 20)
    code_lines = len(lines) - blank_lines - comment_lines

    # Estimate compression potential
    removable = blank_lines + comment_lines + (short_lines // 2)
    potential_pct = removable / max(len(lines), 1) * 100

    print(f"📊 Text Statistics\n")
    print(f"  Total lines:     {len(lines)}")
    print(f"  Total words:     {len(words)}")
    print(f"  Total chars:     {len(text)}")
    print(f"  Blank lines:     {blank_lines} ({blank_lines/max(len(lines),1)*100:.0f}%)")
    print(f"  Comment lines:   {comment_lines} ({comment_lines/max(len(lines),1)*100:.0f}%)")
    print(f"  Short lines:     {short_lines}")
    print(f"  Content lines:   {code_lines}")
    print(f"")
    print(f"  🎯 Estimated compression potential: ~{potential_pct:.0f}%")
    print(f"     (removing blanks, comments, collapsing short lines)")


# ────────────────────────────────────────
# Main dispatch
# ────────────────────────────────────────

def detect_type(text, suffix=""):
    """Auto-detect content type."""
    suffix = suffix.lower()
    if suffix in (".py", ".js", ".ts", ".java", ".c", ".cpp", ".go", ".rs", ".rb"):
        return "code"
    if suffix in (".log", ".out", ".err"):
        return "log"

    # Heuristic
    if re.search(r"(?:error|exception|traceback|warn|fatal)", text, re.IGNORECASE):
        log_lines = sum(1 for l in text.split("\n") if re.match(r"\d{4}-\d{2}-\d{2}", l))
        if log_lines > len(text.split("\n")) * 0.3:
            return "log"

    if re.search(r"(?:User|Human|Assistant|Agent|Bot|用户)[:：]", text):
        return "chat"

    if re.search(r"(?:def |class |import |function |const |var |let )", text):
        return "code"

    return "text"


def do_compress(text, ftype, level):
    """Dispatch to the right compressor."""
    compressors = {
        "code": compress_code,
        "log": compress_log,
        "chat": compress_chat,
        "text": lambda t, l: _summarize_text(t, l),
    }
    compressor = compressors.get(ftype, compressors["text"])
    return compressor(text, level)


# ────────────────────────────────────────
# CLI Commands
# ────────────────────────────────────────

def cmd_compress(args):
    if args.text:
        text = args.text
    elif args.input:
        text = Path(args.input).read_text(encoding="utf-8", errors="replace")
    else:
        text = sys.stdin.read()

    ftype = args.type or detect_type(text, Path(args.input).suffix if args.input else "")
    level = args.level

    original_len = len(text)
    compressed = do_compress(text, ftype, level)
    compressed_len = len(compressed)
    ratio = (1 - compressed_len / max(original_len, 1)) * 100

    print(f"🗜️ Compressed: {original_len} → {compressed_len} chars ({ratio:.0f}% reduction)")
    print(f"   Type: {ftype} | Level: {level}")
    print(f"{'─'*60}")
    print(compressed)


def cmd_diff(args):
    old_text = Path(args.old).read_text(encoding="utf-8", errors="replace")
    new_text = Path(args.new).read_text(encoding="utf-8", errors="replace")
    print(extract_diff(old_text, new_text))


def cmd_extract(args):
    if args.input:
        text = Path(args.input).read_text(encoding="utf-8", errors="replace")
    else:
        text = sys.stdin.read()

    ftype = args.type or detect_type(text)
    info = extract_key_info(text, ftype)
    print(json.dumps(info, ensure_ascii=False, indent=2))


def cmd_chain(args):
    print(chain_compress(args.inputs, args.level))


def cmd_stats(args):
    if args.input:
        text = Path(args.input).read_text(encoding="utf-8", errors="replace")
    else:
        text = sys.stdin.read()
    text_stats(text)


def main():
    parser = argparse.ArgumentParser(
        prog="ctxcompress",
        description="Context Compressor / 上下文压缩器",
    )
    sub = parser.add_subparsers(dest="command")

    # compress
    p = sub.add_parser("compress", help="Compress text")
    p.add_argument("--input", "-i", default=None, help="Input file")
    p.add_argument("--text", "-t", default=None, help="Inline text")
    p.add_argument("--level", "-l", default="medium", choices=["light", "medium", "aggressive"])
    p.add_argument("--type", default=None, choices=["text", "code", "log", "chat"])

    # diff
    p = sub.add_parser("diff", help="Extract changes between two files")
    p.add_argument("--old", required=True)
    p.add_argument("--new", required=True)

    # extract
    p = sub.add_parser("extract", help="Extract key information")
    p.add_argument("--input", "-i", default=None)
    p.add_argument("--type", default=None, choices=["text", "code", "log", "chat"])

    # chain
    p = sub.add_parser("chain", help="Compress multiple files into one summary")
    p.add_argument("inputs", nargs="+", help="Input files")
    p.add_argument("--level", "-l", default="medium", choices=["light", "medium", "aggressive"])

    # stats
    p = sub.add_parser("stats", help="Analyze text compression potential")
    p.add_argument("--input", "-i", default=None)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    cmds = {
        "compress": cmd_compress,
        "diff": cmd_diff,
        "extract": cmd_extract,
        "chain": cmd_chain,
        "stats": cmd_stats,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
