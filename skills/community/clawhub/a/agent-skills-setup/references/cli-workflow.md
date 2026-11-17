# Public CLI workflow

Read for detection, inventory, comparison, profile-aware migration, and command
selection. `smart-ide-migration.sh` is the public wrapper. Set its path to the
installed Skill directory, independent of the project working directory:

```bash
migrator=/path/to/agent-skills-setup/scripts/smart-ide-migration.sh
```

Use concrete `<product>/<profile>` selectors from [Registry v2](registry-v2.json).
Profile aliases, supported surfaces, platforms, and manual boundaries come from
[ide-registry.md](ide-registry.md). Do not substitute paths from another product
or a different profile. Paths can use documented environment/platform overrides;
remote-host surfaces remain experimental.

| Command | Observable result |
| --- | --- |
| `detect` | Offline install/configuration/compatibility detection, with evidence. |
| `inventory` | Resolved surfaces, policy, precedence, and existence. |
| `plan` | Destination paths, statuses, diffs, losses, and rebuild actions. |
| `migrate` | Saved plan, apply manifest, and verification artifact in one flow. |
| `apply` | Execution of a saved, state-validated plan and transaction manifest. |
| `verify` | Whether recorded applied files still match their manifest. |
| `rollback` | Guarded undo using that apply manifest. |
| `snapshot` | Portable ACB directory and collection/exclusion summary. |
| `bundle-verify` | Closed-world checksum, binding, and secret checks; optional trusted signature. |
| `bundle-keygen`, `bundle-sign` | Offline Ed25519 key files or signature artifact. |
| `restore` | Destination-side plan from bundle bytes, optional apply and verify. |
| `doctor` | Complete recorded requirements, executable PATH checks, and reauthentication/rebuild actions. |
| `legacy` | Explicit lookup or zero-write dry-run compatibility only. |

Legacy preview reports stay on stdout, including when `--report` is supplied;
the named file is neither created nor changed. Use `plan --output` to save a
profile-aware plan for review and execution.

`--json` emits one JSON document on stdout; diagnostics go to stderr. Inspect
exit status, item statuses, and applied counts, not merely `ok`. Use
`bash "$migrator" <command> --help` for that command's accepted flags.

## Detect and preview the named project

```bash
bash "$migrator" detect --product cursor --profile ide \
    --workspace /path/to/project --json
bash "$migrator" inventory --product cursor --profile ide \
    --workspace /path/to/project --json
bash "$migrator" plan --source cursor/ide --target claude/code-cli \
    --workspace /path/to/project --scope project \
    --objects skills,instructions,mcp --json
```

The final command emits a preview without saving an artifact. To prepare an
authorized execution, add `--output /path/to/plan.json`, read that file's
`review_preview`, `loss_report`, and `rebuild_manifest`, and apply the same file.
Do not claim a migration from detection, plan output, or an empty inventory.
Broad `detect`/`inventory` without a product filter is for a device-wide request.

## Apply and verify a saved plan

```bash
bash "$migrator" plan --source cursor/ide --target claude/code-cli \
    --workspace /path/to/project --scope project \
    --objects skills,instructions,mcp --output /path/to/plan.json --json
bash "$migrator" apply /path/to/plan.json \
    --manifest /path/to/manifest.json --yes --json
bash "$migrator" verify --manifest /path/to/manifest.json --json
```

Follow [migration-safety.md](migration-safety.md) before execution and
[verification.md](verification.md) for delivery or rollback. Only use `--yes`
within the user's existing authorization. A saved plan locks source/target
states, Registry digest, adapter versions, and Git provenance; drift is a
failure requiring a fresh plan. Apply does not accept arbitrary source files
through legacy flags: stage user-supplied fixtures in an isolated workspace's
documented source surface when testing, without overwriting real configuration.

`--apply-safe` is the default. It applies eligible objects, defers lossy ones
unless accepted, and records manual/forbidden/conflict outcomes. Conflicts block
their target group. `--strict` rejects any non-`ready` item. `--no-apply-safe`
also requires every item to be `ready` before any target write.
`--include lossy` accepts all reviewed lossy items. `--accept-loss` on
`apply`/`migrate` names item IDs such as `3:instructions`, not bare row numbers.
Explicit loss acceptance remains necessary when the original request did not
authorize those semantics.

Instruction/MCP conversions that drop reported fields or redact credentials
are `ready-lossy`; `--yes` alone does not accept those losses. Accepted
conversions still remove unsupported fields and literal credentials. Required
Skill `.env` exclusions remain enforced without making an otherwise eligible
Skill copy require loss acceptance.

## Orchestrated migration

For an authorized scoped migration, `migrate` runs planning, apply, and verify:

```bash
bash "$migrator" migrate --source cursor/ide --target claude/code-cli \
    --workspace /path/to/project --scope project \
    --objects skills,instructions,mcp --plan-out /path/to/plan.json \
    --manifest-out /path/to/manifest.json --verify-out /path/to/verify.json \
    --yes --json
```

Use `--plan-only` when execution should stop at the plan. It still saves the
plan; use ordinary `plan --json` for a preview with no persistent output writes.
Without explicit output paths, orchestration uses `<workspace>/.migration/`;
transaction backups and default apply manifests use
`<workspace>/.agent-context-migration/`.
Choose fresh manifest and verification output paths for each execution. Existing
transaction artifacts are preserved and rejected as outputs; keep them for
verification and rollback instead of replacing them on a repeated run.

`--objects all-portable` selects `skills,instructions,mcp`. Select narrower
objects when requested; `--objects all-inventory` is for inventory/manual/forbidden
reporting, not permission to write those surfaces. Opt-in `plugins` and `handoff`
also require `--include-plugins` or `--include-session`, respectively.
Scopes are `user`, `project`, `local`, or documented unions/all as accepted by
each command; applying `migrate --scope all` requires `--yes`, while
`--plan-only` can preview it without that flag. CLI defaults differ, so pass explicit scopes instead of allowing a project request to inspect user files.

## Backup, signing, diagnostics, and recovery

Use [bundle-workflow.md](bundle-workflow.md) for `snapshot`, `bundle-verify`,
`bundle-keygen`, `bundle-sign`, `doctor`, and bundle-backed `restore`/`apply`.
Use [object-migration.md](object-migration.md) and
[mcp-migration.md](mcp-migration.md) for object-specific boundaries. Remote MCP,
cloud/UI, and unsupported adapters produce reconstruction actions, not silent
fallback copies.

The explicit `legacy` subcommand accepts retained lookup/dry-run syntax:

```bash
bash "$migrator" legacy --print-path cursor project-mcp
```

Implicit legacy flags, direct legacy-engine execution, and every legacy write
are rejected. Legacy `--source-mcp-file`, `--opencode-version`, or `--strategy`
examples cannot authorize a public write; use reviewed profile-aware plans or
manual reconstruction when the current Registry has no writable adapter.
