# Phase 3 Roadmap

Phase 3 turns a safe promotion pipeline into a compounding learning system.

## Goals

- Consolidate repeated learnings into stronger records
- Rank learnings in a backlog by expected future value
- Make periodic review cheap enough that it actually happens
- Prevent duplicate promotions from slowly polluting long-term files

## New building blocks

1. `consolidate_learnings.py`
   - compress merge groups into stronger merged records
   - preserve related ids and combined evidence
   - retain extra summaries as related patterns

2. `build_backlog.py`
   - rank consolidated learnings by reuse, confidence, scope, and worth
   - surface the best promotion candidates first

3. `age_backlog.py`
   - mark fresh, aging, and stale items
   - slightly de-prioritize stale backlog entries

4. `review_backlog.py`
   - render the top backlog items in a human-review-friendly format

5. `check_existing_promotions.py`
   - detect patch candidates already present in long-term files
   - reduce duplicate promotion risk before apply

## Exit criteria

Phase 3 is complete when:
- repeated learnings get consolidated before patch drafting
- backlog ranking surfaces the strongest candidates first
- review output supports periodic review without digging through raw JSONL
- the one-shot pipeline produces scored, merged, consolidated, ranked, and draftable outputs
