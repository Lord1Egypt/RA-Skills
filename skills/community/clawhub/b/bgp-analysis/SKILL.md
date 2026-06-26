---
name: bgp-analysis
description: >-
  BGP protocol analysis with peer state diagnosis, path selection verification,
  route filtering validation, and convergence assessment. Multi-vendor coverage
  for Cisco IOS-XE/NX-OS, Juniper JunOS, and Arista EOS with protocol-first
  diagnostic reasoning.
license: Apache-2.0
metadata:
  safety: read-only
  author: network-security-skills-suite
  version: "1.0.0"
  openclaw: '{"emoji":"🔍","safetyTier":"read-only","requires":{"bins":["ssh"],"env":[]},"tags":["bgp","routing","protocol"],"mcpDependencies":[],"egressEndpoints":[]}'
---

# BGP Protocol Analysis

Protocol-reasoning-driven analysis skill for BGP peering, path selection, and
route propagation. Unlike device health checks that compare metrics against
thresholds, BGP analysis requires interpreting protocol state machines, walking
the best-path algorithm, and validating policy application across the control
plane.

Commands are labeled **[Cisco]**, **[JunOS]**, or **[EOS]** where syntax
diverges. Unlabeled statements apply to all three vendors.

## When to Use

- BGP peer reported down or stuck in a non-Established state
- Suspected route leak — prefixes appearing in tables where they should not
- Path selection not matching expectations after policy changes
- Convergence too slow after planned maintenance or unplanned failover
- Post-change verification of BGP configuration (new peers, policy updates, community changes)
- Capacity planning for prefix table growth or session scaling
- Investigating asymmetric routing caused by inconsistent BGP attributes

## Prerequisites

- SSH or console access to the router (read-only privilege sufficient)
- BGP process running on the device with at least one configured peer
- Knowledge of expected peer topology: which neighbors should be up, expected
  prefix counts per peer, intended path selection outcomes
- Awareness of configured routing policy: route-maps, prefix-lists, community
  filters, AS-path access lists, and local-preference assignments
- For iBGP: understanding of the route-reflector or full-mesh topology

## Procedure

Follow this diagnostic flow sequentially. Each step builds on the data from
prior steps. The procedure moves from broad inventory to targeted diagnosis.

### Step 1: BGP Session Inventory

Collect all peer states and compare against expected topology.

**[Cisco]**
```
show bgp ipv4 unicast summary
```

**[JunOS]**
```
show bgp summary
```

**[EOS]**
```
show ip bgp summary
```

Record each neighbor: address, AS number, state, prefixes received, up/down
time. Compare against expected topology — every configured peer should appear.
A peer missing from output means it was never configured or was removed. Any
peer not showing a numeric prefix count is not Established — proceed to Step 2
for that peer.

### Step 2: Peer State Diagnosis

For any peer not in Established state, the BGP FSM state reveals the failure
domain. This is the core diagnostic reasoning step.

**[Cisco]**
```
show bgp ipv4 unicast neighbors [addr] | include state|last reset|error
```

**[JunOS]**
```
show bgp neighbor [addr] | match "State|Last Error|Last State"
```

**[EOS]**
```
show ip bgp neighbors [addr] | include state|last reset|error
```

Interpret the FSM state to isolate the failure:
- **Idle** → BGP process not attempting connection. Causes: administratively
  shut down, no route to peer address, configured remote AS does not match, or
  maximum-prefix limit hit triggering teardown.
- **Connect** → TCP SYN sent, waiting for response. Peer is unreachable at
  Layer 3 or a firewall is blocking TCP port 179.
- **Active** → TCP connection attempt failed, retrying. Same causes as Connect
  but the router has cycled back. Check: ACLs blocking port 179, peer not
  configured for this neighbor, peer address unreachable.
- **OpenSent** → TCP connected, OPEN message sent, no reply. Remote end
  accepted TCP but is not sending OPEN — typically remote BGP not configured
  for this neighbor or remote peer in admin shutdown.
- **OpenConfirm** → OPEN received but parameters rejected. Check: AS number
  mismatch, capability negotiation failure (AFI/SAFI mismatch), hold timer
  negotiation failure, authentication (MD5/TCP-AO) mismatch.

Check "last reset reason" and "last error" fields — they often provide the
definitive cause. Reference: `references/state-machine.md` for full FSM detail.

### Step 3: Route Table Analysis

For Established peers, verify prefix exchange matches expectations.

**[Cisco]**
```
show bgp ipv4 unicast neighbors [addr] routes | include Total
```

**[JunOS]**
```
show route receive-protocol bgp [addr] table summary
```

**[EOS]**
```
show ip bgp neighbors [addr] received-routes | include Total
```

Compare received prefix count against baseline. Significant deviation indicates:
- Drop >10% → upstream is withdrawing routes (maintenance, filter change, or failure)
- Increase >10% → route leak or new prefixes originated upstream
- Zero received → peer is Established but sending no routes (missing export policy
  on JunOS, or outbound filter on remote blocking everything)

Check advertised prefix count similarly — confirm this router is sending the
expected number of routes to each peer.

### Step 4: Path Selection Verification

When traffic takes an unexpected path, walk the BGP best-path algorithm to
identify which attribute is making the selection.

**[Cisco]**
```
show bgp ipv4 unicast [prefix] bestpath
```

**[JunOS]**
```
show route [prefix] detail | match "AS path|Local|MED|Weight|preference"
```

**[EOS]**
```
show ip bgp [prefix] detail
```

The best-path algorithm evaluates in this order (first difference wins):
1. **Weight** (Cisco/EOS local, highest wins — JunOS does not use weight)
2. **Local Preference** (highest wins, default 100)
3. **Locally originated** (network/aggregate preferred over learned)
4. **AS Path length** (shortest wins)
5. **Origin** (IGP < EGP < Incomplete)
6. **MED** (lowest wins, compared only within same neighbor AS by default)
7. **eBGP over iBGP** (external preferred)
8. **IGP metric to next-hop** (lowest wins)
9. **Router ID** (lowest wins, tiebreaker)

Identify which attribute selects the current best path. If unexpected, check
the route-map or policy applying that attribute on ingress.

### Step 5: Route Filtering Validation

Verify that route-maps, prefix-lists, and community filters apply as intended.

**[Cisco]**
```
show bgp ipv4 unicast neighbors [addr] policy
```

**[JunOS]**
```
show policy [policy-name] | display detail
```

**[EOS]**
```
show route-map [name]
```

For suspected route leaks: examine the RIB for prefixes that should not be
present. Check inbound filters on the peer that is the source. Common leak
causes: missing or misordered prefix-list entry, regex error in AS-path
filter, community match that is too broad.

For missing routes: verify the outbound policy on the advertising peer is not
filtering the prefix. On JunOS, a peer with no export policy sends nothing by
default — this is the most common JunOS-specific omission.

### Step 6: Convergence Assessment

Evaluate convergence behavior and route stability.

**[Cisco]**
```
show bgp ipv4 unicast dampening dampened-paths
```

**[JunOS]**
```
show route damping suppressed
```

**[EOS]**
```
show ip bgp dampening dampened-paths
```

Check for dampened (suppressed) routes — these indicate persistent flapping.
Review the BGP update activity: high update/withdrawal rates indicate churn.
After a planned change, measure convergence time from the change event to the
last BGP update. Compare against the target convergence window.

## Threshold Tables

Operational parameter norms for BGP — these are protocol-level expectations, not
device resource thresholds.

| Parameter | Cisco Default | JunOS Default | EOS Default | Notes |
|-----------|--------------|---------------|-------------|-------|
| Hold Timer | 180s | 90s | 180s | Negotiated to lower value |
| Keepalive Interval | 60s | 30s | 60s | Hold/3 by convention |
| ConnectRetry Timer | 120s | Varies | 120s | Time between TCP attempts |
| MRAI (eBGP) | 30s | 0s (immediate) | 30s | Minimum Route Advertisement Interval |
| MRAI (iBGP) | 5s | 0s | 5s | Lower than eBGP for faster iBGP convergence |
| Default Local Pref | 100 | 100 | 100 | Same across vendors |

**Table Size Norms (IPv4 unicast):**

| Deployment Type | Expected Prefixes | Warning | Critical |
|----------------|-------------------|---------|----------|
| Internet edge (full table) | ~950K | >1M | >1.1M |
| Internet edge (partial) | 5K–100K | Varies | Per design |
| Enterprise WAN | 100–10K | >2x baseline | >5x baseline |
| Data center leaf | 50–5K | >2x baseline | >5x baseline |

**Convergence Targets:**

| Scenario | Target | Acceptable | Degraded |
|----------|--------|------------|----------|
| eBGP failover | < 90s | 90–180s | > 180s |
| iBGP reconvergence | < 30s | 30–60s | > 60s |
| Full table reload | < 5min | 5–10min | > 10min |

## Decision Trees

### Peer Not Established

```
Peer not in Established state
├── State: Idle
│   ├── Admin shut? → Check config for "neighbor shutdown" / "deactivate"
│   ├── No route to peer? → Check IGP/static route to peer address
│   ├── Prefix-limit exceeded? → Check logs for max-prefix teardown
│   └── AS mismatch? → Verify "remote-as" matches peer's local AS
│
├── State: Connect / Active
│   ├── Peer reachable? → Ping/traceroute peer address
│   │   ├── No → Fix Layer 3 reachability (IGP, static route)
│   │   └── Yes → TCP port 179 blocked?
│   │       ├── ACL on local device? → Check interface/control-plane ACL
│   │       ├── ACL on remote device? → Check remote inbound ACL
│   │       └── Firewall between peers? → Verify TCP/179 permitted both directions
│   └── Peer configured? → Verify remote has this router as neighbor
│
├── State: OpenSent
│   ├── Remote not sending OPEN → Peer may not be configured for this neighbor
│   ├── TCP resets after connect → Check for TTL issues (eBGP multihop)
│   └── Authentication? → Verify MD5/TCP-AO passwords match both sides
│
├── State: OpenConfirm
│   ├── Capability mismatch? → Check AFI/SAFI (IPv4/IPv6/VPNv4) match
│   ├── AS mismatch in OPEN? → Verify configured AS matches OPEN AS
│   ├── Hold timer = 0 on one side? → Both peers must agree or both use 0
│   └── Check NOTIFICATION message → Decode error code/subcode
│
└── Established but dropping
    ├── Hold timer expiry? → Keepalives not arriving (CPU, QoS, path issue)
    ├── NOTIFICATION received? → Decode error code for root cause
    ├── Route refresh storm? → Peer sending excessive route-refresh requests
    └── Max-prefix limit? → Peer sending more prefixes than limit allows
```

### Unexpected Route Selection

```
Wrong path selected for prefix
├── Check Weight (Cisco/EOS only)
│   └── Weight set via route-map? → Highest weight wins
├── Check Local Preference
│   └── Local pref differs? → Set via inbound route-map; highest wins
├── Check AS Path Length
│   ├── AS prepending applied? → Verify prepend count
│   └── AS path differs? → Shortest wins
├── Check Origin
│   └── IGP vs Incomplete? → IGP (network statement) preferred
├── Check MED
│   ├── MED comparison enabled across AS? → "always-compare-med"
│   └── MED set correctly? → Lowest wins within same neighbor AS
├── Check eBGP vs iBGP
│   └── External path preferred over internal if equal above
├── Check IGP metric to next-hop
│   └── Closest exit wins (hot-potato routing)
└── All equal → Lowest Router ID wins (or oldest route if stable)
```

## Report Template

```
BGP ANALYSIS REPORT
====================
Device: [hostname]
Vendor: [Cisco | JunOS | EOS]
Check Time: [timestamp]
Performed By: [operator/agent]

SESSION STATUS:
- Total configured peers: [n]
- Established: [n] | Not Established: [n]
- Peers requiring attention: [list with FSM states]

FINDINGS:
1. [Severity] [Category] — [Description]
   Peer: [neighbor address / AS]
   Observed: [state or metric]
   Expected: [normal state or value]
   Root Cause: [diagnosis from decision tree]
   Action: [recommended remediation]

PATH ANALYSIS:
- Prefix: [prefix under review]
- Selected path via: [next-hop / AS path]
- Selecting attribute: [which best-path attribute decided]
- Expected path: [if different, what was expected and why]

ROUTE TABLE SUMMARY:
- IPv4 prefixes received: [total across all peers]
- Baseline deviation: [% change from expected]

RECOMMENDATIONS:
- [Prioritized action list]

NEXT CHECK: [based on severity — CRITICAL: 4hr, WARNING: 24hr, HEALTHY: 7d]
```

## Troubleshooting

### Session Flapping

Peer cycles between Established and Idle/Active repeatedly. Common causes:
unstable underlying transport (IGP flap, link errors), aggressive hold timers
on congested control planes, or MTU issues on the path causing fragmented
keepalives to be dropped. Check `last reset reason` and correlate with interface
or IGP events at the same timestamps.

### Route Oscillation

The same prefix alternates between two or more paths. Caused by inconsistent
MED comparison across route reflectors, or deterministic-MED not enabled when
multiple exit points exist to the same neighbor AS. Enable `always-compare-med`
and `deterministic-med` to stabilize.

### Memory Pressure from Full Table

Full Internet table (~950K IPv4 prefixes) requires 1–2 GB of RIB memory
depending on path diversity. Symptoms: slow convergence, peer resets during
table reload. Mitigate with soft-reconfiguration inbound (trades memory for
stability) or ORF (Outbound Route Filtering) to reduce inbound load.

### Community Stripping

Routes arrive without expected communities. Check each transit AS in the path —
many providers strip non-standard communities by default. Use large communities
(RFC 8092) for end-to-end propagation across providers that strip standard
communities.

### JunOS Default Export Policy

JunOS sends no routes to a peer without an explicit export policy. If a peer
shows Established with zero prefixes sent, add an export policy. This is the
most common JunOS-specific BGP issue and does not occur on Cisco or EOS.
