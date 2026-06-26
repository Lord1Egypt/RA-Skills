# Compaction Prompt Template

When the agent decides to use LLM-based compaction (for complex conversations
where keyword extraction isn't sufficient), use this prompt.

## LLM Prompt

```
Compress the following conversation into a structured session digest.
Be concise. Omit filler, greetings, and repeated information.

Output format:

## Decisions Made
- [date] Decision description

## Facts Established
- [TYPE] Fact (use [PROJ] [TECH] [PREF] [PEOPLE] tags)

## Pending Actions
- [ ] Action description

## Blockers
- Blocker description

## Session Summary
(2-3 sentences max)

Rules:
1. Max 15 items total across all sections
2. No passwords, tokens, or API keys
3. No file paths, internal URLs, or infrastructure details — use placeholders like <PROJECT_ROOT>
4. Skip debugging noise unless it led to a lesson
5. Be specific about decisions but vague about locations
6. Be specific: "chose SQLite for prompt storage" not "chose a database"

Conversation:
---
{conversation_text}
---
```

## When to Use LLM vs Keyword

| Scenario | Method |
|----------|--------|
| Simple Q&A, <20 turns | Keyword (`compact_session.py --extract`) |
| Multi-topic, 20-50 turns | Either works |
| Complex debugging, >50 turns | LLM (needs nuanced understanding) |
| User wants exact summary | LLM (better at following instructions) |
| Quick save before /new | Keyword (fast, zero cost) |
