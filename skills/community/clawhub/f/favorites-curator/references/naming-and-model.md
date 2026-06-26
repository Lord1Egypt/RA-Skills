# Naming And Data Model

## Storage Root

Generated data lives under `favorites/` at the workspace root:
- `favorites/entries/`
- `favorites/snapshots/`
- `favorites/reports/`
- `favorites/enrichment-cache.json`

The skill directory stores code and references only.

## Filename Rule

Use this strict ASCII pattern for entry files:

`<data_type>__merged__<slug>.md`

Rules:
- `data_type`: short taxonomy value such as `git-repo`, `brew-formula`, `brew-cask`, `app`, `skill`, `extension`, `hook`
- `merged`: fixed source bucket for canonical merged entries
- `slug`: lowercase ASCII slug derived from the canonical display name
- Allowed characters: `a-z`, `0-9`, `-`, `_`, `.`
- Separator: double underscore only at the top level so parsers can split reliably

Examples:
- `git-repo__merged__openclaw-backup-tool.md`
- `skill__merged__favorites-curator.md`
- `app__merged__google-chrome.md`

## Frontmatter Schema

Required fields:

```yaml
schema_version: 2
item_id: skill:favorites-curator
canonical_key: skill:favorites-curator
name: favorites-curator
author: inferred
data_type: skill
source_name: workspace-skills
install_path: skills/favorites-curator
install_paths:
  - skills/favorites-curator
observed_locations:
  - source_name: workspace-skills
    source_kind: skill-dir
    source_ref: skills/favorites-curator
    install_path: skills/favorites-curator
variants:
  - source_name: workspace-skills
    data_type: skill
    install_path: skills/favorites-curator
merged_from_count: 1
variant_source_names:
  - workspace-skills
install_time: 2026-03-11T09:00:00+08:00
update_time: 2026-03-11T09:00:00+08:00
summary: Build and maintain a local favorites catalog.
simple_usage: python3 scripts/scan_favorites.py
source_url:
canonical_source_url:
content_fingerprint: {}
content_diff_status: single-variant
field_sources:
  author: inferred
  summary: skill_frontmatter_or_inferred
  simple_usage: inferred
```

Optional helper fields:
- `source_kind`
- `source_ref`
- `tags`
- `created_at`
- `last_scanned_at`
- `score`
- `notable_reason`
- `skill_variant_analysis`

## Merge Model

The scanner is local-first but canonicalizes duplicates into one primary entry.

Key helper fields:
- `install_paths`: all observed install paths after merge
- `observed_locations`: source-level provenance records; never drop paths during merge
- `variants`: preserved per-source variants with summary, source URL, and content fingerprint
- `merged_from_count`: number of raw observations collapsed into this entry
- `variant_source_names`: compact source summary for reports and notifications
- `canonical_key`: merge key derived from normalized source URL, skill name, or stable install basename

## Content Comparison For Skills

When multiple skill variants share the same canonical key, compare:
- `SKILL.md` text fingerprint (`skill_md_hash`)
- `scripts/` file set and per-file hashes (`script_files`)

Result fields:
- `content_fingerprint`: canonical fingerprint summary for the merged entry
- `content_diff_status`: `single-variant`, `skill-md-identical,scripts-identical`, or diff-alert combinations such as `skill-md-different,scripts-different`
- `skill_variant_analysis`: review-oriented detail for manual inspection

## Enrichment Policy

Use local metadata first. Online enrichment is optional and selective.

Rules:
- GitHub API is only used when a GitHub remote or homepage exists and can improve missing or low-quality fields.
- Vendor homepage fetch is only used for non-GitHub `source_url` values and only to improve `author`/`summary` quality.
- `field_sources` must record online provenance such as `github_api` or `vendor_homepage`.
- Cache enrichment results to keep rescans idempotent and low-noise.

## Body Convention

Keep the body short and stable:

```markdown
## Notes

- One or two human-readable details.
- Anything uncertain should say it is inferred.
```

## Snapshot Model

Each scan writes a JSON snapshot containing normalized merged entry objects keyed by `item_id`.
Use snapshots for diffing instead of parsing historical Markdown files.

## Report Heuristics

Daily digests should now highlight:
- merge results
- content diff alerts
- likely similar items still worth manual review
- notable items, with content-diff alerts ranked first
