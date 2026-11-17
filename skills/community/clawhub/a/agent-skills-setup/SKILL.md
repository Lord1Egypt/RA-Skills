---
name: agent-skills-setup
version: "0.10.2"
compatibility: Requires local Bash, Python 3, environment lookup, and filesystem access; optional signing needs installed cryptography; no network access.
description: >-
  Use when a user wants to migrate, back up, restore, compare, or move
  AI-coding-agent context across Cursor, Claude Code, Codex, Cline,
  Copilot, Windsurf, Gemini CLI, or another registered profile, including
  switching computers. Handles Skills, instructions/rules, and MCP with
  secret redaction, preview, verification, rollback, and portable bundles;
  compatible plugin packages and reviewed handoff are available by explicit opt-in.
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - python3
---
# Agent Skills Setup

## Permissions

- Run bundled local Bash/Python helpers and offline discovery only; network access is forbidden. No downloads, installations, or MCP connections.
- Read selected products, requested scopes, workspace, bundles, and named keys. Broad discovery needs a device-wide request; environment lookup resolves paths without exposing credentials.
- Write authorized targets, named plan/bundle/key outputs, and transaction state. `--yes` records existing user authorization for apply/restore/rollback; it does not grant authorization.

## Choose the workflow

- Infer products, objects, workspace, and scope from the request and established context. Project migration uses project scope; include user surfaces only when requested. Ask only for material information or authorization that cannot be inferred.
- An explicit move/apply/restore/rollback request authorizes that scoped action. Preserve prior authorization; preview-only requests stop after preview. Review exact destinations and losses before writing; ask for unresolved conflicts, unapproved losses, or broader scope.
- Save the plan, review its diff/rebuild manifest, and apply that exact file for execution. Changed inputs require a fresh plan and review.

| Request | Entry point and guidance |
| --- | --- |
| Detect or inventory context | `detect`, `inventory`; [registry](references/ide-registry.md) and [CLI guide](references/cli-workflow.md). |
| Compare or preview migration | `plan --json`; [migration safety](references/migration-safety.md). Saving `--output` writes a plan artifact. |
| Migrate context | Saved `plan` → `apply --yes` → `verify`; `migrate` orchestrates the same stages. [CLI guide](references/cli-workflow.md). |
| Back up or switch computers | `snapshot`, `bundle-verify`, `doctor`, `restore`; [bundle workflow](references/bundle-workflow.md). |
| Sign or authenticate a bundle | `bundle-keygen`, `bundle-sign`, `bundle-verify --trusted-key`; [bundle workflow](references/bundle-workflow.md). |
| Verify or undo applied changes | `verify`, `rollback --yes`; [verification](references/verification.md). |

Resolve both product profiles through [ide-registry.md](references/ide-registry.md) / [registry-v2.json](references/registry-v2.json) for migration; use bundle manifest selectors for restore.

1. Read only the selected profiles' `references/ides/<source>.md` and `references/ides/<target>.md` files. Resolve concrete filenames through the [profile index](references/ide-registry.md) and registry reference/alias routing; filenames need not match selectors.
2. Before preview or apply, read [migration-safety.md](references/migration-safety.md).
3. For MCP, read [mcp-migration.md](references/mcp-migration.md); for other objects, [object-migration.md](references/object-migration.md). Load [verification.md](references/verification.md) for delivery evidence.

## Supported boundaries

- Automatic writers cover `skills`, `instructions`, and reviewed local stdio `mcp`. `plugins` needs `--include-plugins` and compatible package surfaces; `handoff` needs `--include-session` and whitelisted reviewed context.
- Prompts, commands, agents, hooks, workflows, and unsupported formats produce review/rebuild actions. Never auto-activate executable content or migrate credentials, trust, approvals, raw history, or generated memory.
- Shared config migration extracts only the authorized subobject and preserves unrelated settings. Cloud/UI and remote MCP remain manual; support is determined per surface, not by product name.
- Use the explicit `legacy` subcommand for lookup/dry-run compatibility only; legacy writes are disabled.
- Deliver artifact paths, applied/deferred counts, verification, backups, and remaining manual work. Parsing proves file validity; runtime and connectivity need their own evidence.
