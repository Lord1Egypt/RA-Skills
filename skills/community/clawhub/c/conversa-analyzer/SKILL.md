---
name: "conversa-analyzer"
description: "Analyze conversation transcripts: decisions, action items, dates, people, executive summary."
metadata:
  - productivity
  - analysis
  - summarization
allowed-tools:
  - read
  - write
  - memory_search
  - memory_get
user-invocable: true
---

# Conversation Analyzer

Extract structured insights from conversation transcripts (WhatsApp, email threads, meeting notes, chat logs).

## Trigger

Invoke when the user shares a conversation transcript or asks "analyze this conversation", "extract decisions", "what came out of this chat".

## Workflow

1. Accept the conversation text (from user message, pasted text, or file).
2. Parse and analyze for each category below.
3. Output a clean structured report.

## Output Structure

### 📝 Executive Summary
3-5 lines: what was discussed, what was decided, key outcome.

### 📌 Decisions Made
- What was decided
- Who was involved
- Context/constraints

### ✅ Action Items
| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|
| 1 | ... | ... | ... | Pending |

### 📅 Dates & Commitments
- Event/commitment → Date → Who committed

### 👤 People Involved
- Name: Role in conversation, responsibilities mentioned

### ⚠️ Open Questions / Risks
Anything unresolved, ambiguous, or risky.

## Notes
- If the input is very long (>10000 chars), summarize first then extract.
- If no conversation context is provided, ask the user to provide the text or point to a file.
- Use bullet lists, not tables, for WhatsApp-friendly output (no markdown tables).

---
⭐ *Gostou desta skill?* Deixe uma estrela no [ClawHub](https://clawhub.ai) para ajudar outros a encontrá-la!
