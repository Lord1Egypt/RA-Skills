# Product Requirements

## Purpose

`dreamlover-skill` is a meta-skill for distilling anime and game virtual characters into reusable agent skills.

The first release is text-first. It accepts user notes, plot summaries, quote collections, and wiki-style summaries. It then produces a character package with three layers:

- `canon`: verified factual layer
- `persona`: behavioral inference layer
- `style_examples`: language texture layer

## Primary User Jobs

- create a new character skill from messy source material
- refine an existing character when new material appears
- separate "this is true in canon" from "this is how the character tends to behave"
- recover role consistency when the generated character drifts out of character

## In Scope For V0.1

- text-only ingestion
- source auditing by reliability
- explicit evidence tags
- layered output generation
- character-level version snapshots

## Out Of Scope For V0.1

- image parsing
- audio or voiceprint analysis
- video scene parsing
- automatic retrieval from remote APIs
- long-form copyrighted corpus storage

## User Flow

1. User provides source material or asks to update a character.
2. The skill routes the request through intake and source audit.
3. Source material is normalized.
4. `canon` is built from directly supported material only.
5. `persona` is built from supported summaries and interaction patterns.
6. `style_examples` captures speech texture.
7. A child `SKILL.md` is composed and written into `characters/{slug}/`.
8. A snapshot is written into the child `versions/` folder.

## Success Criteria

- `canon` never mixes in behavioral speculation
- `persona` never invents new canon facts
- corrections land in the right layer
- the child skill can answer in-character without factual drift
