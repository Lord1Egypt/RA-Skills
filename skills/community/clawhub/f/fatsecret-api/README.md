# FatSecret OpenClaw Skill

[![CI](https://github.com/ivanvmoreno/fatsecret-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/ivanvmoreno/fatsecret-skill/actions/workflows/ci.yml)
[![Publish](https://github.com/ivanvmoreno/fatsecret-skill/actions/workflows/release.yml/badge.svg)](https://github.com/ivanvmoreno/fatsecret-skill/actions/workflows/release.yml)
[![FatSecret API](https://img.shields.io/badge/FatSecret-API-green)](https://platform.fatsecret.com/api/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://docs.openclaw.ai/tools/skills)

Search foods, look up nutrition, log meals, track weight, browse recipes, and manage exercises via the FatSecret API.

## Installation

### Via ClawHub

```
clawhub install fatsecret-api
```

### Manual

Copy the `fatsecret/` skill folder to one of:

```
~/.openclaw/skills/fatsecret/
<workspace>/skills/fatsecret/
```

## Prerequisites

1. Install the Python package:

```
pip install pyfatsecret
```

2. Set environment variables:

| Variable | Required | Description |
|---|---|---|
| `FATSECRET_CLIENT_ID` | Yes | OAuth 2.0 client ID |
| `FATSECRET_CLIENT_SECRET` | Yes | OAuth 2.0 client secret |

Register for API credentials at [platform.fatsecret.com/api](https://platform.fatsecret.com/api/).

## Usage

The skill is invoked automatically by the agent when it matches your request. You can also invoke it directly:

```
python3 scripts/fs_runner.py foods_search --query "chicken breast"
python3 scripts/fs_runner.py food_get --food_id 4384
python3 scripts/fs_runner.py recipes_search --query "low carb dinner"
python3 scripts/fs_runner.py weight_update --current_weight_kg 75.5
```

All commands print JSON to stdout.

## Supported Operations

- **Food search & lookup** — `foods_search`, `foods_autocomplete`, `food_get`, `food_get_v2`, `food_find_id_for_barcode`
- **Food favorites** — `food_add_favorite`, `food_delete_favorite`, `foods_get_favorites`, `foods_get_most_eaten`, `foods_get_recently_eaten`
- **Food diary** — `food_entry_create`, `food_entry_edit`, `food_entry_delete`, `food_entries_get`, `food_entries_get_month`, `food_entries_copy`, `food_entries_copy_saved_meal`
- **Saved meals** — `saved_meal_create`, `saved_meal_delete`, `saved_meal_edit`, `saved_meal_get`, `saved_meal_item_add`, `saved_meal_item_delete`, `saved_meal_item_edit`, `saved_meal_items_get`
- **Recipes** — `recipe_get`, `recipes_search`, `recipe_types_get`, `recipes_add_favorite`, `recipes_delete_favorite`, `recipes_get_favorites`
- **Exercises** — `exercises_get`, `exercise_entries_get`, `exercise_entries_get_month`, `exercise_entries_commit_day`, `exercise_entries_save_template`, `exercise_entry_edit`
- **Profile** — `profile_create`, `profile_get`, `profile_get_auth`
- **Weight** — `weight_update`, `weights_get_month`

See [SKILL.md](SKILL.md) for full parameter details per command.

## Security

- All API calls go to `platform.fatsecret.com` over HTTPS only.
- Credentials are read from environment variables and never logged.
- The script is pure Python — no shell expansion or interpolation of user input.
- See the security manifest in `scripts/fs_runner.py` for full details.

## Releasing

Releases are automated via GitHub Actions. To publish a new version:

1. Update the `version` field in `SKILL.md` frontmatter.
2. Commit and push to `main`.
3. Tag the commit and push the tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The `release.yml` workflow will:
- Validate the skill package (required files, frontmatter, security manifests)
- Publish to ClawHub via `clawhub publish`
- Create a GitHub Release with a zip archive

### Required repository secret

Add `CLAWHUB_TOKEN` to your repo secrets (**Settings > Secrets > Actions**). Generate it by running `clawhub login` locally and copying the token.

### CI on every push/PR

The `ci.yml` workflow runs on every push to `main` and every PR. It validates the skill structure and tests that all subcommands in `fs_runner.py` are parseable and respond to `--help`.

## Setting up the new repo

This skill is designed to live in its own repo (e.g. `fatsecret-skill`). To set it up:

```bash
# From the fatsecret repo root
cp -r skills/fatsecret /path/to/fatsecret-skill
cd /path/to/fatsecret-skill
git init
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:ivanvmoreno/fatsecret-skill.git
git push -u origin main
```

The repo structure should be:

```
fatsecret-skill/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── SKILL.md
├── README.md
└── scripts/
    └── fs_runner.py
```

## References

- **[OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)** — Official docs on skill structure, discovery, eligibility, and configuration
- **[ClawHub Skill Format Spec](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)** — SKILL.md frontmatter fields, allowed files, slugs, and versioning
- **[ClawHub Publishing Checklist](https://gist.github.com/adhishthite/0db995ecfe2f23e09d0b2d418491982c)** — 13-point checklist for publishing skills (frontmatter gotchas, security manifests, required sections)
- **[ClawHub README & CLI Reference](https://github.com/openclaw/clawhub)** — `clawhub publish`, `clawhub install`, auth flows, and registry API
- **[Building Custom OpenClaw Skills](https://lumadock.com/tutorials/build-custom-openclaw-skills)** — Practical guide on SKILL.md structure, runbook-style body, gating, and production templates
- **[What are OpenClaw Skills? (DigitalOcean)](https://www.digitalocean.com/resources/articles/what-are-openclaw-skills)** — Overview of the skill ecosystem, installation, and security considerations
- **[FatSecret API Platform](https://platform.fatsecret.com/api/)** — API registration, documentation, and terms of use
- **[pyfatsecret (PyPI)](https://pypi.org/project/fatsecret/)** — The Python wrapper library this skill wraps
