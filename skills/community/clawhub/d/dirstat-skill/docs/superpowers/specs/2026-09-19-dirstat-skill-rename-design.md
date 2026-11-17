# DirStat_Skill Rename Design

## Goal

Replace the old public and internal identity with `DirStat_Skill` and remove cleanup-oriented language from the runtime, docs, outputs, and OpenClaw integration.

## Core Rules

- the tool is read-only
- the tool never removes anything
- the tool only suggests what a human should review
- invalid engine, platform, and path combinations must fail loudly

## Naming

- repository identity: `DirStat_Skill`
- skill path: `skills/DirStat_Skill/SKILL.md`
- Python package: `dirstat_skill`
- review outputs: `review_report.md` and `review_candidates.csv`

## Review Buckets

- `review first`
- `review carefully`
- `keep protected`

## Runtime Contract

- Windows paths must be scanned on Windows with `windows-native`
- Linux paths must be scanned on Linux with `ncdu`
- remote review must reuse compact outputs instead of forcing the wrong runtime onto the wrong platform
