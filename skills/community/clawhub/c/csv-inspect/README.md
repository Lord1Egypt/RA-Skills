# csv-inspect

Inspect CSV / TSV files before analysis: column names, encoding, delimiter,
row count, inferred types, and first/last rows.

Python 3.9+ **stdlib only** — no pandas.

## Why

Agents often `cat` a whole CSV or jump into a 150-line pandas script. This
skill forces a cheap, streaming peek first.

## Install

`csv-inspect` must be on `PATH` (the skill is gated on that binary).

```bash
# ClawHub
clawhub install csv-inspect
# or use this folder as the skill root

mkdir -p ~/.local/bin
ln -sf /absolute/path/to/skill/scripts/csv-inspect ~/.local/bin/csv-inspect
```

Point the symlink at the `scripts/csv-inspect` that shipped with the skill.
`~/.local/bin` must already be on `PATH`.

## Usage

Invoke the on-PATH command — do not prefix with `python3`, and do not call
`scripts/csv-inspect`.

```bash
csv-inspect FILE
csv-inspect FILE --head 10 --tail 3
csv-inspect FILE --scan 500 --json
csv-inspect FILE --no-header
```

| Flag | Default | Meaning |
|------|---------|---------|
| `--head N` | 5 | First N data rows |
| `--tail N` | 0 | Last N data rows |
| `--scan N` | 200 | Rows used for type / sample inference |
| `--no-header` | off | Treat the first row as data |
| `--json` | off | Machine-readable output |

The file is streamed. Full row count is computed; type inference uses `--scan`
rows only.

## Output (text)

```
file: global_temperature.csv
size_bytes: 73891
encoding: utf-8
delimiter: ,
header: true
rows: 3288
columns: 3
names:
  Source
  Year
  Mean
types (from first 200 data rows):
  Source: str  empty=0  sample=[gcag, GISTEMP]
  Year: date  empty=0  sample=[1850-01, 1850-02]
  Mean: float  empty=0  sample=[-0.6746, -0.3334]
head(5):
  Source | Year    | Mean
  -------+---------+--------
  gcag   | 1850-01 | -0.6746
  ...
```

## Publish (ClawHub)

```bash
clawhub login
clawhub skill publish ./designed-skills/csv-inspect \
  --slug csv-inspect \
  --name "CSV Inspect" \
  --categories development,knowledge \
  --topics "csv,tsv,schema,preview,headers"
```

ClawHub publishes skills under MIT-0.

## License

MIT No Attribution (MIT-0)
