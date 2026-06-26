# Docker Encyclopedia Workflow

## Core stance

Use official Docker docs plus local observed state together.

Default order:
1. check `.Docker-Encyclopedia/` cache/notes
2. check official docs when needed
3. inspect live environment state
4. answer or act
5. record durable learnings

## When docs lookup is mandatory

Do a docs lookup before answering or acting when any of these are true:
- the user asks about Docker command syntax, feature semantics, or configuration behavior
- the task involves Dockerfiles, BuildKit/buildx, Compose, registries, networks, volumes, daemon/rootless config, or credential handling
- the task involves a version-sensitive feature or a behavior you are not highly confident about
- the task involves live CLI/config work and the command path or safety boundaries matter

## Cache-first rule

Before fetching docs, check whether the needed material already exists under:
- `.Docker-Encyclopedia/docs/docs.docker.com/...`
- `.Docker-Encyclopedia/notes/components/...`
- `.Docker-Encyclopedia/notes/patterns/...`
- `.Docker-Encyclopedia/inventory/...`

If the local cache is good enough, use it.
If not, fetch/check the official docs and then cache what you used.

## How to cache docs

Use `scripts/cache_doc.py`.

Typical usage:

```bash
python3 scripts/cache_doc.py \
  --url 'https://docs.docker.com/engine/reference/commandline/run/' \
  --root '<workspace>/.Docker-Encyclopedia'
```

The script will:
- fetch the page
- convert it into a normalized markdown-ish cache file
- place it under `.Docker-Encyclopedia/docs/docs.docker.com/...`
- add metadata such as source URL and fetch timestamp

## How to store local knowledge

### Component notes

Use `.Docker-Encyclopedia/notes/components/<component-name>.md` for:
- component purpose
- access path
- role in deployment
- sensitive boundaries
- discovered quirks

### Pattern notes

Use `.Docker-Encyclopedia/notes/patterns/<topic>.md` for:
- recurring build/runtime patterns
- repeated gotchas
- safe operational sequences
- environment-specific design conventions

### Inventory files

Use `.Docker-Encyclopedia/inventory/` for:
- deployment/access inventory
- topology/runtime layout
- documentation index

## Distinguish evidence types

When writing notes, label information mentally as one of:
- **Official docs** — from Docker documentation
- **Observed local state** — from live environment inspection
- **Inference/recommendation** — your judgment based on docs + local state

Do not blur these together.

## Recommended answer style

When it helps, mention whether your answer is based on:
- cached official docs
- freshly checked official docs
- live environment inspection
- best-practice inference

## High-sensitivity areas

Treat these as high-sensitivity even when you have live access:
- daemon config and auth/credential changes
- image/volume/network pruning or destructive cleanup
- Compose deployment changes
- registry/login/push behavior
- rootless/socket/permission changes
- changes that could break running containers, storage, or host reachability

For these, prefer docs lookup even if you think you remember the command or config path.
