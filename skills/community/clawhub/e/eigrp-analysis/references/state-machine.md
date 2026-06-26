# EIGRP DUAL Finite State Machine

Reference for the Diffusing Update Algorithm (DUAL) that governs EIGRP path
computation. Unlike link-state protocols (OSPF, IS-IS) that flood full topology
databases, EIGRP uses a diffusing computation with query/reply mechanics to
guarantee loop-free convergence without global topology knowledge.

## DUAL States

EIGRP routes exist in one of two states:

```
┌──────────┐          Query sent          ┌──────────┐
│          │  ──────────────────────────►  │          │
│ PASSIVE  │    (successor lost,          │  ACTIVE  │
│          │     no feasible successor)   │          │
│          │  ◄──────────────────────────  │          │
└──────────┘   All replies received       └──────────┘
               (new successor computed)       │
                                              │ SIA timer
                                              │ expires
                                              ▼
                                        Neighbor reset
                                        (reply forced)
```

### Passive State (Normal Operation)

- Route has a valid successor installed in the routing table
- Feasible successors (if any) are available as instant backup paths
- No queries outstanding — DUAL computation is quiescent
- The route can remain Passive indefinitely while the successor is stable

### Active State (Diffusing Computation)

- Triggered when the successor is lost AND no feasible successor satisfies the
  feasibility condition
- Router sends Query packets to ALL neighbors (except the successor that
  triggered the event) asking for alternate paths
- Each neighbor either: replies immediately (has a feasible successor itself),
  or goes Active and queries its own neighbors (the "diffusing" behavior)
- The route remains Active until ALL queries are answered

### Active State Substates

DUAL tracks two independent conditions during Active state:

| Substate | Input Event Origin | Reply Status |
|----------|-------------------|--------------|
| Active (0) | Local event | Waiting for all replies |
| Active (1) | Local event | Query origin — will change distance |
| Active (2) | Query from successor | Waiting for all replies |
| Active (3) | Query from successor | Query origin — will change distance |

The substate determines whether the router can change its distance
advertisement before or after replies are collected.

## Feasibility Condition

The feasibility condition is DUAL's loop-prevention mechanism:

```
A neighbor N is a feasible successor for destination D if:

    RD(N, D) < FD(D)

Where:
    RD(N, D) = Reported Distance — the metric neighbor N advertises
               for destination D (N's own computed cost to D)
    FD(D)    = Feasible Distance — the lowest metric this router has
               ever used for destination D
```

### Why This Guarantees Loop-Freedom

If a neighbor's cost to the destination (RD) is less than the best cost this
router has ever had (FD), then that neighbor cannot be routing through this
router to reach the destination — because if it were, its cost would be at least
as high as this router's cost plus the link cost.

### Example

```
Router A ──── Router B ──── Router C ──── Destination
  10            5              3

FD at A = 10 + 5 + 3 = 18
RD from B = 5 + 3 = 8

Feasibility check: RD(B) = 8 < FD(A) = 18 → B is a feasible successor ✓

If Router B's link to C fails:
RD from B = ∞ (no path)
Router A loses successor → goes Active (no other FS exists)
```

### Successor vs Feasible Successor

| Role | Definition | RIB Installed? | Immediate Failover? |
|------|-----------|----------------|---------------------|
| Successor | Neighbor with lowest FD to destination | Yes | N/A — it IS the current path |
| Feasible Successor | Neighbor where RD < current FD | No (backup) | Yes — instant failover, no query |
| Neither (fail FS check) | RD ≥ current FD | No | No — must go Active and query |

## Query and Reply Process

### Query Scope

When a route goes Active, queries propagate through the EIGRP domain:

```
Query Originator
├── Sends Query to all neighbors (except the lost successor)
├── Each neighbor:
│   ├── Has feasible successor? → Sends Reply immediately
│   └── No feasible successor? → Goes Active, queries its own neighbors
│       └── (Diffusion continues deeper into the network)
└── Waits for all Replies before recomputing
```

**Query scope control mechanisms:**

| Mechanism | Effect on Queries | Configuration |
|-----------|------------------|---------------|
| Stub routing | Stub routers never receive queries | `eigrp stub connected summary` |
| Summarization | Queries stop at summary boundary | `ip summary-address eigrp` |
| Distribute-list | Filters routes but does NOT limit query propagation | `distribute-list` |
| Route filtering | Removes routes but queries still propagate | `route-map` |

> **Critical distinction:** Distribute-lists and route-maps filter routes from
> the topology table, but they do NOT prevent query propagation. Only stub
> configuration and summarization contain query scope.

### Reply Tracking

DUAL tracks replies per-neighbor per-destination:

1. Query sent to neighbor N for destination D → reply pending flag set
2. Reply received from N for D → flag cleared, update D's metric from N
3. All reply flags cleared → recompute successor, return to Passive

### Stuck-in-Active (SIA) Handling

```
Route goes Active at T=0
│
├── T = 0–90s: Waiting for replies normally
│
├── T = 90s (half SIA timer): SIA-Query sent to unresponsive neighbors
│   └── If SIA-Reply received → timer reset, continue waiting
│
├── T = 180s (full SIA timer): No reply received
│   └── Unresponsive neighbor is RESET (adjacency torn down)
│       ├── This forces a reply (neighbor removal counts as reply)
│       ├── Remaining replies may still be outstanding from other neighbors
│       └── Once all replies collected → recompute, return to Passive
│
└── Active timer (default 3 min, configurable with `timers active-time`)
    └── If exceeded → all unresponsive neighbors reset, route cleared
```

**SIA-Query/SIA-Reply** (introduced in later IOS versions) is the intermediate
check that prevents unnecessary neighbor resets. Before SIA-Query existed,
any neighbor that did not reply within the active timer was immediately reset.

## Composite Metric Formula

### Classic Mode (32-bit)

```
Metric = 256 × [ K1 × Bandwidth + (K2 × Bandwidth) / (256 - Load) + K3 × Delay ]
         × [ K5 / (Reliability + K4) ]    ← only if K5 ≠ 0

Where:
    Bandwidth = 10^7 / minimum_bandwidth_kbps (along the path)
    Delay     = sum_of_delays / 10 (delays in tens of microseconds)
    Load      = 0–255 (interface tx load)
    Reliability = 0–255 (interface reliability)
```

With default K-values (K1=1, K2=0, K3=1, K4=0, K5=0):

```
Metric = 256 × (Bandwidth + Delay)

    = 256 × (10^7 / min_BW_kbps + cumulative_delay / 10)
```

The K5=0 special case eliminates the reliability/load term entirely.

### Named Mode — Wide Metrics (64-bit)

Named EIGRP extends the metric to 64 bits to differentiate high-speed
interfaces (10G, 40G, 100G) that produce identical classic metrics:

```
Wide Metric = K1 × (EIGRP_BANDWIDTH × EIGRP_WIDE_SCALE)
            + K3 × (EIGRP_DELAY × EIGRP_WIDE_SCALE)
            + K6 × EIGRP_EXTENDED_ATTRIBUTES

Where:
    EIGRP_BANDWIDTH = 10^7 × 65536 / interface_bandwidth_kbps
    EIGRP_DELAY = interface_delay_in_picoseconds / 10^6
    EIGRP_WIDE_SCALE = 65536
```

The 64-bit metric is scaled down by a `rib-scale` factor (default 128) before
installation in the routing table, which uses 32-bit metrics.

### Metric Comparison Examples

| Link Speed | Classic BW Component | Wide BW Component |
|-----------|---------------------|-------------------|
| 100 Mbps | 100,000 | 6,553,600,000 |
| 1 Gbps | 10,000 | 655,360,000 |
| 10 Gbps | 1,000 | 65,536,000 |
| 40 Gbps | 250 | 16,384,000 |
| 100 Gbps | 100 | 6,553,600 |

Note how classic mode produces the same value (100) for both 100G links — wide
metrics distinguish them clearly.
