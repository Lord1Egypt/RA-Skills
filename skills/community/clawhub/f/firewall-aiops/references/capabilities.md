# firewall-aiops capabilities

> **35 MCP tools** (26 read, 9 write) across OPNsense (REST `/api/...`, API key+secret
> via HTTP Basic) and pfSense (REST v2 `/api/v2/...`, API key via `X-API-Key`). The
> concrete REST paths below are modelled from each project's public API and have not
> yet been exercised against a live firewall — see `docs/VERIFICATION.md`.

A per-target `platform` field (`opnsense` / `pfsense`) selects the API shape; the same
tool name resolves to the right path on each firewall via the platform registry.

## System (read)

| Tool | OPNsense path | pfSense path | Returns |
|------|---------------|--------------|---------|
| `firmware_status` | `/api/core/firmware/status` | `/api/v2/system/version` | version, product, updates available |
| `health_status` | `/api/diagnostics/system/systemInformation` | `/api/v2/status/system` | hostname, uptime, CPU %, mem %, load |
| `interface_status` | `/api/diagnostics/interface/getInterfaceNames` | `/api/v2/status/interfaces` | interfaces with link status + address (down first) |
| `gateway_status` | `/api/routes/gateway/status` | `/api/v2/status/gateways` | gateways with status, loss %, RTT |

## Rules (read)

| Tool | OPNsense path | pfSense path | Returns |
|------|---------------|--------------|---------|
| `list_rules` | `/api/firewall/filter/searchRule` | `/api/v2/firewall/rules` | filter rules normalized (uuid, enabled, action, if, src/dst, evaluations) |
| `rule_detail` | `/api/firewall/filter/getRule/{uuid}` | `/api/v2/firewall/rule?id=` | one rule's full detail |
| `rule_stats` | `/api/diagnostics/firewall/pfStatistics` | `/api/v2/firewall/rules` | per-rule hit counts / evaluations, busiest first |
| `rule_states` | `/api/diagnostics/firewall/queryStates` | `/api/v2/firewall/states` | active state-table entries tied to rules |
| `pending_changes` | (derived from `searchRule`) | (derived from `firewall/rules`) | the staged rule set `apply_changes` would commit + its lockout assessment |

## NAT (read)

| Tool | Returns |
|------|---------|
| `nat_port_forwards` | inbound port-forward (DNAT) rules |
| `nat_outbound` | outbound (source) NAT mappings |
| `nat_one_to_one` | 1:1 NAT mappings (external ↔ internal) |

## Aliases (read)

| Tool | Returns |
|------|---------|
| `list_aliases` | all aliases (name, type, description, member count) |
| `alias_entries` | the member entries (hosts/networks/ports) of one alias |

## VPN (read)

| Tool | Returns |
|------|---------|
| `wireguard_status` | WireGuard peers with connected state, last handshake, transfer |
| `openvpn_sessions` | OpenVPN sessions / connected clients (name, address, bytes) |
| `ipsec_sas` | IPsec security associations (phase-1/phase-2) with state |

## DHCP (read)

| Tool | Returns |
|------|---------|
| `dhcp_leases` | active DHCP leases (IP, MAC, hostname, state); `online_only` filter |
| `dhcp_static_mappings` | DHCP static (reserved) mappings (MAC ↔ IP) |

## Diagnostics (read)

| Tool | Returns |
|------|---------|
| `firewall_log` | recent firewall-log entries, optional `action` filter (pass/block/…) |
| `states_table` | active pf state-table entries |
| `top_talkers` | busiest source hosts, aggregated from the state table by bytes |

## Flagship analyses (read, pure heuristics)

| Tool | What it does |
|------|--------------|
| `gateway_health_rca` | rank gateways by loss (x10) + latency; flag down (status down / 100% loss) and degraded (over threshold); map each to a cause + action. Pass `gateways=` for pure analysis or a target to pull live |
| `rule_hit_and_shadow_analysis` | never-hit enabled rules (0 evaluations), rules shadowed by an earlier terminating rule, and exact duplicates; each finding names the offending/covering rule uuid |
| `blocked_traffic_rca` | aggregate blocked log rows by source; classify as port scan (≥10 distinct ports), service brute-force/probe (busy sensitive port 22/3389/…), or generic; with an action |

## Writes (governed)

| Tool | Risk | Path(s) | Notes |
|------|------|---------|-------|
| `toggle_rule` | **med** | OPNsense `toggleRule/{uuid}/{0\|1}`; pfSense PATCH `firewall/rule` | reads the rule first; records undo (restore prior enabled). Staged — run `apply_changes` |
| `add_alias_entry` | **med** | OPNsense `alias_util/add/{name}`; pfSense `firewall/alias` | captures prior entries; undo removes the added entry |
| `remove_alias_entry` | **med** | OPNsense `alias_util/delete/{name}`; pfSense `firewall/alias` | captures prior entries; undo adds it back |
| `kill_states` | **med** | `diagnostics/…/killStates` / `firewall/states` (DELETE, query-filtered) | flush pf states (optionally one source IP) |
| `restart_service` | **med** | `service/restart/{service}` | restart a firewall service; **refuses** the daemon serving this appliance's own API |
| `apply_changes` | **HIGH** | `filter/apply` / `firewall/apply` | commit staged config — makes edits live; `dry_run` returns the staged set; **refuses** a provable lockout (`override=True` to force); audited |
| `reconfigure` | **HIGH** | `filter/savepoint` / `firewall/apply` | reload/commit a subsystem; `dry_run` + audited |
| `reboot` | **HIGH** | `core/system/reboot` / `diagnostics/reboot` | IRREVERSIBLE — audit only, no undo; `dry_run` |

## Out of scope (v0.1)

- Creating/deleting rules, aliases, or NAT entries from scratch (only toggle + alias
  entry add/remove today).
- Cloud security groups and vendor firewall appliances.
- **Missing something? Open an issue or PR** — contributions welcome.

## Self-lockout guards

A firewall is the one appliance where a routine write severs the connection
carrying it — and the recorded undo needs that same connection. Three writes
refuse rather than let that happen. All of them are **exact** and **fail open**.

### `restart_service`

Refuses the daemon that answers this platform's own management API — OPNsense
`nginx` / `configd` / `php-fpm`, pfSense `lighttpd` / `php-fpm`, plus the
generic aliases (`webgui`, `web`, `webserver`, `gui`, `api`) an agent told
"restart the web service" would actually pass. The list lives on the `Platform`
descriptor, which already knows which daemon serves its own URLs. Matching is
exact and case-insensitive; an unrecognised service name is never blocked on a
guess, so `unbound`, `dhcpd`, `openvpn`, `ipsec` and friends restart normally.

### `apply_changes` / `reconfigure filter`

Both read the staged rule set first (see `pending_changes`) and refuse when
committing it would provably cut management access. Two mirror-image shapes are
dangerous:

- a **disabled `pass`** rule that permits management access — applying removes the permit;
- an **enabled `block`** rule that covers it — applying starts blocking.

"Provably" means a literal match on **both** the management host and port.
Everything short of that fails open with a named warning and proceeds:

| Warning | Meaning |
|---|---|
| `ALIAS_DESTINATION` | destination is an alias; it may resolve to the management address |
| `ANY_DESTINATION` | destination is `any` / a CIDR that may contain the host |
| `ANY_PORT` | no destination port — may include the management port |
| `PORT_RANGE` | port expression could not be parsed to a range |
| `INTERFACE_GROUP` | rule is on `any` / an interface group |

`override=True` proceeds despite a certain finding — for operators with console
access who mean it. A rule set that cannot be READ does not block either, but is
reported as `assessed: false` with the error rather than as a clean bill of
health (a failed probe is not "nothing pending").

### `toggle_rule`

Runs the same assessment at staging time — the cheapest point to warn, since the
rule row is already in hand — and reports `managementImpact` in both directions.
Advisory only: staging is never blocked, because `apply_changes` is where the
change becomes real and where the refusal lives.

### `dry_run` does not bypass the guards

A `dry_run` whose honest answer is "this would be refused" **refuses**. Previewing
success for a call that is then refused is the preview being wrong, and a weak
model reads the later refusal as transient and retries it. So:

- `apply_changes(dry_run=True)` / `reconfigure(subsystem="filter", dry_run=True)`
  run the lockout guard before returning, and honour `override=True` on both paths.
- `restart_service(dry_run=True)` refuses an API-serving service name.

- `toggle_rule(dry_run=True)` reads the rule and reports the same
  `managementImpact` the real call would.

Fail-open semantics are **identical** on both paths — a dry-run never refuses
what the real call would allow.

The CLI's `rules toggle --dry-run` routes through the governed twin, so it
reaches the same assessment **and** records the same audit row. The line's
invariant is: **a dry_run MAY read; it must never write.** A preview that cannot
read cannot answer "would this be refused?", so reads are expected; the mutating
POST/PATCH is the thing that must never happen. (`apply_changes`,
`reconfigure`, `restart_service`, `kill_states` and `reboot` have no CLI command
— they are MCP-only — so `rules toggle` is the whole CLI write surface.)

### Two pfSense reads depend on the pfSense-pkg-RESTAPI version

`wireguard_status` and `dhcp_static_mappings` read endpoints that newer
pfSense-pkg-RESTAPI builds serve and older ones do not (`/api/v2/status/wireguard/peers`,
`/api/v2/services/dhcp_server/static_mappings`). On a build that predates them the
call returns a 404 error payload naming the exact path — it is not "WireGuard is
not configured". Upgrade the package on the firewall to get those surfaces.
Everything else in this table was exercised against pfSense CE 2.7.2 with
pfSense-pkg-RESTAPI 2.4_3.

### `kill_states` is a lost response, not a lockout

Flushing the pf state table drops the state entry for this tool's own
connection, so the call can appear to fail even though the flush ran. Access is
NOT lost: the permitting rule is untouched and the next call re-establishes
state. The dry-run says so in `sessionImpact`, and the result repeats it in
`note`. **Do not retry blindly** — the flush is likely already done.

### Reversible writes survive a lost response

`toggle_rule`, `add_alias_entry` and `remove_alias_entry` stash their before-state
via `capture_prior_state()` immediately before the mutating request. If the
response is lost, the harness records `status=unknown` (not a false `error`) and
can still record the inverse, flagged `effectVerified=false`. The irreversible
writes (`apply_changes`, `reconfigure`, `restart_service`, `kill_states`,
`reboot`) declare no inverse, so they capture nothing — there is nothing to
replay.
