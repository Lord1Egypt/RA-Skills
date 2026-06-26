# Drift Detection Methodology

Section-by-section comparison methodology, golden config normalization rules,
compliance pattern definitions, and drift severity classification.

## Section-by-Section Diff Methodology

Break the full config into logical sections before comparing. This isolates
drift to specific functional domains and enables severity classification.

### Section Definitions

| Section | Scope | Key Identifiers |
|---------|-------|----------------|
| **Routing** | BGP, OSPF, EIGRP, IS-IS, static routes, PBR, route-maps | `router bgp`, `router ospf`, `ip route`, `protocols` (JunOS) |
| **Switching** | VLANs, STP, port-channels, trunk/access port config | `vlan`, `spanning-tree`, `interface.*switchport`, `vlans` (JunOS) |
| **Security** | ACLs, CoPP, AAA, TACACS/RADIUS, crypto, firewall rules | `access-list`, `ip access-list`, `aaa`, `firewall` (JunOS) |
| **Management** | Logging, NTP, SNMP, DNS, users, SSH, banners | `logging`, `ntp`, `snmp-server`, `system` (JunOS) |
| **Services** | DHCP, NAT, QoS, MPLS, multicast, PIM | `ip dhcp`, `ip nat`, `policy-map`, `forwarding-options` (JunOS) |

### Diff Procedure

1. **Extract** both configs (current and baseline/golden)
2. **Normalize** both configs (see normalization rules below)
3. **Partition** each config into the 5 sections listed above
4. **Compare** each section independently using line-by-line diff
5. **Classify** each difference by section → severity (see matrix below)
6. **Report** with section context so the reviewer understands impact

For JunOS set-format configs, sort lines alphabetically within each section
before diffing. Positional differences in set-format are not meaningful.

## Golden Config Normalization

Before comparing, strip or normalize lines that change between captures but do
not represent real configuration drift.

### Lines to Strip (All Vendors)

- Timestamps and build dates (e.g., `! Last configuration change at...`)
- Software version banners (auto-generated on config display)
- Certificate data blocks (change on renewal, tracked separately)
- Auto-generated comments and remark lines added by the OS

### Vendor-Specific Normalization

**Cisco:**
- Strip `! Last configuration change at` lines
- Strip `! NVRAM config last updated at` lines
- Strip `Building configuration...` and `Current configuration:` headers
- Normalize `ntp clock-period` (auto-tuned, changes constantly)
- Strip `certificate` blocks under `crypto pki`

**JunOS:**
- Strip `## Last changed:` timestamp comments
- Strip `version` statement (tracks JunOS version, not config intent)
- Normalize `apply-groups` ordering (non-deterministic in some versions)
- Strip `encrypted-password` values for comparison (compare structure only)

**EOS:**
- Strip `! Last modified at` timestamp lines
- Strip `! boot system` lines (tracks boot image, not config)
- Normalize `ip name-server` ordering (may vary between displays)
- Strip `end` statement at config bottom

### Values to Parameterize

When building golden configs, replace device-specific values with tokens:

| Element | Token | Example |
|---------|-------|---------|
| Hostname | `{HOSTNAME}` | `hostname {HOSTNAME}` |
| Management IP | `{MGMT_IP}` | `ip address {MGMT_IP} 255.255.255.0` |
| Loopback IP | `{LOOPBACK_IP}` | `ip address {LOOPBACK_IP} 255.255.255.255` |
| Interface descriptions | `{DESCRIPTION}` | `description {DESCRIPTION}` |
| SNMP location | `{LOCATION}` | `snmp-server location {LOCATION}` |

## Compliance Rule Definitions

### Required Patterns

Rules that must match at least one line in the configuration. A missing match
is a compliance violation.

| Rule ID | Category | Cisco Pattern | JunOS Pattern | EOS Pattern | Severity |
|---------|----------|--------------|---------------|-------------|----------|
| REQ-001 | AAA | `aaa new-model` | `system authentication-order` | `aaa authorization` | Critical |
| REQ-002 | NTP | `ntp server` | `system ntp server` | `ntp server` | Warning |
| REQ-003 | Logging | `logging host` | `system syslog host` | `logging host` | Warning |
| REQ-004 | SSH-Only | `transport input ssh` (on VTY) | `system services ssh` | `management ssh` | Critical |
| REQ-005 | SNMP ACL | `snmp-server community .* RO \\d+` (ACL ref) | `snmp community .* authorization` | `snmp-server community .* RO \\S+` | High |
| REQ-006 | Banner | `banner login` | `system login message` | `banner login` | Info |
| REQ-007 | Password Encryption | `service password-encryption` | N/A (always encrypted) | `service password-encryption` | High |

### Forbidden Patterns

Rules that must NOT match any line. A match is a compliance violation.

| Rule ID | Category | Cisco Pattern | JunOS Pattern | EOS Pattern | Severity |
|---------|----------|--------------|---------------|-------------|----------|
| FRB-001 | Telnet | `transport input.*telnet` | `system services telnet` | `management telnet` | Critical |
| FRB-002 | HTTP Mgmt | `ip http server` (without secure) | `system services web-management http` | `management http` | Critical |
| FRB-003 | Default Creds | `username admin password admin` | `system login user admin.*password` | `username admin secret` with weak hash | Critical |
| FRB-004 | SNMPv1/v2 No ACL | `snmp-server community \\S+ (RO\|RW)$` (no ACL) | `snmp community` without `client-list` | `snmp-server community \\S+ (RO\|RW)$` | High |
| FRB-005 | No VTY ACL | `line vty` block without `access-class` | `system login` without `allow-commands` | `management ssh` without ACL | High |
| FRB-006 | IP Source Route | `ip source-route` | `system internet-options source-routing` | `ip source-route` | Warning |

## Drift Severity Classification Matrix

Cross-reference the config section with the type of change to determine final
severity.

| Change Type \ Section | Routing | Security | Switching | Management | Services | Cosmetic |
|----------------------|---------|----------|-----------|------------|----------|----------|
| **Line added** | Critical | Critical | High | Warning | Warning | Info |
| **Line removed** | Critical | Critical | High | Warning | Warning | Info |
| **Value modified** | Critical | Critical | High | Warning | Warning | Info |
| **Ordering changed** | Warning | High | Warning | Info | Info | Info |
| **Comment changed** | Info | Info | Info | Info | Info | Info |

### Escalation Triggers

Regardless of section, immediately escalate if any of these conditions are met:

- Any change to AAA or TACACS/RADIUS configuration
- Any ACL modification on management interfaces or VTY lines
- Routing protocol neighbor or network statement changes
- SNMP community string changes or ACL removal
- Any crypto/IPsec/IKE configuration modification
- Spanning-tree root bridge priority or mode changes

## Automated Drift Scoring

Assign a numeric score to quantify overall drift for trending and alerting:

| Severity | Points per Finding |
|----------|--------------------|
| Critical | 10 |
| High | 5 |
| Warning | 2 |
| Info | 1 |

**Aggregate thresholds:**

| Total Score | Status | Action |
|-------------|--------|--------|
| 0 | Compliant | No action — schedule next check per standard interval |
| 1–5 | Minor drift | Document and schedule remediation |
| 6–15 | Moderate drift | Prioritize remediation within 24 hours |
| 16–30 | Significant drift | Immediate investigation and remediation plan |
| > 30 | Critical drift | Escalate to network operations lead, consider rollback |
