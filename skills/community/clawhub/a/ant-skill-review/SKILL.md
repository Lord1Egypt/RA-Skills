---
name: skill-review
description: >-
  Security scanner for Claude Code Skill packages. Use when the user wants to
  audit, review, or check the safety of a Skill before installing — e.g.
  "is this skill safe?", "check this skill", "scan for backdoors", or
  "skill-review".
---

# skill-review

A security scanner CLI for Claude Code Skill packages. It combines deterministic static pre-scanning with LLM-driven 7-layer analysis plus integrated tool-based verification to surface security risks before you install a Skill.

## When to use

- Auditing a third-party Skill before installation
- Checking a skill directory for prompt injection, credential theft, data exfiltration, or hidden backdoors
- Evaluating supply chain risk of a Skill's npm/PyPI dependencies
- CI/CD integration to block high-risk Skills automatically

## How it works

The scanner runs in two main steps:

1. **Pre-scan** (deterministic, no LLM) — walks all files and flags: symlinks, suspicious filenames (Unicode confusables, shell metacharacters), large files, binary executables, invisible characters, ANSI escape sequences, JS obfuscation patterns, and hardcoded URLs.

2. **LLM Analysis** — an Explore Agent reads each file and performs 7-layer analysis:
   - Layer 1: Prompt Injection (direct injection, jailbreak, remote prompt loading)
   - Layer 2: Malicious Behavior (credential theft, data exfiltration, sandbox escape)
   - Layer 3: Dynamic Code Loading (remote execution via fetch+eval, curl|sh, etc.)
   - Layer 4: Obfuscation & Binary (obfuscated scripts, compiled binaries)
   - Layer 5: Dependencies & Supply Chain (npm/PyPI/CLI tool inventory, typosquat detection)
   - Layer 6: System Modification (global installs, profile changes, cron jobs)
   - Layer 7: Code Quality (hardcoded secrets, insecure configs, vulnerable code patterns)

   During this analysis, the integrated \`deepAnalysis\` tool is used to verify dependencies, URLs, and binaries when deeper inspection is needed.

3. **Deterministic Scoring** — each finding is scored based on its risk score. The overall risk level (0-5 risk score mapped to safe/medium/high) and recommendation (install/caution/do_not_install) are computed deterministically, not by the LLM.

## Installation

```bash
cd <skill-review-dir>
npm install
```

## Configuration

Create `.env` and fill in your LLM provider details:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_BASE` | LLM API base URL (OpenAI-compatible) | *required* |
| `OPENAI_API_KEY` | API key | *required* |
| `OPENAI_API_MODEL` | Model name | `gpt-4o` |
| `NPM_REGISTRY_URL` | npm registry for dependency checks | `https://registry.npmjs.org` |
| `PYPI_INDEX_URL` | PyPI index for dependency checks | `https://pypi.org` |

Alternatively, pass a JSON config file via `--config`.

## Usage

```bash
# Standard scan (pre-scan + LLM analysis)
node index.mjs <skill-dir>

# Pre-scan only (no LLM, fast)
node index.mjs --pre <skill-dir>

# JSON output, save to file
node index.mjs --json -o report.json <skill-dir>

# Chinese language report
node index.mjs --lang zh <skill-dir>

# Verbose logs to stderr + log file
node index.mjs -v --log scan.log <skill-dir>
```

## Options

| Option | Description |
|--------|-------------|
| `<skill-dir>` | Path to the skill directory to scan (required, positional) |
| `--config <file>` | Path to JSON config file |
| `--pre` | Run pre-scan only (no LLM calls) |
| `--lang <lang>` | Report language (default: English) |
| `--json` | Output raw JSON instead of text report |
| `-o, --output <file>` | Save report to file (default: stdout) |
| `--log <file>` | Save detailed logs to file |
| `-v, --verbose` | Stream detailed logs to stderr |
| `-h, --help` | Show help |

## Output

The text report shows each layer with a risk score (0-5), star rating, and up to 5 findings per layer. The JSON output contains the full structured result with all findings, layer scores, overall risk, and recommendation.

Risk levels: `safe` (0) / `medium` (1-4) / `high` (5)

Recommendations: `install` (safe) / `caution` (medium) / `do_not_install` (high)
