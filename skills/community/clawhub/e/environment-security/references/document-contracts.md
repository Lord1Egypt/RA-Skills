# Document Contracts

Use this reference when the task is to generate or refresh environment guardrail docs from actual machine state.

## Output Set

Keep these files distinct:

- `environment-baseline.json`
  - Machine-readable source of truth.
  - Store verified tool paths, versions, env vars, PATH highlights, targeted check results, and the detected document language.
- `ENVIRONMENT_POLICY.md`
  - Human-readable master policy.
  - Record the approved environment inventory and the hard rules other agents must obey.
- `AGENTS.environment.md` or an `AGENTS.md` environment section
  - Short, operational rules for agents.
  - Focus on what to read first, what not to change, and how to behave when tools are missing.
- `SKILL.environment.md` or another skill's environment section
  - Reusable snippet for skills that rely on local machine facts.

## Baseline Rules

- Read the existing baseline first if it exists.
- If the baseline is missing, detect the current machine and create it before writing policy docs.
- When only one tool or one task changed, do a targeted verification instead of a full rescan.
- Update JSON and human docs together.
- Do not claim a tool exists until it was verified with a command path or an explicit user-provided path.

## Language Rules

- Detect the current machine language and generate Chinese docs for `zh*` locales and English docs for `en*` locales.
- If the locale cannot be recognized, default to English.
- Keep the JSON baseline language metadata in sync with the rendered docs.
- Allow explicit overrides such as `--lang en` or `--lang zh` when the caller needs deterministic output.

## Facts Worth Recording

- Tool label, executable path, and version.
- Whether the selected executable came from baseline reuse, env-var hints, or PATH lookup.
- Relevant env vars such as `JAVA_HOME` and `MAVEN_HOME`.
- Important PATH entries.
- Shims, wrappers, launchers, or symlinks when they differ from the real install path.
- Service or database checks when the task depends on them.

## Required Hard Rules

Carry these ideas into every generated environment doc:

- Do not install, upgrade, uninstall, or auto-configure tools without explicit user approval.
- Do not silently modify `PATH`, `JAVA_HOME`, `MAVEN_HOME`, or other env vars.
- If a required tool is missing, tell the user what is missing, why it is needed, and which executable path or install directory should be returned after installation.
- Prefer user-managed installation.
- Only install a missing tool yourself when the user explicitly requests and authorizes that action.
- Treat shims, wrappers, launchers, aliases, and symlinks as entry points, not as install roots.

## Update Checklist

Before finishing, verify that:

1. The JSON baseline matches the current verified facts.
2. The human-readable policy reflects the same paths and versions.
3. Newly introduced tools were verified instead of assumed.
4. Missing tools are described as missing, not silently omitted.
5. The language of the generated docs matches the detected or explicitly requested language.
6. The hard rules still forbid unapproved environment changes.
