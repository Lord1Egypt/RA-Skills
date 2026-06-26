---
name: fortisase-audit
description: >-
  Fortinet FortiSASE audit — Secure Web Gateway policy review, ZTNA application
  gateway assessment, thin edge FortiGate integration validation, SD-WAN security
  overlay analysis, FortiClient endpoint compliance verification, and cloud
  security posture evaluation across FortiSASE tenants.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🔒","safetyTier":"read-only","requires":{"bins":[],"env":["FORTISASE_API_TOKEN"]},"tags":["fortisase","fortinet","sase","zero-trust","forticlient"],"mcpDependencies":[],"egressEndpoints":["*.fortisase.com:443","*.forticloud.com:443"]}'
---

# FortiSASE Security Posture Audit

Comprehensive audit of Fortinet FortiSASE cloud-delivered security services.
Unlike traditional perimeter firewall audits that focus on on-premises policy
chains, this skill evaluates the FortiSASE-specific architecture: Secure Web
Gateway (SWG) policy coverage, Zero Trust Network Access (ZTNA) application
gateway posture, thin edge FortiGate integration health, FortiClient endpoint
compliance enforcement, and FortiGuard cloud security service currency.

Covers FortiSASE tenants with SWG, ZTNA, SD-WAN overlay, and FortiClient
endpoint management. For on-premises FortiGate-specific audits, see the
`fortigate-firewall-audit` skill. Reference `references/api-reference.md`
for FortiSASE REST API endpoints and FortiCloud authentication patterns.

## When to Use

- Secure Web Gateway policy review — verifying web filter profiles, application control, and URL category enforcement across all SWG policies
- ZTNA application gateway audit — assessing zero trust access rules, posture tag enforcement, and application definitions
- Thin edge FortiGate security assessment — validating tunnel status, SD-WAN overlay configuration, and security policy consistency between cloud and edge
- FortiClient endpoint compliance gap analysis — checking EMS integration, compliance rules, ZTNA tag assignment, and on/off-fabric detection
- SD-WAN overlay security validation — confirming security controls are applied consistently across all overlay paths and that SLA violations do not bypass inspection
- SSL/TLS inspection coverage review — evaluating deep inspection profile deployment, certificate distribution, and inspection exemptions
- FortiGuard service subscription verification — ensuring all subscribed services (AV, IPS, web filter, DNS filter) are active and signatures are current
- Tenant configuration drift detection — comparing current FortiSASE configuration against organizational baselines or prior audit snapshots

## Prerequisites

- FortiSASE admin portal access or API token with read-only permissions (`FORTISASE_API_TOKEN` environment variable)
- FortiCloud account with IAM permissions sufficient to query tenant configuration, endpoint status, and service health
- Understanding of FortiSASE topology — Points of Presence (PoPs), thin edge sites, endpoint deployment scope, and ZTNA application definitions
- FortiClient EMS integration details — EMS server address, ZTNA tag definitions, compliance rule sets, and endpoint group assignments
- FortiGuard subscription status — which services are licensed (FortiGuard AV, IPS, Web Filter, Application Control, DNS Filter, Inline CASB, DLP)
- Knowledge of expected SWG and ZTNA policy baselines for comparison against current configuration
- Network diagram or inventory showing thin edge FortiGate models, firmware targets, and SD-WAN SLA definitions

## Procedure

Follow this audit flow sequentially. Each step builds on prior findings.
The procedure moves from tenant discovery through SWG policy analysis, ZTNA
assessment, firewall policy review, thin edge validation, SSL inspection,
endpoint compliance, FortiGuard health, and logging infrastructure.

### Step 1: Tenant and Topology Discovery

Authenticate to the FortiSASE API via FortiCloud IAM and enumerate the
tenant topology.

```
# Authenticate to FortiCloud and obtain bearer token
POST https://customerapiauth.fortinet.com/api/v1/oauth/token/
Content-Type: application/json
{
  "username": "<forticloud_user>",
  "password": "<forticloud_pass>",
  "client_id": "<api_client_id>",
  "grant_type": "password"
}
```

After authentication, enumerate tenant resources:

```
# List Points of Presence (PoPs)
GET /api/v1/fortisase/pops

# List thin edge sites
GET /api/v1/fortisase/thin-edges

# Endpoint summary
GET /api/v1/fortisase/endpoints/summary

# License utilization
GET /api/v1/fortisase/license/status
```

Record: tenant name, region, PoP locations and their status, thin edge
site count and registration status, total licensed endpoints versus
connected endpoints, and license expiration dates. Identify any PoPs
in degraded state or thin edges showing as offline.

Flag license utilization above 90% as a capacity Warning — approaching
the licensed endpoint limit may prevent new endpoint connections.

### Step 2: Secure Web Gateway Policy Audit [SWG]

Retrieve all SWG-related security profiles and policies.

```
# Web filter profiles
GET /api/v2/cmdb/webfilter/profile

# Application control lists
GET /api/v2/cmdb/application/list

# Antivirus profiles
GET /api/v2/cmdb/antivirus/profile

# IPS sensor configuration
GET /api/v2/cmdb/ips/sensor

# Video filter profiles
GET /api/v2/cmdb/videofilter/profile

# Inline CASB profiles (if licensed)
GET /api/v2/cmdb/casb/profile
```

For each web filter profile, evaluate:

- **URL category coverage:** Check that all FortiGuard URL categories have
  an explicit action (allow, block, monitor, warning, authenticate). Categories
  left at default may create unintended access. Count categories with explicit
  actions versus total categories.
- **Safe Search enforcement:** Verify safe search is enabled for search
  engines and YouTube restricted mode where required by policy.
- **Content filtering:** Check file type blocking by protocol (HTTP, FTP),
  ActiveX/Java/cookie filtering settings.

For application control, evaluate:

- **Application categories:** Review which application categories are set to
  block, monitor, or allow. High-risk categories (P2P, proxy, remote-access,
  botnet) should have explicit block actions.
- **Application overrides:** Check for individual application overrides that
  contradict category-level policy.
- **Unknown application handling:** Verify the action for applications that
  cannot be identified.

Verify that antivirus and IPS profiles are bound to SWG firewall policies.
An SWG policy without AV and IPS binding passes traffic uninspected for
malware and exploits — this is a Critical finding for internet-bound traffic.

### Step 3: ZTNA Application Gateway Assessment [ZTNA]

Evaluate ZTNA rules, application definitions, and posture tag enforcement.

```
# ZTNA rules
GET /api/v2/cmdb/firewall/access-proxy

# ZTNA server definitions
GET /api/v2/cmdb/firewall/access-proxy/virtual-host

# ZTNA tags (posture tags)
GET /api/v2/cmdb/user/device-category

# User and group definitions for ZTNA
GET /api/v2/cmdb/user/group
```

For each ZTNA access proxy rule:

- **Posture tag enforcement:** Verify that ZTNA rules require device posture
  tags (e.g., compliant OS, AV running, patch level current). Rules without
  posture tags allow access from non-compliant devices — flag as High.
- **User/group-based access:** Confirm rules restrict access by user identity
  or group membership, not just network location. ZTNA rules relying solely
  on source IP contradict zero trust principles.
- **Application definitions:** Review ZTNA server definitions — verify the
  correct backend servers, ports, and SSL settings are configured. Check for
  wildcard or overly broad application definitions.
- **Rule ordering:** ZTNA rules evaluate top-down. Verify that more specific
  rules precede broader rules. Identify shadow rules that never match due to
  a preceding broader rule.
- **Authentication method:** Verify SAML/LDAP/RADIUS authentication source
  integration and that MFA is enforced for sensitive applications.

Calculate the ZTNA posture tag coverage ratio: rules with posture tag
requirements divided by total ZTNA rules. A ratio below 80% indicates
insufficient device compliance enforcement.

### Step 4: Firewall Policy Review [SWG] [ZTNA]

Audit the firewall policies that govern both SWG and ZTNA traffic flows.

```
# Firewall policies
GET /api/v2/cmdb/firewall/policy

# Central SNAT policies
GET /api/v2/cmdb/firewall/central-snat-map
```

For each firewall policy, evaluate:

- **Overly permissive policies:** Policies with `srcaddr "all"`,
  `dstaddr "all"`, `service "ALL"`, and `action accept` are Critical
  findings — they accept all traffic without restriction.
- **Security profile binding:** Verify every accept policy has antivirus,
  web-filter, application-control, IPS sensor, and SSL inspection profile
  bound. Calculate the profile binding coverage percentage.
- **Rule ordering and shadow detection:** Evaluate policies in sequence
  order. Identify shadow rules — rules that can never match because a
  preceding rule with broader criteria matches all their traffic first.
- **Disabled policies:** Policies with `status disable` create audit
  confusion. Flag for cleanup.
- **Logging configuration:** Verify `logtraffic` is set to `all` or `utm`
  on security-relevant policies. Policies with `logtraffic disable` create
  visibility gaps.
- **Schedule-based policies:** Policies with time-based schedules may create
  security windows during off-schedule periods. Validate schedule alignment
  with intended access windows.

Summarize: total policies, accept versus deny, UTM profile coverage ratio,
shadow rule count, and disabled policy count.

### Step 5: Thin Edge FortiGate Integration [Thin Edge]

Validate thin edge FortiGate registration, tunnel health, and policy
consistency.

```
# Thin edge status
GET /api/v1/fortisase/thin-edges

# Per thin edge detail
GET /api/v1/fortisase/thin-edges/{edge_id}

# SD-WAN overlay health
GET /api/v1/fortisase/thin-edges/{edge_id}/sdwan/health

# Thin edge firmware status
GET /api/v1/fortisase/thin-edges/{edge_id}/firmware
```

For each thin edge site:

- **Registration and tunnel status:** Verify the thin edge is registered and
  its IPsec/SSL tunnel to the nearest FortiSASE PoP is established. Tunnels
  in `down` state mean site traffic is not protected by FortiSASE — Critical
  finding.
- **SD-WAN overlay configuration:** Review SD-WAN SLA definitions (latency,
  jitter, packet loss thresholds). Verify health-check targets are reachable
  and meaningful. Check that SLA violation failover does not bypass security
  inspection.
- **Security policy consistency:** Compare the thin edge local firewall policy
  with the FortiSASE cloud policy. Identify discrepancies where thin edge
  local rules may override or conflict with centralized cloud policy.
- **Firmware currency:** Check the thin edge FortiOS version against the
  recommended firmware target. Thin edges running firmware more than one major
  version behind are a High finding due to unpatched vulnerabilities.
- **Dual-tunnel redundancy:** Verify thin edges have tunnels to at least two
  PoPs for redundancy. Single-tunnel configurations create a single point of
  failure.

### Step 6: SSL/SSH Inspection Configuration [SWG] [ZTNA]

Review deep inspection profiles and their deployment coverage.

```
# SSL inspection profiles
GET /api/v2/cmdb/firewall/ssl-ssh-profile

# Certificate inspection settings
GET /api/v2/cmdb/certificate/ca
```

Evaluate:

- **Deep inspection deployment:** Identify which firewall policies use
  `deep-inspection` versus `certificate-inspection`. Policies using only
  certificate inspection cannot inspect encrypted payload — AV and IPS
  profiles see only connection metadata on HTTPS traffic.
- **Inspection exemptions:** Review exempt lists in SSL inspection profiles.
  Overly broad exemptions (entire categories or wildcard domains) reduce
  inspection coverage. Document each exemption with business justification.
- **Certificate deployment:** Verify the FortiSASE CA certificate is
  deployed to all managed endpoints. Endpoints without the CA certificate
  will encounter TLS errors or bypass inspection.
- **Protocol-specific inspection:** Check inspection settings for HTTPS,
  SMTPS, IMAPS, POP3S, and FTPS. Verify all relevant protocols are included
  in the inspection scope.
- **Performance impact assessment:** Deep inspection increases latency and
  resource consumption. Review PoP capacity metrics to ensure deep inspection
  is sustainable at current traffic volumes.

### Step 7: FortiClient Endpoint Compliance [Endpoint]

Assess FortiClient EMS integration and endpoint compliance posture.

```
# FortiClient EMS connection status
GET /api/v1/fortisase/ems/status

# Endpoint compliance summary
GET /api/v1/fortisase/endpoints/compliance

# ZTNA tag assignments
GET /api/v1/fortisase/endpoints/ztna-tags

# Endpoint group inventory
GET /api/v1/fortisase/endpoints/groups
```

Evaluate:

- **EMS integration health:** Verify FortiClient EMS is connected and
  synchronizing. Check last sync timestamp — sync delays exceeding 15
  minutes may indicate connectivity issues.
- **Compliance rule evaluation:** Review compliance rules for each endpoint
  group:
  - OS patch level (days since last patch, minimum OS version)
  - Antivirus status (real-time protection enabled, signatures current)
  - Vulnerability scan results (critical/high vulnerability count)
  - Firewall status (endpoint firewall enabled)
  - Disk encryption status (required for endpoints accessing sensitive data)
- **ZTNA tag assignment:** Verify that compliance evaluation results in
  correct ZTNA tag assignment. Non-compliant endpoints should receive a
  non-compliant tag that restricts ZTNA access. Check for endpoints with
  missing or stale tags.
- **On-fabric vs off-fabric detection:** Verify FortiClient correctly
  detects whether the endpoint is on-fabric (corporate network) or
  off-fabric (remote). Off-fabric endpoints should route through FortiSASE
  SWG; on-fabric endpoints may use local FortiGate. Misconfigured detection
  can create security gaps.
- **Endpoint compliance percentage:** Calculate the percentage of managed
  endpoints meeting all compliance rules. Rates below 85% indicate systemic
  compliance issues requiring remediation campaigns.

### Step 8: FortiGuard Service Validation [SWG] [ZTNA]

Verify subscription status and signature currency for all FortiGuard
security services.

```
# FortiGuard subscription status
GET /api/v2/monitor/fortiguard/service-communication-stats

# Signature database versions
GET /api/v2/monitor/system/fortiguard

# FortiGuard server connectivity
GET /api/v2/monitor/fortiguard/server-list
```

Verify each FortiGuard service:

| Service | Expected Status | Maximum Signature Age |
|---------|----------------|----------------------|
| FortiGuard Antivirus | Active, licensed | 24 hours |
| FortiGuard IPS | Active, licensed | 7 days |
| FortiGuard Web Filter | Active, licensed | 7 days |
| FortiGuard Application Control | Active, licensed | 7 days |
| FortiGuard DNS Filter | Active, licensed | 7 days |
| FortiGuard Inline CASB | Active (if licensed) | 7 days |
| FortiGuard DLP | Active (if licensed) | 7 days |

Check FortiGuard server connectivity from each PoP. FortiSASE relies on
cloud-based FortiGuard queries for real-time web filter rating and DNS
filter lookups. Degraded connectivity forces fallback to cached data, reducing
detection efficacy for newly categorized threats.

Verify the update mechanism — FortiSASE should automatically receive
signature updates from FortiGuard. Check for update failures in the last 7
days and identify root cause (connectivity, license, service outage).

### Step 9: Logging and Analytics [SWG] [ZTNA] [Thin Edge] [Endpoint]

Check FortiAnalyzer Cloud integration and log infrastructure health.

```
# FortiAnalyzer Cloud status
GET /api/v1/fortisase/logging/status

# Log forwarding configuration
GET /api/v1/fortisase/logging/forwarders

# Alert policies
GET /api/v1/fortisase/logging/alerts
```

Evaluate:

- **FortiAnalyzer Cloud integration:** Verify FortiAnalyzer Cloud (or
  on-premises FortiAnalyzer) is connected and receiving logs from all
  FortiSASE components (SWG, ZTNA, thin edges, endpoints).
- **Log types forwarded:** Confirm that traffic logs, UTM logs (AV, IPS,
  web filter, application control), event logs, and ZTNA logs are all
  forwarded. Missing log types create investigation blind spots.
- **Log retention:** Verify log retention period meets compliance
  requirements (typically 90-365 days depending on regulatory framework).
- **Alert policies:** Review configured alert policies for security events.
  At minimum, alerts should cover: malware detection, IPS critical severity,
  ZTNA authentication failures, thin edge tunnel down, FortiGuard update
  failures, and endpoint compliance drops.
- **Threat detection dashboards:** Verify SOC-relevant dashboards are
  configured for SWG threat activity, ZTNA access patterns, and endpoint
  compliance trends.

## Threshold Tables

### SWG Policy Coverage

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| URL categories with explicit action | >90% | 70-90% | <70% |
| AV profile bound to SWG policies | 100% | 80-99% | <80% |
| IPS sensor bound to SWG policies | 100% | 80-99% | <80% |
| Application control profile bound | >95% | 75-95% | <75% |
| High-risk app categories blocked | 100% | 80-99% | <80% |
| SSL deep inspection on internet policies | >80% | 50-80% | <50% |

### ZTNA Tag Enforcement

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| ZTNA rules with posture tag requirement | >90% | 70-90% | <70% |
| Endpoint posture tag compliance rate | >85% | 65-85% | <65% |
| ZTNA rules with user/group restriction | 100% | 80-99% | <80% |
| MFA enforcement on sensitive apps | 100% | 80-99% | <80% |
| ZTNA tag propagation latency | <5 min | 5-15 min | >15 min |

### Thin Edge Health

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Tunnel status | Up (all edges) | 1-2 edges degraded | Any edge down |
| Firmware currency | Current or N-1 | N-2 | >N-2 or EOL |
| SD-WAN SLA compliance | >95% | 80-95% | <80% |
| Dual-tunnel redundancy | All edges dual-tunnel | >80% dual-tunnel | <80% dual-tunnel |
| Policy consistency (cloud vs edge) | 100% match | Minor drift | Major drift |

### FortiClient Compliance

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Endpoints compliant (all rules) | >90% | 75-90% | <75% |
| OS patch currency (<30 days) | >90% | 70-90% | <70% |
| AV signatures current (<24h) | >95% | 80-95% | <80% |
| Vulnerability scan (no critical) | >90% | 75-90% | <75% |
| EMS sync status | Connected, <15min | Connected, 15-60min | Disconnected or >60min |

### FortiGuard Service Health

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Subscription status | All active | Expiring <30 days | Expired or inactive |
| AV signature age | <24 hours | 24-72 hours | >72 hours |
| IPS signature age | <7 days | 7-14 days | >14 days |
| Web filter DB age | <7 days | 7-14 days | >14 days |
| FortiGuard connectivity | All PoPs connected | Intermittent | Disconnected |

## Decision Trees

### SWG Policy Gap Prioritization

```
SWG policy gap identified
├── What type of gap?
│   ├── Missing AV/IPS profile on accept policy
│   │   ├── Policy carries internet-bound traffic?
│   │   │   ├── Yes → CRITICAL: Bind AV + IPS immediately
│   │   │   │   └── Also verify SSL deep inspection is active
│   │   │   └── No (internal SaaS only) → HIGH: Bind AV + IPS
│   │   └── Is policy actively used (hit count > 0)?
│   │       ├── Yes → Prioritize remediation
│   │       └── No → Evaluate for removal
│   │
│   ├── URL category not explicitly actioned
│   │   ├── Category is high-risk (malware, phishing, C2)?
│   │   │   ├── Yes → CRITICAL: Set action to block immediately
│   │   │   └── No → MEDIUM: Review and set explicit action
│   │   └── Category is business-relevant?
│   │       ├── Yes → Set to allow with logging
│   │       └── No → Set to block or monitor
│   │
│   ├── Application control gap
│   │   ├── High-risk categories (P2P, proxy, botnet) not blocked?
│   │   │   └── CRITICAL: Block high-risk categories
│   │   ├── Unknown applications allowed?
│   │   │   └── HIGH: Set unknown apps to monitor or block
│   │   └── Application override contradicts category policy?
│   │       └── MEDIUM: Review and align override with policy
│   │
│   └── SSL inspection gap
│       ├── No deep inspection on internet-bound policies?
│       │   └── HIGH: Deploy deep inspection; distribute CA cert
│       ├── Excessive exemptions in inspection profile?
│       │   └── MEDIUM: Review each exemption for business justification
│       └── CA certificate not deployed to all endpoints?
│           └── HIGH: Deploy via EMS or MDM
│
└── Remediation timeline
    ├── CRITICAL → Immediate (within 24 hours)
    ├── HIGH → Within 7 days
    └── MEDIUM → Within 30 days
```

### ZTNA Access Policy Remediation Path

```
ZTNA access policy finding
├── Rule missing posture tag requirement?
│   ├── Application sensitivity?
│   │   ├── High (financial, PII, admin consoles)
│   │   │   └── CRITICAL: Add posture tags immediately
│   │   │       ├── Require: OS patched, AV current, compliant
│   │   │       └── Block non-compliant with redirect to remediation
│   │   ├── Medium (internal tools, collaboration)
│   │   │   └── HIGH: Add posture tags within 7 days
│   │   └── Low (public-facing info, non-sensitive)
│   │       └── MEDIUM: Add posture tags within 30 days
│   │
│   └── Interim mitigation:
│       └── Enable enhanced logging on untagged rules
│           └── Monitor for non-compliant device access patterns
│
├── Rule missing user/group restriction?
│   ├── Rule uses source IP only?
│   │   └── HIGH: Migrate to identity-based access
│   │       ├── Integrate SAML/LDAP identity source
│   │       └── Define access by group membership
│   └── Rule allows "all users"?
│       └── MEDIUM: Scope to required groups
│
├── Shadow rule detected?
│   ├── Shadow rule more restrictive than matching rule?
│   │   └── Reorder: move restrictive rule above broad rule
│   └── Shadow rule redundant?
│       └── Remove shadow rule; document in change log
│
└── Authentication method insufficient?
    ├── No MFA on sensitive applications?
    │   └── HIGH: Enable MFA via SAML IdP integration
    └── Single-factor only?
        └── MEDIUM: Plan MFA rollout
```

### Thin Edge Security Posture Improvement

```
Thin edge finding identified
├── Tunnel down?
│   ├── Single edge affected?
│   │   ├── Check edge connectivity (WAN link status)
│   │   ├── Verify IPsec/SSL VPN configuration
│   │   └── Check PoP availability in region
│   └── Multiple edges affected?
│       ├── PoP outage? → Check FortiSASE status page
│       └── Configuration push failed? → Check FortiCloud sync
│   └── CRITICAL: Restore tunnel — site unprotected
│
├── Firmware outdated?
│   ├── How far behind?
│   │   ├── N-1 → LOW: Schedule upgrade in maintenance window
│   │   ├── N-2 → MEDIUM: Upgrade within 30 days
│   │   └── >N-2 or EOL → HIGH: Urgent upgrade required
│   └── Check for known CVEs in current firmware version
│       └── Active exploit in the wild? → CRITICAL: Emergency upgrade
│
├── Policy inconsistency (cloud vs edge)?
│   ├── Edge has locally defined rules overriding cloud policy?
│   │   └── HIGH: Align local rules with cloud policy or remove
│   ├── Edge missing security profiles present in cloud?
│   │   └── MEDIUM: Push consistent profiles from FortiSASE
│   └── Edge allows traffic not covered by cloud policy?
│       └── HIGH: Review and restrict; enforce cloud-first policy
│
└── No dual-tunnel redundancy?
    ├── Business-critical site?
    │   └── HIGH: Configure secondary tunnel to alternate PoP
    └── Non-critical site?
        └── MEDIUM: Plan dual-tunnel deployment
```

## Report Template

```
FORTISASE SECURITY POSTURE AUDIT REPORT
=========================================
Tenant: [tenant name]
Region: [primary region]
FortiSASE Service Tier: [tier/license level]
Audit Date: [timestamp]
Performed By: [operator/agent]

TENANT TOPOLOGY:
- Points of Presence (PoPs): [count] ([list with status])
- Thin edge sites: [count] ([registered/total])
- Licensed endpoints: [used] / [total] ([utilization %])
- License expiration: [date]
- PoPs in degraded state: [count or none]

SWG FINDINGS:
- Web filter profiles: [count]
- URL categories with explicit action: [n] / [total] ([%])
- Application control profiles: [count]
- High-risk categories blocked: [yes/no — list gaps]
- SWG policies with full UTM binding (AV+IPS+WebFilter+AppCtrl): [n] / [total] ([%])
- SSL deep inspection coverage: [n] policies / [total internet-bound] ([%])
- Inline CASB enabled: [yes/no]

ZTNA FINDINGS:
- ZTNA access proxy rules: [count]
- Rules with posture tag requirement: [n] / [total] ([%])
- Rules with user/group restriction: [n] / [total] ([%])
- MFA enforced on sensitive apps: [n] / [total sensitive] ([%])
- Shadow rules identified: [count]
- ZTNA server definitions: [count]
- Authentication sources: [SAML/LDAP/RADIUS — list with status]

THIN EDGE FINDINGS:
- Total thin edge sites: [count]
- Tunnels established: [n] / [total]
- Tunnels down: [list sites]
- Dual-tunnel redundancy: [n] / [total] ([%])
- Firmware current (within N-1): [n] / [total] ([%])
- Firmware outdated (>N-2 or EOL): [list sites with versions]
- SD-WAN SLA compliance: [%]
- Policy consistency issues: [count — list sites]

ENDPOINT COMPLIANCE FINDINGS:
- Managed endpoints: [count]
- FortiClient EMS sync status: [connected/disconnected — last sync time]
- Endpoints fully compliant: [n] / [total] ([%])
- Non-compliant breakdown:
  - OS patch overdue: [count]
  - AV signatures stale: [count]
  - Critical vulnerabilities present: [count]
  - Endpoint firewall disabled: [count]
- ZTNA tags assigned correctly: [n] / [total] ([%])
- On-fabric / off-fabric detection issues: [count or none]

FORTIGUARD SERVICE STATUS:
- Antivirus: [active/expired] — signatures [version] ([age])
- IPS: [active/expired] — signatures [version] ([age])
- Web Filter: [active/expired] — DB [version] ([age])
- Application Control: [active/expired] — DB [version] ([age])
- DNS Filter: [active/expired] — DB [version] ([age])
- Inline CASB: [active/expired/not licensed]
- FortiGuard connectivity: [all PoPs connected / degraded — details]
- Update failures (last 7 days): [count or none]

LOGGING AND ANALYTICS:
- FortiAnalyzer Cloud: [connected/disconnected]
- Log types forwarded: [list — traffic, UTM, event, ZTNA, endpoint]
- Log retention: [days]
- Alert policies configured: [count]
- Missing alert coverage: [list gaps]

FINDINGS SUMMARY:
1. [Severity] [Category] — [Description]
   Component: [SWG / ZTNA / Thin Edge / Endpoint / FortiGuard]
   Detail: [specific configuration issue]
   Impact: [security implication]
   Recommendation: [specific remediation action]

REMEDIATION ROADMAP:
- Immediate (0-24 hours): [Critical findings — list]
- Short-term (1-7 days): [High findings — list]
- Medium-term (7-30 days): [Medium findings — list]
- Long-term (30-90 days): [Low findings and improvements — list]

NEXT AUDIT: [CRITICAL findings present: 30 days | HIGH only: 90 days | Clean: 180 days]
```

## Troubleshooting

### FortiCloud API Authentication Failures

FortiCloud API authentication requires a valid API client ID and credentials
with appropriate IAM permissions. Common issues:

- **Token expiration:** FortiCloud bearer tokens have a limited TTL
  (typically 1 hour). Implement token refresh logic for long-running audits.
- **IAM permission scope:** The API user must have read-only access to
  FortiSASE resources. Insufficient permissions return `403 Forbidden` on
  resource endpoints but may succeed on authentication.
- **Multi-factor authentication:** If MFA is enforced on the FortiCloud
  account, API authentication may require an API-specific account without
  MFA or use of service account credentials.
- **Rate limiting:** FortiCloud API enforces rate limits (typically 60
  requests/minute). Implement exponential backoff for `429 Too Many Requests`
  responses. Batch queries where possible.

### Thin Edge Tunnel Flapping

Thin edge tunnels that repeatedly establish and drop indicate underlying
connectivity or configuration issues:

- **WAN link instability:** Check the thin edge WAN interface for errors,
  packet loss, or bandwidth saturation. SD-WAN health checks can trigger
  tunnel failover, but the root cause is the underlay network.
- **MTU mismatch:** IPsec tunnels add overhead. If the path MTU is too
  small, fragmented packets cause tunnel instability. Set the thin edge
  tunnel MTU to 1400 or enable DF-bit clearing.
- **NAT traversal:** Thin edges behind NAT devices require NAT-T
  (UDP 4500). Verify the upstream NAT device allows UDP 4500 and that
  the NAT session timeout exceeds the IPsec DPD interval.
- **DPD (Dead Peer Detection) sensitivity:** Aggressive DPD intervals
  (e.g., 5 seconds) on high-latency links cause false positives. Adjust
  DPD interval to 30 seconds with a retry count of 3.

### FortiClient EMS Sync Delays

When FortiClient EMS synchronization with FortiSASE exceeds expected
intervals:

- **EMS connectivity:** Verify the EMS server can reach FortiSASE cloud
  endpoints (*.fortisase.com:443). Check firewall rules on the EMS host
  and any upstream proxies.
- **Endpoint count scaling:** Large endpoint populations (>10,000) may
  experience sync delays during full synchronization. Verify incremental
  sync is functioning.
- **EMS version compatibility:** Ensure the FortiClient EMS version is
  compatible with the current FortiSASE release. Version mismatches can
  cause sync failures or partial data updates.
- **Certificate trust:** EMS-to-FortiSASE communication requires valid
  TLS certificates. Expired or untrusted certificates cause silent sync
  failures.

### FortiGuard Connectivity Behind Proxy

When FortiSASE PoPs or thin edges cannot reach FortiGuard update servers:

- **Proxy configuration:** If the environment requires an outbound proxy,
  configure FortiGuard to use the proxy for update downloads. Verify proxy
  authentication credentials if required.
- **DNS resolution:** FortiGuard services require DNS resolution for
  `service.fortiguard.net`, `update.fortiguard.net`, and related domains.
  Verify DNS is functioning on all PoPs and thin edges.
- **Port requirements:** FortiGuard uses HTTPS (TCP 443) and may use
  UDP 53/8888 for rating queries. Ensure these ports are permitted.
- **Regional server selection:** FortiGuard uses anycast and regional servers.
  Verify the nearest FortiGuard server is reachable and not blocked by
  geo-IP restrictions.

### ZTNA Tag Propagation Delays

When ZTNA tags updated in FortiClient EMS do not reflect in FortiSASE
access decisions promptly:

- **Propagation pipeline:** Tag updates flow from FortiClient agent to
  EMS to FortiSASE. Each hop introduces latency. Normal propagation is
  under 5 minutes; delays beyond 15 minutes indicate a pipeline issue.
- **EMS-to-FortiSASE sync interval:** Check the configured sync interval
  between EMS and FortiSASE. Default intervals may be too long for
  time-sensitive compliance enforcement.
- **Tag caching:** FortiSASE may cache ZTNA tags at the PoP level. Cache
  TTL settings affect how quickly tag changes take effect. Review cache
  settings if tag changes are not applying within expected timeframes.
- **Compliance rule evaluation frequency:** FortiClient evaluates compliance
  rules periodically (default: every 5 minutes). Increasing evaluation
  frequency reduces the time between a compliance state change and the
  corresponding tag update.

### PoP Capacity and Performance Limitations

When FortiSASE PoP performance degrades or capacity limits are approached:

- **Endpoint concentration:** If too many endpoints connect to a single PoP,
  performance degrades. Enable PoP load balancing or geo-steering to
  distribute endpoints across available PoPs.
- **Deep inspection overhead:** SSL deep inspection significantly increases
  per-session resource consumption. If PoP capacity is constrained, evaluate
  inspection exemptions for high-bandwidth, low-risk traffic (e.g., trusted
  SaaS platforms with their own security controls).
- **Traffic spikes:** Sudden increases in endpoint connections (e.g., start
  of business day across a time zone) can saturate PoP capacity. Review
  capacity planning and consider PoP pre-scaling if supported.
- **Regional PoP availability:** Some regions have limited PoP presence.
  Endpoints in underserved regions may experience higher latency. Review
  FortiSASE regional coverage against endpoint geographic distribution.
