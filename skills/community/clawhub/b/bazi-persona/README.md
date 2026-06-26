# Bazi Persona for OpenClaw

OpenClaw edition of the Bazi Persona skill.

This package keeps the existing runtime, prompts, and knowledge model intact, but adapts installation, packaging, and runtime guidance for OpenClaw so the host is less likely to misread it as a source project that needs to be rebuilt.

## Install

Use OpenClaw's native skill installer:

```bash
openclaw skills install bazi-persona
```

ClawHub page:
https://clawhub.ai/xiaojxiao2021/bazi-persona

Start a new OpenClaw session after install so the skill snapshot refreshes.

## What This Bundle Contains

- `SKILL.md`: OpenClaw-specific runtime and calling guidance
- `dist/`: prebuilt runtime files
- `prompts/`: prompt and knowledge files used by the runtime
- `package.json`: runtime dependency declaration for hosts that install dependencies automatically

## Runtime Expectations

This is a prebuilt runtime package.

- Do not treat it as a source project by default
- Do not run `npm run build` just because `package.json` exists
- Do not add `tsconfig.json`, `src/`, or other source files
- If the host installs runtime dependencies from `package.json`, that is fine
- Only fix dependencies when there is an explicit missing-runtime-dependency error

## Data Storage

Persona data is file-based.

Default location:

```text
<current-skill-dir>/personas
```

Overrides:

- `--base-dir`
- `BAZI_PERSONA_HOME`

If a path has not been verified, do not guess it. If a directory does not exist, report that exact fact instead of inferring memory-only or hidden storage.

## OpenClaw-Specific Notes

OpenClaw can load same-named skills from multiple places. In practice, use the currently verified active skill directory as the source of truth and avoid guessing precedence from memory.

When troubleshooting:

1. Verify the active skill directory first.
2. Verify `dist/`, `prompts/`, `package.json`, and `SKILL.md` are present.
3. Verify runtime dependencies only if there is an explicit missing dependency error.
4. Do not escalate missing paths into a source rebuild workflow.
