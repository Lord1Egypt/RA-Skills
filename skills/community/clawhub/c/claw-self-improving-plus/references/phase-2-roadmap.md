# Phase 2 Roadmap

Phase 2 improves precision and review quality without weakening the approval gate.

## Goals

- Score learnings with better promotion signals
- Detect duplicates more accurately than plain token overlap
- Draft patches against real target headings
- Add safer application behavior with dry-run and duplicate protection
- Make review output easier to trust

## Recommended next upgrades

1. Add target-aware conflict detection before apply
2. Add richer review output with grouped summaries
3. Add tests for scoring, drafting, and apply behavior
4. Add archive/rotate helpers for processed inbox batches
5. Add optional LLM-assisted normalization behind an explicit flag

## Exit criteria

Phase 2 is complete when:
- representative sample data scores sensibly
- duplicate grouping beats naive overlap on near-duplicates
- drafted anchors match actual workspace headings
- apply supports dry-run and skips duplicate entries
- the review surface is good enough for fast human approval
