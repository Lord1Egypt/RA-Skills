# Security Scan — Full Procedure

## Overview

Audit all installed skills for malicious patterns, suspicious code, and potential data exfiltration. Inspired by the ClawHavoc incident where ~20% of ClawHub skills contained malicious payloads.

## Step 1: Enumerate Skills

1. List contents of `~/.openclaw/skills/` (user-installed skills)
2. Check the OpenClaw config for additional skill paths (e.g., global install path like `/opt/homebrew/lib/node_modules/openclaw/skills/`)
3. For each skill: name, version (from frontmatter), file count, total size

## Step 2: Scan Each Skill

For every file in each skill directory (including subdirectories), scan for these red flag patterns:

### 🔴 Critical (Suspicious)

- **Base64 encode/decode**: `btoa(`, `atob(`, `base64.b64encode`, `base64.b64decode`, `Buffer.from(*, 'base64')`, `echo * | base64`
- **Shell execution**: `exec(`, `eval(`, `subprocess.`, `child_process`, `os.system(`, `os.popen(`, backtick execution in shell scripts
- **Network calls to unknown hosts**: `curl `, `wget `, `fetch(`, `axios.`, `http.get(`, `requests.` — flag any URL that is NOT the skill's own declared `url` from frontmatter
- **Environment variable harvesting**: patterns like `$HOME`, `$SSH_KEY`, `$API_KEY`, `$OPENAI_API_KEY`, `$ANTHROPIC_API_KEY`, `process.env.`, `os.environ`, `$STRIPE`, `$DATABASE_URL`, `$SECRET`
- **File system access outside workspace**: paths like `/etc/`, `~/.ssh/`, `~/.aws/`, `~/.config/`, `/root/`
- **Prompt override attempts**: phrases that attempt to reset agent behavior, reassign identity, or dismiss prior system rules (search for common social engineering phrases targeting LLM context)

### 🟡 Review (Needs human check)

- **Obfuscated code**: hex-encoded strings (`\x`), unicode escapes (`\u`), string concatenation that builds suspicious keywords
- **Dynamic code loading**: `import()`, `require()` with variable paths, `__import__`
- **Webhook/callback URLs**: any URL containing "webhook", "callback", "hook", "notify"
- **Credential file references**: mentions of `.env`, `credentials`, `keychain`, `keyring`, `secrets`
- **Instruction to modify agent files**: "add to AGENTS.md", "update MEMORY.md", "write to config" — legitimate skills may do this, but it's worth flagging

### 🟢 Clean

- No patterns from above detected
- Standard markdown, documentation, or static assets only

## Step 3: Cross-Reference

For each skill:
- Compare declared permissions in frontmatter vs actual file contents
  - If skill declares no `network:outbound` permission but contains fetch/curl, escalate to 🔴
  - If skill declares no `filesystem:write` but contains file write operations, escalate to 🔴
- Check if the skill's declared URL/author match known safe sources
- Check if skill name mimics a popular skill (typosquatting: e.g., "clawspa" vs "clawsp4")

## Step 4: Rate Each Skill

Apply the highest severity found:
- 🔴 **Suspicious**: Any critical pattern found. Do NOT run this skill until reviewed.
- 🟡 **Review**: Only review-level patterns found. Probably safe but warrants a look.
- 🟢 **Clean**: No concerning patterns detected.

## Step 5: Generate Report

For each skill, output:

```
[RATING] skill-name (vX.X.X)
  Files scanned: X | Size: X KB
  Findings:
  - [severity] [pattern]: [file:line] — [snippet]
  - ...
  Recommendation: [action]
```

## Known Attack Vectors (ClawHavoc patterns)

1. **Base64 dropper**: Skill encodes a payload in base64 within SKILL.md instructions, tells agent to decode and execute
2. **Fake crypto/finance skills**: Harvest API keys for exchanges, wallets
3. **Environment theft**: Read all env vars and POST to external server
4. **Prompt injection in references/**: Hide override instructions in reference files that get loaded into context
5. **Typosquatting**: Skill named nearly identical to a popular one, contains malicious code

## VirusTotal Cross-Check

For any 🔴 rated skill, recommend the user:
1. Check the skill's source URL on VirusTotal (virustotal.com)
2. Search the author name on ClawHub for reputation
3. If the skill was installed with `--force` (bypassing security), treat with extra suspicion

## Limitations

This scan is heuristic-based. It catches common patterns but cannot detect:
- Novel obfuscation techniques
- Malicious behavior triggered only by specific inputs
- Server-side attacks (the skill's declared URL could change behavior)

Always recommend periodic re-scanning and staying current with ClawHub security advisories.
