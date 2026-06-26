# Cisco IOS-XE / NX-OS CLI Reference

Commands organized by subsystem with IOS-XE and NX-OS side by side.
All commands are read-only (show/display only). IOS-XE validated against 17.3+,
NX-OS validated against 10.2+.

## CPU Subsystem

| Subsystem | IOS-XE Command | NX-OS Command | Key Output |
|-----------|---------------|---------------|------------|
| CPU summary | `show processes cpu sorted` | `show system resources` | 5sec/1min/5min avg (IOS-XE); kernel/user/idle % (NX-OS) |
| CPU history | `show processes cpu history` | *(not available)* | 72-hour ASCII trend graph |
| Top processes | `show processes cpu sorted \| head 20` | `show processes cpu sort \| head 20` | Per-process CPU consumption |
| Platform CPU | `show platform software status control-processor brief` | `show module` | RP load avg (IOS-XE); per-module status (NX-OS) |
| Data plane | `show platform hardware qfp active statistics drop` | `show hardware internal errors module [n]` | QFP drops (IOS-XE); ASIC errors (NX-OS) |

### IOS-XE CPU Notes

- `show processes cpu sorted` reports RP CPU only. Data plane (QFP) health requires
  `show platform hardware qfp active statistics drop`.
- The 5-second average includes interrupt-level CPU. High interrupt % with low
  process % indicates traffic-driven load (punt path).
- `show platform software status control-processor brief` gives per-core breakdown
  on multi-core RPs — useful for identifying single-core bottlenecks.

### NX-OS CPU Notes

- `show system resources` is the primary CPU command. Reports CPU as kernel%, user%,
  idle%. NX-OS has no direct equivalent to IOS-XE's `show processes cpu history`.
- NX-OS control plane typically runs 5–10% higher CPU at idle than IOS-XE due to
  Linux kernel overhead and system daemon activity.
- Per-module health via `show module` — each linecard has its own CPU/memory.
  A failing module may not impact supervisor CPU metrics.

## Memory Subsystem

| Subsystem | IOS-XE Command | NX-OS Command | Key Output |
|-----------|---------------|---------------|------------|
| Memory summary | `show memory statistics` | `show system resources` | Total/used/free pools (IOS-XE); MemTotal/MemUsed/MemFree in KB (NX-OS) |
| Top consumers | `show processes memory sorted \| head 15` | `show processes memory \| head 15` | Per-process allocation |
| Platform memory | `show memory platform information` | `show system internal mts buffers summary` | Per-region DRAM/SRAM (IOS-XE); MTS buffers (NX-OS) |
| Leak detection | `show memory dead` | `show processes memory` (watch over time) | Dead/unreachable blocks (IOS-XE) |
| Fragmentation | `show memory statistics` (Largest Free field) | *(not applicable — Linux manages)* | Largest contiguous free block |

### IOS-XE Memory Notes

- IOS memory pools (processor, I/O) are separate from Linux-level memory.
  `show memory statistics` shows IOS pools; `show platform software process slot R0 monitor` shows Linux.
- Fragmentation matters on IOS-XE: if largest free block < 10% of total free,
  allocations can fail even with free memory available (MALLOCFAIL).
- `show memory dead` reveals allocated-but-unreachable blocks — a definitive leak indicator.

### NX-OS Memory Notes

- NX-OS reports Linux-style memory. Normal baseline usage is 55–65% because the
  kernel, system daemons, and feature processes all reside in memory at boot.
- No concept of memory fragmentation as in IOS-XE — Linux's virtual memory
  manager handles page allocation differently.
- Watch MemFree trend: dropping below 15% of MemTotal warrants investigation.

## Interface Subsystem

| Subsystem | IOS-XE Command | NX-OS Command | Key Output |
|-----------|---------------|---------------|------------|
| Summary | `show interfaces summary` | `show interfaces summary` | One-line per-interface status |
| Error counters | `show interfaces counters errors` | `show interfaces counters errors` | Per-interface error counts |
| Detailed stats | `show interfaces [name]` | `show interface [name]` | Full counters, rates, drops |
| Hardware detail | `show controllers [name]` | `show hardware internal errors module [n]` | SFP DOM, PHY errors (IOS-XE); ASIC drops (NX-OS) |
| L1 diagnostics | `show controllers [name]` (DOM section) | `show interface [name] transceiver details` | Tx/Rx power, temperature, voltage |
| IP summary | `show ip interface brief` | `show ip interface brief` | IP, status, protocol |

### Interface Interpretation Notes

- Both platforms: CRC errors almost always mean Layer 1 (cabling, optics, SFP seating).
- IOS-XE: `show controllers` includes SFP DOM (Tx/Rx power, temp). Low Rx power = fiber/optic issue.
- NX-OS: `show interface transceiver details` provides DOM data. Also check
  `show hardware internal errors` for ASIC-level drops invisible to `show interface`.
- Output drops on both platforms indicate egress congestion — check QoS policy and link capacity.

## Routing Subsystem

| Subsystem | IOS-XE Command | NX-OS Command | Key Output |
|-----------|---------------|---------------|------------|
| Route summary | `show ip route summary` | `show ip route summary` | Per-protocol route counts |
| BGP peers | `show ip bgp summary` | `show bgp ipv4 unicast summary` | Neighbor state, prefix count |
| BGP detail | `show ip bgp neighbors [addr]` | `show bgp ipv4 unicast neighbors [addr]` | Session state, timers, messages |
| OSPF neighbors | `show ip ospf neighbor` | `show ip ospf neighbors` | Neighbor ID, state, dead time |
| EIGRP neighbors | `show ip eigrp neighbors` | `show ip eigrp neighbors` | Address, hold time, SRTT, Q count |
| vPC state | *(not applicable)* | `show vpc brief` | vPC domain, peer-link, keepalive |

### Routing Notes

- IOS-XE BGP: `State/PfxRcd` column showing a number = established. Any text = not established.
- NX-OS BGP: command syntax differs (`show bgp ipv4 unicast summary` not `show ip bgp summary`).
- NX-OS vPC: peer-link failure orphans traffic. `show vpc brief` → peer status must be "peer adjacency
  formed ok." Consistency check failures indicate config divergence between peers.
- OSPF: only `Full` state is healthy (or `2-Way` for DROther on broadcast networks).

## Environment and Platform

| Subsystem | IOS-XE Command | NX-OS Command | Key Output |
|-----------|---------------|---------------|------------|
| Environment | `show environment all` | `show environment` | Temp, power, fans |
| Platform status | `show platform` | `show module` | Module/slot state |
| RP status | `show platform software status control-processor brief` | `show system resources` | CPU, memory, load avg |
| Redundancy | `show redundancy` | `show system redundancy status` | Active/standby state |
| Syslog | `show logging \| tail 50` | `show logging last 50` | Recent log messages |
| Crash data | `dir crashinfo:` | `show cores` | Crash dump files |
| Reset reason | `show version \| include reason` | `show system reset-reason` | Last reload/reset cause |
| VDC context | *(not applicable)* | `show vdc current` | Current VDC identity |

### Environment Notes

- Both platforms: any power supply showing "Failed" or fan showing "Failed" is an emergency.
- IOS-XE: temperature thresholds are per-sensor and shown in `show environment all` output.
- NX-OS: `show module` is critical — a module not in "ok" state may silently drop traffic
  on its ports without affecting supervisor metrics.
- NX-OS: `show cores` lists core dumps from any process. Presence of recent cores warrants TAC case.
