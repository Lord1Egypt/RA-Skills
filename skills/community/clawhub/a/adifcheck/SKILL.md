---
name: adifcheck
description: Check a ham-radio ADIF log's contents — the values LoTW and eQSL actually reject — before upload. Use when asked to validate an .adi or .adx log, find why QSOs were rejected by LoTW or eQSL, or check a log before uploading — for example "check my log before I upload to LoTW", "why did eQSL reject these QSOs", or "validate this ADIF file". Checks modes, submodes and their pairings, band versus frequency, dates and times, satellite fields and state/county codes against the ADIF 3.1.8 specification's own tables, plus the documented LoTW and eQSL acceptance rules. Not for Darwin Core / GBIF occurrence files (that is dwccheck) or iCalendar (.ics) files (that is icslint).
license: MIT
compatibility: Requires Python 3.10+. No dependencies (standard library only) and runs fully offline; network is needed only to install.
---

# adifcheck

## What this tool does

adifcheck validates the *contents* of ADIF log files (`.adi` and `.adx`), not just their syntax: every record is checked against the ADIF 3.1.8 specification's published tables — modes, submodes and their legal pairings, bands and their frequency ranges, dates, times, and cross-field rules — and, optionally, against the documented acceptance rules of LoTW and eQSL. Each finding names the record, the field, what is wrong, and the source the rule comes from. It only reads the files you give it; it never uploads or changes anything.

## Install

```bash
pip install git+https://github.com/RakTikoo/adifcheck
```

This provides the `adifcheck` command.

## Run

Check a log against the core spec rules:

```bash
adifcheck mylog.adi
```

Check against the spec plus both upload services' documented rules, with machine-readable output:

```bash
adifcheck mylog.adi --lotw --eqsl
adifcheck mylog.adi --lotw --eqsl --json
```

Several files can be given at once. `--lotw` adds LoTW's documented rules (minimum fields, satellite name/propagation mismatches, duplicate QSOs); `--eqsl` adds eQSL's published content rules (minimum contents, length limits, and eQSL's own mode/band tables, which differ from ADIF's). `--strict` makes warnings fail the run too.

## Reading the results

Each file gets a summary line (`file: N records, E errors, W warnings`), then one line per finding: `record N (CALL, DATE): FIELD: error|warning: message [source of the rule]`. The last line is the verdict: `result: clean — no findings`, `result: no errors; warnings above are worth a look`, or `result: FAIL — ...`. The exit code matches:

- `0` — clean: no errors (and, under `--strict`, no warnings either).
- `1` — errors found; these are the records an upload service would reject or drop.
- `2` — a file could not be read at all. User errors are one-line messages, never tracebacks.

Warnings are real findings that do not fail the run on their own — for example an import-only (deprecated) value, or a frequency in no ADIF band. With `--json`, the same findings are emitted as structured data with the record, field, severity, message and source for each.

## Limits

- Two grades of rule, never blurred in the findings. The core is spec-proven: every check comes from ADIF 3.1.8's own published tables, and the test suite pins the core to zero errors on ADIF's official test files. The `--lotw` and `--eqsl` packs are behaviour-based: they implement what the services *document* (LoTW's rejection causes in the DX Lab wiki; eQSL's published content-spec page), not a machine-readable rulebook — documentation can lag a service's real behaviour, pack findings cite their document rather than the spec, and where a document looks stale the finding is a warning, not an error.
- Some things cannot be decided from the file alone, by any local tool: whether a callsign is really allocated, whether a satellite name is a real satellite, and which DXCC entity a callsign belongs to are external-database lookups. Service-side state is also invisible: LoTW certificate date ranges and expiry, server processing state, and your eQSL account profile.
- State/county (STATE/CNTY) checks need the DXCC entity in the record (DXCC or MY_DXCC) and a subdivision table in the spec for that entity; US counties are never membership-checked, because ADIF does not enumerate them (CNTY is a free-form "STATE,county" string there). CONTEST_ID is not checked against its enumeration — the spec types the field as a plain string.
- Regional band plans narrower than the ADIF band ranges are outside the spec and outside this tool; frequencies exactly on a band edge are read against the spec's published ranges, inclusive. Free text between records is ignored.
