# Content Extraction Rules (General)

Use this reference **only when you need detailed extraction guidance** for L1/L2/L3 docs.

## Entrypoints & Runtime

- Find entry files (`main`, `index`, `app`, `server`) in the language/framework.
- Capture build/run scripts from package/config files (e.g., `package.json`, `Makefile`, `pyproject.toml`, `pom.xml`).
- Note extension or deployment entrypoints (e.g., `manifest.json`, `Dockerfile`, `helm/`).

## Core Flows

- Identify primary user flows or API flows and map to modules.
- For each flow, note: input → processing → output, plus error handling.

## Data & Storage

- Note persistence mechanisms (DB, localStorage, files, caches), migration paths, and data schemas.

## Testing & QA

- Find test directories, frameworks, and critical test cases.
- Summarize how to run tests and what scenarios are essential.

## i18n / Localization

- Detect locale files and string sources; note sync requirements between app strings and platform-specific locales.
