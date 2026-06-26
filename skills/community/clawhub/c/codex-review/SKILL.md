---
name: codex-review
version: 2.1.0
description: "Three-tier code quality defense: L1 quick scan, L2 deep audit (via bug-audit), L3 cross-validation with adversarial testing. 三级代码质量防线。"
metadata:
  { "openclaw": { "emoji": "🔍" } }
tags:
  - code-review
  - quality-assurance
  - bug-detection
  - security-audit
  - cross-validation
  - ai-code-review
  - nodejs
  - openclaw-skill
  - clawhub
  - devops
---

# Codex Review — Three-Tier Code Quality Defense

Unified orchestration layer: picks audit depth based on trigger phrases. bug-audit is invoked as an independent skill — never modified.

## Security & Privacy

- **Read-only by default**: This skill only reads your project files for analysis. It does NOT modify, delete, or upload your code anywhere.
- **Optional external model**: L1/L3 can use an external code-review API (OpenAI-compatible) for a second opinion. This is **opt-in** — if no API key is configured, the skill works fine with agent-only review.
- **Credentials via environment variables only**: API keys are loaded from `CODEX_REVIEW_API_KEY` env var. Never hardcoded, never logged, never stored.
- **Local-only artifacts**: Hotspot files are written to system temp directory and auto-cleaned. No network transmission of analysis results.
- **No data exfiltration**: Code snippets sent to the external API are limited to the files being reviewed. No telemetry, no analytics, no third-party data sharing beyond the configured review model.

## Prerequisites

- **External model API** (optional, for L1 Round 1 and L3): Any OpenAI-compatible endpoint.
  - Set env vars: `CODEX_REVIEW_API_BASE` (default: `https://api.openai.com/v1`), `CODEX_REVIEW_API_KEY`, `CODEX_REVIEW_MODEL` (default: `gpt-4o`)
  - Works without this — falls back to agent-only audit
- **bug-audit skill** (optional): Required for L2/L3. Without it, L2 uses a built-in fallback.
- **curl**: For API calls (standard on macOS/Linux)

## Trigger Mapping

| User says | Level | What it does | Est. time |
|-----------|-------|--------------|-----------|
| "review" / "quick scan" / "review下" / "检查下" | L1 | External model scan + agent deep pass | 5-10 min |
| "audit" / "deep audit" / "审计下" / "排查下" | L2 | Full bug-audit flow (or built-in fallback) | 30-60 min |
| "pre-deploy check" / "上线前检查" | L1→L2 | L1 scan → record hotspots → L2 audit → hotspot gap check | 40-70 min |
| "cross-validate" / "highest level" / "交叉验证" | L3 | Dual independent audits + compare + adversarial test | 60-90 min |

---

## Level 1: Quick Scan (core of codex-review)

### Flow
1. **Gather code** — local `read`, `git clone <url>`, server scp, user-pasted snippet, or PR diff
2. **Exclude** — node_modules/, .git/, package-lock.json, dist/, *.db, __pycache__/, vendor/
3. **Round 1** — send to external model API for automated scan (skipped if no API key)
4. **Round 2** — current agent does deep supplementary pass
5. **Merge & dedup** — output severity-graded report
6. **Write hotspot file** (for L1→L2 handoff)

### External Model API Call

```bash
curl -s "${CODEX_REVIEW_API_BASE:-https://api.openai.com/v1}/chat/completions" \
  -H "Authorization: Bearer ${CODEX_REVIEW_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "${CODEX_REVIEW_MODEL:-gpt-4o}",
    "messages": [
      {"role": "system", "content": "<REVIEW_SYSTEM_PROMPT>"},
      {"role": "user", "content": "<code content>"}
    ],
    "temperature": 0.2,
    "max_tokens": 6000
  }'
```

**Fallback**: If API call fails or times out (120s), skip Round 1 and complete with agent-only audit.

### System Prompt (L1 External Scan)

```
You are an expert code reviewer. Find ALL bugs and security issues:
1. CRITICAL — Security vulnerabilities (XSS, injection, auth bypass), crash bugs
2. HIGH — Logic errors, race conditions, unhandled exceptions
3. MEDIUM — Missing validation, edge cases, performance issues
4. LOW — Code style, dead code, minor improvements

For each: Severity, File+line, Issue, Fix with code snippet.
Focus on real bugs, not style opinions. Output language: match the user's language.
```

### Agent Round 2 — Universal Checklist
- [ ] Cross-file logic consistency (imports, exports, shared state)
- [ ] Authentication & authorization bypass
- [ ] Race conditions (concurrent requests, DB write conflicts)
- [ ] Unhandled exceptions / missing error boundaries
- [ ] Input validation & sanitization (SQL injection, XSS, path traversal)
- [ ] Memory/resource leaks (unclosed connections, event listener buildup)
- [ ] Sensitive data exposure (keys in code, logs, error messages)
- [ ] Timezone handling (UTC vs local)
- [ ] Dependency vulnerabilities (outdated packages, known CVEs)

### Agent Round 2 — Tech-Stack Specific (auto-detect & apply)

**Node.js/Express:**
- [ ] SQLite pitfalls (DEFAULT doesn't support functions, double-quote = column name)
- [ ] Middleware ordering (auth before route handlers)
- [ ] pm2/cluster mode compatibility

**Python/Django/Flask:**
- [ ] ORM N+1 queries
- [ ] CSRF protection enabled
- [ ] Debug mode in production

**Frontend (React/Vue/vanilla):**
- [ ] innerHTML / dangerouslySetInnerHTML without sanitization
- [ ] WebView compatibility (WeChat, in-app browsers)
- [ ] Nginx sub-path / base URL issues

**Other stacks:** adapt checklist to detected technology.

### Code Volume Control
- Single API request: backend core files only (server + routes + db + config)
- Send frontend as a second batch if needed
- Very large projects (>50 files): summarize file tree first, then scan in priority order

### Hotspot File (L1→L2 handoff)
After L1, write issue summary to `${TMPDIR:-/tmp}/codex-review-hotspots.json`:
```json
{
  "project": "my-project",
  "timestamp": "2026-03-05T22:00:00",
  "hotspots": [
    {"file": "routes/admin.js", "severity": "CRITICAL", "brief": "Admin auth bypass via localhost"},
    {"file": "routes/game.js", "severity": "CRITICAL", "brief": "Score submission no server validation"}
  ]
}
```

This file is only used internally for L1→L2 handoff. bug-audit is unaware of it.

---

## Level 2: Deep Audit

### Flow (bug-audit available)
1. Read bug-audit's SKILL.md and execute its full flow (6 Phases)
2. bug-audit itself is never modified
3. Agent strictly follows bug-audit's specification

### Flow (bug-audit NOT available — built-in fallback)
1. **Phase 1: Project Dissection** — read all source files, build dependency graph
2. **Phase 2: Build Check Matrix** — generate project-specific checklist from actual code patterns
3. **Phase 3: Exhaustive Verification** — verify every checklist item against real code
4. **Phase 4: Reproduce** — for each finding, trace the exact execution path
5. **Phase 5: Report** — output full severity-graded report
6. **Phase 6: Fix Suggestions** — provide concrete code patches

---

## Level 1→2 Cascade: Pre-Deploy Check

### Flow
1. Execute L1 quick scan
2. Write hotspot file
3. Execute L2 (bug-audit or fallback)
4. After L2, **agent does hotspot gap analysis**:
   - Read hotspot file
   - Check if L2 report covers each L1 hotspot
   - Uncovered hotspots → targeted deep analysis, add to report
   - L1 vs L2 conclusions conflict → flag for manual review
5. Output final merged report

---

## Level 3: Cross-Validation (highest level)

### Flow
```
Step 1: External model independent audit
  → Full code to external API with detailed system prompt
  → Output: Report A

Step 2: Agent independent audit (bug-audit or fallback)
  → Full bug-audit flow (or built-in fallback)
  → Output: Report B

Step 3: Cross-compare
  → Both found       → 🔴 Confirmed high-risk (high confidence)
  → Only external    → 🟡 Agent verifies (possible false positive)
  → Only agent       → 🟡 External verifies (possible deep logic bug)
  → Contradictory    → ⚠️ Deep analysis, provide judgment

Step 4: Adversarial testing
  → Ask external model to bypass discovered fixes
  → Validate fix robustness
```

### Adversarial Test Prompt
```
You are a security researcher. The following security fixes were applied to a project.
For each fix, analyze:
1. Can the fix be bypassed? How?
2. Does the fix introduce new vulnerabilities?
3. Are there edge cases the fix doesn't cover?
Be adversarial and thorough. Output language: match the user's language.
```

---

## Report Format (all levels)

```markdown
# 🔍 Code Audit Report — [Project Name]
## Audit Level: L1 / L2 / L3
## 📊 Overview
- Files scanned: X
- Issues found: X (🔴 Critical X | 🟠 High X | 🟡 Medium X | 🔵 Low X)
- [L3 only] Cross-validation: Both agreed X | External only X | Agent only X | Conflict X

## 🔴 Critical Issues
### 1. [Issue Title]
- **File**: `path/to/file.js:42-55`
- **Found by**: External model / Agent / Both
- **Description**: ...
- **Fix**:
(code snippet)

## ✅ Highlights
- [What's done well]
```

## User Options

Users can customize behavior by saying:
- "only scan backend" / "只扫后端" → skip frontend files
- "ignore LOW" / "忽略低级别" → filter out LOW severity
- "output in English/Chinese" → control report language
- "scan this PR" / "审这个PR" → fetch PR diff instead of full codebase
- "skip external model" / "不用外部模型" → agent-only audit

## Notes

1. External API timeout: 120 seconds. On failure, skip that round — agent completes independently
2. Large projects: split into batches (backend → frontend → config)
3. Long reports: split across multiple messages, adapted to current channel
4. L2/L3 bug-audit execution strictly follows its own SKILL.md — no modifications or shortcuts
5. Hotspot file is ephemeral — overwritten each L1 run, not persisted
6. All secrets/keys must come from env vars or user config — never hardcoded in this skill
