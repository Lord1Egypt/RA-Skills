# codemap

A local **code-symbol index** for agents. One command builds a compact SQLite map
of every function, class, method, interface and type across your repos. After
that, "where is X / what's its signature" is a single lookup that returns
`file:line` plus the signature, instead of a tree-wide grep followed by reading
the whole file.

Agents burn tokens re-discovering the same code. The usual loop is: grep the
name across the trees, then read the file the hit lives in (often the whole
thing) to see the signature and its surroundings. `codemap` collapses that to one
short record.

Pure stdlib. No network, no model call, no dependencies.

## Usage

```bash
# build (or rebuild) the index over one or more roots
codemap build ~/conexus ~/workloft-site ~/bob-app

# find a symbol — exact by default
codemap find scan
#   core.py:34  [function] def scan(text, allow=None)

# substring match
codemap find scan --like

# filter by kind
codemap find Pipeline --kind class

# outline a single file
codemap file src/app/roi/page.tsx

# machine-readable
codemap find scan --json
codemap stats
```

`find` exits non-zero when nothing matches, so it drops into a `&&` chain.

## What it indexes

- **Python:** top-level functions, classes, methods (incl. `async def`).
- **JS / TS / JSX / TSX:** function declarations, exported arrow consts,
  classes, interfaces, `type` aliases.

`node_modules`, `.next`, `.git`, `dist` are skipped. Markdown and other non-code
files are ignored. Rebuilds are idempotent — `build` deletes and re-inserts.

## Why it pays for itself

Measured over 40 unique-definition symbols drawn at random from our own indexed
repos (`bench.py`):

| Workflow | chars per lookup | est. tokens |
|---|---|---|
| codemap (compact record) | 104 | ~26 |
| grep + read ±40-line window | 3,187 | ~797 |
| grep + read whole file | 28,251 | ~7,063 |

Against the conservative windowed baseline that's a **96.7% cut**; against
whole-file reads, 99.6%. The index itself is cheap: 409 symbols across 67 files
built in under 0.1s.

## What's still off

- Extraction is regex-based, not a full parser. It catches the common
  declaration forms but will miss exotic ones (decorated factory patterns,
  re-exports, dynamically assigned names).
- No call-graph or reference tracking yet — it answers "where is X defined",
  not "who calls X".
- The index is a snapshot; rebuild after large edits. There is no file-watcher.

## Layout

```
codemap/
  extractors.py   # regex symbol extraction, per language
  index.py        # SQLite build / find / outline / stats
  cli.py          # argparse front end
bin/codemap       # executable shim
tests/            # 22 tests, stdlib unittest
bench.py          # the measurement above
```

Run the tests: `python3 -m unittest discover -s tests`
