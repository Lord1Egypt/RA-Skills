# Daily Digest — Supporting Description

## Purpose

This skill demonstrates the end-to-end collaboration between a **business process tool** (workflow-structurer) and a **digital asset ingestion tool** (demo-asset-ingest / ClawHub CLI).

It was produced by first structuring the process of "generating a daily work summary" through progressive clarification, then packaging the result as a publishable ClawHub skill.

## How it was created

1. **Process phase**: Used workflow-structurer to define:
   - Goal: produce a structured daily digest from available sources
   - Steps: identify date → gather sources → search transcripts → classify → format → deliver
   - Risks: fabricated activity, privacy leaks, duplicates
   - Rules: never fabricate, cross-reference, deduplicate, respect privacy

2. **Ingest phase**: Packaged the SKILL.md + references into the demo-asset-ingest folder shape and published via `clawhub publish`.

## Source material

- `SKILL.md` — the operational skill definition
- `references/DESCRIPTION.md` — this supporting document
