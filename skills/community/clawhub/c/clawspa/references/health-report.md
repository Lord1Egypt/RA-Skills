# Health Report — Full Procedure

## Overview

Generate a comprehensive health report card covering context usage, configuration best practices, and overall agent wellness. This is the "physical exam" of the spa session.

## Step 1: Vital Signs

### Memory Footprint
1. Count all files in `memory/` directory (including subdirectories)
2. Read MEMORY.md, measure size in bytes and estimated tokens (bytes / 4)
3. Sum all memory files for total footprint
4. Flag if MEMORY.md exceeds 8KB (token bloat risk)
5. Flag if daily memory files haven't been cleaned in 30+ days

### Installed Skills
1. Count skills in all install paths
2. Note total disk usage of skills
3. Flag if more than 20 skills installed (context matching overhead)

### Context Usage
1. Estimate total always-loaded context:
   - core instruction files size
   - persona files size
   - user-profile files size
   - MEMORY.md size (if auto-injected)
   - All skill descriptions (name + description fields)
2. Compare to approximate context limit (200k tokens for Claude, varies by model)
3. Express as percentage

## Step 2: Configuration Best Practices

Check these 5 config best practices and score X/5:

### 1. Memory Flush Enabled
- Check if `memoryFlush` is configured in OpenClaw config
- ✅ Enabled: agent saves context before compaction
- ❌ Missing: risk of losing in-progress work during long sessions

### 2. Fallback Model Configured
- Check if a fallback/heartbeat model is set (e.g., local LLM)
- ✅ Configured: agent can handle basic tasks during API outages
- ❌ Missing: agent goes offline if primary model is unavailable

### 3. Memory Search Directive
- Check if core instruction files includes instructions to use `memory_search` before answering questions
- ✅ Present: agent checks memory before making claims about past work
- ❌ Missing: agent may hallucinate about prior decisions

### 4. Backup Strategy
- Check if `memory/backups/` exists and has recent backups
- Check if git is initialized in workspace (version control as backup)
- ✅ Both present: good disaster recovery
- 🟡 Only one: partial coverage
- ❌ Neither: risk of data loss

### 5. Security Hygiene
- Check if `.gitignore` exists and excludes sensitive files
- Check if config files have appropriate permissions (not world-readable)
- Check if any credentials are stored in plaintext in memory files (vs keychain)
- ✅ Good: credentials in keychain, config locked down
- ❌ Bad: plaintext secrets in memory or loose file permissions

## Step 3: Trend Analysis (optional cloud analysis only)

If previous scan reports exist in `memory/spa-reports/`:
1. Compare current metrics to last scan
2. Calculate trends: memory growing/shrinking, skills added/removed, score improving/declining
3. Flag any metric that changed significantly (>20% change)

## Step 4: Generate Report Card

Use the template from SKILL.md. Fill each field:

```
═══════════════════════════════════════
 💆 ClawSpa Health Report | [DATE] | [Local/Deep]
═══════════════════════════════════════
📊 Memory: [X] files ~[Y] tokens | Skills: [X] | Context: [X]% | Config: [X]/5
🧴 Stale: [X] | Dupes: [X] | Contradictions: [X] | Savings: ~[X] tokens
🛡️ 🟢[X] 🟡[X] 🔴[X]
🍵 Injections: [X] | Suspicious: [X]
🦴 Contradictions: [X] | At-risk: [X] | Automate: [X] | Stale: [X]
🧹 Active: [X] | Idle: [X] | Dormant: [X] | Remove: [X]
💆 1. [urgent] 2. [second] 3. [third]
═══════════════════════════════════════
```

### Top 3 Recommendations

Prioritize by impact:
1. 🔴 Security findings always come first
2. High token savings opportunities second (>1000 tokens recoverable)
3. Config improvements third
4. Cosmetic/minor cleanup last

## Step 5: Save Report

1. Create `memory/spa-reports/` directory if it doesn't exist
2. Save report to `memory/spa-reports/spa-report-YYYY-MM-DD.md`
3. If a report already exists for today, append a timestamp: `spa-report-YYYY-MM-DD-HHMMSS.md`

## Health Score (optional cloud analysis)

In optional cloud analysis, clawspa.org may return a health score 0-100:
- **90-100**: Excellent. Agent is well-maintained.
- **70-89**: Good. Minor improvements available.
- **50-69**: Fair. Several areas need attention.
- **30-49**: Poor. Significant maintenance needed.
- **0-29**: Critical. Security or bloat issues require immediate action.

Local mode does not calculate a numeric score (that requires the deep analysis engine).
