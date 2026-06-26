---
name: eigrp-analysis
description: >-
  EIGRP DUAL algorithm analysis with successor/feasible successor evaluation,
  stuck-in-active diagnosis, K-value validation, and redistribution loop
  detection. Cisco IOS-XE and NX-OS dual-platform coverage with protocol-first
  diagnostic reasoning for classic and named EIGRP modes.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🔍","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["eigrp","routing","cisco"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# EIGRP Protocol Analysis

DUAL-reasoning-driven analysis skill for Cisco EIGRP. Unlike link-state
protocols that flood topology databases, EIGRP uses the Diffusing Update
Algorithm (DUAL) to compute loop-free paths through a distributed query/reply
process. Effective EIGRP diagnosis requires understanding successor selection,
the feasibility condition, and stuck-in-active mechanics — not just reading
command output.

Commands are labeled **[IOS-XE]** or **[NX-OS]** where syntax diverges.
Unlabeled statements apply to both platforms.

## When to Use

- EIGRP route missing from the routing table or suboptimal path selected
- Stuck-in-active (SIA) condition — routes locked in Active state, queries
  unanswered
- Neighbor adjacency not forming or flapping between up and down
- K-value mismatch suspected after configuration change or new device addition
- Post-change verification after EIGRP topology modifications, summarization
  changes, or stub configuration
- Redistribution loop suspected between EIGRP and another protocol (commonly
  OSPF)
- Named mode migration — validating behavior parity with classic mode

## Prerequisites

- SSH or console access to Cisco IOS-XE or NX-OS device (read-only privilege
  sufficient)
- EIGRP process running — classic mode (`router eigrp [AS]`) or named mode
  (`router eigrp [name]`)
- On NX-OS: `feature eigrp` must be enabled before any EIGRP configuration
- Knowledge of the EIGRP autonomous system number and expected neighbor topology
- Awareness of configured stub, summarization, and distribute-list settings that
  affect query scope

## Procedure

Follow this diagnostic flow sequentially. Each step builds on data from prior
steps, moving from broad inventory to targeted DUAL-level analysis.

### Step 1: EIGRP Instance and Neighbor Inventory

Verify EIGRP is running and collect the neighbor table.

**[IOS-XE]**
```
show ip eigrp neighbors
```

**[NX-OS]**
```
show ip eigrp neighbors vrf all
```

Record each neighbor: interface, address, hold time, uptime (since), SRTT,
queue counts. Compare against expected topology — every directly connected
EIGRP router should appear. Key observations:

- **Missing neighbor** → interface misconfiguration, passive-interface, K-value
  mismatch, or AS number mismatch (proceed to Step 4)
- **Low uptime** → recent adjacency reset; correlate with change events
- **High SRTT** → slow neighbor responses; potential SIA risk
- **Non-zero queue count (Q Cnt)** → neighbor is congestion-limited; queries
  and updates may be delayed

### Step 2: Topology Table Analysis

Examine DUAL's successor and feasible successor selection for key prefixes.

**[IOS-XE]**
```
show ip eigrp topology [prefix/len]
```

**[NX-OS]**
```
show ip eigrp topology [prefix/len] vrf default
```

For each route entry, interpret the DUAL state:

- **Feasible Distance (FD):** The best metric this router has ever known for
  this destination — used as the threshold for the feasibility condition.
- **Reported Distance (RD):** The metric the neighbor claims for this
  destination from its own perspective (the neighbor's computed distance).
- **Successor:** The neighbor whose path is currently installed in the routing
  table — lowest FD among all feasible paths.
- **Feasible Successor (FS):** A backup neighbor whose RD is strictly less than
  the current FD. This guarantees a loop-free alternate path.

**Feasibility condition:** RD of neighbor < FD of current successor. If a
neighbor's reported distance is lower than the current feasible distance, DUAL
guarantees that neighbor is not part of a routing loop and can serve as a
backup without triggering a query.

If no feasible successor exists and the successor fails, DUAL must go Active
and send queries — proceed to Step 3.

### Step 3: Stuck-in-Active Diagnosis

Identify routes in Active state and diagnose query/reply failures.

**[IOS-XE]**
```
show ip eigrp topology active
```

**[NX-OS]**
```
show ip eigrp topology active vrf default
```

Routes in Active state are waiting for query replies from neighbors. The SIA
timer (default 3 minutes) starts when a route goes Active. If a neighbor does
not reply within half the SIA timer (90 seconds), a SIA-Query is sent. If
still no reply at the full timer, the neighbor is reset.

Determine which neighbor is not responding:

- Check the topology entry — the "replies" counter shows outstanding queries
- Identify the unresponsive neighbor and investigate: is it reachable? Is its
  CPU overloaded? Is it waiting for its own downstream queries?

**Query scope** is the primary lever for SIA prevention. Broad query scope
(queries propagating across the entire EIGRP domain) is the most common root
cause. Mitigations:
- **Stub configuration** — stub routers do not propagate queries
- **Summarization** — summarized routes contain query scope at the summarization
  boundary
- **Distribute-lists** — filter scope but do not affect query propagation

### Step 4: K-Value and Metric Validation

Verify metric parameters match across all neighbors — mismatched K-values
prevent adjacency formation entirely.

**[IOS-XE]**
```
show ip protocols | section eigrp
```

**[NX-OS]**
```
show ip eigrp vrf default
```

Confirm K-values on each device: K1=1, K2=0, K3=1, K4=0, K5=0 (defaults). All
neighbors in the same AS must use identical K-values or adjacency is refused.

Check metric mode: named EIGRP supports **wide metrics** (64-bit) using the
`rib-scale` factor. Classic mode uses 32-bit metrics. If migrating from classic
to named mode, verify metric values remain consistent — wide metrics produce
different values that are scaled before RIB installation.

Validate interface-level delay and bandwidth on key links:

**[IOS-XE]**
```
show ip eigrp interfaces detail
```

**[NX-OS]**
```
show ip eigrp interfaces detail vrf default
```

Incorrect bandwidth or delay on an interface directly affects path selection.
A common misconfiguration is leaving default bandwidth on serial or tunnel
interfaces, causing EIGRP to compute incorrect metrics.

### Step 5: Redistribution and Route Filtering

Check for redistribution loops and verify route filtering.

**[IOS-XE]**
```
show ip route eigrp | include EX
```

**[NX-OS]**
```
show ip route eigrp vrf default | include EX
```

External EIGRP routes (D EX) indicate redistribution. Common issues:

- **Mutual redistribution** between EIGRP and OSPF without proper route tagging
  creates routing loops — redistributed routes circle back and re-enter the
  original protocol with different metrics
- **Missing distribute-list or route-map** on redistribution points allows
  unintended routes to cross protocol boundaries
- **Administrative distance** — EIGRP external routes have AD 170, higher than
  OSPF (110). If the same prefix exists in both, OSPF wins — this may or may
  not be desired

Verify distribute-lists and route-maps are applied correctly at redistribution
points. Check that route tags are used to prevent loops in mutual redistribution
designs.

## Threshold Tables

Operational parameter norms for EIGRP — protocol-level expectations, not device
resource thresholds.

| Parameter | LAN Default | WAN Default | Notes |
|-----------|-------------|-------------|-------|
| Hello Interval | 5s | 60s | WAN = multipoint links < 1.544 Mbps |
| Hold Timer | 15s | 180s | 3x hello by convention |
| Active Timer (SIA) | 3 min | 3 min | Configurable; half-time SIA-Query at 90s |
| Route Update Delay | Immediate | Immediate | No MRAI — updates sent as computed |

**Metric Defaults (Classic Mode):**

| K-Value | Default | Weight | Component |
|---------|---------|--------|-----------|
| K1 | 1 | Bandwidth | 10^7 / min-bandwidth-kbps |
| K2 | 0 | Load | Disabled by default |
| K3 | 1 | Delay | Sum of delays in tens of µs |
| K4 | 0 | Reliability | Disabled by default |
| K5 | 0 | Reliability | Disabled by default |

**Operational Norms:**

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Neighbor count | Matches design | ± 1 from baseline | > 2 missing |
| SIA events / week | 0 | 1–2 | > 3 |
| Active routes | 0 | 1–5 | > 5 or persistent |
| Topology table size | Stable ± 5% | Change > 10% | Change > 25% |
| SRTT (ms) | < 100 | 100–500 | > 500 |

## Decision Trees

### Stuck-in-Active Triage

```
Route stuck in Active state (SIA timer running)
├── Check query scope
│   ├── Queries flooding entire domain?
│   │   ├── No stub routers configured → Add stub config to leaf/branch routers
│   │   ├── No summarization → Add summary routes at distribution boundaries
│   │   └── Large flat topology → Redesign with hierarchy (hub/stub or areas)
│   └── Query scope is bounded → Specific neighbor issue
│       ├── Unresponsive neighbor reachable?
│       │   ├── No → Interface or link failure
│       │   │   ├── Check interface status on both ends
│       │   │   └── Check Layer 2 connectivity (ARP, CDP/LLDP)
│       │   └── Yes → Neighbor processing delay
│       │       ├── CPU overloaded? → Check CPU utilization on neighbor
│       │       ├── Waiting for downstream replies? → SIA is cascading
│       │       │   └── Trace the query chain to the true bottleneck
│       │       └── SIA timer too short? → Extend active-time (if appropriate)
│       └── Multiple neighbors unresponsive?
│           └── Common upstream failure → Check shared infrastructure
```

### Missing or Suboptimal Route

```
Expected EIGRP route missing or wrong path selected
├── Route in topology table?
│   ├── Yes — route known to DUAL
│   │   ├── In Active state? → Go to SIA triage tree above
│   │   ├── Successor installed but suboptimal?
│   │   │   ├── Check FD/RD of competing paths → Lowest FD wins
│   │   │   ├── Interface bandwidth/delay correct? → Misconfigured BW/delay
│   │   │   │   skews metric; verify with `show interfaces`
│   │   │   ├── Variance configured? → Unequal-cost load balancing may select
│   │   │   │   paths within variance multiplier × FD
│   │   │   └── Offset-list applied? → Offset-lists add to delay component
│   │   └── Feasible successor exists but not used?
│   │       └── Normal — FS is backup only, used when successor fails
│   │           (unless variance enables unequal-cost balancing)
│   └── No — route not in topology table
│       ├── Network statement missing? → Verify `network` command covers the prefix
│       ├── Passive-interface? → Check if the source interface is passive
│       ├── Distribute-list filtering? → Check inbound distribute-list or route-map
│       ├── Redistribution missing? → If external route expected, check redistribution config
│       └── Wrong AS number? → Verify AS matches across all routers in the domain
```

## Report Template

```
EIGRP ANALYSIS REPORT
======================
Device: [hostname]
Platform: [IOS-XE | NX-OS]
EIGRP Mode: [Classic AS n | Named instance-name]
Check Time: [timestamp]
Performed By: [operator/agent]

NEIGHBOR STATUS:
- Expected neighbors: [n]
- Established: [n] | Missing: [n]
- Neighbors with high SRTT (>100ms): [list]

DUAL STATE:
- Routes in Passive state: [n] (normal)
- Routes in Active state: [n] (requires attention if > 0)
- Feasible successors available: [n] of [total] routes

FINDINGS:
1. [Severity] [Category] — [Description]
   Route: [prefix/len]
   Observed: [state, FD, successor]
   Expected: [normal state or path]
   Root Cause: [diagnosis from decision tree]
   Action: [recommended remediation]

METRIC VALIDATION:
- K-values consistent: [Yes/No — list mismatches]
- Metric mode: [Classic 32-bit | Wide 64-bit]

REDISTRIBUTION:
- External routes (D EX): [count]
- Route tags in use: [Yes/No]
- Mutual redistribution: [present/absent]

RECOMMENDATIONS:
- [Prioritized action list]

NEXT CHECK: [CRITICAL: 4hr, WARNING: 24hr, HEALTHY: 7d]
```

## Troubleshooting

### K-Value Mismatch

Neighbors with different K-values refuse to form adjacency — no error message
appears in the neighbor table because the adjacency never establishes. Check
`show ip protocols` on both devices and compare K1–K5 values. This is the most
common silent EIGRP adjacency failure.

### Stuck-in-Active Cascading

One unresponsive neighbor can cascade SIA across the domain: Router A queries
Router B, which queries Router C, which is down. If C never replies, B cannot
reply to A, and A resets B. Use `eigrp stub` on leaf routers to prevent query
propagation beyond the distribution layer.

### Redistribution Loops with OSPF

Mutual redistribution (EIGRP→OSPF and OSPF→EIGRP) without route tags creates
loops where routes re-enter their original protocol with altered metrics. Use
route tags at every redistribution point: tag EIGRP-originated routes and deny
those tags on re-entry to EIGRP.

### Named vs Classic Mode Confusion

Named mode uses wide metrics (64-bit) internally and scales them for the RIB.
Mixing classic and named mode routers in the same AS is supported but metrics
may appear different in `show` output. Verify with `show eigrp address-family`
(named) vs `show ip eigrp` (classic) — both should compute the same successor.

### Passive-Interface Misconfiguration

`passive-interface default` suppresses EIGRP on all interfaces. If new
interfaces are added without `no passive-interface`, neighbors will not form.
Check `show ip protocols` to see which interfaces are passive.
