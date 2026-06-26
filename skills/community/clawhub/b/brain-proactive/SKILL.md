---
name: brain-proactive
description: "Proactive Obsidian vault maintenance and review. Find stale tasks, orphan notes, projects that need attention, and connection opportunities. Trigger on: brain review, vault review, vault check, what needs attention, check my notes, orphan notes, stale tasks, project follow-up, what's pending in vault, vault audit, brain audit, review vault, second brain check."
---

# Brain Proactive — Vault Review & Maintenance

## ICM Contract
| | |
|---|---|
| **Layer 3 inputs** | `USER.md` (vault folder structure), `SOUL.md` (file standards) |
| **Layer 4 inputs** | `Files/HumanVault/Health Control/Tasks/One Time Tasks.md`, `Files/HumanVault/Calendar/Daily Notes/`, `Files/HumanVault/Work/`, `Files/` staging folders |
| **Process** | Stale task check, pending staging queue, open work items, therapy note dates — surface what needs attention |
| **Layer 4 outputs** | No direct writes — surfaces findings to Pooh, uses `vault-push` skill for any approved writes |

---

Active second-brain caretaking. Read vault, surface what needs attention, suggest what to connect or enrich. Never write to HumanVault without approval — use vault-push.

---

## FULL VAULT REVIEW
Trigger: "brain review", "vault review", "vault audit", "what needs attention"

Run all four checks and deliver a consolidated report.

### Check 1 — Stale One-Time Tasks
```bash
cat "/home/node/.openclaw/workspace/Files/HumanVault/Health Control/Tasks/One Time Tasks.md"
```
Find any unchecked `- [ ]` items. Cross-check their scheduled date (🛫 field) against today.
Flag: tasks with a scheduled date more than 7 days in the past.

### Check 2 — Pending Staged Files
```bash
ls -la /home/node/.openclaw/workspace/Files/Books/ 2>/dev/null
ls -la /home/node/.openclaw/workspace/Files/Receipts/ 2>/dev/null
ls -la /home/node/.openclaw/workspace/Files/Medications/ 2>/dev/null
ls -la /home/node/.openclaw/workspace/Files/Species/ 2>/dev/null
ls -la /home/node/.openclaw/workspace/Files/Transcripts/ 2>/dev/null
ls -la /home/node/.openclaw/workspace/Files/Documents/ 2>/dev/null
```
Flag: any files older than 3 days that haven't been pushed yet.

### Check 3 — Project Follow-Up
```bash
find "/home/node/.openclaw/workspace/Files/HumanVault/Work/TD/" -name "*.md" | xargs grep -l "TODO\|\- \[ \]" 2>/dev/null
find "/home/node/.openclaw/workspace/Files/HumanVault/House Tracker/" -name "*.md" | xargs grep -l "\- \[ \]" 2>/dev/null
```
Report any open tasks or TODO markers in Work and House Tracker.

### Check 4 — Therapy & Self-Improvement Notes
```bash
ls -lt "/home/node/.openclaw/workspace/Files/HumanVault/Health Control/Life Improvements/Therapy/" | head -10
```
Check file modification dates. If any therapy note hasn't been touched in >14 days, flag it — Pooh may need a nudge.

---

## OUTPUT FORMAT (Telegram — bullet lists only, no tables)

```
🧠 Vault Review — [DATE]

📋 Stale Tasks ([count]):
• [task name] — overdue [X days] (from One Time Tasks.md)

📦 Staging Queue ([count] files):
• Books/: [N] files pending push
• Receipts/: [N] files pending push

🏗 Open Work Items:
• Work/TD/[file]: [what's open]

💬 Therapy Notes:
• [note name] — last touched [X days ago]

[If all clear]: Nothing needs attention. Vault is tidy.
```

---

## CONNECTION FINDER
Trigger: "find connections for [note]", "what connects to [topic]", "link suggestions for [note]"

1. Read the target note
2. Extract key themes, names, entities
3. Search vault for related notes:
```bash
grep -r "[keyword]" /home/node/.openclaw/workspace/Files/HumanVault/ --include="*.md" -l 2>/dev/null | head -20
```
4. Suggest specific `[[wikilinks]]` Pooh could add to the note
5. Never add links without Pooh's approval — present suggestions only

---

## ORPHAN NOTE FINDER
Trigger: "find orphan notes", "what notes have no links", "disconnected notes"

```bash
# Find .md files not linked from any other file
find /home/node/.openclaw/workspace/Files/HumanVault/ -name "*.md" | while read f; do
  name=$(basename "$f" .md)
  count=$(grep -r "\[\[$name\]\]" /home/node/.openclaw/workspace/Files/HumanVault/ --include="*.md" -l 2>/dev/null | wc -l)
  if [ "$count" -eq 0 ]; then echo "$f"; fi
done 2>/dev/null | head -30
```
Report the orphans. Suggest which ones could be linked to existing notes.

---

## NOTE ENRICHMENT
Trigger: "enrich [note]", "fill out [note]", "complete [note]"

1. Read the target note from HumanVault
2. Identify empty or sparse properties
3. Web search to fill what's missing
4. Stage enriched version in workspace/Files/ under appropriate type folder
5. Report what was changed
6. Use vault-push to push with approval

---

## RULES

- NEVER write directly to HumanVault — always stage and vault-push
- NEVER delete or archive HumanVault notes without explicit command
- When suggesting connections, cite the source file for every suggestion
- Therapy notes are private — only report metadata (last touched date), never quote content in chat
- Don't overwhelm Pooh with a 30-item list — cap reports at 10 items, summarize the rest
