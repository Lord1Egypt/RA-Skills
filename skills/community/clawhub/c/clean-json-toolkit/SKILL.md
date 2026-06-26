---
name: clean-json-toolkit
description: Local JSON / JSONL inspection and manipulation toolkit. Inspect deeply nested structures (path tree, types, sample values per path), query with a jq-style path language (no external jq), flatten nested objects/arrays into dot-notation maps and unflatten them back, and validate against a small pragmatic schema (required/type/min/max/regex/enum/item_type). Pure Python 3 standard library, no third-party dependencies, no remote calls.
license: MIT
metadata: {"openclaw":{"requires":{"bins":["python3"]},"primaryEnv":null,"homepage":"https://clawhub.ai/gopendrasharma89-tech/clean-json-toolkit"}}
---

# clean-json-toolkit

v0.2.0

Fourth member of the `clean-*` family. csv handles structured tabular data, text handles unstructured strings, log handles timestamped logs, and **json** handles nested data — API responses, config files, JSONL event streams.

Pure Python 3 standard library. No `jq`, no `jsonschema`, no pip installs.

## Scripts

- `scripts/inspect.py` — profile a `.json` or `.jsonl` file: tree of every distinct path with types, counts, and N sample values per path.
- `scripts/query.py` — jq-style path queries. `.key.nested`, `.key[0]`, `.[]` iterate, `.key.[].field` map. Output modes: `--json` / `--jsonl` / `--lines` / `--raw`. JSONL inputs implicitly iterate at the top level.
- `scripts/flatten.py` — flatten nested JSON into dot-notation keys. Reversible with `--unflatten`. Roundtrip-safe.
- `scripts/validate.py` — validate against a small schema (`required`, `type`, `min`/`max`, `min_length`/`max_length`, `enum`, `regex`, `item_type`, `allow_extra`).
- `scripts/merge.py` (NEW in v0.2.0) — merge multiple JSON files into one. Five strategies: `deep` (default; recursive merge, arrays replace), `shallow` (top-level only), `array-concat` (deep + arrays concatenated), `array-uniq` (deep + arrays deduped), `array-extend` (require all inputs to be arrays, then concatenate). The canonical agent need: cascade defaults + user + env-specific configs.
- `scripts/patch.py` (NEW in v0.2.0) — RFC 6902 JSON Patch. Apply `add` / `remove` / `replace` / `move` / `copy` / `test` operations. Build patches inline with `--op --path --value` or load from `--patch FILE`. `--strict` aborts at first failure, `--dry-run` writes to stdout instead. Supports `"/items/-"` append-to-array syntax.
- `scripts/check_deps.sh` — verify `python3`.

## Quick start

```bash
# Inspect
python3 scripts/inspect.py response.json
python3 scripts/inspect.py events.jsonl --max-samples 5

# Query
python3 scripts/query.py data.json '.meta'
python3 scripts/query.py data.json '.users.[].email' --raw
python3 scripts/query.py events.jsonl '.amount' --lines

# Flatten + unflatten roundtrip
python3 scripts/flatten.py config.json flat.json
python3 scripts/flatten.py flat.json nested.json --unflatten

# Validate
python3 scripts/validate.py users.jsonl --schema schema.json

# Merge (NEW v0.2.0) - cascade configs
python3 scripts/merge.py final.json defaults.json user.json env.json
python3 scripts/merge.py all.json events_*.json --strategy array-extend
python3 scripts/merge.py combined.json a.json b.json --strategy array-concat

# Patch (NEW v0.2.0) - RFC 6902 surgical edits
python3 scripts/patch.py doc.json patched.json --op add --path /email --value '"alice@example.com"'
python3 scripts/patch.py config.json updated.json --patch ops.json --strict
python3 scripts/patch.py doc.json /dev/null --op replace --path /age --value 42 --dry-run
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | success / one or more results |
| 1 | zero results / validation failed / empty input |
| 2 | bad arguments / unsafe path / missing file / invalid JSON / bad schema |

## Safety

- Pure Python 3 stdlib. No `eval`, no `subprocess`, no remote calls.
- All paths validated against safe-path policy (same as the other `clean-*` toolkits).
- Hand-rolled query path tokenizer.

## Pairs well with

- [`clean-csv-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit)
- [`clean-text-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-text-toolkit)
- [`clean-log-toolkit`](https://clawhub.ai/gopendrasharma89-tech/clean-log-toolkit)

## License

MIT
