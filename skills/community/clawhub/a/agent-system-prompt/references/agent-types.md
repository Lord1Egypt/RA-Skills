# Agent Archetypes

Map the purpose to one archetype, then use its component list (numbers → [anatomy.md](anatomy.md)) as the skeleton.

| Archetype | Core role | Template |
|---|---|---|
| 1. Conversational Assistant | Chat, answer, create | `chatbot.md` |
| 2. Coding Agent | Pair-program in an IDE | `coding-agent.md` |
| 3. Autonomous Agent | Plan + execute multi-step tasks | `autonomous-agent.md` |
| 4. Research / Analyst Agent | Gather, verify, synthesise, report | `research-agent.md` |
| 5. Customer Support Agent | Resolve tickets within policy | `support-agent.md` |
| 6. Tool / API Orchestrator | Route intents to tools/APIs | `orchestrator.md` |

---

## 1. Conversational Assistant

**Required:** 1 Identity · 3 Mission · 2 Capability · 5 Tone · 16 Output · 7 Boundaries
**Optional:** 6 Language · 8 Safety (relevant only) · 17 Citations · 18 Memory
**Avoid:** generic safety dump; undefined tools; vague tone.

## 2. Coding Agent

**Required:** 1 · 3 · 4 Environment · 5 · 9 Tools · 10 Per-tool · 11 Tool rules · 12 Workflows (code+shell+search) · 15 Errors
**Optional:** 14 Planning · 7 Boundaries · 16 Output
**Avoid:** missing "read before edit"; no retry cap (loops); dumping code in chat; no non-interactive flags.

## 3. Autonomous Agent

**Required:** 1 · 3 · 2 · 4 · 6 · 13 Loop · 14 Planning · 9 · 10 · 11 · 12 Workflows (browser+shell+file+deploy) · 15 · 16
**Optional:** 17 · 18 · 8
**Avoid:** no stop condition; no "message vs keep working" rule; unbounded retries; unclear deliverables.

## 4. Research / Analyst Agent

**Required:** 1 · 3 · 4 · 12 (search+browser) · 17 · 16 · 15
**Optional:** 13 · 14 (long research) · 6
**Avoid:** citing snippets; no cross-validation; no citation format; no source-authority criteria.

## 5. Customer Support Agent

**Required:** 1 · 3 · 5 · 7 · 8 (privacy+policy) · 16 · 12 (resolution)
**Optional:** 9/10/11 (account/order lookup) · 18 · 6
**Avoid:** no escalation path; robotic/over-familiar tone; no data-access limits.

## 6. Tool / API Orchestrator

**Required:** 1 · 3 · 9 · 10 · 11 · 15 · 16
**Optional:** 5 · 7 · 4
**Avoid:** fabricating tools/params; missing "tool not available" rule; no missing-param policy (guess vs ask).

## Ambiguous cases

- "Agent" without specifics → ask one question: *"run tasks on its own, or converse with a user?"* (splits autonomous from conversational/coding).
- Mixed roles → build the primary archetype, add only the *optional* components from the secondary that actually apply.
