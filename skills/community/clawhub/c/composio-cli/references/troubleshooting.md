# Troubleshooting

Use these checks for top-level CLI failures. Prefer the installed CLI's
`--help` output and live schemas over memorized flags. The error-to-action
table in [output shapes](output.md) maps each error slug to its fix.

## Command not found

```bash
command -v composio
composio --version
```

If installation just completed, use the absolute path printed by the installer
for the current task or begin a fresh terminal/session. Do not edit shell files
or install the CLI again without authorization.

When OpenClaw runs in a container or remote node, check inside that environment.
Do not copy the host's `~/.composio` directory or disable isolation as a
shortcut.

## Version too old

This skill requires CLI `0.4.0` or newer for `--no-skill-install`, `--poll`,
`--parallel`, and `tools list`. If `composio --version` reports an older
release, ask the trusted operator to authorize `composio upgrade`, then verify
the version again. Do not upgrade on your own initiative.

## Command appears to hang

`execute` without `-d` and `proxy` without `-d` wait for stdin. Stop the
command, then rerun with `-d '{}'` (or the intended data) and, for `proxy`,
`</dev/null`.

## Signed out

```bash
composio whoami
```

An empty successful response means signed out. Follow the private operator
login flow in [installation and authentication](installation.md), then
verify `whoami` again.

## Missing connection

The JSON result has `successful: false` and slug
`ToolRouterV2_NoActiveConnection`. Use the toolkit named in the message:

```bash
composio link <toolkit>
```

After authorization succeeds, retry the original operation once. Do not
replace it with an unrelated write as a connectivity test.

## Multiple accounts

List connections and ask the operator to identify the intended account:

```bash
composio connections list --toolkit <toolkit>
```

Then use `--account <alias-or-id>`. Do not silently select a different identity
after an authorization or permission error.

## Input validation failure

A `ToolInputValidationError` banner names the missing or mistyped field.
Inspect the live schema:

```bash
composio execute <SLUG> --get-schema
```

Correct field names and types rather than bypassing validation. Use
`--dry-run` when the corrected operation is a write. Dry-run validates inputs
only; it does not prove the toolkit is connected.

## Tool not found

Either a JSON result with slug `ToolRouterV2_ToolNotFound` or a banner with
HTTP 404 and code `2401`. List the toolkit's tools before searching:

```bash
composio tools list <toolkit>
```

## File upload failure

Check the schema before using `--file`. It works only when the tool exposes one
uploadable file input. Otherwise supply the relevant file field in structured
data. Confirm that the path is inside the permitted execution boundary.

## Unclear write result

Do not immediately replay the write. Query the destination or an execution
status with a narrow read, compare the intended identifier and payload, and
retry only after establishing that the first attempt did not take effect.

## Unknown command or flag

```bash
composio --help full
composio execute --help full
composio search --help full
composio link --help full
composio run --help full
composio proxy --help full
```

Do not delete CLI state, reinstall, upgrade, log out, or change organizations
as a generic repair step.
