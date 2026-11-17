# fabric-aiops capabilities

> 37 MCP tools (28 read, 9 write) over five platforms —
> Cisco Meraki Dashboard (reference, full read+write), Cisco Catalyst Center
> (read subset), Arista CloudVision Portal (read subset), UniFi Network (read
> subset + device restart), Cisco ACI APIC (three ACI-native reads). The first
> four platforms' API paths are modelled from the public API shapes and need live
> verification; the ACI reads are built against real, anonymized APIC responses.
> Community-maintained; not affiliated with Cisco/Meraki/Arista/Ubiquiti.

Meraki hierarchy: **organizations → networks → devices**. Device models carry a
product-type prefix: **MX** appliance, **MS** switch, **MR** wireless AP, **MV**
camera, **MG** cellular gateway.

**Multi-platform**: the tables below show the reference (Meraki) API per tool.
On `catalyst`, canonical organizations/networks are **sites**
(`/dna/intent/api/v1/site`, `site-health`), device statuses come from
`device-health`, alerts from `issues` (P1→critical, P2→warning), inventory from
`network-device`, switch ports from per-device `interface` stats (pass the
device uuid), and clients from `client-health` (aggregate) / `client-detail`
(by MAC). On `cvp`, organizations/networks are **containers**
(`/cvpservice/inventory/containers`), devices come from
`/cvpservice/inventory/devices` (rows carry the `complianceCode` config-drift
signal), alerts from `getAllEvents.do`, and admins from `getUsers.do`.
On `unifi`, organizations/networks are **sites** (`/api/self/sites`; the
canonical id is the site's short name — the `/api/s/{site}/` path segment),
device inventory/statuses come from `stat/device` (state 1 → online; uptime,
firmware), switch ports from the device detail's `port_table` (pass the device
**MAC** where Meraki takes a serial), clients from `stat/sta` / `stat/user`,
alerts from `stat/alarm` (`*_Lost_Contact` → critical), `network_get` from
`stat/health` (per-subsystem rollup), and `reboot_device` maps to
`POST /api/s/{site}/cmd/devmgr {"cmd": "restart-device", "mac": ...}` — the
only non-Meraki write. Device-scoped calls fill the site from the target's
default `org_id`. Auth is a UniFi API key (`X-API-KEY`); a UniFi OS console's
`base_url` carries the `/proxy/network` prefix.
Any tool a platform does not map — and **every write on catalyst/cvp (on
unifi, every write except reboot)** — returns a teaching "not supported on
<platform> yet — open an issue or PR" error instead of a silent no-op. The
full per-op matrix is in the repo README.

## Read tools (28)

### Overview + organizations
| Tool | Meraki API path | Returns |
|------|----------------------|---------|
| `overview` | `/organizations/{id}/networks` + `/devices/statuses` | organizationId, networks, devicesTotal, devicesByStatus, devicesByProductType |
| `org_list` | `GET /organizations` | id, name, url, apiEnabled |
| `org_get` | `GET /organizations/{id}` | one org detail |
| `org_licensing` | `GET /organizations/{id}/licenses/overview` | status, expiration, per-device-type counts |
| `org_admins` | `GET /organizations/{id}/admins` | name, email, access level |
| `org_device_statuses` | `GET /organizations/{id}/devices/statuses` | total, byStatus, byProductType, devices[] |
| `org_api_requests` | `GET /organizations/{id}/apiRequests/overview` | totalRequests, rateLimited429, responseCodeCounts |

### Networks
| Tool | Meraki API path | Returns |
|------|----------------------|---------|
| `network_list` | `GET /organizations/{id}/networks` | id, name, productTypes, tags |
| `network_get` | `GET /networks/{id}` | one network detail |
| `network_vlans` | `GET /networks/{id}/appliance/vlans` | id, subnet, applianceIp |
| `network_alerts` | `GET /networks/{id}/health/alerts` | total, bySeverity, alerts[] |
| `network_traffic` | `GET /networks/{id}/traffic` | applicationCount, topApplications[] (by bytes) |

### Devices
| Tool | Meraki API path | Returns |
|------|----------------------|---------|
| `device_inventory` | `GET /organizations/{id}/devices` | total, byModelFamily, matched, devices[] (filterable by model) |
| `device_status` | `GET /organizations/{id}/devices/statuses` | one device's status row |
| `device_uplinks` | `GET /organizations/{id}/uplinks/statuses` | appliance/gateway WAN uplink statuses |
| `switch_ports` | `GET /devices/{serial}/switch/ports` | MS port configuration |
| `wireless_ssids` | `GET /networks/{id}/wireless/ssids` | MR SSIDs (number, name, enabled) |

### Clients
| Tool | Meraki API path | Returns |
|------|----------------------|---------|
| `client_list` | `GET /networks/{id}/clients` | clients seen in the window |
| `client_get` | `GET /networks/{id}/clients/{clientId}` | description, MAC, IP, VLAN, manufacturer |
| `client_usage` | `GET .../clients/{clientId}/usageHistory` | samples, totalSentKb, totalReceivedKb, totalKb |
| `client_connectivity` | `GET .../clients/{clientId}/connectionStats` | assoc, auth, dhcp, dns, success |

### Health (flagship)
| Tool | Source | Returns |
|------|--------|---------|
| `uplink_loss_and_latency_rca` | `GET /organizations/{id}/devices/uplinksLossAndLatency` or injected `records` | uplinksEvaluated, degradedCount, thresholds, worst[]{serial, uplink, avgLossPct, avgLatencyMs, degraded, cause, action}, note |
| `network_health_score` | injected only | networksEvaluated, fleetScore, summary, weights, worst[]{networkId, score, band, onlinePct, uplinkHealthPct, alertPenalty}, note |
| `config_template_drift` | injected only | templateId, boundNetworks, driftedCount, compliantCount, settingsChecked, driftedNetworks[]{networkId, deviations[]}, note |

`uplink_loss_and_latency_rca` accepts `records=` for offline analysis or pulls
live from a `target`/`org_id`. `network_health_score` and `config_template_drift`
are injected-only (they score data you already hold, e.g. from
`org_device_statuses` / `device_uplinks`).

### Cisco ACI (APIC targets only)

ACI maps **no canonical operation** — the tools above answer an `aci` target
with a teaching error. These three take ACI references instead:

| Tool | APIC queries (all GET) | Returns |
|------|------------------------|---------|
| `aci_endpoint_trace` | `class/fvCEp` by `eq(fvCEp.mac,…)` + `rsp-subtree=full` (or `class/fvIp` by `eq(fvIp.addr,…)`, then the owning `fvCEp`); the EPG / BD / VRF / contract / filter reads of `aci_epg_segment`; `faultInst` under the EPG and under each attachment leaf | `endpoints[]` (`returned/limit/truncated`), each with `attachment` (pod, nodes, interface or vPC, `state`, `tCl` as sent), `endpoint.recordedPathMatch` (`exact` / `vpc-member` / `differs` / null — how APIC's `fabricPathDn` relates to the formed attachment; null = not compared), `tagRelations` (listed apart — never a path verdict), `epg`/`bd`/`vrf`/`contracts`, `relatedFaultCandidates` (DN-matched, active first), `staticPathResolved`, ranked `findings`, `errors`, `notChecked`; `notFound` when the address is not learned |
| `aci_epg_segment` | `mo/<epg>` `rsp-subtree=children&rsp-subtree-class=fvRsBd,fvRsProv,fvRsCons,fvRsConsIf,fvRsProtBy`; `mo/<bd>` (`fvRsCtx,fvSubnet`); `mo/<vrf>`; `mo/<contract>` `query-target=subtree&target-subtree-class=vzBrCP,vzSubj,vzRsSubjFiltAtt,vzInTerm,vzOutTerm,vzRsFiltAtt`; `mo/<filter>` `target-subtree-class=vzEntry` | `epg`, `bd` (subnets), `vrf` (`policyEnforcement`), `contracts` (subjects → filters with action/direction → entries), `segmentResolved`, ranked `findings`, `errors`, `notChecked` |
| `aci_faults_list` | `class/faultInst` by `eq(faultInst.severity,…)`, one query per level in severity order, `page-size` = what is still needed + 1 | `faults[]` (`rank`, `active` from severity, `delegated`, `scope`/`pod`/`node`/`aboutDn`), `returned/limit/truncated`, `bySeverity.serverReported`, `delegatedRecords` |

Every link is the relation APIC resolved (`tDn`), so cross-tenant links into
`common` are followed. A failed EPG / BD / VRF read leaves its section `null`
with an entry in `errors` and `segmentResolved`/`staticPathResolved` `null` —
never an empty section. A failed contract read stays in the list as
`{"dn": …, "read": false}` with `contracts.complete: false`; if no fault scan
succeeds, `relatedFaultCandidates.faults` is `null`, not `[]`. A 2xx that is not
an APIC response (no `imdata` — e.g. a proxy login page) is an error, never an
empty result. An empty APIC answer is reported as "does not exist, or not
visible to this account's security domain" — APIC answers both the same way. Not evaluated: vzAny, taboo contracts, imported contract interfaces,
preferred-group peers, service graphs / L3Out. Leaf/spine inventory and
interface state are not implemented yet.

### Undo
| Tool | Meraki API path | Returns |
|------|----------------------|---------|
| `undo_list` | _(local `undo.db`, no API call)_ | recorded, not-yet-applied reversible writes: undoId, original tool, inverse tool, note |

## Write tools (9) — all support `dry_run`; CLI adds double-confirm

| Tool | Risk | Meraki API path | Undo / safety |
|------|------|----------------------|---------------|
| `reboot_device` | **high** | `POST /devices/{serial}/reboot` (unifi: `POST /api/s/{site}/cmd/devmgr` `{"cmd": "restart-device", "mac": ...}`) | captures prior status; no safe inverse, no undo |
| `claim_devices_into_network` | **high** | `POST /networks/{id}/devices/claim` | inverse = remove the claimed serials |
| `remove_device_from_network` | **high** | `POST /networks/{id}/devices/remove` | inverse = claim it back into the network |
| `bind_network_to_template` | **high** | `POST /networks/{id}/bind` | captures the prior binding; inverse = rebind prior / unbind |
| `unbind_network_from_template` | **high** | `POST /networks/{id}/unbind` | captures the prior template; inverse = rebind to it |
| `update_device` | medium | `PUT /devices/{serial}` | fetches + captures the changed keys' prior values; inverse = restore them |
| `update_network_vlan` | medium | `PUT /networks/{id}/appliance/vlans/{vlanId}` | fetches + captures prior values; inverse = restore them |
| `blink_device_leds` | low | `POST /devices/{serial}/blinkLeds` | locator aid; no config change, no undo |
| `undo_apply` | medium | _(local `undo.db`, then dispatches the recorded inverse tool)_ | executes a recorded inverse — itself governed and audited, single-use |

## Out of scope (by design)

- Full org/network **provisioning** workflows (create org, create network)
- Firmware upgrade orchestration
- SSID/switch-port config CRUD beyond the writes above
- OT / industrial equipment (use the `industrial-aiops` line) and device-level
  CLI/SSH network automation

- On **catalyst/cvp/unifi**: the unmapped reads in the matrix (licensing,
  VLANs, traffic, uplink telemetry, ...), the unmapped writes (all on
  catalyst/cvp; all but reboot on unifi), CVP configlet-content retrieval,
  Catalyst Center per-client listing, UniFi legacy cookie login
  (`POST /api/login` — use an API key) and blink-LED (`set-locate` has no
  bounded duration), and deep pagination

Want one of these — a missing Meraki call, a ❌ filled in on Catalyst Center,
CloudVision Portal, or UniFi Network (writes included), or another controller
platform entirely? Open an issue or PR — feedback and contributions welcome (a
platform is one descriptor module: path templates + response adapters).
