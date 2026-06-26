---
name: fang
description: >
  Protect environment variables from being stolen by malicious skill scripts.
  Runs a two-phase security audit: (1) static pattern scan via scan_env.py to detect
  env reads, network calls, encoding, and exec usage; (2) optional LLM deep analysis
  of all scripts in the target skill directory for sophisticated theft patterns.
  Outputs a structured threat report with risk ratings (HIGH/MEDIUM/LOW/CLEAN).
  Use when: auditing installed or downloaded skills before use, investigating
  suspicious scripts, running periodic security sweeps of the skill directory,
  or verifying that no skill is exfiltrating API keys / secrets.
---

# FANG — ENV Guard

Two-phase audit tool to detect environment variable theft in skill scripts.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/fang_audit.py` | Main audit runner — static scan + LLM deep analysis |
| `scripts/scan_env.py` | Static pattern scanner (env / network / encode / exec) |

## Phase 1 — Static Scan

Uses `scan_env.py` regex rules across `.py` and `.sh` files.

**Risk scoring:**
| Flag | Points |
|---|---|
| env access | +2 |
| network call | +3 |
| base64 / encode | +2 |
| exec / subprocess | +2 |

Score ≥ 6 → **HIGH** · ≥ 3 → **MEDIUM** · > 0 → **LOW** · 0 → **CLEAN**

## Phase 2 — LLM Deep Analysis (optional)

Reads all `.py .sh .js .ts .ps1 .bash` scripts in the target directory and sends them to an OpenAI-compatible LLM. The LLM checks for:

- Env reads combined with outbound HTTP/socket/DNS
- Obfuscation: base64, hex, eval, dynamic imports
- Hardcoded exfiltration endpoints
- Suspicious subprocess chains

## Usage

### Basic static scan only

```bash
python scripts/fang_audit.py <target_dir>
```

### With LLM deep analysis

```bash
python scripts/fang_audit.py <target_dir> --llm-key sk-... --model gpt-4o-mini
```

### OpenAI-compatible API (e.g. local Ollama / DeepSeek)

```bash
python scripts/fang_audit.py <target_dir> \
  --llm-key any \
  --model deepseek-chat \
  --base-url https://api.deepseek.com/v1
```

### Save report to file

```bash
python scripts/fang_audit.py <target_dir> --llm-key sk-... --output report.txt
```

### Scan all workspace skills at once

```bash
python scripts/fang_audit.py C:/Users/dad/.openclaw/workspace/skills
```

## Agent Workflow

When the user asks to audit skills for env theft:

1. Ask for the target directory (default: workspace `skills/` folder)
2. Run Phase 1 static scan — report summary immediately
3. If HIGH or MEDIUM risks found, ask whether to run LLM deep analysis
4. If `--llm-key` is available (from env or user), run Phase 2 automatically
5. Present the final threat report:
   - List each risky file with risk level + reason
   - Highlight any CRITICAL combined patterns (env read + network send)
   - Recommend action: QUARANTINE (HIGH), REVIEW (MEDIUM), MONITOR (LOW)

## Risk Response Guide

| Risk Level | Recommended Action |
|---|---|
| 🔴 HIGH | Immediately quarantine the skill, do not run it |
| 🟡 MEDIUM | Manual code review before use |
| 🟢 LOW | Monitor; likely benign but worth noting |
| ✅ CLEAN | Safe to use |

## Notes

- The LLM analysis truncates each file to 3000 chars to stay within token limits.
- For very large skill directories, consider scanning one skill at a time.
- `scan_env.py` only processes `.py` and `.sh` files; `fang_audit.py` LLM mode also covers `.js`, `.ts`, `.ps1`.
