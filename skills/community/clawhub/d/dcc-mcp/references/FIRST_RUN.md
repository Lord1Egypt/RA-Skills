# First run: explain the environment before operating it

Use this flow on the first request in a new environment or when the user asks
what is installed, registered, ready, or installable. Reuse observations for the
current task; do not make a whole-machine inventory before every tool call.
A new Skill installation does not prove the CLI or any host is installed.

## 1. Check the CLI without accidentally updating it

From this Skill's directory, run:

```bash
python scripts/first_run_report.py --pretty
```

The helper checks the selected executable's availability without launching it,
reads the existing user-provided app-path cache, and labels bundled product
metadata as a snapshot. It never scans the filesystem, contacts a gateway,
installs, launches, or uploads anything. Missing on this lookup means missing
from the selected path, not absent everywhere. A cached path is not proof of a
working installation. Unknown versions remain null.

If missing, explain that the Skill is present but the CLI is needed for the
requested workflow. After setup consent, use the existing SHA-verified helper:
`python scripts/check_cli.py --ensure-cli --pretty`. Do not create another
installer, use an unreviewed shell download, or reinstall after a health error.
An installed but failing CLI needs diagnosis, not an installation assumption.

Before version queries or discovery, follow the safe-entry check in
[UPDATE_INSPECTION.md](UPDATE_INSPECTION.md). Unknown/older builds can activate
staged updates even for `--version` or `--help`. Do not invoke them to discover
whether they are safe. Inspect their package/release metadata first; if safe
support is unknown, show the official upgrade option and obtain approval before
using the existing verified installation owner. Do not claim a minimum release
from a merged source change alone.

## 2. Collect the existing reports at the right boundary

For an inspection-capable binary, capture `update inspect --offline` or an
online inspection when freshness is needed. Preserve both the original report
and its source evidence; installed receipt, executing CLI, bundled Core, and a
separately running gateway/adapter are different versions.

The host commands already own local software discovery and provisioning:

```bash
dcc-mcp-cli --output json host list
dcc-mcp-cli --output json host doctor
```

Prefer `host doctor <exact-host-id>` when the task names one host. `host list`
reports manifest versions, licence classes and platform install channels;
`host doctor` uses existing executable overrides, PATH and known roots, then
runs bounded version probes. It does not prove adapter installation or live
control. Hosts outside this manifest, project-local plugins, custom forks and
unqueried versions remain unknown. Use the existing app-path cache for an
explicit user path; do not build a parallel scanner.

Important: these host handlers do not install, but their normal CLI startup can
activate an already staged update. The early read-only gate currently covers
`update inspect` and `update discover`, not `host`, `list`, or `dcc-types`.
Do not describe the whole invocation as mutation-free or run it during an
unapproved staged upgrade. Verify startup state through the owning install
workflow, or use an isolated, verified test installation with no staged update.
Never clear a staged update, alter a pin, or interrupt a running job just to
complete onboarding.

For an authorized live workflow, use `list` and the local or remote branch in
[ZERO_INSTANCES_CLI.md](ZERO_INSTANCES_CLI.md). Only local observations may use
`dcc-types --dcc-type <dcc>`; never merge a local FileRegistry result into remote
runtime evidence. `list` may ensure a local gateway. Keep this lifecycle action
separate from read-only report composition.

Save explicitly selected, current-environment JSON outputs and compose them:

```bash
python scripts/first_run_report.py --cli <selected-cli> \
  --host-manifest host-list.json --host-report host-doctor.json \
  --decision local-blender-decision.json --update-report update-inspection.json --pretty
```

Each `--decision` accepts one existing Core discovery-decision v1 object and
can be repeated for different products. This first report is local-only:
`--runtime-scope remote` fails closed before projecting local host/cache evidence.
Use the separate remote workflow above instead. The helper does not fetch, execute commands from, or attest the
origin of these files. The agent must bind them to this environment, selected
binary and current observation. Do not supply stale output from another task.
Failed probes can still return valid structured evidence with a nonzero exit
code; preserve it. Missing, malformed or unavailable output is unknown, never
an empty successful inventory. The report omits executable paths, free-form
hints, raw errors, machine names and returned command text; it is still local
onboarding information, not permission to publish diagnostics.

### Provider identity limit

Rows combine only identical identifiers and retain `identity.host_id` and
`identity.dcc_type`; `product` is null for an identifier absent from the bundled
product catalog. Do not infer a product mapping from a display name or fuzzy
alias. For example, current Core host metadata uses `substance` while the
adapter/catalog uses `substance3d_painter`. This tranche keeps those as separate
observations and does not claim a complete one-row-per-application inventory.
Use the original host ID for host commands and the adapter's canonical DCC type
for adapter commands. A reviewed source-owned crosswalk is follow-up work.

## 3. Explain the useful next step

The report keeps host probe/version, cached path, adapter installation,
registration, direct readiness, callability and real-host effect separate.
Current Core discovery decisions do not inspect installed adapter packages, so
`adapter_installed` remains unknown even though the published decision schema
reserves additional states. Positive registration/readiness requires a positive
observed instance count; contradictory evidence is downgraded to unknown.


- `available_for_discovery`: registered and directly ready. Search the requested
  capability and describe the returned exact-instance tool before a call.
  This category never claims that a tool is callable or has succeeded.
- `configuration_needed`: host/path or registration evidence exists, but ready
  typed control is not established. Follow the adapter's existing install or
  bootstrap instructions and diagnose the returned readiness reason.
- `install_available`: the current platform has a manifest-pinned open-source
  host installation channel. This is an offer, not permission or proof that the
  host is absent. Check the relevant probe and exact plan before installation.
- `unknown`: observations are absent or incomplete. Say what is missing without
  claiming that the software is unsupported or uninstalled.

A concise first reply can be: “CLI found; its running version is not yet safely
verified. Blender is detected but its adapter is not registered. OBS has an
official installation route. Which would you like to use?” Replace every part
with actual evidence and omit irrelevant products.

When the user chooses an open-source host, use the existing
`dcc-mcp-cli host install <exact-host-id>` workflow only after consent. It reads
the manifest and lock, checks the platform channel and refuses commercial
hosts. Do not copy a version out of a conversation into an installer. Review
whether the install command remembers consent before selecting `--yes`.
Host installation and `dcc-mcp-cli install --dcc-type <dcc>` adapter installation
are separate steps. Recheck host, registration, readiness, exact tool schema,
and the actual requested effect afterward. Never automatically launch a host.

For new ecosystem software, use [SOFTWARE_REQUEST.md](SOFTWARE_REQUEST.md).
For latest catalogs and updates, use [UPDATE_INSPECTION.md](UPDATE_INSPECTION.md).
