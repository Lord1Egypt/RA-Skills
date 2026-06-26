---
name: rebrickable
description: Use the Rebrickable API through the included CLI for LEGO catalog lookup, user set/part lists, build analysis, lost parts, and guarded collection writes.
version: 1.0.0
---

# Rebrickable AFOL skill

Use this skill when the user asks for Rebrickable catalog lookup, Rebrickable set or part list management, user collection analysis, buildability checks, minifigs from owned sets, all-parts inventory, or lost-parts tracking.

Primary interface: `scripts/rebrickable`.

The skill is self-contained for archive distribution and wraps the Rebrickable API directly using checked-in references inside this skill directory:
- OpenAPI reference: `references/openapi/rebrickable.yaml`
- Domain guidance: `references/prompts/rebrickable-tools.txt`
- CLI source: `scripts/rebrickable_cli.py`

Do not scrape vendor docs or invent parameters when the checked-in OpenAPI reference covers the endpoint. If the reference is insufficient, say what is missing.

## Authentication

Required environment variable:

```bash
export REBRICKABLE_API_KEY=...
```

Optional environment variables:

```bash
export REBRICKABLE_USER_TOKEN=...       # needed for user collection endpoints
export REBRICKABLE_BASE_URL=https://rebrickable.com/api/v3
```

Never print, commit, log, or paste real API keys or user tokens. Commands should reference credentials only indirectly through the CLI.

Rebrickable auth placement matters: API authentication goes in the `Authorization` header as `key <REBRICKABLE_API_KEY>`. The CLI handles that header and redacts it in dry runs.

User-specific endpoints include the user token in the URL path. Treat `REBRICKABLE_USER_TOKEN` as private even though it is not the API key.

## CLI quick reference

Run commands from this skill directory:

```bash
scripts/rebrickable --help
scripts/rebrickable colors --page-size 5
scripts/rebrickable sets --search "Millennium Falcon" --page-size 5
scripts/rebrickable set --set-num 75192-1
scripts/rebrickable set-parts --set-num 75192-1 --page-size 20
scripts/rebrickable parts --part-num 3001
scripts/rebrickable element --element-id 300121
scripts/rebrickable minifigs --search "Darth Vader" --page-size 5
scripts/rebrickable part-categories --page-size 20
scripts/rebrickable themes --page-size 20
```

User read-only examples, only when `REBRICKABLE_USER_TOKEN` is configured or passed with `--user-token`:

```bash
scripts/rebrickable profile
scripts/rebrickable set-lists
scripts/rebrickable set-list-sets --list-id 123
scripts/rebrickable all-sets --search "Star Wars" --page-size 20
scripts/rebrickable part-lists
scripts/rebrickable part-list-parts --list-id 456 --page-size 20
scripts/rebrickable all-parts --part-num 3001 --page-size 20
scripts/rebrickable all-minifigs --search "astromech" --page-size 20
scripts/rebrickable build --set-num 8043-1
scripts/rebrickable lost-parts --page-size 20
```

Mutating commands are guarded. They do nothing unless passed `--yes`; use `--dry-run` first:

```bash
scripts/rebrickable create-set-list --dry-run --name "Wanted builds" --is-buildable true
scripts/rebrickable add-sets-to-list --dry-run --list-id 123 --sets-json '[{"set_num":"8043-1","quantity":1}]'
scripts/rebrickable update-set-in-list --dry-run --list-id 123 --set-num 8043-1 --quantity 2
scripts/rebrickable remove-set-from-list --dry-run --list-id 123 --set-num 8043-1
scripts/rebrickable create-part-list --dry-run --name "Missing dark bluish gray"
scripts/rebrickable add-part-to-list --dry-run --list-id 456 --part-num 3001 --color-id 72 --quantity 4
scripts/rebrickable update-part-in-list --dry-run --list-id 456 --part-num 3001 --color-id 72 --quantity 8
scripts/rebrickable remove-part-from-list --dry-run --list-id 456 --part-num 3001 --color-id 72
scripts/rebrickable add-lost-part --dry-run --inv-part-id 806698 --lost-quantity 1
scripts/rebrickable remove-lost-part --dry-run --lost-part-id 999
```

## Safety rules

Read-only by default:
- public catalog commands: `colors`, `color`, `element`, `minifigs`, `minifig`, `minifig-parts`, `minifig-sets`, `part-categories`, `part-category`, `parts`, `part`, `part-colors`, `part-color`, `part-color-sets`, `sets`, `set`, `set-parts`, `set-minifigs`, `set-alternates`, `themes`, `theme`
- user read commands: `profile`, `set-lists`, `set-list`, `set-list-sets`, `all-sets`, `part-lists`, `part-list-parts`, `all-parts`, `all-minifigs`, `build`, `lost-parts`

Mutating operations require explicit user confirmation in the current conversation before execution:
- `create-set-list`, `update-set-list`, `delete-set-list`
- `add-sets-to-list`, `update-set-in-list`, `remove-set-from-list`
- `create-part-list`, `delete-part-list`
- `add-part-to-list`, `update-part-in-list`, `remove-part-from-list`
- `add-lost-part`, `remove-lost-part`

Stored credentials are not permission. Before any mutation, restate the exact platform, list ID, set number, part number, color ID, quantity, lost-part record, and whether the operation creates, updates, or deletes data. Wait for explicit confirmation such as "yes, add set 8043-1 to Rebrickable list 123".

The CLI enforces this mechanically: mutating commands fail unless `--yes` is passed, and `--dry-run` prints the request shape with the `Authorization` header and `REBRICKABLE_USER_TOKEN` path segment redacted.

If the user asks to "add to my collection" or "show my collection" without naming a platform and Brickset/Rebrickable are both configured, ask which service to use before mutating or reading private collection data. If they explicitly name Rebrickable, use only Rebrickable.

## Endpoint coverage

Catalog coverage:
- `GET /lego/colors/` and `GET /lego/colors/{id}/`
- `GET /lego/elements/{element_id}/`
- `GET /lego/minifigs/`, `GET /lego/minifigs/{set_num}/`, `GET /lego/minifigs/{set_num}/parts/`, `GET /lego/minifigs/{set_num}/sets/`
- `GET /lego/part_categories/` and `GET /lego/part_categories/{id}/`
- `GET /lego/parts/`, `GET /lego/parts/{part_num}/`, `GET /lego/parts/{part_num}/colors/`, `GET /lego/parts/{part_num}/colors/{color_id}/`, `GET /lego/parts/{part_num}/colors/{color_id}/sets/`
- `GET /lego/sets/`, `GET /lego/sets/{set_num}/`, `GET /lego/sets/{set_num}/parts/`, `GET /lego/sets/{set_num}/minifigs/`, `GET /lego/sets/{set_num}/alternates/`
- `GET /lego/themes/` and `GET /lego/themes/{id}/`

User coverage:
- `GET /users/{user_token}/profile/`
- `GET/POST /users/{user_token}/setlists/`
- `GET/PATCH/DELETE /users/{user_token}/setlists/{list_id}/`
- `GET/POST /users/{user_token}/setlists/{list_id}/sets/`
- `GET/PATCH/DELETE /users/{user_token}/setlists/{list_id}/sets/{set_num}/`
- `GET /users/{user_token}/sets/`
- `GET /users/{user_token}/partlists/`
- `POST /users/{user_token}/partlists/`
- `DELETE /users/{user_token}/partlists/{list_id}/`
- `GET/POST /users/{user_token}/partlists/{list_id}/parts/`
- `PUT/DELETE /users/{user_token}/partlists/{list_id}/parts/{part_num}/{color_id}/`
- `GET /users/{user_token}/parts/`
- `GET /users/{user_token}/allparts/`
- `GET /users/{user_token}/minifigs/`
- `GET /users/{user_token}/build/{set_num}/`
- `GET/POST /users/{user_token}/lost_parts/`
- `DELETE /users/{user_token}/lost_parts/{id}/`

Treat set-list names, part-list names, owned sets, part inventories, build analysis, lost parts, emails, and profile data as private. Summarize only what the user needs.

## Known Rebrickable endpoint quirks

Use `sets --search` for fuzzy set lookup, but use `set --set-num` when the user gives an exact Rebrickable set number:

```bash
scripts/rebrickable set --set-num 75192-1
scripts/rebrickable sets --search "Millennium Falcon" --page-size 5
```

When adding sets to a set list, Rebrickable requires a JSON array even for a single set. The CLI validates this before sending the request:

```bash
scripts/rebrickable add-sets-to-list --dry-run --list-id 123 --sets-json '[{"set_num":"8043-1","quantity":1}]'
```

The `all-parts` endpoint is explicitly resource-intensive in the checked-in OpenAPI reference. Use filters such as `--part-num`, `--part-cat-id`, `--color-id`, and small `--page-size` values whenever possible.

`update-set-in-list` updates only the specified set in the specified list. Rebrickable also has broader `/users/{user_token}/sets/{set_num}/` semantics that can create or delete based on quantity; this CLI intentionally does not expose that broader mutation because it is too easy to misuse.

## Live smoke checks

Only run live smoke checks when `REBRICKABLE_API_KEY` is configured. Summarize response shape only, never private field values.

Public read-only smoke:

```bash
scripts/rebrickable sets --search "Millennium Falcon" --page-size 1
```

Optional private read-only smoke, only when `REBRICKABLE_USER_TOKEN` is configured and the user context permits private collection reads:

```bash
scripts/rebrickable profile
scripts/rebrickable set-lists --page-size 1
```

Do not run mutation smoke tests against the live API. Use `--dry-run` for write-shape verification.

## Verification

Local, no-network checks:

```bash
python3 -m py_compile scripts/rebrickable_cli.py
scripts/rebrickable add-sets-to-list --dry-run --user-token dummy --list-id 123 --sets-json '[{"set_num":"8043-1","quantity":1}]'
python3 -m unittest discover -s tests -p 'test_*.py'
scripts/validate-skills.sh
git diff --check
```
