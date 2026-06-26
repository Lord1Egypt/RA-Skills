# Data Pipeline Design Review

**Platforms:** Claude · Codex
**Domain:** Data Engineering

## Purpose

Pressure-tests a proposed data pipeline, ETL/ELT flow, or dbt/SQL model and surfaces the reliability, data-quality, schema-evolution, and cost failures that normally only appear in production. Produces severity-rated findings, a remediation checklist, and a go/no-go recommendation before the design ships.

## When to Use

- Before merging a new pipeline or dbt model into production
- During a design review or architecture sign-off for a data flow
- When a backfill, replay, or reprocessing strategy needs a second opinion
- When investigating why a pipeline produces duplicate, missing, or wrong results

## What It Does

**Phase 1: Intake**
1. Collects sources, transformations, sink, orchestration, and failure expectations — one question at a time, treating missing context as explicit assumptions

**Phase 2: Structured Review**
2. Classifies the artifact (architecture, dbt/SQL model, or streaming flow) and routes review depth
3. Reviews all six dimensions: correctness & grain, idempotency & recovery, data quality, schema evolution, observability, cost & performance
4. Rates each finding Critical/High/Medium/Low and ties it to a concrete production failure scenario

**Phase 3: Output**
5. Produces a findings report, dimension-coverage statement, ordered remediation checklist, and a go/no-go recommendation

## Notes

The skill reviews the design rather than rewriting it. A single Critical finding forces a No-Go until resolved. Designs may reference internal systems; the skill does not store or transmit input beyond the current session.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.