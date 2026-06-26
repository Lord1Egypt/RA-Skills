# clawfeedradar skill (ClawHub/OpenClaw)

`clawfeedradar` is a personal **news radar** skill built on top of an
existing [clawsqlite](https://github.com/ernestyu/clawsqlite) knowledge
base and its interest clusters.

This skill wraps the upstream `clawfeedradar` Python package and exposes
an agent‑friendly JSON API for:

- running the radar once for a single source (HN/RSS/etc.);
- running the radar for multiple sources defined in `sources.json`;
- inspecting the resulting scores and feed files.

It does **not** vend the upstream code or clone the repository. All
logic lives in the PyPI package and is accessed via
`python -m clawfeedradar.cli ...`.

> If you want to hack on the radar itself, use the upstream repo and
> CLI directly. This skill is aimed at OpenClaw agents and orchestrators.

---

## 1. Prerequisites

Before using this skill, you should already have:

1. A clawsqlite knowledge base with interest clusters

   - Use the `clawsqlite-knowledge` skill or the `clawsqlite` CLI to:
     - ingest your own articles/notes;
     - configure embeddings (`EMBEDDING_*` + `CLAWSQLITE_VEC_DIM`);
     - build interest clusters via
       `clawsqlite knowledge build-interest-clusters`.

2. A working `clawfeedradar` configuration

   - The upstream repo lives at:
     <https://github.com/ernestyu/clawfeedradar>
   - Read `README.md` / `README_zh.md` and `docs/SPEC_en.md` /
     `docs/SPEC_zh.md` for the full spec.
   - Configure `.env` with:
     - knowledge base paths (`CLAWSQLITE_ROOT` / `CLAWSQLITE_DB`)
     - embedding service (`EMBEDDING_*` / `CLAWSQLITE_VEC_DIM`)
     - fulltext fetch (`CLAWFEEDRADAR_SCRAPE_CMD` / workers)
     - scoring weights
     - optional LLM settings
     - output directory and optional git publish settings

Once the CLI works (you can run `python -m clawfeedradar.cli run ...`),
this skill will be able to reuse that configuration.

---

## 2. Installation

### 2.1 Install the skill shell

From your OpenClaw workspace:

```bash
openclaw skills install clawfeedradar
```

This will create the skill directory:

```text
~/.openclaw/workspace/skills/clawfeedradar
```

containing:

- `SKILL.md`
- `manifest.yaml`
- `bootstrap_deps.sh`
- `run_clawfeedradar.py`
- `README.md` / `README_zh.md`
- `ENV_EXAMPLE.md`

### 2.2 Install / upgrade the Python package

The `manifest.yaml` includes an install hook that runs
`bootstrap_deps.sh`. The script is responsible for:

- Installing the `clawfeedradar` Python package via `pip`;
- Falling back to a workspace prefix if the main venv is read‑only;
- Printing a `NEXT:` hint indicating where the package was installed
  and which `site-packages` directory will be added to `PYTHONPATH`
  when the skill runs.

In normal usage you do not need to run this manually; the `openclaw
skills install` / `update` commands handle it.

---

## 3. Runtime entry & JSON API

The runtime entry is `run_clawfeedradar.py`. It:

1. Reads a JSON payload from stdin;
2. Looks at the `action` field;
3. Builds a `python -m clawfeedradar.cli ...` command with appropriate
   arguments;
4. Executes it with an augmented `PYTHONPATH` if needed;
5. Parses `stdout` as JSON when possible and returns a normalized JSON
   response to the caller.

Every response has at least:

- `ok: true|false`;
- `data: ...` on success, or `error` / `exit_code` / `stdout` /
  `stderr` on failure;
- `next: [...]` when underlying tools print `NEXT:` hints;
- `error_kind` to help agents classify failures (missing embedding,
  scraper, git, etc.).

The actual CLI flags and behavior are fully documented in the upstream
clawfeedradar repo; this skill only exposes a thin JSON interface.

---

## 4. Supported actions

### 4.1 `run_once`

Run the radar once for a single source URL.

Payload example:

```json
{
  "action": "run_once",
  "source_url": "https://feeds.bbci.co.uk/news/technology/rss.xml",
  "max_source_items": 30,
  "max_items": 12,
  "score_threshold": 0.4,
  "source_lang": "en",
  "target_lang": "zh",
  "enable_preview": true,
  "preview_words": 512,
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

The JSON fields map directly to the CLI options described in
`README.md` / `SPEC_en.md`:

- `source_url` → `--url`
- `max_source_items` → `--max-source-items`
- `max_items` → `--max-items`
- `score_threshold` → `--score-threshold`
- `source_lang` / `target_lang` → `--source-lang` / `--target-lang`
- `enable_preview` → `--no-preview` (inverted)
- `preview_words` → `--preview-words`
- `root` → knowledge base `--root` (overriding `CLAWSQLITE_ROOT`)

The result JSON mirrors the CLI’s `--json` output, including:

- how many candidates were fetched;
- how many passed the score threshold;
- output file paths;
- per-item scores and interest cluster matches.

### 4.2 `schedule_from_sources_json`

Run the radar for multiple sources defined in a `sources.json` file.

Payload example:

```json
{
  "action": "schedule_from_sources_json",
  "sources_file": "/home/node/.openclaw/workspace/clawfeedradar/sources.json",
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

The `sources_file` must follow the format described in the upstream
clawfeedradar README/SPEC. Each enabled source may define its own:

- URL
- per-source `max_source_items` / `max_items`
- scoring overrides
- language and preview behavior

The skill aggregates the per-source runs and returns a structured
summary.

---

## 5. Environment configuration

The skill itself does not read a `.env` file; instead it relies on
clawfeedradar and clawsqlite, which both support project‑level
`.env`.

In OpenClaw you typically configure env vars on the agent or host so
both the skill and direct CLI usage see the same environment.

See the upstream `ENV.example` and `README` in the `clawfeedradar`
project for the authoritative list of env vars and recommended values.
Do **not** create a `.env` inside this skill directory; configure env on
the agent/host or in the upstream CLI project instead.

---

## 6. Security notes

- This skill does not alter the clawsqlite database schema or write to
  its tables; it only reads embeddings and interest clusters.
- All external network access (feeds, scraping, LLM, git) happens inside
  the clawfeedradar CLI and is fully observable via logs.
- If you want to restrict which sources are allowed, or disable publishing
  entirely, enforce that at the agent configuration level (env vars,
  sources.json path, etc.).

For deeper internals, metrics formulas, and tuning strategies, refer to
`docs/SPEC_en.md` / `docs/SPEC_zh.md` in the upstream repository.
