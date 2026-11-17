---
name: fabric-aiops
slug: fabric-aiops
displayName: "Cisco Meraki / Catalyst / ACI & Multi-vendor Controller AIops"
summary: "Governed Cisco Meraki/Catalyst/ACI, Arista CVP & UniFi ops — 37 MCP tools with audit."
license: MIT
homepage: https://github.com/AIops-tools/Fabric-AIops
tags: [aiops, mcp, governance, cisco, meraki, aci, arista, unifi]
description: >
  Use this skill whenever the user needs to operate a network fabric through a controller API — Cisco Meraki Dashboard (full read+write), Cisco Catalyst Center / DNA Center (read subset), Arista CloudVision Portal / CVP (read subset), or UniFi Network (self-hosted controller / UniFi OS console; read subset + device restart) — a one-shot fabric health overview; organization/site/container reads (list/get, licensing, admins, org-wide device statuses, API usage); network reads (list/get, VLANs, health alerts, traffic); device reads (inventory by model MX/MS/MR/MV/MG, status, uplinks, switch ports / interface stats, wireless SSIDs); client reads (list, detail, usage, connectivity); three flagship analyses — uplink loss & latency RCA (rank worst MX WAN uplinks + cause/action), network health score (composite per-network), and config template drift (settings drifted from a bound template); and eight guarded writes (reboot, blink LEDs, update device, update VLAN, claim/remove devices, bind/unbind a config template — Meraki-only except device restart, which unifi also maps; other unmapped writes return a teaching "not supported yet" error).
  Always use this skill for "Meraki org overview", "which uplinks are worst", "uplink loss and latency", "WAN degradation RCA", "network health score", "config template drift", "list Meraki networks/devices/clients", "reboot a Meraki device", "blink device LEDs", "claim a device into a network", "bind a network to a template", "Catalyst Center site health / device health / issues", "DNA Center inventory", "CloudVision inventory / compliance / events", "UniFi site health / alarms / clients", "restart a UniFi AP or switch" when the context is a controller-managed network fabric.
  Do NOT use when the target is OT / industrial equipment (Modbus, OPC-UA, PLCs — use industrial-aiops), a hypervisor, a storage appliance, a backup product, a container/cluster orchestrator, or device-level CLI/SSH network automation (negative routing hints only).
  Covers common controller fabric operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers). The test suite is mock-based; no platform has yet been exercised against a live controller (see docs/VERIFICATION.md).
installer:
  kind: uv
  package: fabric-aiops
argument-hint: "[org/network/device id or describe your fabric task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["fabric-aiops","uvx"]},"optional":{"env":["FABRIC_AIOPS_CONFIG","FABRIC_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Fabric-AIops","emoji":"🛰️","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed network-fabric controller operations. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency. Multi-platform by construction (a platform registry): meraki (Cisco Meraki Dashboard, reference platform, full read+write), catalyst (Cisco Catalyst Center, read subset — sites stand in for organizations/networks), cvp (Arista CloudVision Portal, read subset — containers stand in for organizations/networks), and unifi (UniFi Network controller / UniFi OS console, read subset — sites stand in for organizations/networks — plus the device-restart write via a cmd/devmgr command envelope). Unmapped ops raise a teaching "not supported on <platform> yet" error; all writes are Meraki-only except UniFi device restart.
  All write operations are audited to a local SQLite DB under ~/.fabric-aiops/ (relocatable via FABRIC_AIOPS_HOME).
  Credentials: the controller secret (Meraki API key / Catalyst Center username:password / CVP service-account token / UniFi API key) is stored ENCRYPTED in ~/.fabric-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'fabric-aiops init' to onboard, or 'fabric-aiops secret set <target>' to add one. The store is unlocked by a master password from FABRIC_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var FABRIC_<TARGET_NAME_UPPER>_APIKEY is still honoured as a fallback with a deprecation warning (migrate with 'fabric-aiops secret migrate'). Meraki/CVP/UniFi secrets ride the platform auth header (Authorization: Bearer, X-Cisco-Meraki-API-Key, or UniFi's X-API-KEY) at request time; the Catalyst Center secret is exchanged via POST /dna/system/api/v1/auth/token for a short-lived X-Auth-Token (auto-refreshed once on 401). UniFi legacy cookie login (POST /api/login) is not implemented — use an API key (UniFi OS console or self-hosted Network Server 9.0+; a UniFi OS console's base_url carries the /proxy/network prefix). Secrets are held only in memory and never logged or echoed.
  State-changing operations require double confirmation at the CLI layer and support --dry-run. All write tools pass through the @governed_tool decorator (pre-check + budget guard + audit + risk-tier label) and take a dry_run preview. Mutating/reversible writes fetch the real before-state first and record a faithful inverse undo descriptor; irreversible ops (reboot, blink) record only the before-state.
  Webhooks: none — no outbound network calls beyond the configured controller REST API base URL.
  SSL: verify_ssl defaults to true; disable only for a self-signed on-prem controller proxy.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  Verification status: the test suite is mock-based; the Dashboard API paths are modelled from the public API shape and have not yet been exercised live — docs/VERIFICATION.md defines the checklist. Community-maintained; not affiliated with or endorsed by Cisco/Meraki — trademarks belong to their owners.
---

# Fabric AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by Cisco, Meraki, Arista, Ubiquiti, or any network-controller vendor.** Product and trademark names belong to their owners. Source at [github.com/AIops-tools/Fabric-AIops](https://github.com/AIops-tools/Fabric-AIops) under the MIT license.

Governed network-fabric controller operations — **37 MCP tools** over **five platforms** (Cisco Meraki Dashboard: full read+write; Cisco Catalyst Center and Arista CloudVision Portal: read subsets; UniFi Network: read subset + device restart; Cisco ACI APIC: read-only endpoint path trace, EPG segment and faults), every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.fabric-aiops/`, token/runaway budget guard, undo-token recording, and descriptive risk tiers. The controller secret is stored **encrypted** (`~/.fabric-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk.

> **Standalone**: the governance harness is bundled in the package (`fabric_aiops.governance`) — fabric-aiops has no external skill-family dependency. No platform has yet been exercised by this tool against a live controller; the ACI reads are tested against real, anonymized APIC responses from a production fabric (see `docs/VERIFICATION.md`).

## Platform support

| Platform | `platform:` | Coverage | Auth |
|----------|-------------|----------|------|
| Cisco Meraki Dashboard | `meraki` | full (all reads + all 8 writes) | API key (Bearer / X-Cisco-Meraki-API-Key) |
| Cisco Catalyst Center | `catalyst` | read subset: sites (as orgs/networks), device+site+client health, issues→alerts, inventory, interface stats | `username:password` → short-lived X-Auth-Token (auto-refresh on 401) |
| Arista CloudVision Portal | `cvp` | read subset: containers (as orgs/networks), inventory (+ complianceCode drift signal), events→alerts, users→admins | service-account token (Bearer) |
| Cisco ACI (APIC) | `aci` | **no canonical op** — three ACI-native reads instead: endpoint path trace (MAC/IP → leaf/interface → EPG → BD → VRF → contracts → filter entries, plus DN-matched fault candidates), EPG segment, fabric faults | `username:password` → `aaaLogin` session cookie (refreshed; one re-login on 401/403) |
| UniFi Network | `unifi` | read subset: sites (as orgs/networks), stat/device inventory+statuses, stat/health, alarms→alerts, stat/sta clients, device port_table→switch ports; **plus the device-restart write** (cmd/devmgr) | API key (`X-API-KEY`, stateless); base_url = classic `https://<host>:8443` or UniFi OS console `https://<console>/proxy/network` |

Ops a platform does not map — and **every write on catalyst/cvp (on unifi, every write except reboot)** — return a teaching "not supported on `<platform>` yet — open an issue or PR" error, never a silent no-op. Full matrix in the repo README.

## What This Skill Does

| Domain | Tools | Count | Read or Write |
|--------|-------|:-----:|:-------------:|
| **Overview** | fabric fleet overview | 1 | 1 read |
| **Organizations** | list/get, licensing, admins, device statuses, API usage | 6 | 6 read |
| **Networks** | list/get, VLANs, health alerts, traffic | 5 | 5 read |
| **Devices** | inventory (by model), status, uplinks, switch ports, SSIDs | 5 | 5 read |
| **Clients** | list, detail, usage, connectivity | 4 | 4 read |
| **Health (flagship)** | uplink loss/latency RCA, network health score, config template drift | 3 | 3 read |
| **Cisco ACI** (APIC targets) | endpoint path trace, EPG segment, fabric faults | 3 | 3 read |
| **Remediation** | reboot, claim, remove, bind, unbind | 5 | 5 write (high) |
| | update device, update VLAN | 2 | 2 write (medium) |
| | blink LEDs | 1 | 1 write (low) |
| **Undo** | list recorded reversible writes | 1 | 1 read |
| | apply a recorded inverse (governed, single-use, `dry_run`) | 1 | 1 write (medium) |

`network_health_score` and `config_template_drift` are injected-only (they score data you already hold); `uplink_loss_and_latency_rca` accepts injected `records` for offline analysis, or pulls live from a configured target. Meraki device models carry a product-type prefix: **MX** appliance, **MS** switch, **MR** wireless AP, **MV** camera, **MG** cellular gateway.

## Quick Install

```bash
uv tool install fabric-aiops
fabric-aiops init       # interactive wizard: platform choice (meraki/catalyst/cvp/unifi) + encrypted secret
fabric-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/fabric-aiops
openclaw skills info fabric-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Triage an organization (`overview`): network count + device status/product rollup
- Find the worst WAN uplinks (`health uplink-rca` / `uplink_loss_and_latency_rca`): ranked by loss + latency with a likely cause and action
- Score fleet health per network (`health score` / `network_health_score`): a composite 0-100, worst first, every component shown
- List/inspect organizations, networks, devices (by model), and clients
- Reboot/blink a device, update device or VLAN attributes (reversible), claim/remove devices, or bind/unbind a config template — all with dry-run + double-confirm
- On a Cisco ACI fabric: find where an endpoint (MAC/IP) attaches and which EPG / BD / VRF / contracts carry it (`aci trace` / `aci_endpoint_trace`), inspect an EPG's segment (`aci segment`), or list faults worst-first (`aci faults`)

**Do NOT use when** the target is OT/industrial equipment (use industrial-aiops), a hypervisor, a storage appliance, a backup product, a container cluster, or device-level CLI/SSH network automation.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| Cisco Meraki fabric: uplinks, health, config templates, device lifecycle | **fabric-aiops** (this skill) |
| Cisco Catalyst Center (DNA Center): site/device/client health, issues, inventory | **fabric-aiops** (this skill, `platform: catalyst`) |
| Arista CloudVision Portal: inventory, compliance drift signal, events | **fabric-aiops** (this skill, `platform: cvp`) |
| UniFi Network (self-hosted controller / UniFi OS console): site health, alarms, clients, device restart | **fabric-aiops** (this skill, `platform: unifi`) |
| Cisco ACI (APIC): endpoint location, EPG/BD/VRF/contract chain, fabric faults | **fabric-aiops** (this skill, `platform: aci`) |
| OT / industrial edge (Modbus, OPC-UA, PLC, PROFINET) | the **industrial-aiops** line |
| Hypervisor VM lifecycle (power, snapshot, migrate) | a hypervisor ops skill |
| Container/cluster lifecycle | a cluster ops skill |

## Common Workflows

### "The branch VPN keeps dropping" — diagnose degraded WAN uplinks

1. `fabric-aiops health uplink-rca` → worst MX WAN uplinks ranked by avg loss + latency, each citing the measured numbers plus a likely cause and action
2. `fabric-aiops health uplink-rca --loss-pct 2 --latency-ms 100` → tighten the thresholds if nothing crosses the defaults but users still complain
3. `fabric-aiops device uplinks` → the raw per-appliance uplink statuses across the org (WAN1/WAN2, active vs failover) behind the ranking — confirm the flagged appliance rather than trusting the summary
4. `fabric-aiops network alerts <networkId>` → check whether the controller already raised a matching alert (independent corroboration before you touch anything)
5. **Failure branch**: if the RCA returns no uplink records at all, the org has no appliances reporting uplink telemetry, or the API key lacks org-wide read — run `fabric-aiops doctor` and re-check the org id with `fabric-aiops org list` rather than assuming the WAN is healthy.

### Rank the fleet and fix the worst network's device attributes (reversible)

1. `fabric-aiops overview` → org-level rollup: network count and device status/product mix
2. `fabric-aiops health score` → composite 0-100 per network, worst first, with every scoring component shown
3. `fabric-aiops org device-statuses` → find the offline/alerting devices dragging the worst network's score
4. `fabric-aiops device status <serial>` → confirm the device before changing it
5. `fabric-aiops remediate update-device <serial> '{"name":"branch-ap-01"}' --dry-run` → preview the exact `PUT /devices/<serial>` call; then run without `--dry-run` (double confirmation). The real before-state is fetched first and recorded as a faithful inverse
6. **Failure branch**: wrong attribute or wrong device — `fabric-aiops undo list`, then `fabric-aiops undo apply <id>` restores the captured prior attributes. Re-run `fabric-aiops device status <serial>` to confirm the restore landed rather than trusting the undo's success message.

### Bring a drifted network back to its config template (reversible)

1. `fabric-aiops network list` → the networks in scope and their ids
2. Pass the template plus its bound networks to `config_template_drift(template=..., networks=[...])` → the settings that deviate, per network
3. `fabric-aiops network vlans <networkId>` → confirm the drifted VLAN's current values before changing anything
4. Fix the specific setting — `fabric-aiops remediate update-vlan <networkId> <vlanId> '{"name":"data"}' --dry-run`, then for real — or re-establish the binding itself: `fabric-aiops remediate bind <networkId> <templateId> --dry-run`, then without `--dry-run` (double confirmation). Both capture the real before-state and record an inverse descriptor (for `bind`, the inverse is unbind or a rebind to the prior template)
5. **Failure branch**: if the rebind makes things worse, `fabric-aiops undo apply <id>` returns the network to its captured prior binding; `fabric-aiops remediate unbind <networkId>` is the manual escape hatch. Re-run `config_template_drift` to confirm the drift actually cleared instead of trusting the write's success message.

### Stage a replacement device into a branch network

1. `fabric-aiops device inventory` → confirm the replacement serial is in the org inventory and unassigned
2. `fabric-aiops network get <networkId>` → confirm the target network
3. `fabric-aiops remediate claim <networkId> <serial> --dry-run` → preview `POST /networks/<networkId>/devices/claim`; then run for real (double confirmation) — the inverse (remove from network) is recorded
4. `fabric-aiops remediate blink-leds <serial> --duration 30` → low-risk physical confirmation that you are at the right box in the rack
5. `fabric-aiops health score` → confirm the network's score recovers once the device reports in
6. **Failure branch**: wrong network — `fabric-aiops undo apply <id>` or `fabric-aiops remediate remove <networkId> <serial>`. Note `fabric-aiops remediate reboot <serial>` is `no undo` by construction (a reboot has no safe inverse); it records only the before-state, so use it last, not as a first response.

### "This VM can't reach its database" — reconstruct the ACI path (read-only)

1. `fabric-aiops aci trace --ip <vm-ip>` → the endpoint's attachment (pod / leaf / interface or vPC), its EPG → bridge domain → VRF, the contracts the EPG provides/consumes down to filter entries, and faults whose DN names the EPG or the interface
2. Read `findings` first (worst-first, each with its signal): an unformed attachment or an unresolved BD/VRF/contract relation is where the configured chain breaks
3. `fabric-aiops aci trace --ip <db-ip>` → the peer's chain; compare VRFs and whether one EPG provides a contract the other consumes
4. `fabric-aiops aci faults` → fabric-wide faults worst-first, when the chain itself is clean
5. **Failure branch**: `notFound` means the fabric has not learned the address now (silent hosts age out) — not that the host is down. A section that is `null` with an entry in `errors` was not read; do not report it as absent. `staticPathResolved: true` is configuration, not proof traffic flows — this is not a reachability test, and vzAny / taboo / preferred-group rules are listed in `notChecked`, not evaluated.

### Offline analysis (no live controller)

1. Export the org's uplink, device-status, and template data to JSON
2. Feed it straight to the analysis tools — `uplink_loss_and_latency_rca(records=[...])`, `network_health_score(device_statuses=[...])`, `config_template_drift(template=..., networks=[...])` — no connection or credentials required
3. **Failure branch**: a tool that rejects the injected records means the export is missing fields the analysis needs (loss/latency samples, device status, template settings) — re-export rather than hand-editing, so the findings stay traceable to the controller.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide
whether a write is permitted. That is your agent's judgement, or the permission
of the account you connect it with (a Meraki API key whose admin has read-only
organization access — writes then fail at the controller). There is no read-only
switch, policy file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.fabric-aiops/audit.db` (relocatable via `FABRIC_AIOPS_HOME`): params, outcome summary, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `FABRIC_AUDIT_APPROVED_BY` / `FABRIC_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window trips a circuit breaker. Disable with `FABRIC_RUNAWAY_MAX=0`.
- Destructive writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI.
- Mutating/reversible writes fetch the real before-state and record an inverse descriptor (`update_device`/`update_network_vlan`→restore prior values, `claim`↔`remove`, `bind`↔`unbind`/rebind); irreversible ops (`reboot_device`, `blink_device_leds`) record only the before-state.

## References

- `references/capabilities.md` — full tool + field reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
