# financial-experts-said: runtime contract (ClawHub skills-only), bootstrap, diagnostics

## Version pinning

ClawHub skill version maps to a Git tag of the runtime repository:

| ClawHub skill | Git tag | Commit |
|---|---|---|
| 0.1.6 | `openclaw-v0.1.6` | `419cafe0a833d470867d3bd0e1c77773c6ff1095` |

Always clone the tag that matches the installed skill version; do not clone a
moving `main`.

## Path contract

| Variable | Meaning | If missing |
|---|---|---|
| `FES_ROOT` | Runtime directory (`pipeline/`, `chart/`) | env var or user-provided path; verify `$FES_ROOT/pipeline` and `$FES_ROOT/chart` exist |
| `FES_WORKSPACE` | User working directory | propose a safe directory in the current project; never write inside the skill/runtime |
| `FES_DB` | SQLite database | default `$FES_WORKSPACE/fti.db` |

Always build executable paths from `FES_ROOT`. Never run `python3 pipeline/...`
relative to the current directory.

## Bootstrap (version-pinned)

```bash
git clone --depth 1 --branch openclaw-v0.1.6 \
  https://github.com/bzSega/financial-experts-said.git "$FES_ROOT"
```

After clone, verify the pin before any command:

```bash
# must output exactly: openclaw-v0.1.6
git -C "$FES_ROOT" describe --exact-match --tags HEAD

# must equal the pinned SHA from the table above
if [ "$(git -C "$FES_ROOT" rev-parse HEAD)" != "419cafe0a833d470867d3bd0e1c77773c6ff1095" ]; then
  echo "pin mismatch" >&2
  exit 1
fi
```

Abort with a clear error (`runtime_missing`, pin mismatch) if either check fails.

Then verify both exist:
- `"$FES_ROOT/pipeline/init_db.py"`
- `"$FES_ROOT/chart/ticker_chart_html.py"`

Then (with user consent only):

```bash
python3 "$FES_ROOT/pipeline/init_db.py" --db "$FES_WORKSPACE/fti.db"
python3 "$FES_ROOT/pipeline/seed_demo.py" --db "$FES_WORKSPACE/fti.db"   # demo data
```

## Dependencies

Python 3.10+ (stdlib only for the pipeline). Charts need internet:
MOEX ISS API + lightweight-charts CDN (Apache 2.0) — see the network
disclosure in [chart.md](chart.md).

## Diagnostics

| Status | Meaning |
|---|---|
| `ready` | runtime, deps and DB available |
| `runtime_missing` | no `FES_ROOT` or required scripts — offer version-pinned bootstrap |
| `dependencies_missing` | python modules missing |
| `database_missing` | offer init/demo seed, only with user consent |
| `source_incomplete` | indexing lacks URL, date or text |
