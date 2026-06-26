---
name: a-mem-memory-organization
description: Organize project, agent, or user memory using an A-MEM-style workflow with structured notes, semantic tags, contextual summaries, explicit links, and lightweight memory evolution. Use when Codex or OpenClaw needs to store long-term memory, maintain project context across sessions, build a memory file or memory store, retrieve relevant historical facts, or improve memory quality beyond flat append-only notes.
---

# A-MEM Memory Organization

Use this skill to turn raw observations into structured memory notes that are easier to retrieve, connect, and refine over time.

## Quick Start

When the user asks to "remember", "keep context", "build memory", "organize knowledge", "create long-term memory", or "make the agent learn from history", do the following:

1. Capture the new memory as a note with `content`, `context`, `keywords`, `tags`, `category`, `timestamp`, and `links`.
2. Search existing memory for semantically related notes before writing the new note.
3. Link the new note to the strongest neighbors if the relationship is concrete.
4. Prefer updating tags/context only when the new evidence genuinely improves the older note.
5. Keep memory atomic. Split unrelated facts into separate notes.

## Note Format

Represent each memory note with this schema:

```json
{
  "id": "uuid-or-stable-id",
  "content": "Atomic fact, preference, event, or lesson learned.",
  "context": "One sentence explaining the situation, domain, or why the note matters.",
  "keywords": ["specific terms", "entities", "concepts"],
  "tags": ["broader-category", "retrieval-label"],
  "category": "Preference | Project | Decision | Fact | Workflow | Bug | Research",
  "timestamp": "YYYYMMDDHHmm",
  "links": ["related-note-id"],
  "source": "optional source or conversation anchor"
}
```

If the surrounding system has no formal database yet, store notes in a Markdown or JSON memory file using the same fields.

## Write Workflow

Use this write workflow whenever adding memory:

1. Normalize the user input into one atomic note.
2. Generate 3-6 precise `keywords`.
3. Generate 2-5 broader `tags`.
4. Write a compact `context` sentence that explains why the memory matters.
5. Search for related notes using the combined retrieval text:

```text
content: ...
context: ...
keywords: ...
tags: ...
```

6. Link only to genuinely related memories. Avoid link spam.
7. If the new note sharpens an older note, update the older note conservatively.

## Retrieval Workflow

When answering from memory or selecting context for future work:

1. Expand the query into both a literal form and a semantic form.
2. Retrieve using the combined note text, not raw content alone.
3. Prefer topically relevant and specific notes over vaguely similar ones.
4. Include linked neighbors only when they help answer the task.
5. If there is noise, rerank manually by:
   exact entity overlap,
   stronger contextual match,
   recency when the information is time-sensitive,
   explicit links from already-relevant notes.

## Evolution Rules

Apply memory evolution carefully. The goal is refinement, not constant rewriting.

Safe evolution operations:

- Add a missing tag that improves retrieval.
- Clarify context when a later note disambiguates the old one.
- Add a link between notes with a clear relationship.
- Mark a note obsolete if later evidence supersedes it.

Avoid:

- rewriting old notes based on weak similarity,
- merging unrelated memories,
- broadening tags until everything looks related,
- losing the original fact while summarizing.

If uncertain, store a new note and link it instead of mutating old notes.

## What To Build In Practice

If the user wants this skill "made real" inside a project, choose the lightest form that matches the repo:

- For a documentation-first repo: create `memory/notes.json` or `memory/notes.md`.
- For an app repo: add a memory module plus persistence layer.
- For an agent repo: add note construction, retrieval, linking, and evolution hooks around the agent loop.
- For a coding assistant: maintain durable notes for project decisions, preferences, recurring bugs, and environment facts.

## Output Conventions

When you use this skill during a task:

- Tell the user what memory structure you are creating or updating.
- Show the proposed note fields if the user is designing the system.
- If implementing code, keep the data model explicit and testable.
- If no storage exists yet, propose a minimal file-based memory store first.

## References

Read [references/memory-patterns.md](references/memory-patterns.md) when you need:

- examples of good and bad note construction,
- category and tag heuristics,
- guidance on conservative memory evolution,
- suggestions for integrating this pattern into an agent loop.
