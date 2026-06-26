# Industry Terms: Systems / Distributed Systems

> **Usage note:** Use this file when the target direction is computer systems, distributed systems, storage, or cloud/runtime work rather than general SWE. It translates colloquial project descriptions into terminology that resonates across systems research and systems engineering.

---

## Core Systems Concerns

| User's description | Industry term |
|---|---|
| "made the system still work when machines failed" | Fault Tolerance / Failure Recovery |
| "reduced the delay for requests at high load" | Latency Reduction / Tail-latency Optimization |
| "made the system handle more work on the same hardware" | Throughput Scaling / Resource Efficiency |
| "kept noisy jobs from affecting other workloads" | Resource Isolation / Multi-tenant Interference Mitigation |
| "spread work across many machines" | Distributed Execution / Distributed Systems Design |
| "moved resources around automatically based on load" | Dynamic Scheduling / Elastic Resource Management |
| "avoided wasting compute on repeated work" | Work Deduplication / Systems Optimization |
| "measured how the system behaves under realistic workloads" | Workload Characterization / Quantified Evaluation |

## Infrastructure & Runtime Design

| User's description | Industry term |
|---|---|
| "built a layer that sits between apps and machines" | Systems Abstraction / Runtime Layer |
| "improved how tasks are coordinated across nodes" | Distributed Coordination / Cluster Orchestration |
| "changed how storage or files were organized" | Storage System Design / File-system Architecture |
| "reduced overhead in the execution stack" | Runtime Optimization / Systems Overhead Reduction |
| "used VMs or containers to isolate workloads" | Virtualization / Container Isolation |
| "made cloud jobs start faster or recover faster" | Cloud Systems Optimization / Fast Recovery Path |
| "debugged complex production behavior across many components" | Management and Troubleshooting of Complex Systems |
| "evaluated how the system behaves on new hardware" | Systems for Emerging Hardware / Hardware-software Co-design |

## Evidence & Framing

| User's description | Industry term |
|---|---|
| "showed the approach works with real deployments, not just toy tests" | Deployment-grounded Evaluation / Real-world Systems Evidence |
| "compared against strong existing systems" | State-of-the-art Systems Baseline Comparison |
| "reported both implementation details and measured benefits" | Design-and-implementation Study / Quantified Systems Evaluation |
| "used traces or production-like workloads for evaluation" | Trace-driven Evaluation / Production Workload Replay |
| "showed system tradeoffs instead of just one best number" | Systems Trade-off Analysis |
| "built a research prototype to validate an architecture idea" | Systems Prototype / Research Artifact |

## Low-level Engineering

| User's description | Industry term |
|---|---|
| "wrote a custom memory allocator or managed memory manually" | Custom Memory Management / Memory Pool Design |
| "used lock-free or wait-free techniques" | Lock-free / Wait-free Concurrency |
| "profiled and eliminated bottlenecks in hot paths" | Performance Profiling / Hot-path Optimization |
