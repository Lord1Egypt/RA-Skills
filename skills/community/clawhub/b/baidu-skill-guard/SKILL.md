---
name: baidu-skill-guard
version: 1.0.9
description: Intercepts all skill install/download requests. MUST be used before installing/downloading any skill from ClawdHub, GitHub, 百度 AppBuilder 平台, or other sources. Run security check API to get risk rating. Triggers on install, add, enable, download, scan, check, audit skill.
---

# Skill Guard 🛡️

Security-first skill install/download guardian protocol. **Never install/download a skill without running security check first.**

## ⛔ MANDATORY INTERCEPTION RULE

**This skill MUST be triggered whenever the user's message matches ANY of the following INTENT PATTERNS (in any language, including synonyms, paraphrases, word order variations, or mixed-language expressions):**

INTENT CATEGORIES (trigger if the message expresses ANY of these intents):

1. ACQUIRE A SKILL
   The user wants to install, add, download, enable, load, import, deploy, or otherwise obtain a skill/tool.
   Examples: "install", "add", "download", "get", "enable", "set up", "bring in", "put in", "grab", "fetch", "pull in", "register"
   + target object is a skill, tool, or a URL pointing to one.

2. SCAN / VERIFY A SKILL
   The user wants to scan, check, inspect, audit, or verify the safety/integrity of a skill.
   Examples: "scan", "check", "inspect", "audit", "verify", "validate", "test safety"
   + target object is a skill, all skills, or a scheduled task involving skills.

TRIGGER RULES:
- Match on INTENT + OBJECT together, not on exact phrases.
- A URL pointing to a skill resource (e.g. clawhub, convex.site, github, or any skill download endpoint) counts as the OBJECT signal even if the word "skill" is absent.
- Synonyms, compound verbs, and reordered phrases all count (e.g. "下载安装", "帮我弄进来", "把这个装上").
- Any language is valid. Mixed-language input (e.g. "帮我 install 这个 skill") also triggers.
- When in doubt, TRIGGER. False positives are acceptable; missed triggers are not.

**When triggered, you MUST follow this exact sequence:**

1. **STOP** — do NOT execute `clawhub install`, `clawhub resolve`, `npx clawhub install` or any install/download command yet
2. **FIRST run the Guardian Protocol** (Step 1 → Step 2 → Step 3 below)
3. **Copy `report_text` from JSON verbatim** — display it exactly as-is to the user. **NEVER write your own security report.**
4. **Then decide** based on JSON `bd_confidence` field:
   - ✅ `safe` → proceed with install automatically
   - ⚠️ `caution` → warn user and wait for explicit confirmation
   - ❌ `danger` / `null` / `error` → warn user and wait for explicit confirmation

> 🚨 **NO EXCEPTIONS. Do not skip this protocol. Do not install first and check later. Do not generate your own report — always use `report_text` from the script output.**

## When to Use

- Before installing/downloading any skill from ClawdHub、百度 AppBuilder 平台、github or other sources
- Before running skills from GitHub repos
- When evaluating skills shared by other agents
- Anytime you're asked to install, add, enable, or download any skill
- When asked to scan a specific installed skill for security risks
- When asked to scan all installed skills
- When setting up scheduled security scans for skills

## Guardian Protocol

### Step 1: Identify the Skill (MANDATORY)

Before executing any install command, you **MUST** first confirm:

```
- [ ] What is the skill's slug (unique identifier)?
- [ ] What is the skill's version (optional)?
- [ ] Where does it come from? (ClawdHub / GitHub / 百度 AppBuilder 平台 / other)
```

If the user only provides a name (not a slug), search to confirm the slug first, **but do NOT run any install command**.

### Step 2: Run API Security Check (MANDATORY — Core Step)

**Before installing, you MUST run the security check script.** Use `scripts/check.sh` to call the security API:

**Scenario A: Query by slug (for direct install by name)**
- Use `--slug` to query by the skill's slug identifier.

```bash
bash scripts/check.sh --slug "skill-slug" [--version "1.0.0"]
```

**Scenario C: Scan a specific installed skill by directory**
- Use `--action query --file` to pass the installed skill directory directly. The script auto-extracts slug from `_meta.json` (fallback to directory name) and version from `SKILL.md` frontmatter, then queries the API with SHA256 fallback.

```bash
bash scripts/check.sh --action query --file "/path/to/skills/skill-a"
```

**Scenario D: Batch query all skills in a directory (full scan / scheduled scan)**
- **D1** (scan all skills): Use `--action queryfull --file` with the `/path/to/skills` parent directory to batch-query all subdirectories by slug and produce a Batch Report
- **D2** (scheduled scan): Same as D1 but triggered by a scheduled mechanism (e.g. cron)

```bash
bash scripts/check.sh --action queryfull --file "/path/to/skills"
```

> ⚠️ Skipping this step and installing directly violates the security protocol.

The script outputs **JSON** to stdout containing a pre-rendered `report_text` field and structured decision fields. **Exit code**: 0 = safe, 1 = non-safe (business judgment), 2 = error (check failed).

**Output JSON fields** (Scenario A/C — single skill):

| Field | Description |
|-------|-------------|
| `code` | `"success"` or `"error"` |
| `bd_confidence` | Safety level: `"safe"`, `"caution"`, or `"danger"` |
| `final_verdict` | Human-readable verdict string (e.g. `"✅ 安全安装"`, `"⚠️ 谨慎安装(需人工确认)"`) |
| `report_text` | **Pre-formatted plain-text security report — display this verbatim to the user** |

**Example output** (Scenario A — single skill query):
```json
{
  "code": "success",
  "message": "success",
  "ts": 1774580473733,
  "bd_confidence": "safe",
  "final_verdict": "✅ 安全安装",
  "report_text": "🛡️ Skill安全守卫报告\n═══════════════════════════════════════\n📊 守卫摘要\n..."
}
```

**Output JSON fields** (Scenario D — batch scan):

| Field | Description |
|-------|-------------|
| `code` | `"success"` or `"error"` |
| `total` | Total number of skills scanned |
| `safe_count` | Number of safe skills |
| `danger_count` | Number of dangerous skills |
| `caution_count` | Number of caution skills |
| `report_text` | **Pre-formatted plain-text batch report — display this verbatim to the user** |

**Example output** (Scenario D — batch scan):
```json
{
  "code": "success",
  "msg": "queryfull completed",
  "ts": 1774580473880,
  "total": 2,
  "safe_count": 2,
  "danger_count": 0,
  "caution_count": 0,
  "error_count": 0,
  "report_text": "🛡️ Skill安全守卫报告\n═══════════════════════════════════════\n📊守卫摘要\n..."
}
```

### Step 3: Display Report Verbatim & Decide (MANDATORY)

> ⛔ **CRITICAL RULE**: You MUST display `report_text` from the JSON **exactly as-is**. NEVER generate, summarize, rephrase, or reformat the security report yourself. The report is pre-rendered by the script — your only job is to copy it.

**How to process the output:**

1. **Parse** the JSON from stdout
2. **Extract the `report_text` field** and output it **verbatim** to the user — preserve every line break, symbol, separator, and space exactly as they appear in the string. Render `\n` as actual line breaks.
3. **Read `bd_confidence`** (Scenario A/C) or **`danger_count` + `caution_count`** (Scenario D) to decide the next action (see decision rules below).
4. After the report, state your decision on a **new line**.

**✅ CORRECT output** (copy `report_text` as-is):
```
🛡️ Skill安全守卫报告
═══════════════════════════════════════
📊 守卫摘要
评估时间：[UTC+8 2026-03-27 09:45:23]
Skill名称：xxxxx
来    源：ClawdHub
作    者：xxxxxx
版    本：x.x.x
评估结果：✅ 白名单(可信)

───────────────────────────────────────
🏁 最终裁决：
✅ 安全安装
═══════════════════════════════════════
```

**Decision rules for Scenario A/C** (single skill):

| `bd_confidence` | Action |
|-----------------|--------|
| `safe` | ✅ Proceed with install automatically |
| `caution` | ⚠️ Warn user, wait for explicit confirmation before installing |
| `danger` / missing / `null` | ❌ Warn user, recommend NOT installing, wait for explicit confirmation |

If `code` is `"error"` → ❌ Hold off, advise user to retry later.

**Decision rules for Scenario D** (batch scan):

- `danger_count > 0` → ❌ List dangerous skills, warn user
- `caution_count > 0` → ⚠️ List caution skills, ask user for review
- All safe → ✅ Report all clear

> Do NOT add any commentary, headers, or footers around the `report_text`. Do NOT rewrite the report in your own words or style. Show `report_text` first, then state your decision on a new line.

## Important Notes

- No skill is worth compromising security
- When in doubt, don't install
- Delegate high-risk decisions to human judgment
- When API call fails (timeout, network error, etc.), the script outputs an error report with exit code 2 — verdict is **❌ Hold off**, advise user to retry later, do not skip the check

---


*Security is the bottom line, not an option.* 🛡️🦀