# AIDE Integration

Use this reference only when the user asks how to install, sync, or invoke `design-guide` across AI development environments.

## Local Source of Truth

Primary folder:

```text
~/.codex/skills/design-guide
```

Use the current repository as the source of truth. A conventional Codex installation uses the folder above; the sync script safely skips it when source and target are identical.

## Known Local Targets

Supported local skill roots:

```text
~/.codex/skills
~/.claude/skills
~/.cursor/skills
~/.qwen/skills
```

Recommended install paths:

```text
~/.codex/skills/design-guide
~/.claude/skills/design-guide
~/.cursor/skills/design-guide
~/.qwen/skills/design-guide
```

## Invocation Guide

- Codex: "use design-guide", `design-guide`, `$design-guide`, or `@design-guide` if the interface supports it.
- Claude Code: `/design-guide` when installed as a Claude skill; otherwise say "use design-guide".
- Cursor: say "use design-guide"; if it does not detect the skill, point it to the local `SKILL.md`.
- Qwen Code: say "use design-guide"; if it does not detect the skill, point it to the local `SKILL.md`.
- Unknown AIDE: add the folder to the tool's skill/rule/context directory, or paste the `SKILL.md` path and ask the agent to follow it.

## Sync

Run:

```bash
bash ~/.codex/skills/design-guide/scripts/sync-aide.sh
```

The script copies the source folder into Codex, Claude, Cursor, and Qwen skill directories. It skips any target that resolves to the source itself.

Each target is a managed mirror. Files that no longer exist in the source are removed. Repository metadata, temporary review artifacts, generated Python caches, and `.design-guide/profile.md` are excluded.

For an isolated verification or managed environment, redirect only the target root:

```bash
F_DESIGN_TARGET_HOME=/path/to/sandbox \
  bash ~/.codex/skills/design-guide/scripts/sync-aide.sh
```

The source can be overridden independently with `F_DESIGN_SRC`.

The sync command ends with a strict doctor check. A successful copy is not reported as synchronized until every public-file digest matches the source.

## Version And Upgrade Diagnosis

Check the repository version and every local AIDE mirror:

```bash
python3 scripts/design-guide-doctor.py --strict
```

Machine-readable output:

```bash
python3 scripts/design-guide-doctor.py --strict --json
```

Upgrade a Git clone source, verify it, and synchronize the local mirrors:

```bash
git -C ~/.codex/skills/design-guide pull --ff-only
python3 ~/.codex/skills/design-guide/scripts/design-guide-doctor.py
bash ~/.codex/skills/design-guide/scripts/sync-aide.sh
```

If the active source is another checkout, set `F_DESIGN_SRC` explicitly before syncing. Restart or reload each AIDE after an upgrade when it caches skill discovery.

## Compatibility Verification

Use three levels of evidence and report them separately:

1. **Installed:** the AIDE CLI and its `design-guide/SKILL.md` path exist.
2. **Synchronized:** the installed copy matches the source after documented exclusions.
3. **Invoked:** the AIDE is asked to use `design-guide` and demonstrates navigation or execution behavior in a real session.

Do not report version checks or file synchronization as successful invocation. Real invocation may contact an external model provider, so run it only when that external request is authorized.

## Project And Local Preferences

Portable default rules live in the skill folder. Personal preferences should stay outside the public skill source:

```text
.design-guide/profile.md
~/.design-guide/preferences.md
```

Use these templates when needed:

```text
references/project-profile.example.md
references/local-overrides.example.md
```

Do not hard-code private names, brands, directories, API keys, or personal taste into `SKILL.md` before publishing.

## Compatibility Principle

Do not rely on one product's invocation syntax inside the skill body. The portable contract is:

```text
Read SKILL.md and follow design-guide.
```

## CLI Language

The AIDE invocation syntax and the helper CLI locale are independent. Use `--locale zh-CN` for a single command or set `F_DESIGN_LOCALE=zh-CN` for the session. See `references/internationalization.md` for precedence, fallback, and JSON stability rules.
