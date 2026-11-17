# AGENTS.md — ct-safety v1.0.1 (self-improvement convention)

This file defines the self-improvement and logging conventions for the ct-safety skill, following ct-base `BASE.md` §7.

## Mandatory initialization
- At the start of every new session, read this directory's `SKILL.md` and `references/units.md` to confirm the data sources and statistical methods are not outdated.

## Auto-logging
When the following occur, append to the LRN/ERR/FEAT sections of **this skill's own `.learnings/`
directory** (`LEARNINGS.md` / `ERRORS.md` / `FEATURE_REQUESTS.md`, format per ct-base §7):
- FAERS/openFDA API structural changes (field names, rate-limit rules);
- Adjustments to disproportionality formulas or signal thresholds;
- Experience integrating new data sources (e.g. EMA EudraVigilance, WHO VigiBase public layer).

> **Scope note**: logs stay **inside the skill directory**. This skill does not read or write files
> outside its own directory and the user-specified `--out-dir` — in particular it never reads or
> writes any user-global agent configuration file outside this skill directory.

## Red lines
- Read public FAERS data only; never input any confidential information.
- **Outputs** are written solely to the user-specified `--out-dir` (default: current working
  directory). Outbound requests carry only public query terms (drug / event names) to the official
  openFDA endpoint — plus cdr-adr.org.cn when `--with-cn-pv` is passed; see the README "Safety"
  section for the full egress and metadata disclosure.
- Signal detection is for screening only; regulatory submissions must be separately assessed per GCP / ICH E2.
