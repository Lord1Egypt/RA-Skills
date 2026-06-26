# Command Patterns - Clawic CLI

## Install the CLI

```bash
npm install -g clawic
clawic --version
```

For one-off use without a global install:

```bash
npx clawic registry
```

## Search

```bash
clawic search pocketbase
clawic search "skill installer" --limit 5
```

Use exact nouns the target skill is likely to contain in its slug, name, or description.

## Show

```bash
clawic show pocketbase
```

Typical output includes:
- skill name and slug
- description
- version and homepage when present
- repository path
- file count
- source repository and branch
- optional summary

## Install

```bash
clawic install pocketbase
clawic install pocketbase --dir ./vendor-skills
clawic install pocketbase --dir ./vendor-skills --force
```

Behavior:
- default root: `./skills`
- final directory: `<root>/<slug>/`
- without `--force`, existing files cause a write failure

## Registry Base

```bash
clawic registry
CLAWIC_REGISTRY_BASE_URL=https://raw.githubusercontent.com/clawic/skills/main/registry clawic registry
```

`registry` prints the active base URL. It does not validate the host or manifest shape.
