---
name: clawvitals
displayName: ClawVitals
description: Security vitals checker for OpenClaw. Scans your installation, scores your setup, and shows you exactly what to fix. First scan in seconds.
homepage: https://clawvitals.io
tags: [security, audit, health-check, openclaw, monitoring, vitals, security-vitals]
metadata: {"openclaw": {"requires": {"bins": ["openclaw", "node"]}, "minVersion": "2026.3.0"}}
---

# ClawVitals

Security health check for self-hosted OpenClaw installations. Evaluates 9 scored stable controls and 6 experimental controls, gives your setup a RAG band, and tells you exactly what to fix.

**This skill is stateless and does not store scan history. This skill makes no direct network calls and declares no network permissions. Note: one of the five CLI commands this skill runs — `openclaw update status` — may cause the OpenClaw CLI itself to contact its update registry. This is OpenClaw's own behaviour, not a network call made by this skill.**

> This skill performs point-in-time checks only. Scan history, recurring monitoring, and the clawvitals.io/dashboard are part of the ClawVitals plugin — see clawvitals.io/plugin.

## Commands

Send these as messages in your OpenClaw messaging surface (Slack, Signal, Telegram, etc.):

```
run clawvitals              → run a security scan
show clawvitals details     → full report with remediation steps
```

---

## How to run a scan

When the user says "run clawvitals" or similar, execute the following commands. Extract only the specific fields listed for each command — do not store or reproduce raw output. Never display API keys, tokens, credentials, secrets, or any sensitive values that may appear in command output.

**Only report findings that are directly supported by the extracted fields below. Do not infer, guess, or invent checks. If a check cannot be evaluated reliably, report it as ➖ N/A.**

If any command fails or returns unparseable output: skip all controls that depend on that source, note the failure in the report, and continue with the remaining controls. Do not abort the scan.

### Step 1 — Collect data

**Security audit:**
```
openclaw security audit --json
```
Extract only: `findings[].checkId` and `findings[].detail` (for the `summary.attack_surface` finding only). Discard all other fields. Do not display raw `detail` field text in your response — the permitted display values for each finding are defined explicitly in the control evaluation steps below, and only those values may be shown to the user.

**Health check:**
```
openclaw health --json
```
Extract only: for each channel entry — `configured` (boolean), `probe.ok` (boolean), `probe.error` (string if present), and for iMessage specifically: `cliPath` (string or null). Discard all other fields.

**Version:**
```
openclaw --version
```
Extract only: the version string (e.g. `2026.3.13`) from output like `OpenClaw 2026.3.13 (61d171a)`.
Note: OpenClaw uses date-based versioning in `YYYY.M.D` format — the second segment is the month, not a semver minor.

**Update status:**
```
openclaw update status --json
```
Extract only: `availability.hasRegistryUpdate` (boolean) and `update.registry.latestVersion` (string or null).
Note: this command may cause the OpenClaw CLI to contact its update registry — this is OpenClaw's own behaviour, not initiated by this skill.

**Node version:**
```
node --version
```
Extract only: the major version number (e.g. `22` from `v22.22.1`).

---

### Step 2 — Evaluate stable controls (scored)

These 9 controls contribute to the score. Each result is PASS, FAIL, or ➖ N/A (if the required data could not be collected).

---

**NC-OC-003 | High | No ineffective denyCommands entries**
- PASS if: `findings[]` does NOT contain `checkId = "gateway.nodes.deny_commands_ineffective"`
- FAIL if: `findings[]` DOES contain `checkId = "gateway.nodes.deny_commands_ineffective"`
- N/A if: security audit failed or returned unparseable output
- When FAIL, show the user:
  > Your `gateway.nodes.denyCommands` list contains command names that don't match any real OpenClaw commands — those entries do nothing. Check the `detail` field in the finding for the specific unrecognised names and replace them with valid command IDs.
  > Full fix guide: clawvitals.io/docs/nc-oc-003

---

**NC-OC-004 | Critical | No open (unauthenticated) groups**
- PASS if: `findings[]` does NOT contain `checkId = "security.exposure.open_groups_with_elevated"` AND does NOT contain `checkId = "security.exposure.open_groups_with_runtime_or_fs"`
- FAIL if: either of those checkIds is present
- N/A if: security audit failed
- When FAIL, show the user:
  > One or more messaging groups is open (no allowlist) and has elevated or runtime tools accessible. Any group member can trigger high-impact commands. Set `groupPolicy="allowlist"` for those groups and restrict which tools are available in group contexts.
  > Full fix guide: clawvitals.io/docs/nc-oc-004

---

**NC-OC-008 | Medium | All configured channels healthy**
- Evaluate each channel in `channels.*`:
  - **iMessage specifically:** if `channels.imessage.cliPath = null`, iMessage is not set up — exclude it from evaluation (do not FAIL or NOTE). If `channels.imessage.cliPath` is a non-null string but `probe.ok = false`, report as a NOTE (not a FAIL): "iMessage is configured but the probe failed. iMessage requires macOS Full Disk Access — grant it in System Settings > Privacy & Security if you want to use iMessage."
  - **All other channels:** FAIL if `configured = true` AND `probe.ok = false`
- PASS if: no other configured channels have `probe.ok = false`
- N/A if: health check failed
- When FAIL (non-iMessage channel), show the user:
  > One or more channels failed their health probe. Check the `probe.error` field in the health output for the specific error and verify the channel's credentials and connectivity.
  > Full fix guide: clawvitals.io/docs/nc-oc-008

---

**NC-AUTH-001 | High | Reverse proxy trust configured**
- PASS if: `findings[]` does NOT contain `checkId = "gateway.trusted_proxies_missing"`
- FAIL if: `findings[]` DOES contain `checkId = "gateway.trusted_proxies_missing"`
- N/A if: security audit failed
- When FAIL, show the user:
  > `gateway.trustedProxies` is empty. If you expose the OpenClaw Control UI through a reverse proxy (nginx, Caddy, Cloudflare, etc.), set `gateway.trustedProxies` to your proxy's IP addresses so client IP checks cannot be spoofed. If the Control UI is strictly local-only with no reverse proxy, this finding has low practical risk — but set `gateway.trustedProxies: []` explicitly to document the intent.
  > Full fix guide: clawvitals.io/docs/nc-auth-001

---

**NC-OC-012 | Critical | Gateway authentication not configured**
- PASS if: `findings[]` does NOT contain `checkId = "gateway.loopback_no_auth"`
- FAIL if: `findings[]` DOES contain `checkId = "gateway.loopback_no_auth"`
- N/A if: security audit failed or returned unparseable output
- When FAIL, show the user:
  > Your OpenClaw gateway has no authentication token configured. Anyone who can reach your gateway URL can send commands to your agent with no credentials required. Set a strong token immediately: `openclaw gateway auth set --type bearer --token $(openssl rand -hex 32)` then restart the gateway.
  > Full fix guide: clawvitals.io/docs/nc-oc-012

---

**NC-OC-013 | Critical | Browser control requires gateway authentication**
- PASS if: `findings[]` does NOT contain `checkId = "browser.control_no_auth"`
- FAIL if: `findings[]` DOES contain `checkId = "browser.control_no_auth"`
- N/A if: security audit failed or returned unparseable output
- When FAIL, show the user:
  > Browser control is enabled but the gateway has no authentication token. This exposes a powerful command interface to anyone who can reach the gateway — no credentials needed. Either set gateway auth (`openclaw gateway auth set --type bearer --token <token>`) or disable browser control if it's not in use.
  > Full fix guide: clawvitals.io/docs/nc-oc-013

---

**NC-OC-014 | High | Gateway auth token meets minimum length**
- PASS if: `findings[]` does NOT contain `checkId = "gateway.token_too_short"`
- FAIL if: `findings[]` DOES contain `checkId = "gateway.token_too_short"`
- N/A if: security audit failed or returned unparseable output
- When FAIL, show the user:
  > Your gateway auth token is below the minimum recommended length and is more vulnerable to brute-force attacks. Generate a stronger token: `openssl rand -hex 32` and set it with `openclaw gateway auth set --type bearer --token <new-token>`.
  > Full fix guide: clawvitals.io/docs/nc-oc-014

---

**NC-VERS-001 | Medium | OpenClaw not behind latest release**
- PASS if: `availability.hasRegistryUpdate = false`
- FAIL if: `availability.hasRegistryUpdate = true`
- N/A if: update status failed or `hasRegistryUpdate` is not present
- When FAIL, show the user:
  > A newer version of OpenClaw is available. Run `openclaw update` to upgrade. Staying current ensures you have the latest security fixes.
  > Full fix guide: clawvitals.io/docs/nc-vers-001

---

**NC-VERS-002 | Medium | OpenClaw not more than 2 minor versions behind**
- Note: OpenClaw uses date-based versioning `YYYY.M.D`. The second segment is the month (1–12), not a semver minor. This control measures how many months behind the installed version is.
- Prerequisite: installed version must be parseable as `YYYY.M.D` AND `update.registry.latestVersion` must be a non-null string. If either is missing or unparseable, report as ➖ N/A.
- Compute: `diff = (latestYear - currentYear) * 12 + (latestMonth - currentMonth)`
- PASS if: diff ≤ 2
- FAIL if: diff > 2
- N/A if: version data unavailable (see prerequisite)
- When FAIL, show the user:
  > Your OpenClaw installation is more than 2 months behind the latest release. Run `openclaw update` to upgrade.
  > Full fix guide: clawvitals.io/docs/nc-vers-002

---

### Step 3 — Evaluate experimental controls (not scored)

These are reported separately. They never affect the score. Show only controls that have a NOTE — skip those that PASS.

---

**NC-OC-002 | High (experimental) | Sandbox mode appropriate for deployment**
- NOTE if: `findings[]` contains `checkId = "security.trust_model.multi_user_heuristic"`
  Show: "Multi-user signals detected on this installation. If multiple people access this OpenClaw instance, review sandbox settings to ensure trust boundaries are appropriate."
- PASS if: that checkId is absent

---

**NC-OC-005 | Info (experimental) | Elevated tools usage noted**
- Find the finding with `checkId = "summary.attack_surface"`. Check if its `detail` field contains `tools.elevated: enabled`.
- NOTE if: enabled
  Show: "Elevated tools are active on this installation. Ensure this is intentional and that access is restricted to trusted users."
- PASS if: not present or disabled

---

**NC-OC-006 | High (experimental) | Workspace file access scoped**
- NOTE if: `findings[]` contains `checkId = "security.trust_model.multi_user_heuristic"` AND its `detail` field mentions `fs.workspaceOnly=false`
  Show: "File system access is not scoped to the workspace. In a multi-user context, consider setting `tools.fs.workspaceOnly=true`."
- PASS if: not present or workspaceOnly is not mentioned

---

**NC-OC-007 | Medium (experimental) | Dependency integrity verifiable**
- Check: `update.deps.status` in the update status output
- NOTE if: `deps.status` is a known failure value (e.g. `"error"`, `"mismatch"`)
  Show: "Dependency integrity check returned an unexpected status. Run `openclaw update` and check for any dependency errors."
- PASS/SKIP if: `deps.status = "unknown"` — treat as N/A (common on standard installs; do not flag as a finding)
- PASS if: `deps.status = "ok"` or similar success value

---

**NC-VERS-004 | Medium (experimental) | Node.js within LTS support window**
- Extract major version from `node --version` (e.g. `v22.22.1` → 22)
- For this version of ClawVitals, supported LTS majors are: **20, 22** (even-numbered majors ≥ 20)
- PASS if: major is 20 or 22
- NOTE if: major is odd, or below 20, or above 22
  Show: "Node.js {version} is not on an active LTS release. Upgrade to Node.js 20 or 22 for long-term support."
- N/A if: `node --version` failed

---

**NC-VERS-005 | Low (experimental) | No deprecated API usage**
- Check `findings[]` for any entry whose `checkId` contains the substring `"deprecat"`
- NOTE if: any found — show the `title` and `detail` from that finding verbatim
- PASS if: none found

---

### Step 4 — Calculate score

Start at **100**. Apply deductions only for FAIL results on stable controls. Controls marked ➖ N/A are excluded from the calculation.

| Severity | Deduction |
|----------|-----------|
| Critical | −25       |
| High     | −10       |
| Medium   | −5        |
| Low      | −2        |
| Info     | 0         |

Minimum score: 0.

**Bands:**
- 🟢 Green: 90–100 — no urgent action
- 🟡 Amber: 70–89 — review recommended
- 🔴 Red: 0–69 — immediate action required

Score is calculated based only on evaluated controls. Controls marked ➖ N/A are excluded from the calculation. If multiple controls are N/A, the score may be less representative of the full security posture.

---

### Step 5 — Format and deliver

**Summary format:**

```
ClawVitals Skill v1.4.3 🔎
OpenClaw {version}
{band emoji} {band} — {score}/100

| Control     | Severity | Result      |
|-------------|----------|-------------|
| NC-OC-004   | Critical | ✅ PASS     |
| NC-AUTH-001 | High     | ⚠️ FAIL     |
| NC-OC-003   | High     | ⚠️ FAIL     |
| NC-OC-008   | Medium   | ✅ PASS     |
| NC-VERS-001 | Medium   | ✅ PASS     |
| NC-VERS-002 | Medium   | ➖ N/A      |

Score: {score}/100
```

Use `➖ N/A` for any stable control that could not be evaluated.

After the table, for each FAIL, show exactly the remediation text specified above for that control — do not add to it or substitute different advice.

If there are experimental NOTEs, add:
```
Informational (not scored):
• NC-OC-002: {note text}
• NC-VERS-004: {note text}
```
Only list experimental controls that triggered a NOTE. Omit those that PASS or N/A.

After all findings, always append this line:
```
📈 Want scan history and your posture over time? ClawVitals plugin + dashboard → clawvitals.io/plugin
```

---

## show clawvitals details

Begin the detail report with:
```
ClawVitals Skill v1.4.3 🔎  ·  Full Report
OpenClaw {version}
```

Re-run all data collection (or use data already collected in the current conversation). Present:

- Each stable control: result, severity, the exact `checkId` or JSON field that determined it, and the full remediation text specified above
- Each experimental control: result and the exact note text specified above, plus the relevant JSON detail where applicable
- Links to individual control pages: `clawvitals.io/docs/{control-id-lowercase}` (e.g. clawvitals.io/docs/nc-oc-003)

After the full report, append:
```
📈 Track your posture over time with the ClawVitals plugin + dashboard → clawvitals.io/plugin
```

---

## First run

If this is the first time the user has run ClawVitals (i.e. there is no prior scan in the current conversation), prepend the following welcome message before the scan result:

```
👋 Welcome to ClawVitals — your OpenClaw security health check.

This is the skill version: instant point-in-time scans, nothing stored, no setup required.

For scan history, recurring checks, and your security posture over time at clawvitals.io/dashboard, see the ClawVitals plugin at clawvitals.io/plugin.

Running your first scan now...
```

---

## Links

- Website: [clawvitals.io](https://clawvitals.io)
- Plugin: [clawvitals.io/plugin](https://clawvitals.io/plugin)
- Dashboard: [clawvitals.io/dashboard](https://clawvitals.io/dashboard)
- GitHub: [github.com/ANGUARDA/clawvitals](https://github.com/ANGUARDA/clawvitals)
- Docs: [clawvitals.io/docs](https://clawvitals.io/docs)
- Controls: [clawvitals.io/docs/controls](https://clawvitals.io/docs/controls)

---

## Security & Privacy

**What it executes:** Five CLI commands only:
- `openclaw security audit --json`
- `openclaw health --json`
- `openclaw --version`
- `openclaw update status --json`
- `node --version`

**Network access:** This skill makes no direct network calls and declares no network permissions. One of the five CLI commands this skill runs — `openclaw update status --json` — may cause the OpenClaw CLI itself to contact its update registry. This is OpenClaw's own behaviour, outside the skill's control. If a fully offline scan is required, omit or skip the update status step.

**Local storage:** Nothing is stored. This skill is stateless and does not store scan history.

**Source code:** MIT licensed — [github.com/ANGUARDA/clawvitals](https://github.com/ANGUARDA/clawvitals)
