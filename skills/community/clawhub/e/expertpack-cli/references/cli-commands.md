# ExpertPack CLI Commands Reference

## Obsidian Setup

Copy the `.obsidian/` config from the ExpertPack repo template into your pack root. This enables Dataview and Templater pre-configured. See the ExpertPack repo at github.com/brianhearn/ExpertPack — the command is: `cp -r template/.obsidian ./your-pack-slug/.obsidian`

## OpenClaw RAG Configuration

Add to `openclaw.json` under `agents.defaults.memorySearch`:

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "extraPaths": ["path/to/pack"],
        "chunking": { "tokens": 500, "overlap": 0 },
        "query": {
          "hybrid": {
            "enabled": true,
            "mmr": { "enabled": true, "lambda": 0.7 },
            "temporalDecay": { "enabled": false }
          }
        }
      }
    }
  }
}
```

## Validator (ep-validate.py)

`ep-validate.py` is a local Python script from the public ExpertPack repo (`tools/validator/`). It reads pack files only — no network calls, no external dependencies beyond Python stdlib.

Run as: `python3 ep-validate.py /path/to/pack [--verbose] [--json]`

Must pass with 0 errors before committing. Warnings are advisory.

## Doctor (ep-doctor.py)

`ep-doctor.py` auto-fixes common issues. **Always run without `--apply` first (dry-run is the default) — inspect proposed changes before applying.**

- Dry-run: `python3 ep-doctor.py /path/to/pack`
- Apply all: `python3 ep-doctor.py /path/to/pack --apply`
- Apply specific category: `python3 ep-doctor.py /path/to/pack --fix links --apply`

Fix categories: `links` | `fm` | `prefix`

- **links** — convert path-based `related:` to bare filenames, markdown links → wikilinks, bidirectional `related:` enforcement
- **fm** — add missing frontmatter fields (title, type, tags, pack), fix `canonical_verbatim` paths
- **prefix** — rename files to content-type prefixes (`sum-`, `vbt-`, `facts-`, `meta-`, `mind-`, `prop-`, `rel-`, `pres-`)

Recommended workflow: ep-doctor dry-run → ep-doctor --apply → ep-validate → commit.

## Broken Wikilink Fixer (ep-fix-broken-wikilinks.py)

Removes broken wikilinks pointing to non-existent files. Safe for composites with cross-sub-pack references.

Run without `--apply` first to preview, then add `--apply` to execute.

All tools are in `ExpertPack/tools/validator/` in the public repo.

## Companion Skills

Install via the clawhub CLI (these are optional — install only if needed):
- `expertpack-eval` — EK ratio measurement and quality evals
- `expertpack-export` — export an OpenClaw agent as an ExpertPack
- `obsidian-to-expertpack` — convert an Obsidian vault to an ExpertPack
