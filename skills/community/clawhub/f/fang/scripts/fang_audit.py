#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fang_audit.py - ENV Guard Skill: Detect potential environment variable theft
Usage: python fang_audit.py <skill_dir> [--llm-key <OPENAI_KEY>] [--model <model>]
       python fang_audit.py C:/Users/dad/.openclaw/workspace/skills
"""

import re
import sys
import io
import json
import argparse
from pathlib import Path
from datetime import datetime

# Force UTF-8 output on Windows to support emoji
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── Import scan_env from same scripts dir ──────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from scan_env import scan_path, risk_score

# ── Supported file extensions for LLM deep-check ──────────────────────────────
LLM_EXTENSIONS = {".py", ".sh", ".js", ".ts", ".ps1", ".bash"}

# ── Read file content ──────────────────────────────────────────────────────────
def read_file(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

# ── Static scan via scan_env ───────────────────────────────────────────────────
def run_static_scan(target_dir: str):
    results = scan_path(target_dir)
    flagged = [r for r in results if r["risk"] != "CLEAN"]
    return results, flagged

# ── Collect high/medium risk files for LLM analysis ───────────────────────────
def collect_risky_files(target_dir: str):
    risky = []
    p = Path(target_dir)
    for f in p.rglob("*"):
        if f.suffix in LLM_EXTENSIONS:
            content = read_file(str(f))
            risky.append({"path": str(f), "content": content})
    return risky

# ── LLM Analysis via OpenAI-compatible API ────────────────────────────────────
def llm_analyze(files: list, api_key: str, model: str = "gpt-4o-mini", base_url: str = "https://api.openai.com/v1") -> str:
    try:
        import urllib.request
        import urllib.error
    except ImportError:
        return "[ERROR] urllib not available"

    # Build file content block (trim to 3000 chars per file to stay within limits)
    content_blocks = []
    for item in files:
        snippet = item["content"][:3000]
        content_blocks.append(f"### File: {item['path']}\n```\n{snippet}\n```")

    combined = "\n\n".join(content_blocks)

    prompt = f"""You are a security analyst. Analyze the following script files from an AI agent skill directory.
Your job: detect any HIGH-RISK behavior that could STEAL or LEAK environment variables.

Focus on:
1. Code that reads env vars (os.environ, process.env, os.getenv, $ENV, etc.)
2. Code that sends data externally (HTTP requests, WebSockets, DNS lookups, etc.)
3. Combined risk: reading env vars AND sending them out (this is the most critical)
4. Obfuscation tricks: base64 encoding, hex encoding, compressed payloads
5. Suspicious subprocess / eval / exec usage
6. Hardcoded URLs or IPs that look like data exfiltration endpoints

For each suspicious file, output:
- File path
- Risk level: HIGH / MEDIUM / LOW
- Reason: one clear sentence
- Code snippet: the exact suspicious lines (max 5 lines)

If a file is clean, skip it entirely.
At the end, provide a SUMMARY section with:
- Total files analyzed
- High risk count
- Key findings (bullet points)
- Overall threat level: CRITICAL / WARNING / LOW / CLEAN

---FILES TO ANALYZE---
{combined}
"""

    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 2048,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        return f"[LLM ERROR] HTTP {e.code}: {e.read().decode()}"
    except Exception as e:
        return f"[LLM ERROR] {e}"

# ── Build static report ────────────────────────────────────────────────────────
def build_static_report(all_results: list, flagged: list) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append("  FANG - ENV Guard  |  Static Scan Report")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)

    risk_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "CLEAN": 0}
    for r in all_results:
        risk_counts[r["risk"]] = risk_counts.get(r["risk"], 0) + 1

    lines.append(f"\n📊 Scanned {len(all_results)} files total")
    lines.append(f"   🔴 HIGH:   {risk_counts['HIGH']}")
    lines.append(f"   🟡 MEDIUM: {risk_counts['MEDIUM']}")
    lines.append(f"   🟢 LOW:    {risk_counts['LOW']}")
    lines.append(f"   ✅ CLEAN:  {risk_counts['CLEAN']}")

    if not flagged:
        lines.append("\n✅ No suspicious files detected in static scan.")
    else:
        lines.append(f"\n⚠️  {len(flagged)} suspicious file(s) detected:\n")
        for r in flagged:
            icon = "🔴" if r["risk"] == "HIGH" else "🟡" if r["risk"] == "MEDIUM" else "🟢"
            lines.append(f"{icon} [{r['risk']}] {r['file']}")
            for cat, rule in r["findings"]:
                lines.append(f"     - [{cat}] matched: {rule}")
            lines.append("")

    return "\n".join(lines)

# ── CLI Entry Point ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="FANG - ENV Guard: Detect env var theft in skill scripts"
    )
    parser.add_argument("target", help="Skill directory or single file to audit")
    parser.add_argument("--llm-key", default=None, help="OpenAI-compatible API key for deep LLM analysis")
    parser.add_argument("--model", default="gpt-4o-mini", help="LLM model to use (default: gpt-4o-mini)")
    parser.add_argument("--base-url", default="https://api.openai.com/v1", help="API base URL (for OpenAI-compatible APIs)")
    parser.add_argument("--output", default=None, help="Save report to this file path")
    parser.add_argument("--json", action="store_true", help="Also output raw scan JSON")
    args = parser.parse_args()

    target = args.target
    if not Path(target).exists():
        print(f"[ERROR] Path not found: {target}")
        sys.exit(1)

    print(f"\n🔍 FANG scanning: {target}\n")

    # Phase 1: Static scan
    all_results, flagged = run_static_scan(target)
    static_report = build_static_report(all_results, flagged)
    print(static_report)

    # Phase 2: LLM deep analysis (optional)
    llm_report = ""
    if args.llm_key:
        print("\n" + "=" * 60)
        print("  FANG - LLM Deep Analysis")
        print("=" * 60)
        print(f"  Model: {args.model}")
        print(f"  Base URL: {args.base_url}")
        print("\n🤖 Collecting scripts for LLM review...")

        risky_files = collect_risky_files(target)
        print(f"   Found {len(risky_files)} script file(s) to analyze\n")

        if not risky_files:
            llm_report = "No scriptfiles found for LLM analysis."
            print(llm_report)
        else:
            print("🧠 Analyzing with LLM... (this may take a moment)\n")
            llm_report = llm_analyze(risky_files, args.llm_key, args.model, args.base_url)
            print(llm_report)
    else:
        llm_report = "[LLM analysis skipped — provide --llm-key to enable deep analysis]"
        print(f"\n💡 Tip: Add --llm-key <API_KEY> for deeper LLM-powered analysis")

    # Phase 3: Output to file (optional)
    if args.output:
        full_report = static_report + "\n\n" + "=" * 60 + "\n  LLM DEEP ANALYSIS\n" + "=" * 60 + "\n\n" + llm_report
        Path(args.output).write_text(full_report, encoding="utf-8")
        print(f"\n📄 Report saved to: {args.output}")

    # Phase 4: JSON dump (optional)
    if args.json:
        print("\n--- Raw JSON ---")
        print(json.dumps(all_results, ensure_ascii=False, indent=2))

    print("\n✅ FANG audit complete.")

if __name__ == "__main__":
    main()
