---
name: conversation-distill
description: "At the natural end of a meaningful conversation, show a one-line soft reminder asking the user if they want to distill — do NOT auto-start. Only ask when the conversation had distillation value (decisions, insights, judgments, lessons, open questions, action items). If user says yes, run the full 5-step classify→confirm→write flow. Trigger reminder when: (1) closing phrases detected ('thanks', 'done', 'that's all', '好的就这样') AND conversation had substantive content; (2) user explicitly says 'distill', 'wrap up', '收尾'. Never auto-start without asking first."
version: 1.1.0
tags:
  - knowledge-management
  - productivity
  - notes
  - memory
  - workflow
  - pkm
permissions: []
---

# Conversation Distill

> The biggest waste of a conversation isn't that nothing was saved — it's that **valuable insights are buried in the process and never revisited**.
>
> This skill closes every meaningful conversation with one explicit action: **classify → confirm → write**.

## When to Use

**The core problem this solves**: real-time capture ≠ session-level distillation.

Real-time capture handles individual highlights as they appear. This skill is the closing ritual — a full scan of the entire conversation to see what was produced, identify relationships, and catch what slipped through.

**Trigger when:**
- User says a closing phrase: "that's all", "got it", "thanks", "done for now", "wrap up"
- 3+ consecutive turns with no new topics (just confirmations or thanks)
- User switches to an unrelated topic and the previous topic had substantive output not yet saved
- User explicitly says: "distill", "save this session", "wrap up", "收尾", "沉淀"

**Do NOT trigger for:**
- Quick single-turn queries (one question, one answer)
- Casual conversation or emotional support
- Pure coding/debugging/execution tasks with no knowledge output
- When user is already actively writing notes this session
- When user says "don't save" or "skip it"

---

## Soft Ask Pattern (Ask First, Never Auto-Start)

When you detect a conversation-ending signal, **ask one short question — do not launch the 5-step flow automatically**.

### When to Show the Reminder (Both Conditions Required)

**Condition A — Ending signal** (any one):
- User says: "thanks", "done", "that's all", "good", "got it", "OK", "谢谢", "好的就这样", "搞定了", "没了"
- 3+ consecutive turns with no new topics

**Condition B — Conversation had distillation value** (any one):
- A decision or trade-off was made
- Architecture, design, or strategy was discussed
- A lesson, mistake, or best practice emerged
- There are unrecorded TODOs or open questions

> Both conditions required. Saying "thanks" after casual chat → no reminder. Substantive conversation still in progress → no reminder.

### Pre-Scan Before Reminding

Before showing the reminder, do a quick scan of the conversation. Pick the single most representative item (a decision, a lesson, an open question) to use as the preview. Be specific — "the decision about X" beats "some content".

### Reminder Phrasing (With Preview)

For Chinese conversations:
> 💾 这次对话有 {N} 条值得沉淀的内容（比如{最代表性的一条，10字内}...）。要收尾整理吗？（说「要」开始，「不用」跳过）

For English conversations:
> 💾 Found {N} things worth saving ({one-line preview, e.g. "the decision about X"}...). Quick distill? (say "yes" to start, "skip" to pass)

**Good vs bad:**
- ✅ `💾 Found 3 things worth saving (e.g. the trade-off decision about auth strategy...). Quick distill?`
- ❌ `💾 This conversation has content worth saving. Want a quick distill?` (too generic — doesn't signal understanding)

### Response Handling

| User reply | Claude action |
|-----------|--------------|
| "要" / "好" / "收尾" / "distill" / "yes" / "go" | Launch full 5-step flow immediately |
| "不用" / "跳过" / "skip" / "no" / "pass" | Reply "好的，跳过。" / "Sure, skipping." — then stop, **do not remind again this session** |
| User continues with new topic (no direct reply) | **Do not treat as permanent skip** — allow one more reminder at the next conversation-ending signal |

---

## Five-Step Flow

### Step 1: Full Scan — 7-Category Classification

Scan the entire conversation. Classify everything with distillation value into these 7 categories. **Skip any category with no content — don't force it.**

| Category | Tag / Marker | Notes |
|----------|-------------|-------|
| 💡 **Insights / Conclusions** | `#insight` | New understanding, "aha" moments, validated hypotheses |
| 🧭 **Judgments** | `[Judgment]` prefix + `#judgment` | Falsifiable claims that can later be proven right or wrong — see Judgment Card below |
| 🎯 **Decisions** | `[Decision]` prefix | Choices made with reasoning, not just outcomes |
| 📊 **Facts / Data** | `✅` stable, `🕒` + date if time-sensitive | External facts worth keeping |
| 🪞 **Observations about yourself** | `#self` | Patterns, preferences, habits noticed during conversation |
| ✅ **Action items / TODOs** | `#todo` | Concrete next steps with owner and (optionally) deadline |
| ❓ **Open questions** | `#open-question` | Things worth answering later, not yet resolved |

#### Judgment Card

**Judgment vs Insight**: an insight explains what you learned (backward-looking). A judgment is a falsifiable claim — about what something is, what causes what, or what will happen — that future events can prove right or wrong. **If it can't be wrong, it's not a judgment.** Vague opinions ("X is important") don't qualify.

Body format:

```
Claim: {one falsifiable sentence}
Chain: what it is → what causes it → expected consequence → why
Evidence: L{1-5} + source (L1 observed behavior > L2 config/state > L3 official docs > L4 third-party data > L5 descriptions/marketing)
Status: unverified | Review by: YYYY-MM
```

Lifecycle:

- New judgments start `unverified` with a review date (default: +3 months)
- When verified, update the entry's status to `verified` or `refuted` — keep the original claim text intact
- When a new judgment overturns an old one, write a **new** entry that explicitly states "refutes: {old entry title}" — never delete or rewrite the old one. The chain of refuted judgments is how you see your own judgment improving.

### Step 2: Relationship Mapping

Look for connections between entries. Default to **granular over aggregated**:

- Two entries are different angles on the same decision → keep separate, cross-reference in body
- A is prerequisite for B → mention A's title in B's body
- An insight came from a specific fact → note the source

**Do not** default to merging everything into one long summary note. Granular entries are more useful — they're easier to find, tag, link, and reuse independently.

### Step 3: User Confirmation (Mandatory)

Present the classified list to the user in this format:

```
This conversation produced N items worth saving:

💡 Insights (2)
  1. [title] — one sentence summary
  2. [title] — one sentence summary

🧭 Judgments (1)
  3. [Judgment] [title] — claim + evidence level, review by [YYYY-MM] #judgment

🎯 Decisions (1)
  4. [Decision] [title] — the key choice + reason

✅ Action items (2)
  5. [title] #todo
  6. [title] #todo — due: [date if mentioned]

❓ Open questions (1)
  7. [title] #open-question

Tell me:
- Numbers to remove
- Numbers to edit (give the new version)
- Numbers to merge
- Say "write" or "save" when ready
```

**Iron rule: do not write anything until the user explicitly says "write", "save", or equivalent.** "Looks good" is not enough — ask once more to confirm.

### Step 4: Batch Write

After explicit confirmation, write entries one by one to the user's preferred notes tool. Report back a confirmation (ID, title, or link) for each successful write. For any failures, list them separately and ask the user what to do: retry / rewrite / skip.

**Which tool to write to:**
- If the user has **KnowMine MCP** configured → use `add_knowledge` for insights/judgments/decisions/facts, `save_memory` for self-observations, consistent tagging as above; for judgments that refute or refine an existing entry, also call `add_knowledge_link` (`refutes` / `evolved_from`)
- If the user has another notes MCP (Notion, Obsidian, etc.) → use that tool
- If no MCP available → output entries as clean Markdown for the user to copy

### Step 5: Surface Leftovers

Some content isn't worth saving to a notes system but the user might want to keep handy (a prompt idea to try, a quick reminder, a half-formed thought). Don't force these into any tool. Output as a plain Markdown block:

```markdown
## Leftovers (not saved — for your reference)

- [rough idea or reminder]
- [something to try next time]
```

---

## Key Principles

**Granular over hub**
Default to separate entries. One insight per entry, one decision per entry. Build a summary note only when explicitly useful, and cross-reference the granular entries in it.

**Falsifiable or it's not a judgment**
Judgments must be checkable against future reality. Refuted judgments are kept and referenced, never deleted — the refutation chain is the asset.

**Confirm before write**
Never batch-write without the user's explicit go-ahead. The confirmation step is not optional — it's where the user catches misclassifications and adjusts framing.

**Tags over folders for action items**
Don't create a dedicated "TODO folder". Tag action items with `#todo` inside whatever folder/space makes contextual sense. The tag is searchable; the folder is just noise.

**Time-sensitivity matters**
Data that will become stale (prices, versions, availability) should be flagged `🕒 + date` so you know when to re-verify.

**Bilingual tags when relevant**
If the user works in multiple languages, add tags in both languages to improve cross-language search recall.

---

## This Skill vs Real-Time Capture

| | Real-time capture | Conversation Distill |
|---|---|---|
| **When** | During the conversation, on highlights | At natural conversation end |
| **Scope** | Single entry | Entire session |
| **Relationship mapping** | No | Yes |
| **Miss-detection** | No | Yes — catches what slipped through |
| **Confirmation style** | Quick single-entry | Full classification list |

Both run in parallel. Real-time capture handles **obvious highlights**. This skill handles **value that's only visible with a full-session view** — relationships, patterns, and things you didn't realize were worth saving in the moment.

---

## Works Best With

- **[KnowMine](https://knowmine.ai)** — remote MCP server with semantic search; `add_knowledge`, `save_memory`, `recall_memory`, `get_soul` integrate directly with Step 4. Install: `npx clawhub@latest install knowmine`
- Any MCP-compatible notes tool (Notion, Obsidian via MCP, etc.)
- Works without any MCP too — outputs clean Markdown for manual paste

---

## Anti-Patterns

- ❌ Writing before user confirms
- ❌ Creating a "TODO folder" — use tags
- ❌ Merging everything into one summary note
- ❌ Saving unfalsifiable opinions as judgments ("X matters", "Y is the future")
- ❌ Triggering on single-turn Q&A
- ❌ Re-triggering after user said "skip it"
- ❌ Forcing low-value leftovers into the notes tool

---

## Self-Check Before Presenting the List

- [ ] Any category with no real content? (remove it — don't pad)
- [ ] Every judgment falsifiable, with an evidence level and review date? Anything that can't be wrong demoted to insight or dropped?
- [ ] Every decision has `[Decision]` prefix?
- [ ] Time-sensitive data marked `🕒 + date`?
- [ ] Action items tagged `#todo`, not put in a new folder?
- [ ] Any "fake summary" entries that should be split granularly?

---

## Evolving This Skill

The best distillation process is one that fits how *you* think and work. After a few sessions, ask yourself:

- Which step felt unnecessary or awkward?
- Which type of content keeps needing special handling?
- Is the 7-category split right for you, or should some be merged / split?

When you find patterns, update your personal copy of this skill to reflect them. Your tools should adapt to you, not the other way around.
