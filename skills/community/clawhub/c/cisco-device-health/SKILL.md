---
name: cisco-device-health
description: >-
  Cisco IOS-XE and NX-OS device health check and triage procedure. Use when
  troubleshooting Cisco routers, switches, or Nexus platforms — assessing CPU,
  memory, interfaces, routing, and environment. Covers both IOS-XE (ISR, ASR,
  Catalyst 9K) and NX-OS (Nexus 3K/5K/7K/9K) with platform-specific commands,
  thresholds, and decision trees that account for IOS-XE QFP/RP architecture
  and NX-OS VDC isolation.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🔍","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["cisco","health","triage","nx-os"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# Cisco IOS-XE / NX-OS Device Health Check

Structured triage procedure for assessing Cisco device health across IOS-XE and
NX-OS platforms. Produces a prioritized findings report with severity
classifications and recommended actions.

Commands are labeled **[IOS-XE]** or **[NX-OS]** where they diverge. Unlabeled
commands work on both platforms.

## When to Use

- Device reported as slow, dropping traffic, or unresponsive
- Scheduled health audit of IOS-XE routers/switches or Nexus platforms
- Post-change verification after upgrades, patches, or configuration changes
- Capacity planning data collection for CPU, memory, and link utilization
- Incident response when a Cisco device is suspected as the fault domain
- NX-OS VDC isolation troubleshooting — health check scoped to a specific VDC

## Prerequisites

- SSH or console access to the device (privilege 1 minimum for IOS-XE, `show` role for NX-OS)
- IOS-XE 16.x/17.x or NX-OS 9.x/10.x (commands validated against IOS-XE 17.3+ and NX-OS 10.2+)
- Network reachability to management interface confirmed
- Awareness of the device's normal baseline (CPU, memory, traffic patterns)
- For NX-OS: identify which VDC you are operating in (`show vdc current`)

## Procedure

Follow this sequence. Each step produces data for the final report. If the device
is unresponsive, skip to Step 6 for crash recovery.

### Step 1: Establish Baseline Context

Collect identity, uptime, and platform context.

**[IOS-XE]**
```
show version | include uptime|Version|bytes of memory
show inventory | include PID
show clock
```

**[NX-OS]**
```
show version | include uptime|system version|Memory
show inventory | include PID
show clock
show vdc current
```

Record: hostname, OS version, uptime, hardware model, current time.
Short uptime means a recent reload or crash — investigate immediately.
On NX-OS, confirm VDC context: all subsequent commands apply to this VDC only.

### Step 2: CPU Utilization

IOS-XE separates Route Processor (RP) and QuantumFlow Processor (QFP). Triage
both planes independently. NX-OS uses a unified supervisor model — `show system
resources` is the primary view.

**[IOS-XE]**
```
show processes cpu sorted | head 20
show processes cpu history
show platform software status control-processor brief
show platform hardware qfp active statistics drop
```

**[NX-OS]**
```
show system resources
show processes cpu sort | head 20
show module
```

**IOS-XE interpretation:** Compare 5-second, 1-minute, and 5-minute RP averages.
If RP CPU is normal but QFP drops are climbing, the data plane is overloaded while
control plane is healthy — different remediation than RP overload. Key RP processes:
IP Input (traffic storms), BGP Router (route churn), Crypto IKMP (VPN storms),
IOSD (control plane congestion).

**NX-OS interpretation:** `show system resources` reports CPU as kernel + user
percentages. Normal idle should be above 60%. NX-OS control plane CPU runs hotter
than IOS-XE RP because the supervisor handles both planes. Key processes: `netstack`
(forwarding), `bgp` (route processing), `stp` (spanning tree), `vpc` (vPC keepalive).

### Step 3: Memory Utilization

**[IOS-XE]**
```
show memory statistics
show processes memory sorted | head 15
```

**[NX-OS]**
```
show system resources
show processes memory | head 15
```

**IOS-XE:** Calculate used percentage from processor pool: `(Total - Free) / Total * 100`.
Check fragmentation: if largest free block < 10% of total free, memory is fragmented.

**NX-OS:** `show system resources` reports memory as total/used/free in KB. NX-OS
reserves a larger kernel memory footprint than IOS-XE — used percentages above 60%
are typical. Watch for `MemFree` dropping below 15% of total.

### Step 4: Interface Health

```
show interfaces summary
show interfaces counters errors
```

**[IOS-XE]**
```
show interfaces | include line protocol|drops|error|CRC
show controllers [name]
```

**[NX-OS]**
```
show interface [name] | include errors|drops|CRC
show hardware internal errors module [n]
```

For each interface with errors:
- Calculate error rate: `errors / (input + output packets) * 100`
- CRC errors → Layer 1 issue (cabling, optics, SFP seating)
- Input errors without CRC → buffer overruns
- Output drops → congestion; check QoS policy or link capacity
- On NX-OS, `show hardware internal errors` reveals ASIC-level drops not visible
  in standard interface counters

### Step 5: Routing Protocol Health

```
show ip route summary
```

**[IOS-XE]**
```
show ip bgp summary
show ip ospf neighbor
show ip eigrp neighbors
```

**[NX-OS]**
```
show bgp ipv4 unicast summary
show ip ospf neighbors
show ip eigrp neighbors
show vpc brief
```

Verify: expected route count, all neighbors in established/full state, no unexpected
withdrawals. On NX-OS, vPC peer-link state is critical — a failed peer-link orphans
traffic. BGP prefix counts that deviate >10% from baseline indicate route churn.

### Step 6: Environment and Platform

**[IOS-XE]**
```
show environment all
show platform software status control-processor brief
show logging | include %|Error|Warning|traceback | tail 50
dir crashinfo:
```

**[NX-OS]**
```
show environment
show module
show logging last 50
show cores
```

Check: power supply status, fan health, temperature readings. Any environmental
alarm escalates immediately. On IOS-XE, review crashinfo: for recent crash dumps.
On NX-OS, `show cores` lists supervisor and module core dumps — presence indicates
a process crash requiring investigation.

## Threshold Tables

Reference: `references/threshold-tables.md` for detailed per-parameter thresholds.

| Parameter | Normal | Warning | Critical | Platform Notes |
|-----------|--------|---------|----------|----------------|
| CPU 5-min avg | < 40% | 40–70% | > 70% | NX-OS: expect 5–10% higher baseline |
| CPU 5-sec spike | < 80% | 80–90% | > 90% | IOS-XE RP only; NX-OS: use system resources |
| QFP drops/sec | < 100 | 100–1000 | > 1000 | IOS-XE only |
| Memory used | < 70% | 70–85% | > 85% | NX-OS: normal baseline is 55–65% |
| Interface error rate | < 0.01% | 0.01–0.1% | > 0.1% | Both platforms |
| Output drops/hr | < 100 | 100–1000 | > 1000 | Both platforms |
| Routing neighbors | All established | Flapping | Down | NX-OS: include vPC state |
| Temperature | Within spec | 5°C of max | At/above max | Per-sensor spec varies |

## Decision Trees

### Primary Triage

```
Is the device reachable?
├── No → Check console, power, environment. Collect crashinfo after recovery.
└── Yes
    ├── Identify platform → IOS-XE or NX-OS?
    │
    ├── [IOS-XE] CPU issue?
    │   ├── RP CPU high, QFP normal → Control plane overload
    │   │   ├── BGP Router high → Route churn, check peer stability
    │   │   ├── IP Input high → Traffic storm, check ACLs/CoPP
    │   │   └── Other process → Collect 'show tech-support' for TAC
    │   ├── RP normal, QFP drops high → Data plane overload
    │   │   └── Check traffic rates, ACL complexity, NAT sessions
    │   └── Both high → Platform capacity exceeded, reduce load
    │
    ├── [NX-OS] CPU issue?
    │   ├── Check VDC context → Are you in the correct VDC?
    │   ├── System resources CPU high
    │   │   ├── netstack high → Forwarding overload, check ARP/routes
    │   │   ├── bgp high → Route churn, check table size and peers
    │   │   ├── stp/vpc high → L2 instability, check topology
    │   │   └── Other → Collect 'show tech-support' for TAC
    │   └── Per-module issue → Specific linecard problem
    │       └── show module → Identify failed/degraded module
    │
    ├── Memory issue? (either platform)
    │   ├── [IOS-XE] Fragmentation high → Schedule reload during window
    │   ├── [NX-OS] MemFree < 15% → Identify top consumers
    │   └── Steady growth → Memory leak, collect allocation data, plan reload
    │
    ├── Interface errors? → Classify error type
    │   ├── CRC/input errors → Layer 1 (cable, optic, SFP)
    │   ├── Output drops → QoS or congestion
    │   └── [NX-OS] ASIC errors → Hardware issue, check module health
    │
    └── All within thresholds → Document clean health
```

### Escalation Criteria

Escalate to senior engineer or TAC when:
- CPU sustained > 90% for 15+ minutes with no identifiable cause
- Memory below 15% free with no recent change to explain consumption
- Traceback, CPUHOG, or MALLOCFAIL in logs (IOS-XE); core dump present (NX-OS)
- Any environmental alarm (power, fan, temperature)
- More than 3 routing neighbor state changes in the last hour
- NX-OS module in non-OK state or vPC peer-link failure
- QFP drops exceeding 10,000/sec with no traffic anomaly explanation (IOS-XE)

## Report Template

```
DEVICE HEALTH REPORT
====================
Device: [hostname]
Platform: [IOS-XE | NX-OS]
Model: [PID from inventory]
Software: [version]
Uptime: [uptime string]
VDC: [VDC name — NX-OS only, omit for IOS-XE]
Check Time: [timestamp]
Performed By: [operator/agent]

SUMMARY: [HEALTHY | WARNING | CRITICAL | EMERGENCY]

FINDINGS:
1. [Severity] [Component] — [Description]
   Platform: [IOS-XE | NX-OS]
   Observed: [metric value]
   Threshold: [normal/warning/critical range]
   Action: [recommended action]

2. ...

PLATFORM-SPECIFIC NOTES:
- [IOS-XE: QFP drop summary or NX-OS: VDC/module status]

RECOMMENDATIONS:
- [Prioritized action list]

NEXT CHECK: [date based on severity — CRITICAL: 24hr, WARNING: 7d, HEALTHY: 30d]
```

## Troubleshooting

### Device Unresponsive to SSH

Try console access. If console also unresponsive, check power and environment
via out-of-band management (CIMC for UCS-based, smart PDU, or console server).
On IOS-XE: collect `dir crashinfo:` after recovery. On NX-OS: `show cores` and
`show system reset-reason`.

### NX-OS VDC Context Confusion

Health data is VDC-scoped. If metrics look wrong, verify VDC: `show vdc current`.
Switch VDC with `switchto vdc [name]`. The default VDC contains system-level
resources; admin VDC shows aggregate hardware.

### CPU Spikes During Health Check

Show commands and SNMP polling can briefly spike CPU. Wait 30 seconds after
connecting before collecting CPU data. Use `terminal length 0` (IOS-XE) or
`terminal length 0` (NX-OS) to avoid paging pauses.

### IOS-XE QFP Drops vs RP CPU

High QFP drops with normal RP CPU means the data plane is stressed but control
plane is healthy. Do not restart the device — the RP is functioning normally.
Investigate traffic patterns, ACL complexity, and NAT session counts. Use
`show platform hardware qfp active feature` to identify which QFP feature is
consuming resources.

### NX-OS Module Issues

If `show module` reports a module not in "ok" state, collect `show module
internal exception-log module [n]` before taking action. Powercycling a linecard
(`poweroff module [n]` / `no poweroff module [n]`) can resolve transient failures
but requires change control.

### Inconsistent Memory Between Platforms

IOS-XE and NX-OS report memory differently. IOS-XE `show memory statistics` shows
IOS memory pools; NX-OS `show system resources` shows Linux-level memory. NX-OS
baseline memory usage is higher (55–65% is normal) because the Linux kernel and
system daemons consume more than IOS-XE's monolithic process model.
