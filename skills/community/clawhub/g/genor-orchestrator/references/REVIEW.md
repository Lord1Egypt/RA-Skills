# SENIOR DEV CODE REVIEW — genor-orchestrator
## Reviewer: External Senior Software Engineer
## Date: 2026-06-09
## Verdict: 18 issues found — 4 critical, 7 medium, 7 cosmetic

---

## 🔴 CRITICAL (must fix — correctness/behavior issues)

### 1. SKILL.md Decision Matrix references DELETED skills
**Location:** SKILL.md, Phase 2 table, row "UI/design"
**Problem:** `Frontend-design` is listed as a primary tool. This skill no longer exists. The agent will try to look it up, fail, and waste context tokens on the confusion.
```
| UI/design | Frontend-design | Shadcn/ui | Manual |
```
**Fix:** Remove the `Frontend-design` column entirely. If a UI task comes up, agent should use shadcn-ui or ask user.

### 2. SKILL.md Slash Commands section — commands that don't exist
**Location:** SKILL.md, Part 1 "Slash Commands"
**Problem:** Lists `/genor-orchestrator onboard`, `/genor-orchestrator webui`, etc. These are NOT real OpenClaw slash commands. OpenClaw doesn't have a custom slash command registration system like this. This misleads the agent into thinking it should register/handle these.
**Fix:** Either remove this section entirely, or rename to "Conversational Triggers" with clear language like "When the user says X, do Y."

### 3. SKILL.md — massive context bloat from README.md duplication
**Problem:** SKILL.md is ~320 lines. README.md is ~600 lines covering the SAME topics with MORE detail. Having both means:
- SKILL.md gets loaded every session (it's the skill file)
- The agent is told "SKILL.md contains quick-reference pointers; this file has the full procedures" — so it tries to read BOTH
- This DOUBLES the context cost for the same information
**Fix:** SKILL.md should be the ONLY authoritative doc. Delete README.md OR make SKILL.md comprehensive and delete README.md's overlapping sections.

### 4. models.json — `intermittent` is not a valid status
**Location:** models.json, model `lmstudio/laptop/gemma-4-e4b-ultra-heretic`
**Problem:** Status is `"intermittent"` but the server.py load_models() function only checks for `"active"`, `"broken"`, `"removed"`. An "intermittent" model will be counted as `agent_ready=True` and `status != "removed"` — treated as fully active, which is wrong.
**Fix:** Either normalize the status to "broken" or handle "intermittent" in server.py.

---

## 🟡 MEDIUM (should fix — quality/maintainability issues)

### 5. ROUTING.md is a mostly-empty template
**Location:** ROUTING.md
**Problem:** It's a template with `[Your best coding model]` placeholders. This file is listed in AGENTS.md as a pointer. The agent will read it and find NO actionable data. Pure token waste.
**Fix:** Either populate it with the actual current routing table, or delete it and point to models.json / MODEL_CATALOG.md instead.

### 6. session_log.md still references `project-orchestration`
**Location:** session_log.md rows 1-3
**Problem:** Historical entries list "project-orchestration" as the project name. Confusing for dashboard users.
**Fix:** Rename to "genor-orchestrator" with a note, or leave as-is since it's historical.

### 7. README.md section 10 (Fallback Master Table) conflicts with SKILL.md
**Location:** README.md section 10 vs SKILL.md Part 6
**Problem:** Two different fallback tables with different columns and different fallback levels. Agent sees contradictory info.
**Fix:** Consolidate into one table in SKILL.md, remove from README.md.

### 8. PART 2 says "PHASES 0-13" but only defines Phases 0-6
**Location:** SKILL.md header "PART 2: EXECUTION WORKFLOW — PHASES 0-13"
**Problem:** Claims 13 phases but defines 0-6. Agent thinks it's missing something.
**Fix:** Change to "PHASES 0-6".

### 9. Sub-agent prompt injection mentions "Repowise first"
**Location:** SKILL.md PART 4
**Problem:** Repowise was deleted. Sub-agents will try to find a tool that doesn't exist.
**Fix:** Replace with "Understand the codebase first (exec find as fallback)"

### 10. Phase 2 mentions "See TDD protocol" / "See Improve-architecture" — deleted skills
**Location:** SKILL.md Phase 2 Decision Matrix
**Problem:** TDD skill deleted. "Improve-architecture" doesn't tell agent WHERE. "Diagnose protocol" points to Phase 5 but the reference is vague.
**Fix:** Update references to point to actual sections within SKILL.md.

### 11. Phase 0 "Repowise first" — no explanation of HOW
**Location:** SKILL.md Phase 0
**Problem:** "If project exists, index + search" — but there's no explanation of HOW. Repowise is gone.
**Fix:** Replace with actual commands.

---

## 🟢 COSMETIC (nice to fix — minor quality issues)

### 12. Version history has 5 entries for what's essentially 2 releases
**Minor.** Keep as-is if you want full audit trail.

### 13. README.md references non-existent slash commands
**Same as #2.** Remove from README too.

### 14. README.md "exec find . -type f | head -200" is naive
**Problem:** head -200 truncates arbitrarily. Better: group by directory, show key entry points.

### 15. README.md "Available UI tools from installed skills" is too vague
**Problem:** Which skills? What tools? Agent will be confused.

### 16. models.json `free_models` key is empty/unused
**Problem:** models.json has a `free_models` key. server.py never reads it. Either use it or remove it.

### 17. SKILL.md Vision last resort says "the-host (SLOW)"
**Problem:** the-host is a hostname, not a model name. Agent won't know what this means.

### 18. BOOTSTRAP.md "Analysis" section contains internal deliberation notes
**Problem:** Bloats BOOTSTRAP.md with content the agent should never act on.

---

## SUMMARY

| Severity | Count |
|----------|-------|
| 🔴 Critical | 4 |
| 🟡 Medium | 7 |
| 🟢 Cosmetic | 7 |
| **Total** | **18** |

### TOP 3 priorities:
1. **Delete references to deleted skills** in SKILL.md — causes real runtime errors
2. **Decide SKILL.md vs README.md** strategy — duplicated content doubles context cost
3. **Fix "Phases 0-13" → "Phases 0-6"** — trivial but signals unfinished work
