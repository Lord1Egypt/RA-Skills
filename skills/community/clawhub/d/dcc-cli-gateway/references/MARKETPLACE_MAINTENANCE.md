## Marketplace Intent — Search Unless the Exact ID Is Known

Requests to find, compare, or recommend a DCC-MCP marketplace Skill use the official CLI catalog when the request concerns DCC-MCP.
A generic marketplace request alone does not select this ecosystem. Install/update requests without
an exact package ID follow the same discovery path:

```bash
dcc-mcp-cli marketplace search --query "maya rigging" --limit 20
dcc-mcp-cli marketplace inspect <exact-name-from-search>
```

Marketplace discovery does not require a live DCC instance. Do not apply
the live-inventory `total == 0` stop rule to `marketplace search` or `inspect`.
Use the user's capability words first. If there are no results, retry once with
a shorter capability query or without the DCC filter; never invent a package
name or substitute a web recommendation for the CLI result.

Catalog entries may be a Skill, legacy multi-Skill bundle, or Agent Plugin. When present, read
`entry.package.format` and `entry.package.skills`; install, update, and uninstall the package once, not each component.

Installing or updating changes local state. Inspect unfamiliar packages and obtain user consent before
`marketplace install` or `update`. For a known exact ID, install directly with `--reload`, then use
`load-skill` only when needed. The Python REST fallback does not implement marketplace commands, so
a missing CLI follows the consent-gated official CLI installation path below.
Normal CLI invocations reuse the existing cached update mechanism; do not add a
synchronous ecosystem scan or call `update check` before every command. Follow
the TTL, backoff and notification guidance in UPDATE_INSPECTION.md. Report
observed updates and ask confirmation before `marketplace update`.
`uninstall --reload` removes and refreshes; omit `--dcc` only for a package installed on one DCC.

## Updates and Marketplace Maintenance

For version truth, compatibility/pin evidence, release notes, known fixes,
offline status, and reviewed diagnostic drafts, follow
[Version and Update Evidence](UPDATE_INSPECTION.md). Use its safe-entry-point
check before invoking an older CLI: even a query can activate a staged update
in builds that apply updates before argument parsing.

Use the gateway release manifest for binary checks. An available binary must have a valid SHA-256; `update apply` verifies it during download, binds one component to the exact CLI installation, and re-verifies it before replacement and restart. Legacy unsigned staging is quarantined. A running server must be updated in its own environment. The Admin Instances panel is check-only for every binary because the gateway cannot prove an installation root. See the CLI cheatsheet for platform manifests, server updates, and the verified `dcc-cua` sibling contract.

```bash
dcc-mcp-cli update check
dcc-mcp-cli update apply
```

For marketplace Skills, search first when the exact package ID is not known:

```bash
dcc-mcp-cli marketplace search --query "maya rigging" --limit 20
dcc-mcp-cli marketplace inspect <package_name>
dcc-mcp-cli marketplace install <package_name> --dcc maya --reload
dcc-mcp-cli marketplace install <profile_package_name> --target game:the-bazaar
```

`--query "maya rigging"` remains supported for scripts. Search and inspect are
read-only; install/update require consent. Inspect is optional when the exact
package ID is already known, and `--dcc` is optional for single-DCC packages.
Catalog Git installs require a full commit object ID and ZIP installs require a
valid SHA-256 before I/O. Direct `marketplace add-repo` installation requires `--commit <40-hex-oid>`; only its read-only `--list` mode may omit it.
After updates or installs without `--reload`, run `reload-skills`; then use `load-skill` only if the adapter did not auto-load it.

Use `install` for adapter plans, never for marketplace Skills:

```bash
dcc-mcp-cli install --dcc-type maya
```
Ask before `--execute`, follow the returned `next_steps`, and do not treat
package installation as live registration. Pip plans must preserve the catalog-pinned artifact; see the CLI cheatsheet. If no standard DCC is found, ask for an absolute path and pass `--dcc-path`. If auto-install is disabled, show
the returned policy prompt and hand off to the named deployment owner.

The CLI is the **default agent-facing control plane**. The Python fallback uses
the same gateway REST endpoints only when the CLI is unavailable after a verified install attempt fails.
The gateway still serves MCP for IDE clients in parallel; choosing this skill does not replace or disable the IDE MCP path.
