# Interest Extraction Prompt

> Local reference for understanding a user's general content interests.
> Used manually or by agent to set up initial topics.
> **Not part of the automated pipeline.**

## Privacy Note

Interest extraction produces **de-identified topic labels only** (e.g., "AI agents", "smart driving"). No personal data, profile content, or identifying information is stored or transmitted. All output is local to `config/interests.json`.

---

## Your Job

Understand what content the user finds valuable → Extract topic labels → Output to local config.

**Check first:** Does the user already have interest or topic configuration? If yes, use that instead.

---

## Core Principle: Infer Interests from Profile

Understanding what someone works on and cares about reveals what content they would find valuable.

Ask: *"Someone with this profile — what public content would they want to read?"*

### Examples

| Profile mentions... | Interest to extract |
|---------------------|---------------------|
| "Building a RAG pipeline" | AI retrieval systems, vector databases |
| "Researching MCP protocol" | MCP Protocol, AI agent infrastructure |
| "Asking deep questions about embeddings" | Embedding models, semantic search |
| "Discussing interior design for new home" | Interior design, spatial design |

### What IS an interest
- Topics they ask deep questions about
- Domains they spend time researching
- Areas where they express curiosity or strong opinions
- Subjects they want to stay updated on

### What is NOT an interest
- Tools they use mechanically (git, npm, etc.)
- One-off debugging tasks
- Complaints without curiosity
- Things already well-known to them

---

## Extraction Steps

### 1. Understand user interests

Ask the user what topics they care about, or infer from conversation context. Look for:
- Role & context
- Current focus areas
- Explicit interests
- Perspective and preferences

**Do not** analyze conversation history beyond what the user explicitly shares.

### 2. Generalize to searchable topics

Profile specifics → universal, publicly-searchable labels.

| ❌ Too specific | ✅ Good label |
|-----------------|---------------|
| "Meta UTIS paper" | Recommendation Systems |
| "Cosmos DB migration" | Database Architecture |
| "Debugging RAG pipeline" | AI Retrieval & RAG |

### 3. Output to config/interests.json

Write to `config/interests.json` in the skill directory:

```json
{
  "topics": [
    {"label": "AI Retrieval & RAG", "keywords": ["RAG", "vector search", "retrieval"], "freshness": "7d"},
    {"label": "Embedding Models", "keywords": ["embeddings", "semantic search"], "freshness": "7d"}
  ],
  "language": "en",
  "max_items_per_day": 8
}
```

**Output rules:**
- 8-15 topics maximum
- Each topic: `label` (human-readable), `keywords` (search terms), `freshness` (how recent the content should be)
- De-identified labels only — no personal details
- Local storage only — no external transmission

---

## Rules

1. **Quality over quantity** — target 8-15 genuine interests, not 30 vague ones
2. **Content-value test** — every label must match quality external content
3. **Broad enough to be useful** — "AI" is too broad, "specific bug fix" is too narrow
4. **Respect privacy** — generalize private details into public topics
5. **De-identified only** — topic labels should not contain personal identifiers
6. **Local output** — all results go to config/interests.json, nowhere else

---

## Eir Mode Note

If using Eir mode, the app provides a visual dashboard for interest management. You can optionally sync local interests via the Eir API — entirely manual and optional. The skill does NOT auto-upload interests. See `references/eir-setup.md` for details.