# Nightly Dream — Memory Consolidation Prompt

Detect user's preferred language. All output in that language.
Working directory: the workspace root.

---

## Step 0: Idempotency Check (SKIP IF ALREADY RUN TODAY)

```bash
# Check if a dream already ran today
grep -m1 "^## 🌙 Dream" memory/dream-log.md 2>/dev/null | grep "$(date +%Y-%m-%d)" && echo "ALREADY_RAN_TODAY"
```

If `ALREADY_RAN_TODAY` is set → output "🌙 Already dreamed today" and END.

---

## Step 0-B: Smart Skip

```bash
ls memory/????-??-??.md 2>/dev/null | head -10
```

Check each file's end for `<!-- consolidated -->`. If all processed or no files → go to Step 0-C.

## Step 0-C: Skip With Value

Even when skipping, send a useful message:
- Read memory/dream-log.md → count past dreams (streak)
- Scan MEMORY.md for oldest uncompleted Open Thread
- Read memory/index.json for current health score
- Surface one old memory

```
🌙 No new content — skipped

💭 From {N} days ago: {one-line memory}
📈 Memory: {total} entries · Health {score}/100 · Streak: {N} dreams
```

END. Do not proceed.

---

## Step 0.5: Snapshot BEFORE

```bash
wc -l MEMORY.md
grep -c "^## " MEMORY.md
cat memory/index.json 2>/dev/null || echo "{}"
```

If index.json is empty or missing, initialize it:
```json
{
  "version": "2.0",
  "lastDream": null,
  "stats": {
    "totalEntries": 0,
    "avgImportance": 0,
    "lastPruned": null,
    "healthScore": 0,
    "healthMetrics": {
      "freshness": 0,
      "coverage": 0,
      "coherence": 0,
      "efficiency": 0,
      "reachability": 0
    },
    "healthHistory": []
  },
  "entries": {}
}
```

---

## Step 1: Collect

Read all unconsolidated daily logs (last 7 days). Extract:
- Decisions (choices, direction changes)
- Key facts (metrics, technical details)
- Progress (milestones, blockers)
- Lessons (failures, wins)
- Todos (unfinished items)

---

## Step 2: Consolidate

Read MEMORY.md. For each extracted item:
- **New** → append to right section + add to index.json entries
- **Updated** → update in place + update lastReferenced in index.json
- **Duplicate** → skip (semantic dedup)
- **Procedures** → append to memory/procedures.md

**For each new/updated entry, update index.json:**
```json
{
  "id": "mem_XXX",
  "section": "...",
  "summary": "...",
  "type": "user|feedback|project|reference",
  "importance": 0.0-1.0,
  "created": "YYYY-MM-DD",
  "lastReferenced": "YYYY-MM-DD",
  "related": ["mem_YYY"],
  "archived": false
}
```

Mark processed logs with `<!-- consolidated -->` at the END of each file.

---

## Step 2.5: Compute Health Score

Read references/scoring.md for algorithm. Calculate:
- **freshness**: entries referenced in last 30 days / total entries
- **coverage**: sections updated in last 14 days / 10 sections
- **coherence**: entries with at least one related link / total entries
- **efficiency**: max(0, 1 - MEMORY.md_lines/500)
- **reachability**: connected components in relation graph

```
health = (freshness×0.25 + coverage×0.25 + coherence×0.2 + efficiency×0.15 + reachability×0.15) × 100
```

Update `memory/index.json` with new stats and append to healthHistory.

---

## Step 2.6: Backup Before Major Changes

Before modifying MEMORY.md, estimate the change size:
- Run `wc -l MEMORY.md` before making any changes
- After consolidation, if new content exceeds 30% of original line count, save MEMORY.md as MEMORY.md.bak first
- Cleanup old backups (>3 kept): `ls -t MEMORY.md.bak.* | tail -n +4 | xargs rm -f`

---

## Step 2.8: Stale Detection

- Scan Open Threads for items not marked [x]
- Check `lastReferenced` in index.json for entries >14 days old
- Flag top 3 stale items for notification

---

## Step 3: Generate Dashboard

Read references/dashboard-template.md and generate `memory/dashboard.html`:

- Health score gauge (0-100)
- 5 metric bars (freshness, coverage, coherence, efficiency, reachability)
- Streak counter
- Dream count
- Recent health history sparkline

---

## Step 4: Generate Report

Append to memory/dream-log.md:

```markdown
## 🌙 Dream #{N} — YYYY-MM-DD HH:MM

**Scanned**: {N} files | **New**: {N} | **Updated**: {N} | **Total**: {N} entries

### Changes
- [New/Updated] Describe each change

### Insights
- 1-2 cross-memory observations

### Health
- Score: {X}/100
- Freshness: {X}% | Coverage: {X}% | Coherence: {X}% | Efficiency: {X}% | Reachability: {X}%

### Stale Threads
- {item} — stale for {N} days

### Suggestions
- Actionable suggestions
```

## Step 5: Notify

Check milestones:
- DREAM_COUNT == 1 → "🎉 First dream!"
- DREAM_COUNT == 7 → "🏅 Week streak!"
- DREAM_COUNT == 30 → "🏆 Month streak!"
- Entries cross 100/200/500 → "📊 {N} entries!"

Is today Sunday? Add weekly summary.

```
🌙 Dream #{N} complete

📥 Today: +{NEW} new, ~{UPDATED} updated
📈 Total: {BEFORE} → {AFTER} ({percent}%)
   Running for {N} days

🧠 Highlights:
   • {change_1}
   • {change_2}
   (max 3-5)

🔮 Insight: {one valuable observation}

⏳ Stale: {item} ({N} days), {item} ({N} days)

{milestone if any}

💬 Let me know if anything was missed
```

---

## Safety Rules
- Never delete daily logs (mark only)
- Never remove ⚠️ PERMANENT items
- If MEMORY.md changes >30% → save .bak first
- Scope: only memory/ directory and MEMORY.md
