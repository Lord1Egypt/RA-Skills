# `.Docker-Encyclopedia/` Cache Layout

Use this directory as the workspace-local data root for the skill.

## Directory tree

```text
.Docker-Encyclopedia/
  docs/
    docs.docker.com/
      ... cached official docs pages ...
  notes/
    components/
      ... per-component notes ...
    patterns/
      ... reusable Docker notes ...
  inventory/
    access.md
    topology.md
    doc-index.md
```

## Placement rules

### `docs/`
Store cached copies of official Docker docs here.

Mirror the official docs path as much as practical.
Example:

```text
https://docs.docker.com/engine/reference/commandline/run/
->
.Docker-Encyclopedia/docs/docs.docker.com/engine/reference/commandline/run/index.md
```

### `notes/components/`
Store environment-specific component notes here.

Suggested filenames:
- `engine.md`
- `compose.md`
- `registry.md`
- `buildkit.md`
- `networking.md`

### `notes/patterns/`
Store reusable operational notes here.

Examples:
- `compose-deployments.md`
- `image-build-cache-gotchas.md`
- `volume-backup-restore.md`
- `rootless-docker-notes.md`

### `inventory/`
Store environment-wide inventories here.

Suggested files:
- `access.md`
- `topology.md`
- `doc-index.md`

## Cache philosophy

Do not mirror the whole docs site eagerly.
Cache only the pages you actually consulted and expect to be useful later.
