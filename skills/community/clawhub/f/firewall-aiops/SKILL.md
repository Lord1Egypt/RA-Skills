---
name: firewall-aiops
slug: firewall-aiops
displayName: "OPNsense / pfSense Firewall Operations"
summary: "Governed OPNsense + pfSense firewall ops: rules, NAT, VPN, DHCP, RCA. 35 tools."
license: MIT
homepage: https://github.com/AIops-tools/Firewall-AIops
tags: [aiops, mcp, governance, firewall]
description: >
  Use this skill whenever the user needs to operate an OPNsense or pfSense firewall — a one-shot overview, firmware/health, interfaces and gateways, firewall rules with hit-counts and shadow analysis, NAT (port-forward/outbound/1:1), aliases and their entries, VPN (WireGuard/OpenVPN/IPsec), DHCP leases and static mappings, the firewall log and state table, three flagship RCAs (gateway health, rule hit/shadow, blocked traffic), and governed writes (toggle a rule, add/remove an alias entry, kill states, restart a service, apply/reconfigure to make edits live, reboot).
  Always use this skill for "OPNsense", "pfSense", "firewall rule", "port forward", "NAT", "alias", "WireGuard", "OpenVPN", "IPsec", "DHCP lease", "firewall log", "blocked traffic", "why is my WAN down", "gateway loss/latency", "unused / shadowed rules", "apply firewall changes", "reboot the firewall" when the context is an OPNsense/pfSense firewall.
  Do NOT use when the target is something other than an OPNsense/pfSense firewall (a hypervisor, storage appliance, backup product, container-orchestration cluster, multi-vendor router/switch config, or OT/industrial equipment) — route those to the appropriate other AIops-tools skill. Cloud security groups and vendor firewall appliances are out of scope.
  Governed firewall operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers). Live-verified against real OPNsense 26.7 and pfSense CE 2.7.2 on top of the mock test suite; see docs/VERIFICATION.md for exactly what each run proved and what is still untested.
installer:
  kind: uv
  package: firewall-aiops
argument-hint: "[a rule/alias id, an IP, or describe your firewall task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["firewall-aiops","uvx"]},"optional":{"env":["FIREWALL_AIOPS_CONFIG","FIREWALL_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Firewall-AIops","emoji":"🛡️","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed firewall operations across OPNsense (REST API /api/..., API key+secret via HTTP Basic auth) and pfSense (REST API v2 /api/v2/..., API key via X-API-Key header). Each target in the config names its own platform, and a name-keyed platform registry selects the API shape, so the same tools work on both and one config can span a mixed estate. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.firewall-aiops/ (relocatable via FIREWALL_AIOPS_HOME).
  Credentials: the OPNsense API secret (paired with the API key) or the pfSense API key is stored ENCRYPTED in ~/.firewall-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'firewall-aiops init' to onboard (it asks for the platform), or 'firewall-aiops secret set <target>' to add one. The store is unlocked by a master password from FIREWALL_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var FIREWALL_<TARGET_NAME_UPPER>_SECRET is still honoured as a fallback with a deprecation warning (migrate with 'firewall-aiops secret migrate'). The secret is presented as HTTP Basic auth (OPNsense) or an X-API-Key header (pfSense) at request time and held only in memory; secrets are never logged or echoed.
  State-changing operations pass through the @governed_tool decorator (budget guard + audit + a descriptive risk-tier label, not a gate). The high-risk commits (apply_changes, reconfigure) and reboot are risk=high with dry_run; reboot is irreversible. Reversible writes (toggle_rule, add_alias_entry, remove_alias_entry) capture the real fetched before-state and record an inverse undo descriptor. Three writes additionally refuse to destroy the tool's own management path: restart_service refuses the daemon serving this appliance's API, and apply_changes / reconfigure refuse a staged rule set that would provably cut management access.
  Webhooks: none — no outbound network calls beyond the configured OPNsense / pfSense REST API.
  SSL: verify_ssl defaults to false-friendly for self-signed lab certs; enable for production.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
---

# Firewall AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by the OPNsense project, Deciso, Netgate, or the pfSense project.** OPNsense, pfSense and Netgate are trademarks of their respective owners. Source at [github.com/AIops-tools/Firewall-AIops](https://github.com/AIops-tools/Firewall-AIops) under the MIT license.

Governed firewall operations — **35 MCP tools** across **OPNsense** (REST `/api/...`)
and **pfSense** (REST v2 `/api/v2/...`), every one wrapped with the bundled
`@governed_tool` harness: a local unified audit log under `~/.firewall-aiops/`,
policy engine, token/runaway budget guard, undo-token recording, and
descriptive risk-tier labelling. A per-target `platform` field selects the API shape,
so the same tools work on both firewalls and one config can span a mixed estate. The
OPNsense API secret / pfSense API key is stored **encrypted**
(`~/.firewall-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk.

> **Standalone**: the governance harness is bundled in the package
> (`firewall_aiops.governance`) — no external skill-family dependency. Both platform
> halves have been exercised against real firewalls (OPNsense 26.7, pfSense CE 2.7.2)
> in addition to the mock suite; `docs/VERIFICATION.md` records what each live run
> proved, and what remains untested on each platform.

## What This Skill Does

| Group | Tools | Count | R/W |
|-------|-------|:-----:|:---:|
| **System** | firmware_status, health_status, interface_status, gateway_status | 4 | read |
| **Rules** | list_rules, rule_detail, rule_stats, rule_states, pending_changes | 5 | read |
| **NAT** | nat_port_forwards, nat_outbound, nat_one_to_one | 3 | read |
| **Aliases** | list_aliases, alias_entries | 2 | read |
| **VPN** | wireguard_status, openvpn_sessions, ipsec_sas | 3 | read |
| **DHCP** | dhcp_leases, dhcp_static_mappings | 2 | read |
| **Diagnostics** | firewall_log, states_table, top_talkers | 3 | read |
| **Flagship analyses** | gateway_health_rca, rule_hit_and_shadow_analysis, blocked_traffic_rca | 3 | read |
| **Writes** | toggle_rule, add_alias_entry, remove_alias_entry, kill_states, restart_service | 5 | write (med) |
| **Writes** | apply_changes, reconfigure, reboot | 3 | write (**high**) |
| **Undo** | undo_list, undo_apply | 2 | read / write |

The three flagship analyses are transparent heuristics that report their numbers,
never a black-box verdict: `gateway_health_rca` ranks gateways by loss + latency and
maps each down/degraded one to a cause + action; `rule_hit_and_shadow_analysis` finds
never-hit and shadowed/redundant rules; `blocked_traffic_rca` classifies the noisiest
blocked sources as scan / brute-force / probe.

## Quick Install

```bash
uv tool install firewall-aiops
firewall-aiops init       # wizard: pick platform (opnsense/pfsense) + encrypted secret
firewall-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/firewall-aiops
openclaw skills info firewall-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Get a one-shot snapshot (`overview` / `firmware_status` / `gateway_status`)
- Investigate a down/degraded WAN (`gateway_health_rca`) → cause + action
- Audit the ruleset (`rule_stats` hit counts, `rule_hit_and_shadow_analysis` for
  never-hit / shadowed / redundant rules)
- Triage hostile traffic (`firewall_log --action block`, `blocked_traffic_rca`,
  `top_talkers`)
- Inspect NAT, aliases, VPN tunnels (WireGuard/OpenVPN/IPsec), and DHCP leases
- Safely toggle a rule or edit an alias (`toggle_rule` / `add_alias_entry` /
  `remove_alias_entry`, reversible + undo-recorded), then **make it live** with
  `apply_changes` (dry-run + audit)

**Do NOT use when** the target is not an OPNsense/pfSense firewall — route hypervisor,
storage, backup, cluster, multi-vendor router/switch config, or OT/industrial work to
the appropriate other AIops-tools skill.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| OPNsense / pfSense firewall ops | **firewall-aiops** (this skill) |
| A non-firewall platform (hypervisor, storage, backup, cluster, network config, OT edge) | the appropriate **other AIops-tools** skill |
| Cloud security groups / vendor firewall appliances | out of scope for this tool |

## Common Workflows

The CLI surface is `init` / `doctor` / `overview` / `log` / `rules` / `secret` / `undo`;
the flagship RCAs, NAT / alias / VPN / DHCP reads, and the remaining governed writes are
MCP tools (start the server with `firewall-aiops mcp`). Recipes below say which is which.

### 1. "The internet keeps dropping" — WAN gateway triage

1. `firewall-aiops doctor` → confirm the firewall is reachable and the secret unlocks
   (a red doctor means you are debugging credentials, not the WAN).
2. `firewall-aiops overview` → one-shot: firmware/version, gateway + interface health,
   rule count. Down interfaces sort first.
3. MCP `gateway_health_rca` → gateways ranked worst-first, each row citing its measured
   loss % and RTT, mapped to a cause (last-mile loss / congestion / latency / hard down)
   and a concrete action. The ranking is computed on an internal score that is not
   returned, so weigh each row's own numbers rather than trusting the order.
4. If the RCA points at a stuck daemon rather than the circuit, MCP
   `restart_service(service="dpinger", dry_run=true)` to preview, then re-run for real
   (medium risk, audited, undo-recorded).
5. Re-run `firewall-aiops overview` to confirm the gateway came back green.
6. **Failure branch**: if the restart does not clear it, the gateway is genuinely down
   upstream — stop touching the firewall and escalate to the ISP. If the restart made
   things worse, `firewall-aiops undo list` → `firewall-aiops undo apply <id>` reverses
   the recorded inverse. Do **not** reach for `reboot` (high risk, irreversible, no undo)
   until a read confirms it is the only remaining option.

### 2. Ruleset spring-clean — retire a rule that never fires

1. MCP `rule_hit_and_shadow_analysis` → enabled rules with 0 evaluations (dead or
   misordered), rules shadowed by an earlier terminating rule, and exact duplicates —
   each finding names the offending and the covering rule uuid.
2. `firewall-aiops rules list --interface wan` → confirm the candidate's position in the
   evaluation order (a "never hit" rule below a broad allow is misordered, not useless).
3. `firewall-aiops rules show <uuid>` → read the full rule before touching it.
4. `firewall-aiops rules toggle <uuid> --disable --dry-run` → prints the exact call,
   changes nothing.
5. `firewall-aiops rules toggle <uuid> --disable` → double-confirm; the write fetches the
   rule's real prior enabled flag and records an inverse undo descriptor with an `_undo_id`.
6. MCP `pending_changes` → read what the commit would actually make live, including
   whether any staged rule covers the endpoint this tool manages the firewall through.
   `toggle_rule` already reported `managementImpact` in step 5 if so.
7. MCP `apply_changes` to commit the staged config — **risk=high**, so set
   `FIREWALL_AUDIT_APPROVED_BY` and `FIREWALL_AUDIT_RATIONALE` first. It refuses
   outright if a staged rule would provably cut management access; pass
   `override=True` only with console access in hand.
8. **Failure branch**: if traffic breaks after the commit, `firewall-aiops undo apply <id>`
   restores the rule's prior enabled state, then `apply_changes` again to make the
   restoration live. The toggle is staged until applied — before step 6 you can simply
   toggle it back with no commit at all.

### 3. Brute-force against the WAN — block the source with an alias

1. `firewall-aiops log --action block --limit 100` → the raw recent blocks, so you are
   reading real log lines and not just a summary.
2. MCP `blocked_traffic_rca` → noisiest blocked sources ranked and classified (port scan,
   service brute-force on 22/3389/…, or generic probe), each with a recommended action.
3. MCP `top_talkers` and `states_table` → cross-check whether the source also has
   *established* states, i.e. whether anything already got through.
4. MCP `list_aliases` → find your blocklist alias, then `alias_entries(<alias>)` to see
   what is already in it.
5. MCP `add_alias_entry(alias=<blocklist>, entry=<src-ip>)` → medium risk, reversible,
   undo descriptor recorded from the fetched before-state.
6. MCP `apply_changes` (high risk, audited) to make the alias live, then
   `kill_states(source=<src-ip>)` to tear down any states the attacker already holds.
7. **Failure branch**: if you blocked too wide a range and locked out legitimate traffic,
   MCP `remove_alias_entry` (or `firewall-aiops undo apply <id>`) and `apply_changes`
   again. If you locked *yourself* out of the web UI, the CLI still works over the API
   as long as the management rule was untouched — recover there before rebooting.

### 4. Verify and roll back a change window

1. Before the window: `firewall-aiops overview` and `firewall-aiops rules list` → capture
   the baseline you intend to return to.
2. Make the staged changes (`rules toggle`, MCP alias edits), each one dry-run first.
3. MCP `apply_changes` with `FIREWALL_AUDIT_APPROVED_BY` set → commit.
4. Validate: `firewall-aiops overview`, MCP `gateway_health_rca`, and
   `firewall-aiops log --action block --limit 50` → make sure the change did not start
   silently dropping wanted traffic.
5. `firewall-aiops undo list` → every reversible write in the window, newest first, with
   its `_undo_id`.
6. **Failure branch**: roll the window back in reverse order with
   `firewall-aiops undo apply <id>` per entry, then one final `apply_changes` to commit
   the rollback. Writes that declare **no** undo (`reboot`, and `apply_changes` itself)
   cannot be reversed this way — they are audit-only, which is why every reversible edit
   goes in *before* the commit.

> **Authorization is not this skill's job**: there is no read-only switch, policy
> file, or approval gate. Whether a write runs is the agent's judgement or the
> connecting account's permissions — point the tool at an API user without write
> scope and writes fail at the server. Every call is still audited.
> `FIREWALL_AUDIT_APPROVED_BY` / `FIREWALL_AUDIT_RATIONALE` are optional audit
> annotations, recorded when set but never required.

## Governance & Safety

- Every tool is audited to `~/.firewall-aiops/audit.db` (relocatable via
  `FIREWALL_AIOPS_HOME`).
- High-risk ops (`apply_changes`, `reconfigure`, `reboot`) are labelled risk=high
  and audited; `FIREWALL_AUDIT_APPROVED_BY` / `FIREWALL_AUDIT_RATIONALE` are
  optional audit annotations, recorded when set but never required.
- Writes support `--dry-run` and double confirmation at the CLI. `reboot` is
  irreversible (audit only).
- Reversible writes capture the real fetched before-state and record an inverse
  descriptor (toggle→toggle-back, add-alias↔remove-alias).

## References

- `references/capabilities.md` — full tool + platform + API-path reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
- `docs/VERIFICATION.md` — live-verification checklist (what the mock suite covers, and what a real-firewall run must prove)
