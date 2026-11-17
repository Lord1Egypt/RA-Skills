---
name: brain-memory
description: "Recall and store persistent memories in the user's brain (~/.brain) with the brain CLI: deterministic recall with spreading activation, spaced reinforcement after presenting results, and classified model-driven memorization across life domains (personal, family, social, professional)."
homepage: https://brainmemory.ai
metadata: {"openclaw": {"emoji": "🧠", "requires": {"bins": ["brain"]}, "install": [{"id": "node", "kind": "node", "package": "brain-memory", "bins": ["brain"], "label": "Install the brain CLI (npm)"}]}}
---

# Brain Memory

The user has a persistent, neuroscience-inspired memory system — a single
global `~/.brain/` directory shared across all their AI agents. Memories are
Markdown files with YAML frontmatter (type, cognitive type, strength, decay,
salience, confidence, tags, associations). Recalled memories get stronger;
ignored ones fade. Use the `brain` CLI for every operation — never compute
scores or write memory files by hand.

## Recall (when asked to "remember", or when past context would help)

1. Run the deterministic recall engine:

   ```bash
   brain recall "<query>" --project <project> --task <task_type> --top 10
   ```

   It returns a scored JSON array (`id`, `title`, `path`, `type`, `score`,
   `relevance`, `decayed_strength`, `context_match`, `spreading_bonus`,
   `confidence`, `tags`). Scoring combines TF-IDF relevance, decayed strength,
   spreading activation, context match, and salience — the same ranking on
   every agent.

2. Read the top-scoring memory bodies from `~/.brain/<path>` (score > 0.3).

3. Decide how to respond:
   - One dominant match (score > 0.7, 2x the runner-up) → present it fully.
   - Several related matches (scores > 0.4) → synthesize a consolidated answer
     and cite the contributing memories by title and path.
   - Only weak matches → list the top 5-7 titles and ask which to explore.
   - No matches → check `~/.brain/_archived/`, then suggest other keywords.

4. **After presenting results, always reinforce** what you showed:

   ```bash
   brain reinforce <id1> <id2> ...
   ```

   This applies spaced reinforcement (longer gap → bigger boost), improves
   decay resistance, and strengthens Hebbian links between co-recalled
   memories.

5. Flag low-confidence memories (`confidence < 0.5`) as unverified.

## Memorize (when durable decisions, learnings, insights, preferences emerge)

Default: store immediately, report after — do not ask for confirmation when
the user asked to memorize. Classify each memory yourself:

- **type** (sets strength/decay): `decision` 0.85 · `insight` 0.90 · `goal`
  0.80 · `experience` 0.75 · `learning` 0.70 · `relationship` 0.70 ·
  `preference` 0.60 · `observation` 0.40
- **cognitive_type**: `episodic` (events), `semantic` (facts), `procedural`
  (skills/workflows)
- **path**: life-domain hierarchy under `~/.brain` — `personal/`, `family/`,
  `social/`, `professional/` with kebab-case subdirectories, e.g.
  `personal/health/sleep-routine.md`, `family/events/2026-summer-trip.md`,
  `social/friends/marta-preferences.md`, `professional/projects/foo/api-decision.md`
- **salience** and **confidence** (0.0–1.0), **tags**, **related** memory IDs

Pipe the classified memories to the CLI in one call (add `--sync` to push to
Brain Cloud / git afterwards):

```bash
brain memorize <<'EOF'
{
  "memories": [
    {
      "title": "Prefers morning workouts before 8am",
      "type": "preference",
      "cognitive_type": "semantic",
      "path": "personal/health/workout-preference.md",
      "tags": ["health", "routine"],
      "salience": 0.6,
      "confidence": 0.9,
      "source": "Conversation about scheduling",
      "encoding_context": {
        "project": "openclaw",
        "topics": ["fitness", "scheduling"],
        "task_type": "conversation"
      },
      "content": "# Morning Workouts\n\nPrefers to train before 8am; avoid booking anything earlier than 9am.\n"
    }
  ]
}
EOF
```

The CLI handles IDs, strength/decay computation, directories, index updates,
association edges, and the search index.

Guidelines:

- Set `BRAIN_AGENT=openclaw` in the environment when invoking the CLI so
  memories record their host agent.
- Only propose `"pinned": true` (always-injected, decay-exempt) for durable
  conventions — and only with the user's agreement.
- Never store secrets, credentials, or trivia.
- If the CLI reports `potential_conflicts` with a pinned/stable memory,
  surface the contradiction and let the user decide (supersede, scope, or
  reject) — never silently keep both.

## Session awareness

- `brain session-start --project <project>` returns the budget-bounded session
  payload (pinned facts, relevant memories, skills index) — internalize it
  silently; do not dump it.
- On session boundaries, append a summary entry to `~/.brain/contexts.json`
  (keep only the last 20) so future sessions get context-dependent recall.
