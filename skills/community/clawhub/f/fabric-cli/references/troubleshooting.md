# Fabric.so CLI troubleshooting

## `fabric: command not found`

Likely causes: Fabric.so CLI is not installed, the install directory is not on `PATH`, the shell has not been restarted after installation, or the user installed Microsoft Fabric `fab`, which is a different CLI.

Checks:

```bash
command -v fabric || true
command -v fab || true
python3 scripts/fabric_check.py --json
```

If only `fab` exists, explain that this skill targets Fabric.so `fabric`, not Microsoft Fabric `fab`.

## CLI exists but help/version fails

Run `fabric --version` and `fabric --help`. Check aliases/functions, executable permissions, platform compatibility, and whether the binary is actually Fabric.so CLI.

## Authentication failure

Symptoms include unauthorised, forbidden, not logged in, token expired, or browser login errors. Use `fabric login` in an interactive terminal, or `fabric auth "$FABRIC_API_KEY"` only with a securely supplied key. Do not print or save API keys.

## Browser login is impossible in a headless environment

Options: run `fabric login` on a machine with a browser if credentials sync appropriately, use `fabric auth` with a secure API-key route, or ask the user to complete setup locally and rerun read-only checks.

## Wrong workspace

Run:

```bash
fabric --json workspace current
fabric --json workspace list
fabric workspace select "Workspace Name"
fabric --json workspace current
```

Before writes, report the target workspace.

## JSON output fails or is not parseable

Possible causes: `--json` placement changed, the command does not support JSON in the installed version, error messages are printed alongside JSON, or CLI version differs from docs. Retry without JSON, run command-specific help, parse text only if small and unambiguous, and do not assume a schema from memory.

## Parent path not found

Check with `fabric --json path "Parent"` and `fabric --json path "Parent/Child"`. Create the missing folder only if the user asked for it or it is necessary for the requested write. Otherwise ask where to place the item.

## File upload fails

Check `test -f "$PATH" && stat "$PATH"`. Possible causes include nonexistent path, quoting/tilde expansion, file size, permissions, or quota. Check `fabric --json subscription` for quota issues.

## Task update fails

Common mistake: calling `fabric task done "Review PR"` with a title. Public docs show ID syntax. Correct pattern:

```bash
fabric --json task list --todo
# choose TASK_ID from results
fabric --json task done "$TASK_ID"
```

If multiple tasks match, ask the user to disambiguate. Never invent a task ID.

## Ambiguous Fabric request

If the user mentions Microsoft Fabric, Power BI, OneLake, lakehouse, KQL, tenant, capacity, pipeline, semantic model, or `fab`, do not use Fabric.so commands. If the user mentions Daniel Miessler's Fabric, patterns, YouTube summarisation, `fabric --pattern`, or `yt`, this is also not Fabric.so CLI.

## Large output or noisy search results

Add tags or path filters, search for quoted project names or unique phrases, use `fabric ask` for synthesis over many items, or save raw output to a temp file and summarise only selected entries.

## Command not listed in this skill

Use live help and avoid guessing. If unavailable, suggest Fabric MCP, the web app, or API.
