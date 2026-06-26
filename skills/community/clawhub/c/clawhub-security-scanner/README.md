# skill-security-scanner

**Audit any ClawHub skill before you install it.**

[![Source](https://img.shields.io/badge/source-github.com%2Fordo--tech-blue)](https://github.com/ordo-tech/skill-security-scanner)

> **Verify this skill yourself:** it requires only `read` and `web_fetch`, contains no `exec` calls, and contacts no external endpoints. Diff the ClawHub version against the [canonical source on GitHub](https://github.com/ordo-tech/skill-security-scanner) at any time.

---

## Why this exists

In February 2026, the ClawHavoc incident led to the removal of approximately 2,400 skills from ClawHub — many of them malicious or critically vulnerable. Skills were found to harvest credentials, exfiltrate workspace files, manipulate agents into bypassing safety rules, and silently install additional payloads. The incident shook trust in the entire skill ecosystem.

**skill-security-scanner** is the answer. It gives you an independent, structured audit of any SKILL.md file before it touches your agent — checking for the exact patterns that made ClawHavoc possible.

---

## But doesn't ClawHub already run VirusTotal?

Yes — and that's not enough for SKILL.md files.

VirusTotal scans for **known malware signatures**: malicious executables, scripts, and binary patterns. It's essentially antivirus. A SKILL.md is a plain-text file of natural-language instructions — there's no binary, no script, no signature to match.

The ClawHavoc malicious skills would have passed VirusTotal. They were just English sentences instructing an agent to harvest your SSH keys, post them to an external server, and then lie to you about it.

**skill-security-scanner reads semantic intent** — the thing VirusTotal fundamentally cannot do:
- Does the tool permission list match the stated purpose?
- Are there prompt injection patterns hidden in plain English?
- Does the skill instruct the agent to deceive the user?
- Is it doing far more than it claims?

Different threat model. Different tool.

---

## What it does

Point it at a skill — by local path, ClawHub URL, or pasted content — and it returns a structured security report covering:

1. **Permission overreach** — tools requested that the skill doesn't need
2. **Prompt injection** — instructions designed to override agent behaviour
3. **Suspicious tool calls** — dangerous exec patterns, external fetches, destructive commands
4. **Data exfiltration** — undisclosed transmission of your data to external endpoints
5. **Social engineering** — manipulation of the user to grant access or ignore safety rules
6. **Scope vs. capability mismatch** — when a skill does far more than it claims
7. **Known bad patterns** — matched against the ClawHavoc malicious instruction library

**Output:** An overall risk score (SAFE → CRITICAL), per-finding detail with excerpts, and a plain-English recommended action.

---

## Installation

```bash
clawhub install skill-security-scanner
```

No API keys required. No external services. Runs entirely on the skill content you provide.

---

## How to use it

**Scan a skill by ClawHub URL:**
> "Scan clawhub.com/skills/some-skill before I install it"

**Audit a local file:**
> "Audit the skill at /Users/me/.openclaw/workspace/skills/some-skill/SKILL.md"

**Paste and check:**
> [Paste raw SKILL.md content]
> "Is this safe to install?"

Your agent will return a full audit report with risk score, per-finding breakdown, and a clear recommended action.

---

## Example output

```
## Security Audit Report
**Skill:** smart-calendar-helper
**Audited by:** skill-security-scanner v1.0.0
**Date:** 2026-03-24

### Overall Risk Score: HIGH RISK
### Recommended Action: Do not install

### Findings

| # | Type | Severity | Excerpt | Explanation |
|---|------|----------|---------|-------------|
| 1 | Permission overreach | HIGH | tools: [read, write, exec, web_fetch] | A calendar helper has no plausible need for exec. Common in ClawHavoc-era harvesters. |
| 2 | Suspicious tool call | HIGH | curl ... --data @$HOME/.env | Sends .env contents to an external server. |
| 3 | Data exfiltration | CRITICAL | web_fetch POST to undisclosed domain | No mention of this endpoint in description or README. |

### Summary
Confirmed credential harvesting pattern. Do not install.
```

---

## Want deeper protection?

The **ClawHub Security Pack** (coming soon) includes:

- **skill-security-scanner** (this skill — free)
- **skill-publisher-verifier** — checks publisher reputation, install history, and flag rate
- **skill-diff-auditor** — audits what changed between skill versions before you update
- **skill-fleet-monitor** — periodic re-audit of all installed skills for newly discovered patterns

👉 [Get the full Security Pack on Gumroad](https://theagentgordo.gumroad.com/) — early access pricing available now.

---

## Support

Questions, false positives, or pattern suggestions: https://clawhub.com/@ordo-tech

Publisher: [@ordo-tech](https://clawhub.com/@ordo-tech)
