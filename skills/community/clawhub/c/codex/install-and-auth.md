# Install and Auth

## Minimum Readiness Check

Confirm the CLI exists before thinking about prompts or repo work:

```bash
codex --version
codex --help
```

If the binary is missing, install Codex through the current official OpenAI distribution path instead of random third-party wrappers.

## Login Paths

Prefer an existing Codex login session when one already exists:

```bash
codex login status
```

If login is required, use the interactive flow:

```bash
codex login
```

If the environment intentionally uses an API key flow:

```bash
printenv OPENAI_API_KEY | codex login --with-api-key
```

## First Safe Run

Start with a no-surprises command in a known repo:

```bash
codex exec -C /path/to/repo -s read-only -a on-request \
  "Inspect this repository and summarize the stack, entrypoints, and test surface."
```

This proves auth, working directory, and basic execution before any write-capable run.

## App Versus CLI

`codex app` launches the desktop app path. That is not the same as `codex app-server`.
Use the CLI first unless the user explicitly wants the app or an IDE integration path.
