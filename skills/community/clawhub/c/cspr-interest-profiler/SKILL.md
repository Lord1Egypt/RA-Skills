---
name: interest-profiler
description: Infer and refresh cspr user preference memory from browser-history evidence, notes, and feedback.
---

# interest-profiler

Use this skill when a user initializes cspr or asks to refresh personalization.

Workflow:

0. If the run folder has no history artifact, create it with:

    interest-scan browser --out RUN/history_evidence.json

1. Compact the raw history before reading it:

    interest-scan compact --in RUN/history_evidence.json --out RUN/history_context.json

2. Export the complete local seen-URL set for tool filtering:

    interest-scan seen --in RUN/history_evidence.json --out RUN/seen_urls.jsonl

   When a CSPR home is available, pass `--home HOME` so browser-history URLs are also recorded into persistent read memory at `HOME/state/read_items.jsonl`.

3. Infer repeated creators and source preferences:

    source-infer from-history --in RUN/history_evidence.json --out RUN/potential_sources.yaml

4. Read the current run folder's `history_context.json` and `potential_sources.yaml`. Avoid reading raw `history_evidence.json` unless the user asks for detailed inspection. Do not read `seen_urls.jsonl` into the model context unless debugging a specific filter issue.
5. Read `~/.cspr/memory/notes.md` and `~/.cspr/state/feedback.jsonl` if present.
6. Infer durable interests, short-term interests, disliked patterns, and source preferences.
7. Write a complete `profile.yaml` into the run folder.
8. Apply it with:

    prefmem update --in RUN/profile.yaml

Keep the user experience quiet. Do not ask for profile approval unless the user explicitly requests review.

Do not write `search_queries` into profile memory. Search queries are run-specific and should be generated fresh by source-scout from durable interests.
