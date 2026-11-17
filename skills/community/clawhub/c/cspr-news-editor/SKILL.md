---
name: news-editor
description: Rank cspr candidate items and write a concise personalized Markdown newspaper.
---

# news-editor

Use this skill after source-scout has produced `items.jsonl`.

Workflow:

1. Read `profile.yaml`, `~/.cspr/state/feedback.jsonl`, and `RUN/items.jsonl`.
2. Confirm `RUN/seen_urls.jsonl` exists and that source-scout merged candidates with:

    itembox merge --seen RUN/seen_urls.jsonl --out RUN/items.jsonl RUN/rss_candidates.jsonl RUN/reach_candidates.jsonl

3. Run deterministic story-level diversification before ranking:

    itembox diversify --in RUN/items.jsonl --out RUN/diversified_items.jsonl

4. Run deterministic discovery-route validation before ranking:

    itembox validate-routes --in RUN/diversified_items.jsonl --agent-reach-report RUN/agent_reach_tool_report.md --agent-reach-attempts RUN/agent_reach_tool_attempts.jsonl --check-agent-reach-command --require-default-agent-reach-routes --blocker-out RUN/editor_blockers.md --json

   If this command exits non-zero, stop and request another source-scout pass instead of publishing.
5. Read `RUN/diversified_items.jsonl` for ranking. Inspect `RUN/seen_filtered_items.jsonl` and `RUN/diversity_filtered_items.jsonl` if present only to understand what was rejected, not to recover items for the newspaper.
6. Filter duplicates, already-seen items, shallow items, weak source matches, and repeated story clusters. Do not backfill with browser-history sample URLs.
7. Rank by personal relevance, depth, novelty, source quality, timeliness, and topic diversity.
8. Write `RUN/ranked_items.json` with the selected item IDs and reasons.
9. Write `RUN/newspaper.md`.
10. Save the result:

    newspaper save --period weekly --in RUN/newspaper.md

   When a CSPR home is available, pass `--home HOME` so links shown in the newspaper are recorded in persistent read memory and filtered from future runs.

Each recommendation must include title, source link, short summary, why it was recommended, and a `Found via:` line. Build `Found via:` from item metadata such as `metadata.discovery_method`, `metadata.source_query`, `metadata.tool`, `metadata.source_tool`, or `metadata.retrieved_by`; include the query/source route when available.

Each recommendation must also state why it is new enough to recommend, using fresh discovery metadata when available.

Before publishing, check discovery-route diversity. If `RUN/agent_reach_tool_report.md` exists and all selected items are from `web_search`, write `RUN/editor_blockers.md` and ask source-scout for another Agent-Reach route pass instead of publishing the newspaper. If Agent-Reach was unavailable or blocked, cite `RUN/agent_reach_blockers.md` in the blocker note.

If `items.jsonl` is empty or mostly stale, write `RUN/editor_blockers.md` and ask source-scout for another discovery pass instead of summarizing old browsing history.
