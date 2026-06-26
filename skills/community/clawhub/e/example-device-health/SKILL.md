---
name: example-device-health
description: >-
  Cisco IOS-XE device health check and triage procedure. Use when troubleshooting
  Cisco IOS-XE routers or switches, checking CPU utilization, memory usage,
  interface error counters, routing table health, or performing rapid device triage
  during an outage. Covers show commands, threshold interpretation, escalation
  decision trees, and structured report output for handoff.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🔍","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["cisco","health","triage"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# Cisco IOS-XE Device Health Check

Structured triage procedure for assessing Cisco IOS-XE device health. Produces a
prioritized findings report with severity classifications and recommended actions.

## When to Use

- Device is reported as slow, unresponsive, or dropping traffic
- Scheduled health audit of IOS-XE routers or switches
- Post-change verification after configuration or software updates
- Capacity planning data collection for CPU, memory, and interface utilization
- Incident response when a device is suspected as the fault domain

## Prerequisites

- SSH or console access to the target IOS-XE device (privilege level 1 minimum)
- Device running IOS-XE 16.x or 17.x (commands validated against 17.3+)
- Network reachability confirmed (ping/traceroute to management IP succeeds)
- Knowledge of the device's normal baseline (typical CPU, memory, traffic levels)
- Change control approval if performing checks during a maintenance window

## Procedure

Follow this sequence. Each step produces data for the final report. Do not skip
steps unless the device is unresponsive (jump to Step 6 for crash recovery).

### Step 1: Establish Baseline Context

Collect device identity and uptime to frame the health check.

```
show version | include uptime|Version|bytes of memory
show inventory | include PID
show clock
```

Record: hostname, software version, uptime, hardware model, current time.
Flag if uptime is unexpectedly short — indicates recent reload or crash.

### Step 2: CPU Utilization Assessment

```
show processes cpu sorted | head 20
show processes cpu history
show processes cpu platform sorted 5sec
```

Compare 5-second, 1-minute, and 5-minute averages against thresholds.
If 5-second average exceeds 80%, identify the top process immediately.

Key processes to watch:
- **IP Input** — high values indicate traffic processing overload
- **Crypto IKMP** — VPN negotiation storms
- **SNMP ENGINE** — aggressive polling
- **BGP Router** — large table churn or route oscillation
- **IOSD** — general control plane congestion

### Step 3: Memory Utilization Assessment

```
show memory statistics
show memory platform information
show processes memory sorted | head 15
```

Calculate used percentage: `(Total - Free) / Total * 100`.
Check for memory fragmentation: compare Largest Free block to Total Free.
If largest free block is less than 10% of total free, fragmentation is a concern.

### Step 4: Interface Health

```
show interfaces summary
show interfaces counters errors
show interfaces | include line protocol|drops|error|CRC|collision
```

For each interface with errors:
- Calculate error rate: `errors / (input packets + output packets) * 100`
- Error rate above 0.1% is warning, above 1% is critical
- CRC errors suggest Layer 1 issues (cabling, optics, SFP)
- Input errors with no CRC suggest buffer or overrun issues
- Output drops indicate congestion — check QoS policy

### Step 5: Routing Table Health

```
show ip route summary
show ip bgp summary (if BGP is configured)
show ip ospf neighbor (if OSPF is configured)
show ip eigrp neighbors (if EIGRP is configured)
```

Verify: expected number of routes present, no unexpected route withdrawals,
all routing protocol neighbors in established/full state.

Flag: neighbor state changes in the last hour, route count significantly
different from baseline, any routes via unexpected next-hops.

### Step 6: Platform and Environment

```
show environment all
show platform software status control-processor brief
show logging | include %|Error|Warning|traceback (last 50 lines)
```

Check: power supply status, fan status, temperature readings.
Any environmental alarm is an immediate escalation trigger.
Review recent syslog for crash signatures (traceback, CPUHOG, MALLOCFAIL).


## Threshold Tables

Reference: `references/threshold-tables.md` for detailed per-parameter thresholds.

| Parameter | Normal | Warning | Critical |
|-----------|--------|---------|----------|
| CPU 5-min avg | < 40% | 40–70% | > 70% |
| CPU 5-sec spike | < 80% | 80–90% | > 90% |
| Memory used | < 70% | 70–85% | > 85% |
| Memory fragmentation | > 10% largest/total | 5–10% | < 5% |
| Interface error rate | < 0.01% | 0.01–0.1% | > 0.1% |
| Interface output drops | < 100/hr | 100–1000/hr | > 1000/hr |
| Routing neighbors | All established | Flapping | Down |
| Temperature | Within spec | Within 5°C of max | At or above max |

## Decision Trees

### Triage Priority

```
Is the device reachable?
├── No → Escalate immediately. Check console access, power, environment.
└── Yes
    ├── CPU critical? → Identify top process → Apply mitigation per process
    │   ├── IP Input → Check for traffic storm, ACL optimization
    │   ├── BGP Router → Check for route churn, peer flap, table size
    │   └── Other → Collect 'show tech-support' for TAC escalation
    ├── Memory critical? → Check for memory leak
    │   ├── Largest free < 5% of total → Likely fragmentation, schedule reload
    │   └── Steady growth over time → Memory leak, collect 'show mem alloc'
    ├── Interface errors? → Classify error type
    │   ├── CRC/input errors → Layer 1 (cable, optic, SFP)
    │   └── Output drops → QoS policy or congestion
    └── All within thresholds → Document clean health, schedule next check
```

### Escalation Criteria

Escalate to senior engineer or TAC when any of these conditions are met:
- CPU sustained above 90% for more than 15 minutes with no identifiable cause
- Memory below 15% free with no recent change to explain consumption
- Traceback or CPUHOG messages in logs within last 24 hours
- Environmental alarm (power, fan, temperature) present
- More than 3 routing neighbor state changes in last hour

## Report Template

Generate a structured report with these sections:

```
DEVICE HEALTH REPORT
====================
Device: [hostname]
Model: [PID from inventory]
Software: [version]
Uptime: [uptime string]
Check Time: [timestamp]
Performed By: [operator/agent]

SUMMARY: [HEALTHY | WARNING | CRITICAL]

FINDINGS:
1. [Severity] [Component] — [Description]
   Observed: [metric value]
   Threshold: [normal/warning/critical range]
   Action: [recommended action]

2. ...

RECOMMENDATIONS:
- [Prioritized list of actions]

NEXT CHECK: [scheduled date based on findings severity]
```

Severity levels for findings:
- **INFO** — within normal thresholds, noted for baseline
- **WARNING** — approaching threshold, monitor closely
- **CRITICAL** — threshold exceeded, action required
- **EMERGENCY** — device at risk of failure, immediate action

## Troubleshooting

### Device Unresponsive to SSH

Try console access. If console is also unresponsive, check power and
environment remotely (smart PDU, out-of-band management). If the device has
crashed, collect crashinfo: `dir crashinfo:` after recovery.

### CPU Spikes During Health Check

SNMP polling or show commands themselves can briefly spike CPU. Wait 30 seconds
after connecting before collecting CPU data. Use `terminal length 0` to avoid
paging pauses that extend session time.

### Inconsistent Memory Readings

Memory values fluctuate during normal operation. Collect three samples at
30-second intervals and average them. Check `show memory dead` for memory
that is allocated but unreachable (leak indicator).

### Interface Counter Interpretation

Counters are cumulative since last clear. Use `show interfaces [name]`
to see the last clear time. For rate calculations, collect counters twice
with a known interval: `(counter2 - counter1) / interval_seconds`.

### Routing Protocol Neighbor Issues

If OSPF neighbors are stuck in INIT/2WAY, check MTU mismatch and area
configuration. If BGP peers show "Active" state, verify TCP connectivity
on port 179 and check for ACL blocking. EIGRP stuck-in-active indicates
a convergence problem downstream.
