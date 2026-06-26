---
name: config-management
description: >-
  Configuration backup, drift detection, and golden config validation across
  Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS. Covers running vs startup
  comparison, config archival, section-level drift analysis, and compliance
  validation for ongoing configuration assurance.
license: Apache-2.0
metadata:
  safety: read-write
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🔧","safetyTier":"read-write","requires":{"bins":["ssh"],"env":[]},"tags":["config","backup","drift"],"mcpDependencies":["git-netops-mcp"],"egressEndpoints":[]}'
---

# Configuration Management

Ongoing configuration assurance skill covering backup, drift detection, and
golden config validation. This skill identifies unauthorized or unintended
changes by comparing device configurations against known-good baselines and
organizational compliance rules.

Commands are labeled **[Cisco]**, **[JunOS]**, or **[EOS]** where syntax
diverges. Unlabeled statements apply to all three vendors.

> **Safety Note — Read-Write Operations:** This skill includes procedures that
> may modify device state (config archival to remote storage, rollback, config
> replace). Steps that write to devices are marked with ⚠️ **WRITE**. Always
> confirm authorization and maintenance window status before executing write
> operations. Read-only assessment steps can be run at any time without risk.

## When to Use

- Scheduled configuration compliance audit against golden baselines
- Investigating suspected unauthorized configuration changes
- Post-maintenance verification that running config was saved to startup
- Validating configuration consistency across device groups or stacks
- Checking that security-mandated patterns (AAA, NTP, logging) are present
- Ensuring forbidden patterns (default credentials, telnet, SNMPv1) are absent
- Building or refreshing a configuration archive before a change window
- Periodic drift detection as part of operational hygiene (daily/weekly)

## Prerequisites

- SSH or console access to the device (read-only sufficient for assessment;
  enable/configure privilege required for remediation or archival steps)
- A golden config baseline or previous archived config for comparison
- Knowledge of organizational compliance requirements: required services (AAA,
  NTP, syslog), forbidden protocols (telnet, HTTP management, SNMPv1/v2c
  without ACL), and mandatory security features (ACLs, CoPP)
- For archival: reachable SCP/TFTP/FTP server or local flash storage
- Awareness of any active maintenance window that may explain expected drift

## Procedure

Follow these steps sequentially. Steps 1–2 are always safe (read-only).
Steps 3–7 include optional write operations marked with ⚠️.

### Step 1: Config Collection

Capture the current running and startup/saved configurations.

**[Cisco]**
```
show running-config
show startup-config
```

**[JunOS]**
```
show configuration | display set
show configuration | compare rollback 0
```

**[EOS]**
```
show running-config
show startup-config
```

On JunOS, the candidate configuration model means the active config is the
committed config. Use `show configuration` to view committed state. See
`references/cli-reference.md` for architectural differences.

### Step 2: Running vs Startup Comparison

Detect unsaved changes — running config that would be lost on reload.

**[Cisco]**
```
show archive config differences system:running-config nvram:startup-config
```

**[JunOS]**
```
show | compare rollback 0
```

**[EOS]**
```
show running-config diffs
```

Any differences indicate unsaved changes. Record the diff output and timestamp.
Classify the age of unsaved changes — see Threshold Tables for severity. If
changes are intentional (active maintenance), note the maintenance ticket.

### Step 3: Config Archival

⚠️ **WRITE** — Back up the current configuration with timestamped naming.

**[Cisco]**
```
copy running-config tftp://[server]/[hostname]-YYYYMMDD-HHMM.cfg
```

**[JunOS]**
```
request system configuration save /var/tmp/[hostname]-YYYYMMDD-HHMM.conf
```

**[EOS]**
```
copy running-config flash:[hostname]-YYYYMMDD-HHMM.cfg
```

Use consistent naming: `{hostname}-{YYYYMMDD}-{HHMM}.cfg`. Verify the backup
was written successfully by checking file size and comparing a hash of the
backup against the running config. Maintain a minimum of 3 archived configs per
device for rollback options.

### Step 4: Golden Config Baseline

Retrieve the golden (intended-state) configuration for this device role. Golden
configs are maintained per device role (e.g., access-switch, core-router,
WAN-edge) and contain all mandatory configuration sections.

If no golden config exists yet, establish one:
1. Start from a known-compliant device config
2. Remove device-specific values (hostnames, IPs, interface descriptions)
3. Keep all compliance-mandated sections (AAA, NTP, logging, SNMP, ACLs)
4. Document the golden config version and approval date

For comparison, normalize both configs before diffing — see
`references/drift-detection.md` for normalization rules.

### Step 5: Drift Detection

Compare current config against the golden baseline section by section.

Partition the configuration into logical sections for structured comparison:

| Section | Cisco Examples | JunOS Examples | EOS Examples |
|---------|---------------|----------------|--------------|
| Routing | `router bgp`, `router ospf` | `protocols` | `router bgp`, `router ospf` |
| Switching | `spanning-tree`, `vlan` | `vlans`, `protocols rstp` | `spanning-tree`, `vlan` |
| Security | `access-list`, `line vty` | `firewall`, `system login` | `ip access-list`, `management` |
| Management | `logging`, `ntp`, `snmp` | `system syslog`, `system ntp` | `logging`, `ntp`, `snmp-server` |
| Services | `ip dhcp`, `ip nat` | `forwarding-options` | `ip dhcp`, `ip nat` |

For each section, identify additions, deletions, and modifications compared
to the baseline. Classify each difference by severity — see Threshold Tables.

### Step 6: Compliance Validation

Check for required and forbidden configuration patterns.

**Required patterns** (must be present):
- AAA authentication configured and active
- NTP synchronization to authorized time sources
- Syslog forwarding to centralized logging servers
- SNMP with ACL restrictions (no unrestricted community strings)
- Management access restricted to SSH only (no telnet, no HTTP)

**Forbidden patterns** (must be absent):
- Default credentials (e.g., `username admin password admin`)
- Telnet or HTTP enabled for management (`transport input telnet`, `no ip http secure-server`)
- SNMPv1/v2c without source ACL restriction
- Unrestricted VTY access (no ACL applied to VTY lines)
- DHCP snooping or ARP inspection disabled on access ports

Reference `references/drift-detection.md` for full compliance rule definitions
with vendor-specific pattern matching.

### Step 7: Remediation Guidance

⚠️ **WRITE** — Address drift findings based on severity classification.

For **Critical** drift (routing, security sections):
1. Verify if the change was authorized (check change tickets)
2. If unauthorized, prepare a rollback to the last known-good config
3. **[Cisco]** `configure replace flash:[backup].cfg force`
4. **[JunOS]** `rollback [n]` then `commit`
5. **[EOS]** `configure replace flash:[backup].cfg`

For **Warning** drift (management plane, logging):
1. Document the deviation in the drift report
2. Schedule remediation during the next maintenance window
3. Apply missing configuration elements incrementally

For **Info** drift (cosmetic — descriptions, banners, comments):
1. Log the deviation for tracking
2. Remediate opportunistically during scheduled maintenance

After any remediation, re-run Steps 1–2 to confirm the config matches the
intended state and save the corrected running config to startup.

## Threshold Tables

### Drift Severity by Config Section

| Config Section | Severity | Rationale |
|---------------|----------|-----------|
| Routing (BGP, OSPF, static) | Critical | Direct traffic impact, potential outage |
| Security (ACLs, AAA, CoPP) | Critical | Exposure to unauthorized access |
| Switching (STP, VLANs) | High | Loop risk, VLAN leakage |
| Management (logging, NTP, SNMP) | Warning | Operational visibility loss |
| Services (DHCP, NAT) | Warning | Service-level impact, no network-wide risk |
| Cosmetic (descriptions, banners) | Info | No operational impact |

### Unsaved Change Age

| Age | Severity | Action |
|-----|----------|--------|
| < 1 hour | Info | Likely active maintenance — verify with operator |
| 1–4 hours | Warning | Check if maintenance window is active |
| 4–24 hours | High | Likely forgotten save — prompt operator to save or revert |
| > 24 hours | Critical | Unsaved changes at high risk of loss — immediate save or revert |

### Config Archive Freshness

| Last Archive | Status | Action |
|-------------|--------|--------|
| < 7 days | Current | No action needed |
| 7–30 days | Stale | Schedule archive refresh |
| 30–90 days | Warning | Archive before any changes |
| > 90 days | Critical | Immediate archive required |

## Decision Trees

### Drift Detected

```
Drift found between running config and golden baseline
├── Classify section
│   ├── Routing / Security → Critical
│   ├── Switching → High
│   ├── Management / Services → Warning
│   └── Cosmetic → Info
│
├── Check authorization
│   ├── Change ticket exists for this device/window?
│   │   ├── Yes → Authorized drift
│   │   │   ├── Update golden baseline if change is permanent
│   │   │   └── Document as accepted deviation if temporary
│   │   └── No → Unauthorized drift
│   │       ├── Critical/High → Escalate and prepare rollback
│   │       └── Warning/Info → Document and schedule remediation
│   └── Cannot determine → Treat as unauthorized, notify operator
│
└── Remediation path
    ├── Rollback available? (archived config within freshness threshold)
    │   ├── Yes → Apply config replace (Step 7)
    │   └── No → Manual remediation required
    └── Post-remediation → Re-run Steps 1–6 to confirm compliance
```

### Running ≠ Startup

```
Running config differs from startup config
├── Maintenance window active?
│   ├── Yes → Expected — changes in progress
│   │   └── Remind operator to save when maintenance completes
│   └── No → Unexpected unsaved changes
│       ├── Age < 1 hour → Possible recent change, check with operator
│       ├── Age 1–24 hours → Likely forgotten save
│       │   └── Prompt: save to startup or revert to startup config
│       └── Age > 24 hours → Critical risk
│           └── Immediate action: save or revert, then archive
│
└── Cannot determine age
    └── Check last config change timestamp
        ├── [Cisco] show running-config | include Last config
        ├── [JunOS] show system commit
        └── [EOS] show running-config | include Last modified
```

### Compliance Violation

```
Required pattern missing or forbidden pattern present
├── Classify violation severity
│   ├── Security (AAA missing, default creds, telnet) → Critical
│   ├── Logging (syslog missing, NTP missing) → Warning
│   └── Best practice (banner missing) → Info
│
├── Auto-remediation candidate?
│   ├── Additive fix (add NTP server, add logging host) → Yes
│   │   └── Generate remediation config snippet
│   │       └── Apply during maintenance window (Step 7)
│   ├── Removal required (remove telnet, remove default creds) → Yes with caution
│   │   └── Verify no dependencies before removing
│   └── Structural change (enable AAA, reconfigure SNMP) → No — manual review
│       └── Create change request for manual implementation
│
└── Document in compliance report with violation details
```

## Report Template

```
CONFIGURATION MANAGEMENT REPORT
=================================
Device: [hostname]
Vendor: [Cisco | JunOS | EOS]
Device Role: [access-switch | core-router | WAN-edge | ...]
Check Time: [timestamp]
Performed By: [operator/agent]
Golden Config Version: [version/date]

SAVED STATE:
- Running vs Startup: [Match | Differs]
- Unsaved change age: [duration or N/A]
- Last archive date: [date]
- Archive freshness: [Current | Stale | Warning | Critical]

DRIFT SUMMARY:
- Sections checked: [n]
- Deviations found: [n]
  - Critical: [n] | High: [n] | Warning: [n] | Info: [n]

DRIFT FINDINGS:
1. [Severity] [Section] — [Description]
   Golden: [expected config line/block]
   Current: [actual config line/block]
   Authorization: [ticket# | Unauthorized | Unknown]
   Action: [Rollback | Schedule fix | Accept | Update baseline]

COMPLIANCE STATUS:
- Required patterns: [n/total] present
- Forbidden patterns: [n] found
- Violations:
  1. [Severity] [Rule] — [detail]

REMEDIATION ACTIONS:
- [Prioritized action list with target maintenance window]

NEXT CHECK: [CRITICAL: 4hr | HIGH: 8hr | WARNING: 24hr | HEALTHY: 7d]
```

## Troubleshooting

### Config Diff Shows False Positives

Diffs include generated lines (timestamps, certificate hashes, build
information) that change between captures but are not real drift. Normalize
configs before comparison by stripping timestamps, build strings, and
auto-generated comments. See `references/drift-detection.md` for normalization
patterns per vendor.

### JunOS Candidate Config Confusion

JunOS uses a candidate-commit model. `show configuration` displays committed
(active) config. Uncommitted candidate changes appear only with `show |
compare`. If drift analysis shows differences between a JunOS device and its
golden config, verify that no uncommitted candidate changes are pending —
uncommitted changes do not affect the running device but will take effect on
next commit.

### Archive Transfer Failures

Config export to remote servers may fail due to: ACL on the device blocking
outbound SCP/TFTP, DNS resolution failure for server hostname, authentication
failure on SCP, or insufficient flash space for local copy. Test connectivity
with ping first, verify SCP credentials, and check available flash space with
`dir flash:` (Cisco/EOS) or `file list /var/tmp/` (JunOS).

### Large Config Diff Overwhelms Analysis

Configs exceeding 10,000 lines produce diffs that are difficult to analyze
holistically. Break the comparison into the section categories from Step 5 and
analyze one section at a time. Prioritize sections by severity tier from the
Threshold Tables. For structured configs (JunOS set-format, EOS section mode),
sort lines before diffing to reduce positional noise.

### Compliance Rule Vendor Variations

The same security requirement maps to different config syntax per vendor. For
example, disabling telnet: Cisco uses `transport input ssh` on VTY lines, JunOS
uses `delete system services telnet`, and EOS uses `no management telnet`.
Reference `references/drift-detection.md` for vendor-specific compliance
patterns to avoid false positives or missed violations.
