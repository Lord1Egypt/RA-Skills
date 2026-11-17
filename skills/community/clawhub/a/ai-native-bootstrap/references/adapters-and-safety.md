# Agent adapters, capability boundaries, and deployment caveats

Version: 1.0 · Validation date: 2026-11-13

## Runtime install directories

| Agent | User scope | Project scope | Canonical repository instructions |
|---|---|---|---|
| Codex | `~/.agents/skills/ai-native-bootstrap` | `<repo>/.agents/skills/ai-native-bootstrap` | `AGENTS.md` |
| Claude Code | `~/.claude/skills/ai-native-bootstrap` | `<repo>/.claude/skills/ai-native-bootstrap` | `CLAUDE.md` (point to shared `AGENTS.md` if appropriate) |
| OpenCode | `~/.config/opencode/skills/ai-native-bootstrap` | `<repo>/.opencode/skills/ai-native-bootstrap` | `AGENTS.md` |

OpenCode also discovers some `.agents/skills` and `.claude/skills` locations. Installing the same ID in multiple discoverable directories can cause precedence surprises; install only one source per agent unless deliberate. Skill discovery should be checked in a fresh agent session, not inferred from file existence.

Documentation checked (links, not permission grants):
- https://developers.openai.com/api/reference/cli
- https://developers.openai.com/blog/skills-agents-sdk
- https://opencode.ai/docs/skills
- https://code.claude.com/docs/en/skills

## Project policy ownership

- The canonical cross-tool project policy is `AGENTS.md` **only if the repository has no existing canonical policy**. Never auto-overwrite a preexisting file.
- Where Claude needs a bootstrap pointer, a minimal `CLAUDE.md` can instruct it to read `AGENTS.md`. This is **advisory** and must be tested with the installed Claude environment; we do not assume a loader performs any special import.
- Existing CI scripts, project documentation or company policies may already be authoritative. Link to them rather than duplicating their full content.

## Guardrail truth table

| Control | Can enforce by itself? | Required backing |
|---|---|---|
| Skill instructions | No | Tests, reviewer, CI, runtime permissions |
| AGENTS.md / CLAUDE.md | No | Repository/host permissions and verification |
| Local hooks | Partial | Remote branch protection, CI and service-side authorization |
| CI file present | No | CI must actually run; branch protection must be separately verified |
| `check.py` exit 0 | Only enabled checks passed | Correct coverage, real test cases, approved environment |
| Production gate claimed | No without remote proof | Deployment credentials, environment protection, server-side policy |

The provided `bootstrap.py` intentionally never creates a production hook, deploys, pushes, edits CI credentials, installs dependencies, enables evaluation calls, or executes application checks. Those steps require project-specific review and independent authorization.

## Scope, risks and migration

- `audit` / `plan` / `verify` are read-only. `init` without `--apply` is also read-only.
- `init --apply`: refuses dirty Git states, default/protected branch names (`main`, `master`, `trunk`), symlinked ancestors, existing conflicting target files; no commits or remote operations.
- New empty non-Git directories may bootstrap, but audit reports traceability missing. Existing non-Git projects must first establish isolation/version control.
- `init --upgrade --apply` adds only missing files, never overwrites changed templates or existing rules; migration of existing content requires explicit human review.
- `install --upgrade --apply` verifies the previously installed manifest and refuses locally modified installations; it preserves the old copy in a timestamped backup on disk.
- The check runner reads an explicit JSON command array with `shell=False`; no automatic invocation of guessed commands. That alone is **not** a sandbox. Only run trusted project commands in an environment without live production credentials.
- If a detected candidate script is ambiguous or may have side effects (e.g. `postinstall`), treat it as untrusted, even if its name looks like `test`.

## Results and status semantics

The bootstrapper can establish D01–D04 and D08 artifacts, but not real project D05/D06 or remote D07 proof by itself. Thus, after the scaffold phase the overall project integration is **CONDITIONAL**, never FULL PASS, until follow-through tests and remote controls are independently confirmed. The bundle itself can pass isolated fixture tests without implying integration success on a real repository.
