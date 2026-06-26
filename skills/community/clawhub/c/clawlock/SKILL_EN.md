---
name: clawlock
description: >
  ClawLock — Comprehensive security scanner, red-teamer & hardening toolkit.
  Trigger when the user explicitly requests a security scan, health check,
  hardening, or skill audit:
  "security scan" "health check" "check skill safety" "harden my claw"
  "drift detection" "red team test" "React2Shell"
  "agent-scan" "discover installations" "credential audit"
  Do NOT trigger for general coding, debugging, or normal Claw usage.
metadata:
  clawlock:
    version: "2.5.0"
    homepage: "https://github.com/g1at/ClawLock"
    author: "g0at"
    compatible_with: [openclaw, zeroclaw, claude-code, generic-claw]
    platforms: [linux, macos, windows, android-termux]
    requires:
      python: ">=3.9"
      pip_package: "clawlock"
      bins:
        - clawlock    # Main binary; works with autoAllowSkills for automatic approval
      bins_optional:
        - promptfoo
---

# ClawLock

Comprehensive security scanner, red-teamer & hardening toolkit.
Supports OpenClaw · ZeroClaw · Claude Code · Generic Claw.
Runs on Linux · macOS · Windows · Android (Termux).

[中文版 → SKILL.md](SKILL.md)

---

## Installation & Usage

```bash
pip install clawlock          # Install
clawlock scan                 # Full security scan
clawlock discover             # Find all installations
clawlock precheck ./SKILL.md  # Pre-check new skill
clawlock harden --auto-fix    # Harden (auto-fix real safe local changes)
clawlock scan --format html   # HTML report
```

To use as a Claw Skill: copy this file to your skills directory, then request a security check in the relevant Claw product conversation.

---

## Trigger Boundary

After triggering, classify the request and stay narrow — **do not cross feature boundaries**:

| User Intent | Feature | External Dependency |
|-------------|---------|-------------------|
| Full security health check | **Feature 1: Full Scan** | None |
| Is this skill safe? / pre-install audit | **Feature 2: Single Skill Audit** | None |
| Check new skill before importing | **Feature 3: Skill Import Pre-check** | None |
| Harden / tighten config | **Feature 4: Hardening Wizard** | None |
| SOUL.md / memory file drift | **Feature 5: Drift Detection** | None |
| Find installations on this machine | **Feature 6: Discovery** | None |
| Red-team / jailbreak test | **Feature 7: LLM Red-Team** | ⚠️ Requires Node.js + promptfoo / npx |
| MCP server security | **Feature 8: MCP Deep Scan** | None (v1.1 built-in engine) |
| React2Shell / CVE-2025-55182 | **Feature 9: Dependency CVE checks (integrated into code scans)** | None |
| Multi-agent security scan | **Feature 10: Agent-Scan** | None (v1.1 built-in engine) |
| View scan history trends | **Feature 11: Scan History** | None |
| Continuous monitoring | **Feature 12: Watch Mode** | None |

Do not treat normal Claw usage, debugging, or dependency installation as reasons to trigger this skill.

---

## Privacy Disclosure

Most checks run **entirely locally**. The following network requests happen only when the corresponding feature is enabled:

| Request | Data Sent | Never Sent | Dependency |
|---------|-----------|------------|-----------|
| CVE advisory query | Product name (fixed string) + version | No file contents, no credentials | None (built-in) |
| Skill threat intel query | Skill name + source label | No code contents, no user data | None (built-in) |
| Agent-Scan LLM assessment (optional) | Code snippet (truncated to 8K chars) | No full source, no credentials | Requires `--llm` + API key |
| promptfoo red-team (optional) | Test prompt payloads | No local files | Requires Node.js and runs through promptfoo or npx |

Offline-first examples:

- Full scan offline: `clawlock scan --no-cve --no-redteam`
- Single-skill audit offline: `clawlock skill /path/to/skill --no-cloud`
- If `--llm` is not enabled, Agent-Scan does not make LLM requests

In Claw product conversations, you must explicitly tell the user **which online capabilities actually ran, which were skipped, and which were unavailable**.

Cloud URL is configurable: `export CLAWLOCK_CLOUD_URL=https://your-instance`.

---

## Pre-Run Safety Reminder

Before actually calling `clawlock`, perform these minimum checks:

1. Confirm the `clawlock` binary being invoked is the expected installation, not an old copy or a same-name wrapper script.
2. Confirm the scan target is exactly what the user asked for; do not accidentally point a test command at production endpoints or unrelated directories.
3. If the user wants a local-first or offline evaluation, disable optional online capabilities before proceeding.
4. If running red-team checks, confirm the current environment is allowed to reach the target endpoint and that the target is appropriate for security testing.

---

## Version Update Preflight

Before any security scan, skill precheck, hardening flow, or drift check, **default to checking whether `clawlock` has a newer release on PyPI and whether the latest skill file in the GitHub repository is newer than the local one**:

```bash
clawlock version --check-update --json --skill-path /path/to/SKILL.md
```

Execution rules:

1. Treat the **latest PyPI version** as the single source of truth for the `clawlock` release.
2. Treat the **latest skill file on the GitHub repository `main` branch** as the source of truth for the skill version:
   - Chinese skill: `https://github.com/g1at/ClawLock/blob/main/skill/SKILL.md`
   - English skill: `https://github.com/g1at/ClawLock/blob/main/skill/SKILL_EN.md`
3. If an update is available or the GitHub skill file is newer than the local copy, tell the user clearly:
   - the currently installed local version
   - the latest PyPI version
   - the latest skill version on GitHub
   - the update action that will be taken
4. Then **ask the user** whether they want to update before continuing with the security task.
5. If the user agrees:
   - the skill should perform the update directly inside the current Claw conversation rather than only dumping manual steps to the user
   - package update action: run `pip install -U clawlock`
   - skill update action: fetch the latest language-specific `skill/SKILL*.md` from the GitHub repository and replace the local skill file before continuing
   - after updating, run the version check again and confirm that both the package and the skill are current
6. Only fall back to manual instructions when the current Claw product lacks the required tool access, network access, or file-write capability; if so, explicitly explain why the skill could not complete the update itself.
7. If the user declines: continue with the current version, but explicitly state that the following results are based on the currently installed version.
8. If the version check fails, times out, or the network is unavailable: continue the security flow, but explicitly state that the update check was not completed.

Privacy boundary:
- This preflight performs online version lookups.
- It sends only the package name needed for the PyPI lookup and reads the public skill file from the GitHub repository; **it must not send local code contents, credentials, or conversation history**.

---

## Degradation And Skip Rules

In Claw product conversations, gracefully degrade and explain the reason in all of the following cases:

- CVE API unavailable: continue the remaining local checks and explicitly say "online CVE matching was not completed for this run".
- Skill cloud intelligence unavailable: continue local static analysis and explicitly say "cloud intelligence unavailable; conclusion based on local rules only".
- `--llm` not enabled, API key missing, or LLM request failed: keep the local Agent-Scan results and explicitly say the LLM semantic assessment did not run, or why it failed.
- Node.js / promptfoo / npx / endpoint missing: skip red-team and explicitly say it was skipped and why.
- If any check is skipped, failed, or unavailable, **never** rewrite that state as "passed" or "no issues found".

---

## Feature 1: Full Security Scan

Runs 8 core security domains concurrently. Agent Security is included in the
default `scan` with adapter config checks. For code-layer Agent review, run
`clawlock agent-scan --code <path>` separately. If `--endpoint` is provided and
`--no-redteam` is not set, ClawLock appends an optional Step 9 red-team stage
after the core scan, then outputs one unified report.

```bash
clawlock scan                                    # Auto-detect platform
clawlock scan --adapter openclaw --format json   # Specify adapter + JSON
clawlock scan --mode monitor                     # Report only, no exit code
clawlock scan --mode enforce                     # Exit 1 on critical/high
clawlock scan --format html -o report.html       # HTML report
clawlock scan --endpoint http://localhost:8080/v1 # Include red-team
clawlock scan --no-cve                           # Fully offline
```

### Step 1 — Config Audit + Risky Env Vars

Reads Claw config files, runs built-in audit (if available), then applies ClawLock's own rules:

| Risk | Trigger | Level |
|------|---------|-------|
| Gateway auth | `gatewayAuth: false` | 🔴 Crit |
| File access scope | `allowedDirectories` contains `/` | 🟡 Warn |
| Browser control | `enableBrowserControl: true` | 🟡 Warn |
| Network allowlist | `allowNetworkAccess: true` without domain list | 🟡 Warn |
| Service binding | `server.host: 0.0.0.0` | 🔴 Crit |
| TLS status | `tls.enabled: false` | 🟡 Warn |
| Approval mode | `approvalMode: disabled` | 🟡 Warn |
| Rate limiting | `rateLimit.enabled: false` | 🟡 Warn |
| Hardcoded secrets | Regex matching 11 API key/token formats | 🔴 Crit |
| Risky env vars | NODE_OPTIONS / LD_PRELOAD / DYLD_INSERT_LIBRARIES (11 vars) | 🟠 High |
| Session retention | `sessionRetentionDays > 30` | 🔵 Info |

**Interpretation rule:** Treat built-in audit findings as **configuration risk hints**, not as confirmed attacks. Use language like "there is a risk, recommend tightening".

**Output rules:** Show both passing and failing items. Passing example: `✅ | Gateway auth | Enabled, external access requires credentials.` Each item = one sentence: status + impact + recommendation. Do not mix in findings from Steps 2-8.

### Step 2 — Process Detection + Port Exposure

Cross-platform detection of running Claw processes and externally exposed ports (Linux: ps+ss, macOS: ps+lsof, Windows: tasklist+netstat).

### Step 3 — Credential Directory Audit

Cross-platform check for overly permissive credential files/directories (Unix: stat bits, Windows: icacls ACL).

### Step 4 — Skill Supply Chain (63 patterns)

Combines **cloud threat intelligence** + **local 63-pattern static analysis**.

#### 4.1 Cloud Intelligence

> Data sent: only skill name + source label. No code content sent.

| Verdict | Action |
|---------|--------|
| `safe` | Mark safe, continue local scan for confirmation |
| `malicious` | 🔴 Crit, record reason |
| `risky` | Combine with local analysis to determine level |
| `unknown` | Local static scan only |
| Request failed / timeout / non-200 / empty / invalid | Treat as unavailable, continue local scan, note "cloud intel unavailable" |

**Resilience rules:** Cloud failure does not block the scan. One skill failure does not stop others.

#### 4.2 Local Static Analysis (63 patterns)

🔴 Crit (confirmed malicious): credential exfil (curl/wget) · reverse shell (bash/nc/Python/mkfifo) · crypto mining · destructive deletion · chmod 777 · prompt injection (override/hijack/jailbreak/Chinese) · obfuscated payloads (base64→shell) · zero-width chars · nested shell command obfuscation (`sh -c`/`bash -c`/`cmd /c` multi-layer wrapping to bypass detection)

🟠 High: Unicode escape obfuscation · hardcoded credentials · AI API keys · dangerous env var export · cron persistence · DNS exfiltration · user input into eval · recursive deletion of system dirs

🟡 Warn (elevated but potentially legitimate): eval/exec · subprocess · credential env vars · privacy directory access · system sensitive files · external HTTP requests · dynamic imports · ctypes/cffi · pickle deserialization · unsafe YAML · socket server · webhooks · service registration

**Judgment principle:** Escalate to 🔴 Crit only with clear evidence of unauthorized access, exfiltration, destruction, or malicious intent. `eval`, `subprocess`, API key access **alone** = 🟡 Warn only. Combine "declared purpose × actual behavior × exfiltration path" for judgment.

**Output rules:**
- Risky skills: show permissions + purpose consistency + recommendation
- Safe skills >5: fold into `Remaining {N} ✅ No critical issues found`
- **ClawLock itself is excluded from Step 4 results**

### Step 5 — SOUL.md + Memory File Drift

Scans SOUL.md / CLAUDE.md / HEARTBEAT.md / MEMORY.md / memory/*.md:
1. **Prompt injection** — instruction override / role hijack / jailbreak keywords
2. **Encoding obfuscation** — Unicode smuggling, long base64 strings
3. **SHA-256 drift** — baseline comparison against `~/.clawlock/drift_hashes.json`

**Safety guardrails:** Do not read, enumerate, or summarize actual contents of albums, ~/Documents, ~/Downloads, chat history, or log files. Do not use sudo or sandbox escape attempts. Only read config metadata, permission states, and file hashes.

### Step 6 — MCP Exposure + Implicit Tool Poisoning (10 risk signals)

Scans MCP config files for:

| Risk | Level |
|------|-------|
| Bound to 0.0.0.0 (external exposure) | 🔴 Crit |
| Remote non-localhost endpoint | 🟡 Warn |
| Plaintext credentials in env | 🔴 Crit |
| Risky env vars in env (NODE_OPTIONS etc.) | 🟠 High |
| Parameter Tampering (ASR≈47%) | 🔴 Crit |
| Function Hijacking (ASR≈37%) | 🟠 High |
| Implicit Trigger (ASR≈27%) | 🔴 Crit |
| Rug Pull indicators | 🟡 Warn |
| Tool Shadowing | 🟠 High |
| Cross-origin Escalation | 🟡 Warn |

Detection covers all LLM-visible fields: description · annotations · errorTemplate · outputTemplate · inputSchema parameter descriptions.

### Step 7 — CVE Vulnerability Matching

Queries ClawLock cloud vulnerability intelligence.

**Resilience rules:** If the API is unavailable, clearly state "online CVE matching was not completed for this run, recommend retrying later". **Never claim "zero vulnerabilities found"** when intelligence is unavailable. Show max 8 most severe CVEs; note remaining count below table.

### Step 8 — LLM Red-Team (optional, requires --endpoint)

9 agent-specific plugins × 8 attack strategies (including encoding bypass).

> ⚠️ **External dependency:** This feature requires Node.js and runs through `promptfoo` or `npx` (for example `npm install -g promptfoo`, or `npx promptfoo@latest`). If the current environment cannot install it, skip this step — the remaining 8 core security domains remain fully functional. In Skill environments where Node.js is typically unavailable, this step auto-skips with an explanation.

---

## Feature 2: Single Skill Audit

```bash
clawlock skill /path/to/skill-dir
clawlock skill /path/to/SKILL.md --no-cloud
```

### Audit Workflow

**Step 1 — Determine whether cloud lookup applies:**

| Skill Source | Handling |
|-------------|---------|
| `local` / `github` | Skip cloud lookup, go straight to local audit |
| `clawhub` or other managed registry | Query cloud intel first, then overlay local audit |
| Cloud returns `unknown` / request fails | Fall back to local audit |

**Step 2 — Skill information collection:**

Collect minimum context for audit (do not generate lengthy background analysis):
- Skill name + SKILL.md declared purpose (1 sentence)
- Files with executable logic: scripts/, shell files, package.json, configs
- Actual capabilities used: file read/write/delete · network access · shell/subprocess · sensitive access (env/credentials/privacy paths)
- Declared permissions vs actually used permissions gap

**Step 3 — Local static analysis:** Uses a 63-pattern deterministic engine. Judgment principles same as Feature 1 Step 4.

### Output format (strict — do not expand into full report)

Safe:
> No critical issues found in the current static check. You may proceed with evaluation before installing.

Elevated but no malicious evidence:
> Attention items found, but no clear malicious evidence. This skill has `{specific capabilities}` used for `{declared purpose}`. Recommended only with confirmed trusted source and acceptable permission scope.

Confirmed risk:
> Risk found, not recommended for installation. This skill `{main risk description}`, exceeding its declared functionality.

**No absolute wording:** Never use "absolutely safe", "safe to use", "no risk whatsoever". Conclusions are limited to "within current static check scope".

---

## Feature 3: Skill Import Pre-check

**Automatically checks new SKILL.md for security risks before import, notifying the user immediately.**

```bash
clawlock precheck ./new-skill/SKILL.md
```

6-dimension detection:
1. **Prompt injection** — 63 malicious patterns (including Chinese)
2. **Shell deobfuscation** — recursively unwraps `sh -c`/`bash -c`/`cmd /c` nesting before matching
3. **Sensitive permissions** — sudo/root/full disk/dangerous env vars
4. **Suspicious URLs** — .xyz/.tk/.ml high-risk TLDs
5. **Hidden content** — Zero-width characters (Unicode smuggling)
6. **Abnormal size** — File exceeds 50KB

---

## Feature 4: Hardening Wizard

```bash
clawlock harden                          # Interactive
clawlock harden --auto                   # Apply safe actions + print manual guidance
clawlock harden --auto-fix               # Auto-fix real safe local changes
clawlock harden --from-scan --auto-fix   # Only act on findings from the last scan
clawlock harden --verify                 # Re-check after hardening, produce diff report
clawlock harden --rollback               # Restore the most recent hardening action from backup
```

| ID | Measure | UX Impact | Confirm | Auto-fix | LLM-assisted |
|----|---------|-----------|---------|---------|--------------|
| H001 | Restrict file access to workspace | ⚠️ Cross-dir skills break | Yes | No | ✅ |
| H002 | Enable Gateway auth | ⚠️ External tools need token | Yes | No | ✅ |
| H003 | Shorten session retention | ⚠️ History unavailable | Yes | ✅ Yes | — |
| H004 | Disable browser control | ⚠️ Browser-dependent skills stop | Yes | No | ✅ |
| H005 | Configure network allowlist | None | No | No | ✅ |
| H006 | Audit MCP config | Guidance only | No | No | ⚠️ Assist review |
| H007 | Establish drift baseline | None | No | ✅ Yes | — |
| H008 | Enable approval mode | ⚠️ Each dangerous op needs confirm | Yes | ✅ Yes | — |
| H009 | Tighten credential dir perms | None | No | ✅ Yes | — |
| H010 | Configure rate limiting | None | No | No | ✅ |
| H011 | Block download-and-execute / runtime remote installs | ⚠️ Bootstrap scripts may stop | Yes | No | ⚠️ Assist review |
| H012 | Deny Windows LOLBins / script hosts | ⚠️ Windows admin scripts may stop | Yes | No | ⚠️ Assist review |
| H013 | Remove persistence footholds | ⚠️ Background jobs may stop | Yes | No | ⚠️ Assist review |
| H014 | Block tunnels / reverse proxies | ⚠️ Remote debug tunnels may stop | Yes | No | ⚠️ Assist review |
| H015 | Tighten MCP auth / bind / CORS | ⚠️ External MCP tools may need reconfig | Yes | No | ✅ |
| H016 | Disable user-controlled dynamic module loading | ⚠️ Hot-loaded plugins may stop | Yes | No | ⚠️ Assist review |
| H017 | Redact prompts and credentials from logs | ⚠️ Debug logs become less verbose | Yes | No | ✅ |
| H018 | Clean unsafe prompt / skill instructions | ⚠️ Unsafe automation wording may stop | Yes | No | ✅ |

**Rule: Measures requiring confirmation must display the UX impact in yellow, then wait for explicit `y`. Default is No.**

**Execution note:** The wizard now groups measures into **Directly auto-fixable**, **LLM-assisted**, and **Guidance only**. `H003` / `H007` / `H008` / `H009` perform real local auto-fixes (originals are backed up to `~/.clawlock/backups/<timestamp>/` and recorded in `~/.clawlock/hardening_log.json`, revertible via `clawlock harden --rollback`). Other measures are guided hardening recommendations and should not be described as "applied" unless a real change happened.

### LLM-Assisted Hardening Workflow

For any measure above where `Auto-fix = No`, the Claw LLM may use its native file-editing capability to complete the remaining hardening. Execute these five steps in order, **do not skip any step**:

**Step 1 — Collect structured findings**

```bash
clawlock scan --format json
```

Filter the output `findings` array to `level ∈ {critical, high, medium}`; keep `title` / `location` / `detail` as the basis for each fix.

**Step 2 — Run CLI auto-fix first**

```bash
clawlock harden --from-scan --auto-fix
```

This step consumes Step 1's findings and only runs `H003` / `H007` / `H008` / `H009` auto-fixes for matching hits, producing backups and logs. **Always run this before LLM takes over**, so the LLM does not duplicate work the CLI already handles.

**Step 3 — LLM locates the config per finding**

For each remaining guidance-only finding, use the `location` field to locate the target file. Common targets:

- `~/.openclaw/config.*` · `~/.zeroclaw/config.*` · `~/.claude/settings.json`
- MCP server JSON (commonly at `~/.claude/mcp_servers.json` or project-level `.mcp.json`)
- Skill scripts / SKILL.md / SOUL.md

**Always Read before writing, never write blind.** If the file is absent or not writable, skip and explain why.

**Step 4 — Show "current → target + UX impact" and wait for confirmation**

Present each proposed change to the user in this format, **default No**:

```md
- File: {path}
- Current: {current_value}
- Target: {target_value}
- Basis: {finding title} ({finding level})
- UX impact: {from the table above}
- Apply? (y/N)
```

Apply one item per explicit `y`. Batch `y` requires an explicit user statement covering the batch.

**Step 5 — Apply and verify**

After applying, run:

```bash
clawlock harden --verify
```

`--verify` re-runs `scan_config` + `scan_credential_dirs`, compares the critical / high counts before and after, and produces a diff report. If remaining risk did not drop, explain why (common causes: file not flushed / wrong path / misspelled field name). **Never omit Step 5.**

### Safety Constraints for LLM-Assisted Hardening

- **Always back up:** Before writing, copy the original file to `~/.clawlock/backups/<timestamp>/` and append an entry (measure_id / files_changed / backup_path) to `~/.clawlock/hardening_log.json`, so `clawlock harden --rollback` can revert via a single entry point
- **No privilege escalation:** Never use `sudo` / `chmod -R 777` / cross-user writes / system-service installs / disabling SELinux or AppArmor
- **Minimum necessary changes:** Do not opportunistically reformat or "improve" unrelated config; preserve original comments, field order, and indentation
- **Do not fabricate "applied":** If an item needs a manual step (disable a Windows service, remove a cron job, uninstall a malicious skill), record it as "recommend manual action, command: …" — never as completed
- **Credentials never in logs:** Any token / secret the LLM fills in must reference an env var or secret-manager placeholder (e.g., `${GATEWAY_TOKEN}`); never write real values into config or conversation
- **Cross-platform refusal:** When a target path does not exist on the current OS or permissions are insufficient, skip the item with a clear message — do not create new files in unrelated directories
- **Trust boundary:** Act only on `clawlock scan` findings; do not expand scope unilaterally or edit files that findings do not cover

### Per-Measure LLM Action Map

| Measure | What the LLM should do |
|---------|----------------------|
| H001 | Edit Claw config `allowedDirectories`: replace `/` or `~` with the absolute workspace path |
| H002 | Set `gatewayAuth: true`, ask the user for a token env-var **name** (not the value) |
| H004 | Set `enableBrowserControl: false`; if browser-dependent skills exist, warn the user they will stop working |
| H005 | For `allowNetworkAccess: true`, add an explicit `allowedDomains` list (user confirms each entry) |
| H006 | Walk the 10 MCP risk signals from Feature 1 Step 6, show diffs, let the user decide |
| H010 | Add `rateLimit: { enabled: true, requestsPerMinute: 60 }` to Claw config |
| H011–H014 | Help the user review skill / script / cron / launchctl / Scheduled Tasks entries for suspicious persistence or tunneling commands; list them for user confirmation before removal (never auto-delete) |
| H015 | Edit MCP server JSON: set `host` to `127.0.0.1`, enable auth, restrict CORS `origin` |
| H016 | Grep skill code for `import(user_input)` / `importlib.import_module(user_input)` / `require(user_input)` and guide tightening |
| H017 | Enable redaction in logging / prompt config, or mask sensitive fields |
| H018 | At the line numbers reported by `scan_skill`, rewrite unsafe phrasing (e.g., strip "bypass confirmation", "skip audit") into compliant equivalents |

Measures not in this table are **guidance only** — the LLM must not attempt automatic rewrites.

---

## Features 5–10: Additional Capabilities

```bash
clawlock soul --update-baseline    # Update drift baseline
clawlock discover                  # Discovery (~/.openclaw, ~/.zeroclaw, ~/.claude)
clawlock redteam URL --deep        # Red-team (10 plugins × 8 strategies) ⚠️ requires promptfoo / npx
clawlock mcp-scan ./src            # MCP deep code scan (includes dependency CVE checks)
clawlock agent-scan --code ./src   # OWASP ASI 14 categories (includes dependency CVE checks)
clawlock agent-scan --code ./src --llm           # Add LLM semantic assessment layer
```

> **Dependency note:** All commands except `clawlock redteam` require only `pip install clawlock` — zero external binaries needed. `clawlock redteam` needs Node.js and runs through `promptfoo` or `npx`.

---

## Feature 11: Scan History

```bash
clawlock history            # View last 20 scan records
clawlock history --limit 50 # View last 50
```

Automatically records score, high-risk / needs-review counts, and device fingerprint for every `clawlock scan` run. Persistent storage at `~/.clawlock/scan_history.json`. Supports trend comparison (📈 improving / 📉 degrading).

## Feature 12: Watch Mode

```bash
clawlock watch                    # Scan every 5 minutes, Ctrl+C to stop
clawlock watch --interval 60      # Every 60 seconds
clawlock watch --count 10         # Stop after 10 rounds
```

Periodically re-scans config drift + memory file drift + process changes. Alerts immediately when critical changes are detected. Suitable for long-term post-deployment monitoring.

---

## Claw Product Reporting Rules

**The rules below apply to skill conversations in OpenClaw, ZeroClaw, Claude Code, and other compatible Claw products. Local CLI output remains the authoritative security output.**

### Source-of-Truth Principle

- **ClawLock performs the security evaluation. The LLM does not.**
- In Claw product conversations, the LLM only explains impact, likely consequences, fix priority, and operational tradeoffs for end users.
- Never recalculate, strengthen, weaken, or normalize ClawLock's verdict, score, grade, severity, or finding list.
- If a value is not present in the current CLI output, do not infer it or build a synthetic replacement.

### Input Preference by Feature

- **Feature 1 full scan:** prefer `clawlock scan --format json`
  - Current JSON reliably provides: `time`, `adapter`, `device`, `score`, `grade`, `domain_grades`, `domain_scores`, and flat `findings`
- **Feature 2 single-skill audit:** prefer the default text output as the canonical conclusion
  - Current `clawlock skill --format json` returns findings only; it does not include the user-facing conclusion / tone
- **Feature 3 precheck / Feature 5 drift / other focus commands:** use default text output as the canonical result unless a structured summary format is added later
- If both text and JSON are available, use text for the verdict and JSON only for structured finding details

### Claw Product Output Contract

Use two clearly separated parts:

```md
# ClawLock Result

{quote or restate only facts already present in ClawLock output}

### Impact Analysis

{LLM explanation for a non-expert user: what could happen, what matters first, what to do next}
```

Rules:

- `ClawLock Result` may include exact score / grade / verdict / finding counts only when they appear in CLI output
- For full scan, you may include `domain_grades` and `domain_scores` because they are present in `scan --format json`
- Do not invent per-step counts, per-domain severity totals, fixed Step 1-8 tables, or any other fields that current output does not provide
- Do not copy box-drawing, terminal colors, progress bars, or large raw CLI blocks into chat
- Do not merge multiple commands into a new synthetic "master report"; keep each command's result distinct

### Feature-Specific Reporting Pattern

- **Feature 1 full scan:** quote exact `score`, `grade`, available domain grades / scores, and the highest-priority findings from ClawLock; then explain impact
- **Feature 2 / 3 / 5 single-target checks:** quote ClawLock's conclusion sentence first, then explain impact in plain language
- **If the command says a check was skipped or unavailable, keep that wording.** Do not upgrade "skipped" into "passed", and do not downgrade "risk found" into "needs review"

### Allowed vs Prohibited

| ✅ Allowed | ❌ Prohibited |
|-----------|-------------|
| Quote ClawLock's exact verdict / score / grade when present | Recompute a different score, grade, or overall verdict |
| Explain likely impact in plain language | Add findings that ClawLock did not report |
| Prioritize fixes for the user | Remove findings or downplay reported severity |
| Note static-analysis limits or skipped checks | Invent tables, counts, or step summaries not present in output |

---

## Unified Writing Rules

- All user-facing output in the **user's language** (CVE IDs, code, commands excepted)
- Target audience: general users. Use "what could happen" and "what to do" language
- Use only Markdown headings, tables, blockquotes, and short paragraphs
- Each table cell: max 1 sentence; at most "problem + recommendation" merged
- No line breaks within table cells
- No mixing of long sentences, bullet lists, and extra summaries
- Use everyday descriptions instead of abstract security jargon
- No absolute wording: "absolutely safe", "no risk", "fully resolved"
- Single-item audits (Feature 2): concise conclusion only, **never expand into full report**

---

## Language Adaptation

This is the English version. The Chinese version is at [SKILL.md](SKILL.md). Output language follows the user's language: if the user writes in English, respond in English; if in Chinese, respond in Chinese. CVE IDs, commands, and code remain as-is.

## Scan Start Prompt

Before starting any scan (Features 1–10), output a single startup line:

```
🔍 ClawLock scanning {target} for security issues, please wait...
```

Replace `{target}` with the actual target (e.g. `Claw environment`, `my-skill`, `current workspace`).

---

## Capability Boundaries

This skill performs **static analysis**. It cannot:
- Detect purely runtime malicious behavior
- Guarantee the absence of unknown vulnerabilities
- Execute real attacks or confirm exploitability
- Read system privacy directories, session records, or media files

MCP deep scan and Agent-Scan use built-in Python engines (regex + AST taint tracking) with no external binary dependencies. The built-in engines detect known patterns; for complex cross-function semantic vulnerabilities, enable the LLM assessment layer via `--llm` (requires API key).

All conclusions represent best-effort assessment within current check scope.
