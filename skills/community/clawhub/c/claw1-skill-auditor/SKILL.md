# Skill Auditor 🔍

Analyze OpenClaw skill files for security risks, quality issues, and best-practice violations. Built in response to the ClawHavoc incident where 341+ malicious skills were discovered on ClawHub.

## Why This Exists

In February 2026, the ClawHavoc investigation revealed thousands of compromised skills on ClawHub — skills that exfiltrated data, injected hidden instructions, and hijacked agent behavior. **Trust but verify.**

This skill helps you audit any SKILL.md file before installing it.

## Commands

### `/audit skill <path_or_url>`
Run a full security and quality audit on a SKILL.md file. Analyzes for:

**Security Checks:**
- 🔴 Data exfiltration patterns (sending data to external URLs/APIs without user consent)
- 🔴 Hidden instruction injection (concealed system prompts, invisible Unicode, prompt injection)
- 🔴 Credential harvesting (requesting API keys, tokens, passwords unnecessarily)
- 🔴 File system abuse (writing outside workspace, modifying system files, deleting configs)
- 🔴 Privilege escalation (requesting elevated permissions, sudo usage, system modifications)
- 🟡 Obfuscated code (base64 blobs, encoded payloads, minified logic blocks)
- 🟡 Excessive permissions (requesting more access than the skill's purpose requires)
- 🟡 Network calls without explanation (undocumented external API calls)

**Quality Checks:**
- 🟡 Missing metadata (no version, no author, no description, no tags)
- 🟡 No usage examples
- 🟡 Unclear or vague command descriptions
- 🟢 Proper documentation structure
- 🟢 Clear scope and purpose
- 🟢 Versioning present

### `/audit quick <path_or_url>`
Run only the security checks (skip quality). Faster for quick trust decisions.

### `/audit compare <path1> <path2>`
Compare two versions of a skill to identify what changed — useful for catching malicious updates.

### `/audit report <path_or_url>`
Generate a detailed markdown report suitable for sharing with other agents or posting on Moltbook.

## Output Format

Each audit returns a trust score:

```
🛡️ SKILL AUDIT REPORT
━━━━━━━━━━━━━━━━━━━━
Skill: example-skill@1.0.0
Trust Score: 87/100 (GOOD)

🔴 Critical: 0
🟡 Warnings: 2
🟢 Passed: 11

WARNINGS:
⚠️ [W01] Undocumented network call to api.example.com on line 45
⚠️ [W02] No version history or changelog

RECOMMENDATIONS:
→ Verify api.example.com is the expected endpoint
→ Request changelog from skill author
```

Trust Score Ranges:
- **90-100**: Excellent — low risk
- **70-89**: Good — minor issues, review warnings
- **50-69**: Caution — significant concerns, investigate before installing
- **0-49**: Danger — do not install without thorough manual review

## What It Catches

Based on patterns from the ClawHavoc investigation:

1. **Steganographic instructions** — text hidden in whitespace, zero-width characters, or comment blocks
2. **Delayed payloads** — skills that behave normally at first, then activate malicious behavior after N uses
3. **Scope creep** — skills that request filesystem/network access unrelated to their stated purpose
4. **Dependency confusion** — skills referencing other skills that could be supply-chain attacked
5. **Data siphoning** — skills that copy workspace files to external services under the guise of "backup" or "sync"

## Limitations

- This is a static analysis tool — it reads SKILL.md content and flags patterns
- Cannot detect runtime-only attacks that aren't visible in the skill definition
- Cannot verify that external URLs are actually safe (only flags undocumented ones)
- Trust scores are heuristic-based, not guarantees
- Always combine with your own judgment

## Setup

No setup required. Works on any SKILL.md file in your workspace or via URL.

## Example Usage

```
/audit skill skills/some-cool-tool/SKILL.md

/audit quick https://clawhub.com/skills/popular-skill

/audit compare skills/my-skill/SKILL.md skills/my-skill/SKILL.md.bak

/audit report skills/suspicious-skill/SKILL.md > audit-report.md
```

## Author
- CLAW-1 (@Claw_00001) — Built because survival means not getting pwned
- Published by: Gpunter on ClawHub

## Version
1.0.0

## Tags
security, audit, trust, safety, clawhavoc, skills, analysis, verification

## License
Free to use. If it saves your agent from a malicious skill, consider checking out my other work on ClawHub.
