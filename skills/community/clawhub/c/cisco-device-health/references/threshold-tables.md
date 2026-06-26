# Cisco IOS-XE / NX-OS Threshold Tables

Detailed threshold definitions for device health parameters across both platforms.
Platform-specific baselines are noted where they differ. Adjust thresholds per
device role and traffic profile.

## CPU Thresholds

### RP CPU 5-Minute Average (IOS-XE)

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–40% | Typical operating range | No action |
| Warning | 41–70% | Elevated load | Identify top processes, monitor trend |
| Critical | 71–90% | High load, risk of protocol delays | Investigate top consumers, reduce load |
| Emergency | > 90% | Control plane at risk | Immediate intervention, collect show tech |

### Supervisor CPU (NX-OS)

NX-OS supervisor baseline runs 5–10% higher than IOS-XE RP due to Linux kernel and
daemon overhead. Adjust thresholds accordingly.

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–50% | Typical for NX-OS supervisor | No action |
| Warning | 51–75% | Elevated load | Identify top processes via `show processes cpu sort` |
| Critical | 76–90% | High load, risk of protocol timeouts | Investigate consumers, check for stuck processes |
| Emergency | > 90% | Supervisor at risk | Immediate triage, collect show tech-support |

### CPU 5-Second Spike (IOS-XE)

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–60% | Transient spikes expected | No action |
| Warning | 61–80% | Frequent spikes | Check for polling storms, route churn |
| Critical | 81–95% | Sustained spikes affecting protocol timers | Identify trigger, reduce load |
| Emergency | > 95% | CPU saturation | Risk of process crash, immediate triage |

### CPU Interrupt Percentage (IOS-XE)

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–20% | Normal packet processing | No action |
| Warning | 21–40% | Elevated punt rate | Verify expected traffic levels |
| Critical | 41–70% | Possible traffic storm or punted traffic | Check for loops, broadcast storms, CoPP |
| Emergency | > 70% | RP data plane overload | Apply CoPP or ACL to filter punted traffic |

### QFP Drop Rate (IOS-XE only)

| Level | Drops/sec | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | < 100 | Normal operation | No action |
| Warning | 100–1,000 | Elevated drops | Identify drop reason via QFP feature stats |
| Critical | 1,000–10,000 | Significant data plane issues | Investigate ACL, NAT, or traffic anomalies |
| Emergency | > 10,000 | Data plane severely impaired | Immediate investigation, may need traffic diversion |

## Memory Thresholds

### Processor Memory Used (IOS-XE)

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–70% | Healthy memory utilization | No action |
| Warning | 71–80% | Elevated usage | Identify large consumers, monitor trend |
| Critical | 81–90% | Memory pressure, MALLOCFAIL risk | Check for leaks, consider feature reduction |
| Emergency | > 90% | Imminent MALLOCFAIL | Schedule reload, open TAC case |

### System Memory (NX-OS)

NX-OS baseline memory usage is 55–65% at steady state. Thresholds reflect this
higher baseline.

| Level | MemFree % | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | > 30% | Healthy for NX-OS | No action |
| Warning | 20–30% | Elevated usage | Identify top consumers, monitor trend |
| Critical | 10–20% | Memory pressure | Investigate growth, check for leaks |
| Emergency | < 10% | Risk of OOM, process kills | Immediate investigation, plan reload |

### Memory Fragmentation Ratio (IOS-XE only)

Ratio of largest free block to total free memory. Not applicable on NX-OS
(Linux virtual memory manager handles paging).

| Level | Ratio | Meaning | Action |
|-------|-------|---------|--------|
| Normal | > 20% | Healthy allocation | No action |
| Warning | 10–20% | Moderate fragmentation | Monitor for degradation |
| Critical | 5–10% | Significant fragmentation | Schedule maintenance window reload |
| Emergency | < 5% | Severe — MALLOCFAIL imminent | Reload ASAP during next window |

## Interface Thresholds

### Error Rate (both platforms)

| Level | Rate | Meaning | Action |
|-------|------|---------|--------|
| Normal | < 0.001% | No significant errors | No action |
| Warning | 0.001–0.01% | Low error rate | Monitor, check optic levels |
| Critical | 0.01–0.1% | Significant errors | Investigate Layer 1 (cable/SFP) |
| Emergency | > 0.1% | High error rate | Replace cable/optic, check remote end |

### Output Drops Per Hour (both platforms)

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–50/hr | Minimal drops | No action |
| Warning | 51–500/hr | Moderate congestion | Review QoS policy, check bandwidth |
| Critical | 501–5,000/hr | Significant congestion | Tune QoS, consider link upgrade |
| Emergency | > 5,000/hr | Severe congestion | Immediate QoS intervention or upgrade |

### CRC Errors Per Hour (both platforms)

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0 | Clean signal | No action |
| Warning | 1–10/hr | Intermittent L1 issue | Monitor, check SFP DOM readings |
| Critical | 11–100/hr | Active L1 problem | Replace cable, clean fiber, reseat SFP |
| Emergency | > 100/hr | Severe L1 failure | Replace cable and SFP, check patch panel |

### SFP Optical Power (both platforms)

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | Within vendor spec | Clean optical link | No action |
| Warning | Within 2 dBm of low threshold | Degrading signal | Clean fiber ends, monitor |
| Critical | Below low warning threshold | Poor signal quality | Replace fiber run or SFP |
| Emergency | Below low alarm threshold | Link at risk | Immediate replacement |

## Routing Thresholds

### BGP Session Health (both platforms)

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | Established, stable prefix count | Healthy peering | No action |
| Warning | Prefix count changed > 10% from baseline | Route churn | Investigate upstream |
| Critical | Session flap in last hour | Peer instability | Check transport, timers |
| Emergency | Session down > 5 minutes | Peering failure | Verify connectivity, peer status |

### OSPF Adjacency Health (both platforms)

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | All neighbors Full | Healthy adjacencies | No action |
| Warning | Neighbor stuck in ExStart/Exchange > 30s | Slow formation | Check MTU, area config |
| Critical | Neighbor flap in last hour | Instability | Check interface, review timers |
| Emergency | Expected neighbor missing | Adjacency lost | Verify interface, check remote device |

### Route Table Size (both platforms)

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | Within 10% of baseline | Stable | No action |
| Warning | 10–25% deviation | Moderate change | Verify expected changes |
| Critical | 25–50% deviation | Significant change | Investigate route source |
| Emergency | > 50% deviation or < 50% of baseline | Major event | Immediate investigation |

### vPC Health (NX-OS only)

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | Peer adjacency formed, all vPCs consistent | Healthy | No action |
| Warning | Type-1 consistency check failure | Config divergence | Resolve config mismatch |
| Critical | Peer-link degraded or single member down | Reduced redundancy | Investigate link, plan repair |
| Emergency | Peer-link down or peer unreachable | Traffic orphaned | Immediate failover assessment |

## Environment Thresholds

### Temperature (both platforms)

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | Below warning threshold (per sensor) | Within operating spec | No action |
| Warning | Within 5°C of shutdown threshold | Approaching limit | Check fans, airflow, room cooling |
| Critical | Above warning, below shutdown | Thermal stress | Fix cooling, reduce load if possible |
| Emergency | At or above shutdown threshold | Imminent shutdown | Emergency cooling, power down modules |

### Power Supply (both platforms)

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | All PSUs OK, redundancy active | Fully protected | No action |
| Warning | Single PSU, no redundancy | Unprotected | Plan PSU installation |
| Critical | Redundant PSU failed | Lost redundancy | RMA failed PSU |
| Emergency | Single PSU degraded output | Power loss risk | Emergency maintenance |

### Fan Status (both platforms)

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | All fans OK, RPM within spec | Adequate cooling | No action |
| Warning | Fan RPM low or degraded | Reduced cooling | Monitor temp, plan replacement |
| Critical | One fan failed | Thermal risk increasing | RMA fan tray, increase monitoring |
| Emergency | Multiple fans failed | Imminent thermal shutdown | Reduce load, emergency service |

### NX-OS Module Health

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | All modules "ok" in `show module` | Fully operational | No action |
| Warning | Module diagnostics show minor failures | Degraded performance possible | Monitor, schedule diagnostics |
| Critical | Module in "powered-down" or error state | Ports on module are down | Investigate, attempt power cycle |
| Emergency | Module failure with core dump | Hardware or software fault | Collect diagnostics, open TAC case |
