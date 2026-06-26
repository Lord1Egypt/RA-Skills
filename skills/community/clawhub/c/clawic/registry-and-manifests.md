# Registry and Manifests - Clawic CLI

## Default Registry Base

The package defaults to:

```text
https://raw.githubusercontent.com/clawic/skills/main/registry
```

This can be replaced with `CLAWIC_REGISTRY_BASE_URL` when the user intentionally wants a compatible alternate registry.

## Fetch Flow

### `search`

1. Fetch `index.json`
2. Score results locally
3. Print matching skills

The query text is not sent to a hosted search backend by the CLI itself.

### `show`

1. Fetch `skills/<slug>.json`
2. Read the manifest fields
3. Print a human-readable summary

### `install`

1. Fetch `skills/<slug>.json`
2. Iterate over `manifest.files`
3. Download each `downloadUrl`
4. Write each file into `<root>/<slug>/<path>`

## Manifest Model

Useful fields exposed by the registry:
- `skill.slug`
- `skill.name`
- `skill.description`
- `skill.summary`
- `skill.version`
- `skill.homepage`
- `skill.repositoryPath`
- `repository.owner`
- `repository.repo`
- `repository.branch`
- `files[].path`
- `files[].downloadUrl`

Treat `files[]` as the install contract. If a path is absent there, `install` will not create it.
