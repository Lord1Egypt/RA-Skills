# IOS-XE Device Health CLI Reference

Vendor CLI commands organized by subsystem for Cisco IOS-XE 17.x devices.
All commands are privilege level 1 (read-only) unless noted otherwise.

## CPU Subsystem

| Command | Purpose | Key Output Fields |
|---------|---------|-------------------|
| `show processes cpu sorted` | Top processes by CPU usage | 5sec, 1min, 5min averages; per-process % |
| `show processes cpu history` | CPU utilization graph over time | ASCII graph of 72-hour CPU trend |
| `show processes cpu platform sorted 5sec` | Platform-level CPU (QFP, RP) | Per-core utilization, data plane vs control plane |
| `show platform software process slot R0 monitor` | Linux-level process view | RSS memory, CPU %, process tree |

### CPU Interpretation Notes

- The 5-second average includes both interrupt and process-level CPU. A high
  interrupt percentage often indicates a traffic-driven issue.
- `show processes cpu platform` separates data plane (QFP) from control plane (RP).
  High QFP utilization with normal RP usually means forwarding-path overload.
- The `history` command shows trends — a gradual increase suggests a growing
  problem, while spikes suggest event-driven issues.

## Memory Subsystem

| Command | Purpose | Key Output Fields |
|---------|---------|-------------------|
| `show memory statistics` | Overall memory allocation | Processor pool total, used, free |
| `show memory platform information` | Platform-specific memory | Per-region allocation, DRAM/SRAM split |
| `show processes memory sorted` | Per-process memory consumption | Allocated, freed, holding per process |
| `show memory dead` | Unreachable allocated memory | Dead memory blocks (leak indicator) |
| `show memory allocating-process totals` | Allocation summary by process | Net allocation per process over time |

### Memory Interpretation Notes

- IOS-XE uses a Linux kernel underneath. `show memory statistics` shows IOS
  memory pools, while `show platform software` commands show Linux-level memory.
- Memory "used" includes caches and buffers that can be freed under pressure.
  True available memory is higher than the "Free" counter suggests.
- Track `show processes memory sorted` output over time to identify leaks:
  a process with steadily increasing "Holding" value is the prime suspect.

## Interface Subsystem

| Command | Purpose | Key Output Fields |
|---------|---------|-------------------|
| `show interfaces summary` | One-line-per-interface status overview | State, IP address, method, protocol |
| `show interfaces counters errors` | Error counters per interface | Align, FCS, Xmit, Rcv, UnderSize, OutDiscard |
| `show interfaces [name]` | Detailed single-interface stats | Bandwidth, delay, reliability, txload, rxload, all counters |
| `show interfaces [name] counters` | Raw packet and byte counters | InOctets, OutOctets, InPkts, OutPkts |
| `show controllers [name]` | Hardware-level interface details | SFP type, DOM readings, PHY errors |
| `show ip interface brief` | IP address and status summary | IP, OK?, Method, Status, Protocol |

### Interface Interpretation Notes

- `show controllers` reveals SFP DOM (Digital Optical Monitoring) data:
  Tx power, Rx power, temperature. Low Rx power indicates a fiber or optic issue.
- Reliability is displayed as x/255. Values below 255/255 indicate recent errors.
  Calculate percentage: `reliability_value / 255 * 100`.
- txload and rxload are x/255 representing bandwidth utilization.
  Values above 200/255 (78%) warrant investigation.

## Routing Subsystem

| Command | Purpose | Key Output Fields |
|---------|---------|-------------------|
| `show ip route summary` | Route table size by protocol | Connected, static, OSPF, BGP, EIGRP counts |
| `show ip route` | Full routing table | Prefix, next-hop, interface, metric, age |
| `show ip bgp summary` | BGP neighbor overview | Neighbor IP, AS, state/prefix-count, up/down time |
| `show ip bgp neighbors [addr]` | Detailed BGP peer info | State, hold time, keepalive, messages sent/rcvd |
| `show ip ospf neighbor` | OSPF adjacency table | Neighbor ID, state, dead time, interface |
| `show ip ospf interface brief` | OSPF interface participation | Area, cost, state, neighbor count |
| `show ip eigrp neighbors` | EIGRP neighbor table | Address, interface, hold time, uptime, SRTT, Q count |

### Routing Interpretation Notes

- BGP "State/PfxRcd" showing a number means the session is established and
  that many prefixes are received. Any text state (Active, Idle, Connect)
  means the session is not established.
- OSPF neighbor states progress: Down → Init → 2-Way → ExStart → Exchange →
  Loading → Full. Only "Full" (or "2-Way" for DROther on broadcast) is healthy.
- EIGRP Q count (outstanding unacknowledged packets) should be 0. Non-zero
  Q count indicates communication problems with that neighbor.

## Environment and Platform

| Command | Purpose | Key Output Fields |
|---------|---------|-------------------|
| `show environment all` | Temperature, power, fan status | Sensor readings, alarm thresholds |
| `show platform` | Module and port status | Slot, state, insert time |
| `show platform software status control-processor brief` | RP status summary | CPU %, memory %, load average |
| `show redundancy` | RP redundancy state | Active/standby, switchover history |
| `show logging \| tail 50` | Recent syslog messages | Timestamp, facility, severity, message |
| `dir crashinfo:` | Crash dump files | Crash file names, dates, sizes |

### Environment Interpretation Notes

- Temperature readings vary by platform. The `show environment` command
  includes per-sensor thresholds — compare readings against those, not generic values.
- Power supply status should show "OK" or "Good". "Not Present" is expected
  for single-PSU configs. "Failed" or "Shutdown" requires immediate attention.
- Fan status "OK" with RPM values. Some platforms show "Low" before failure.
  Any fan in "Failed" state means the device is at risk of thermal shutdown.
