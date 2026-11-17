# Migration safety and conflicts

Read before previewing or writing migration targets. Use the user's requested
products, objects, workspace, and scope. Infer ordinary defaults from the request:
a named project implies project scope; personal context needs user scope. Inspect
other products only for a requested device-wide inventory or backup. Ask when a
profile, destination, conflict choice, or authorization is materially ambiguous.

An explicit request to move, apply, restore, or undo context authorizes that
scoped action, including necessary planning and verification. Retain prior
authorization across turns. Preview-only requests authorize no target writes;
if the user forbids all writes, use `plan --json` without `--output`. Writing a
plan or bundle is still an artifact write. `--yes` records authorization for
execution; it never supplies missing user consent. Ask before expanding scope,
accepting unapproved semantic loss, or resolving a conflict that the request
does not settle.

## Review and execute the plan

Resolve concrete profiles using [ide-registry.md](ide-registry.md). Review both
canonical and compatibility locations; ambiguous alternatives produce conflicts.
Use documented precedence where it resolves the choice, and retain activation
and directory hierarchy when instructions have multiple files.

Save the plan before execution and review each destination, diff, loss report,
and rebuild action. Apply that exact file. Its checksum binds the Registry,
adapter versions, resolved surfaces, source/target states, and Git provenance.
Changed inputs require a new plan and review; renewed user approval is needed
only when the revised action exceeds existing authorization. `migrate` performs
planning, apply, and verification in one invocation; use separate `plan`/`apply`
when the user wants to inspect or approve the exact artifact first.

The default safe apply writes eligible items and records deferred ones. Inspect
the resulting counts and reasons; a successful verification does not mean every
requested item migrated. Instruction/MCP conversions with reported losses are
`ready-lossy` and deferred until accepted; `--yes` alone is insufficient.
Required Skill environment-file exclusions still apply to eligible copies.
`--strict` requires all items to be `ready`.
`--include lossy` accepts all lossy items; `--accept-loss` on `apply`/`migrate`
accepts selected item identifiers. See [the CLI guide](cli-workflow.md).
Neither option authorizes previously unapproved loss. Executable draft surfaces
remain review/rebuild actions and are never activated by safe apply.

Apply stages and validates outputs before target mutation, snapshots destinations,
and records a checksummed manifest. Write or manifest failure restores earlier
mutations in reverse order. Existing targets are backed up under
`<workspace>/.agent-context-migration/backups/`; public profile-aware commands
do not expose legacy `skip`/`backup`/`overwrite` strategies. MCP migration preserves
unrelated settings while replacing the selected server map; inspect added,
removed, and changed servers in the saved preview. Bulk restore merges selected
bundle sources before writing and reports conflicts. Do not invent renamed
fallback servers.

Plan, manifest, bundle, extraction, and key outputs must not overlap selected
sources/targets or the Registry. Reject symlink escapes and credential-bearing
objects; exclude `.env` and `.env.*` from Skill copies. Keep source bytes intact.
Shared configuration transfers only the authorized subobject, including when
the registry uses plain file storage. Trust, credentials, approvals, raw history,
and generated memory never become portable objects.

## Bundles and recovery

For backup, destination-side restore planning, signing, or dependency diagnostics,
read [bundle-workflow.md](bundle-workflow.md). A restore source is the verified
bundle; an installed source product on the destination device cannot override it.
Review-only restore can stage ephemeral source files and optionally save a plan;
`--restore-root` explicitly requests a persistent extraction tree. Extraction
alone does not prove that any destination product received context.

Use [verification.md](verification.md) for applied-state evidence and guarded
rollback. No step here installs or launches plugins, contacts MCP servers,
changes trust, or performs authentication. Cloud/UI and remote MCP require
reviewed reconstruction; [mcp-transport.md](mcp-transport.md) defines that boundary.

The explicit `legacy` subcommand permits lookup and zero-write dry-runs only.
Implicit legacy flags and all legacy writes are rejected; execute saved
profile-aware plans instead.
