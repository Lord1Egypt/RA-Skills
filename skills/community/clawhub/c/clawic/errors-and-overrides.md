# Errors and Overrides - Clawic CLI

## No results for an obviously real skill

Likely causes:
- the query is too abstract
- the target words are not in slug, name, description, or summary
- the active registry base is not the one you think it is

Better move:
- rewrite the query into exact nouns
- run `clawic registry`
- inspect a likely slug directly with `show`

## Request failed with 404

Likely causes:
- bad slug
- wrong `CLAWIC_REGISTRY_BASE_URL`
- registry layout is incompatible with the expected JSON paths

Check:

```bash
clawic registry
clawic show <slug>
```

## Install fails because files already exist

That is expected when the target path already contains the same filenames and `--force` was not set.

Safer options:
- choose a fresh `--dir`
- inspect the destination first
- use `--force` only when overwrite is intentional

## Custom Registry Override

Example:

```bash
export CLAWIC_REGISTRY_BASE_URL=https://example.com/registry
clawic registry
clawic show some-skill
```

The alternate registry must expose the same shape:
- `index.json`
- `skills/<slug>.json`
- `files[].downloadUrl` values that are reachable

## Node or package execution problems

If the CLI fails before any registry fetch:
- confirm Node.js 20+
- retry with `npx clawic registry`
- if a global install is stale, reinstall the package
