# File-backed object migration

Read with [migration-safety.md](migration-safety.md) for non-MCP objects.

| Object | Handling |
| --- | --- |
| Skills | Preflight all source text, then copy credential-free named directories as units. |
| Rules / Instructions | Parse and emit the selected product's native frontmatter; never flatten conditional activation into an unconditional file. |
| Prompts / Commands | Produce reviewed native-format reconstruction actions; no automatic writer. Check Gemini TOML and UI/enterprise libraries only when selected. |
| Workflows / Cron / Automation | Record reconstruction actions and required target engine features; no automatic writer or activation. |
| Config / project | Manual-only; never copy whole config or opaque trees. |
| Agents / Droids / Modes / Personas | Report native permission, event, and command schemas to rebuild; `draft-disabled` is a plan status, not proof that a file was generated. |
| Hooks | Review lifecycle event mapping and command permissions; no shell script is written to a live product surface. |
| Plugins / Extensions | With `--objects plugins --include-plugins`, copy compatible registry-declared packages as units after preflight; no installation or execution. Other packages produce manual rebuild actions. |
| Handoff | With `--objects handoff --include-session`, serialize only reviewed summary, branch, selected relative file list, and explicit patch; reject private runtime state. |
| Sessions / Chat logs | Strictly non-transferable; runtime conversation logs and state are excluded from migration (handoff uses strict whitelist serialization). |
| Memory / Context | Do not copy or inspect private/generated state outside scope (e.g. `~/.cline/data` generated memory); the user may select reviewed context to rewrite as rules. |
| Bundles (ACB) | Package reviewed objects into secret-redacted offline `.acb` directories; use [bundle-workflow.md](bundle-workflow.md) for allowlists, subobject isolation, signatures, and replayable restore plans. |

Treat living or generated files, including Replit `replit.md`, as manual conversation state rather than overwrite targets. When no compatible target format is documented, describe reconstruction instead of an unvalidated copy. There is no generic embedded-config exception: a sub-object is automatic only when Registry v2 names a reviewed source and target adapter for the exact profile/version.

For Skill copies, preserve upstream `SKILL.md`, references, scripts, and assets
as one package; exclude environment files and reject credential findings or
unsafe links before copying. Do not optimize or rewrite a migrated skill's
instructions as part of migration unless the user separately requests that edit.
When using ACB for scripts, check the recorded `files[].mode` and the restored
executable bits as described in [bundle-workflow.md](bundle-workflow.md);
content hashes alone do not prove permission preservation. No copied script is
executed or activated by migration.
For instructions, preserve scoped activation and hierarchy. Review dropped
frontmatter and same-name changes before accepting any loss.

The reviewed instruction adapters use native fields for Augment (`type`), Cline/Claude (`paths`), Cursor and Continue (`alwaysApply`/`globs`), Kiro (`inclusion`/`fileMatchPattern`), Copilot (`applyTo`), Trae/Qoder (`alwaysApply`), and Windsurf (`trigger`). Unknown frontmatter is reported as loss. A conversion becomes manual when the target cannot preserve `always`, glob, model-decided, or manual activation semantics.
