# Zero instances — typed discovery and setup

Use this guide when local `dcc-mcp-cli list` reports `total: 0`, or when a
selected remote profile reports no matching live instance. A zero inventory is
only runtime-registration evidence. It does not prove that the application is
unsupported, uninstalled, impossible to bootstrap from a project, or
incompatible because of a version string or custom fork.

Do not run `search`, `describe`, or `call` without a live matching instance and
an identity returned by discovery. Read-only catalog inspection, diagnosis, and
install planning are safe before mutation consent.

## Select the evidence boundary

Determine whether the zero-instance result came from the local profile or a
named remote gateway before choosing a command. These branches are mutually
exclusive: never use a local registry decision or its `next_action` as evidence
for a remote gateway.

### Remote zero-instance branch

When `list --gateway <name>` or the selected non-local profile reports zero
matching instances, keep that remote result as the only runtime-registration
evidence. Do not run the targeted local `dcc-types --dcc-type <dcc>` decision
and do not execute a `next_action` produced from the local FileRegistry.

First inspect the catalog without a registry filter:

```bash
dcc-mcp-cli --output json dcc-types
```

Match the requested DCC against exactly one canonical `dcc_type`. Only after an
exact match may you generate the read-only plan:

```bash
dcc-mcp-cli --output json --non-interactive install --dcc-type <dcc>
```

If there is no exact catalog match, keep public support, package installation,
project bootstrap, version compatibility, and custom-fork compatibility
unknown. Do not generate an install plan from a fuzzy or inferred match. A plan
is guidance only; it is not remote inventory, readiness, or real-host evidence.

### Local zero-instance branch

Confirm the requested DCC type, then run the versioned local decision:

```bash
dcc-mcp-cli --output json dcc-types --dcc-type <dcc>
```

The command does not start a gateway. Its `schema_version: 1` result follows
Core's
[`dcc-discovery-decision-v1.schema.json`](https://github.com/dcc-mcp/dcc-mcp-core/blob/main/contracts/dcc-discovery-decision-v1.schema.json)
contract and keeps these facts independent:

| Gate | What it proves |
|------|----------------|
| `public_adapter` | The bundled public catalog has a matching adapter; a missing row remains unknown support rather than an unsupported verdict. |
| `released_catalog` | The selected DCC appears in the bundled release catalog. A custom catalog is reported as unknown, never as the released catalog. |
| `package_installation` | Package state observed by an installation check. Catalog presence alone leaves this unknown. |
| `adapter_import` | Whether the adapter imports in its owning runtime. Inventory does not answer this. |
| `project_bootstrap` | Whether an adapter-owned project plugin can be configured. A machine-wide miss does not prove a project-local plugin absent. |
| `registry_registration` | Whether the local FileRegistry contains a live matching row. |
| `direct_readiness` | Whether a matching local row is ready for direct typed control. |
| `gateway_capability_index` | Whether the live instance has been indexed by the gateway. |
| `search_hit` | Whether a targeted capability search returned a matching hit. An absent hit is not adapter-absence evidence. |
| `exact_instance_call` | Whether an exact instance-qualified call was run and passed. |
| `real_host_effect` | Whether the real host visibly or structurally accepted the requested effect; fixtures and package checks are not this proof. |
| `uncertainties` | Unresolved `version`, `custom_fork`, and `real_host` evidence. |
| `failure_stage` / `failure_reason` | Bounded public-safe failure classification, without paths, PIDs, host names, project names, or credentials. |
| `next_action` | One safe argv and its consent requirement. |

`live_instances: 0` means zero matching live registry rows were observed in the
local FileRegistry. `live_instances: null` means the registry observation was
unavailable or the requested identifier was invalid. Neither value proves any
of the earlier installation, bootstrap, or support gates. Keep every
unobserved gate `unknown`.

Only in this local branch, when `next_action` reports
`requires_consent: false`, execute its `command` argv exactly. For a bundled
catalog adapter with zero live rows, this is the plan-only
`install --dcc-type <dcc>` command and may include the public adapter-owned
`instructions_url`. The plan is evidence and guidance; it does not install a
package, modify a project, launch a host, or prove a real-host effect.

When `direct_readiness` is `not_ready`, follow the returned `wait-ready`
action before capability search. Search only after readiness, and call only a
slug or exact instance identity returned by that live search.

The targeted decision reads only the local FileRegistry. Return to the remote
branch above whenever the selected runtime boundary is not local.

## Legacy CLI fallback

If the installed CLI rejects `--dcc-type` on `dcc-types`, preserve the same
boundaries with the older read-only commands:

```bash
dcc-mcp-cli --output json dcc-types
```

Match only an exact canonical catalog identifier. If no row matches, report
catalog absence and unknown public support; do not infer package absence,
project-plugin absence, version incompatibility, or an unsupported host. Only
after an exact match, generate the plan:

```bash
dcc-mcp-cli --output json --non-interactive install --dcc-type <dcc>
```

The `read-install-instructions` URL remains the adapter-owned setup source.
Updating the CLI is a separate consent-gated operation.

## Diagnose local startup state

Run `dcc-mcp-cli doctor` when the selected profile, registry, or gateway state
is unclear. Local `list` first ensures the loopback gateway and then reads the
FileRegistry. DCC adapters register through their sidecar/server runtime;
package installation alone does not create a row.

If a row exists but `direct_control.ready=false`, inspect its bounded
`direct_control.diagnostics.failure_stage` and `failure_reason`, then use the
typed `wait-ready` action. Do not switch to generic UI automation.

## Mutation consent

Before executing installation, editing a project or environment, enabling a
plugin, or launching a GUI application, confirm:

1. The exact DCC product and project or host runtime in scope.
2. Whether the user wants commands suggested or executed.
3. Any adapter-owned `--project`, `--dcc-path`, or host-Python input required
   by the returned installation instructions.
4. That the user will complete authentication, licensing, purchase, security,
   and native confirmation steps themselves.

Until consent is explicit, do not pass `--execute`, edit environment files,
modify project configuration, or launch a host. A read-only decision or plan
with `requires_consent: false` does not authorize its later mutating steps.

When the host application itself is missing, ask one concise follow-up before
choosing a setup path: “未发现 `<dcc>` 的可用实例。你已经安装它了吗？如果没有，
是否需要我提供或执行官方安装方式？” If the product record has `host_install`,
show that official HTTPS source. Keep this separate from
`dcc-mcp-cli install --dcc-type <dcc>`, which installs the DCC-MCP adapter and does
not prove that the host application is installed. Never download, install, or
launch the host from a missing path without the user's explicit consent.

For a CLI-managed open-source or portable application, follow
[host software deployment](HOST_SOFTWARE_DEPLOYMENT.md). Its software manifest,
version probe and install receipt do not establish an adapter catalog entry,
MCP registration, readiness or native document effect. Reuse existing explicit
authorization when it already covers the same download, installation and launch.

## Source-only adapter review

A maintained adapter repository can precede a released installation route. If
the requested work already authorizes source development and setup, inspect its
exact reviewed commit and adapter-owned `install.md`; catalog absence still
leaves released support unknown. Do not fabricate an installable catalog match
or substitute an unpinned package-name install for a source checkout.

An explicitly selected local catalog must keep its `explicit` provenance.
Core's pinned Git install step verifies and checks out the full commit, then
checks the resulting files. It does not install the Python package into a
runtime, import its entry point, or start the adapter. Follow the owning runbook
for those separate steps, then verify live registration, ready dispatch and the
requested native effect. A successful source run does not update the released
product snapshot or the official signed installation feed.

## Plan and bootstrap

Build the plan using the exact argv from the decision. For a legacy CLI, use:

```bash
dcc-mcp-cli --output json --non-interactive install --dcc-type <dcc>
```

Read the plan's `read-install-instructions` URL first. That adapter-owned
runbook decides whether `--project`, `--dcc-path`, a host Python interpreter,
or manual editor/plugin enablement is required. Do not infer those inputs from
a screenshot, display name, registry miss, or version string.

After mutation consent, add only the arguments required by that runbook. Use
`--execute` only when the catalog plan supports it and
`install_policy.auto_install_enabled=true`:

```bash
dcc-mcp-cli install --dcc-type <dcc> --python "<dcc-python>" --execute
```

Game-engine hosts need the same evidence separation:

- Unreal can use a project-mounted plugin and engine-bundled Python path; do
  not require legacy Remote Execution or an optional native bridge unless the
  current adapter contract does.
- Unity and supported Tuanjie builds share the adapter-owned compatibility
  decision; a `t` version string is not an unsupported verdict.
- Godot may use a project-local EditorPlugin plus an external sidecar; a
  machine-wide inventory miss does not prove that addon absent.

These are routing boundaries, not real-host acceptance claims. Preserve
version and custom-fork uncertainty until the owning adapter's compatibility
check runs.

After installation or bootstrap:

1. Start or enable the adapter-owned host plugin.
2. Run `dcc-mcp-cli doctor`.
3. Re-run `dcc-mcp-cli list` and select the exact row.
4. Run `dcc-mcp-cli wait-ready --dcc-type <dcc>` when needed.
5. Search for the requested capability.
6. Call only the returned instance-qualified slug, then verify the real-host
   effect through an authoritative typed readback.

If no Python runtime or trusted studio package manager is available, stop and
ask the operator to provision one. Never fetch and execute an installer through
an unreviewed shell pipeline.
