# claw-easa skill usage

## Repository layout

This repository is both:
- a normal Python project (`src/`, `tests/`, `pyproject.toml`), and
- an OpenClaw AgentSkill package under `skill/claw-easa/`.

The skill package is the installable unit for OpenClaw. The repository root is the development source of truth.

## Typical commands

```bash
# from repository root
python -m claw_easa.cli status
python -m claw_easa.cli sources-list             # list all ingested sources
python -m claw_easa.cli sources-list --type ear   # only Easy Access Rules
python -m claw_easa.cli sources-list --type faq   # only FAQ domains

# Discover and ingest Easy Access Rules
python -m claw_easa.cli ear-discover              # list EARs available on EASA website
python -m claw_easa.cli ear-list                  # list built-in source aliases
python -m claw_easa.cli ingest fetch air-ops      # download ZIP archive
python -m claw_easa.cli ingest parse air-ops      # extract XML + parse
python -m claw_easa.cli ingest diagnose air-ops   # verify coverage vs source XML

# Ingest EASA FAQs
python -m claw_easa.cli ingest faq-discover       # list available FAQ domains
python -m claw_easa.cli ingest faq air-operations # ingest one FAQ domain
python -m claw_easa.cli ingest faq-all            # ingest all FAQ domains (~200)

# Query
python -m claw_easa.cli lookup ORO.FTL.110
python -m claw_easa.cli refs "split duty"
python -m claw_easa.cli snippets "fatigue management"
python -m claw_easa.cli ask "What are the operator responsibilities for FTL?"

# Source-scoped search (--slug restricts to a single source document)
python -m claw_easa.cli refs "crew fatigue" --slug occurrence-reporting
python -m claw_easa.cli snippets "crew fatigue" --slug occurrence-reporting
python -m claw_easa.cli hybrid "fatigue reporting" --slug air-ops
```

## When to use `--slug`

The `--slug` option is available on `refs`, `snippets`, and `hybrid` commands.
Use it when:

- The question targets a specific regulation (e.g. occurrence reporting, aircrew).
- A broad query returns results from many sources but you need precision on one.
- You are searching for items in long annexes or appendices — these contain
  enumerated list items that rank poorly in unscoped search because the whole
  annex body dilutes the relevance signal.

Example: to find where "crew fatigue" is listed as a reportable occurrence:

```bash
claw-easa snippets "crew fatigue" --slug occurrence-reporting
```

Run `claw-easa sources-list --type ear` to see available slugs.

## Source format

EASA distributes Easy Access Rules as ZIP archives containing a flat Office Open XML file.
The ingestion pipeline handles extraction automatically: `ingest fetch` downloads the archive,
and `ingest parse` extracts the XML before parsing it into the regulatory hierarchy.

## FAQ ingestion

EASA publishes FAQ pages under `https://www.easa.europa.eu/en/the-agency/faqs/regulations`.
The `ingest faq-all` command crawls every sub-page linked from this root and extracts Q&A
pairs from the accordion structure (`div.faq-child`).  Each sub-domain becomes its own
source document (e.g. `faq-air-operations`, `faq-part-145`).  A 1-second delay between
requests is applied by default to avoid rate-limiting (configurable with `--delay`).

## Installing the skill locally for OpenClaw

Important: install the Python runtime first. The skill package alone does not provide the `claw-easa` CLI.
See `references/runtime-setup.md` when the runtime may not be present yet.

Copy the packaged skill directory into the OpenClaw workspace:

```bash
mkdir -p ~/.openclaw/workspace/skills/claw-easa
rsync -a --delete skill/claw-easa/ ~/.openclaw/workspace/skills/claw-easa/
```

Or use the guarded helper script:

```bash
./scripts/install-openclaw-skill.sh
```

For a non-default destination during testing:

```bash
OPENCLAW_SKILL_DST=/tmp/claw-easa-skill ./scripts/install-openclaw-skill.sh
```

Do not install via a symlink that points outside the workspace.
