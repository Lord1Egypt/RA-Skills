# Device Health Threshold Tables

Detailed threshold definitions for Cisco IOS-XE device health parameters.
These values represent general guidance — adjust baselines per device role
and traffic profile.

## CPU Thresholds

### CPU 5-Minute Average

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–40% | Typical operating range | No action needed |
| Warning | 41–70% | Elevated load | Identify top processes, monitor trend |
| Critical | 71–90% | High load, risk of packet loss | Investigate top consumers, consider load reduction |
| Emergency | > 90% | Control plane at risk | Immediate intervention, collect show tech |

### CPU 5-Second Spike

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–60% | Transient spikes expected | No action needed |
| Warning | 61–80% | Frequent spikes | Check for polling storms, route churn |
| Critical | 81–95% | Sustained spikes | Identify trigger, reduce load |
| Emergency | > 95% | CPU saturation | Risk of process crash, immediate triage |

### CPU Interrupt Percentage

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–20% | Normal packet processing | No action needed |
| Warning | 21–40% | Elevated packet rate | Verify expected traffic levels |
| Critical | 41–70% | Possible traffic storm | Check for loops, broadcast storms |
| Emergency | > 70% | Data plane overload | Apply CoPP or ACL to filter traffic |

## Memory Thresholds

### Processor Memory Used Percentage

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–70% | Healthy memory utilization | No action needed |
| Warning | 71–80% | Elevated usage | Identify large consumers, monitor trend |
| Critical | 81–90% | Memory pressure | Check for leaks, consider feature reduction |
| Emergency | > 90% | Risk of MALLOCFAIL | Schedule reload, open TAC case |

### Memory Fragmentation Ratio

Ratio of largest free block to total free memory.

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | > 20% | Healthy allocation pattern | No action needed |
| Warning | 10–20% | Moderate fragmentation | Monitor for degradation |
| Critical | 5–10% | Significant fragmentation | Schedule maintenance window reload |
| Emergency | < 5% | Severe fragmentation | Imminent MALLOCFAIL risk, reload ASAP |

### Dead Memory

| Level | Threshold | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | 0 bytes | No leaked memory | No action needed |
| Warning | < 1 MB | Minor leak | Monitor growth rate |
| Critical | 1–10 MB | Active memory leak | Identify leaking process, plan reload |
| Emergency | > 10 MB | Severe leak | Schedule reload, open TAC case with output |

## Interface Thresholds

### Error Rate (errors per total packets)

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | < 0.001% | No significant errors | No action needed |
| Warning | 0.001–0.01% | Low error rate | Monitor, check optic levels |
| Critical | 0.01–0.1% | Significant errors | Investigate Layer 1, check cable/SFP |
| Emergency | > 0.1% | High error rate | Replace cable/optic, check remote end |

### Output Drops (per hour)

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0–50/hr | Minimal drops | No action needed |
| Warning | 51–500/hr | Moderate congestion | Review QoS policy, check bandwidth |
| Critical | 501–5000/hr | Significant congestion | Implement or tune QoS, consider upgrade |
| Emergency | > 5000/hr | Severe congestion | Immediate QoS intervention or link upgrade |

### CRC Errors (per hour)

| Level | Range | Meaning | Action |
|-------|-------|---------|--------|
| Normal | 0 | Clean signal | No action needed |
| Warning | 1–10/hr | Intermittent L1 issue | Monitor, check SFP DOM readings |
| Critical | 11–100/hr | Active L1 problem | Replace cable, clean fiber, reseat SFP |
| Emergency | > 100/hr | Severe L1 failure | Replace cable and SFP, check patch panel |

### SFP Optical Power (DOM)

| Level | Tx/Rx Power | Meaning | Action |
|-------|-------------|---------|--------|
| Normal | Within vendor spec | Clean optical link | No action needed |
| Warning | Within 2 dBm of low threshold | Degrading signal | Clean fiber ends, monitor trend |
| Critical | Below low warning threshold | Poor signal quality | Replace fiber run or SFP |
| Emergency | Below low alarm threshold | Link at risk of failure | Immediate fiber/SFP replacement |

## Routing Thresholds

### BGP Session Health

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | Established, stable prefix count | Healthy peering | No action needed |
| Warning | Prefix count changed > 10% from baseline | Route churn | Investigate upstream changes |
| Critical | Session flap in last hour | Peer instability | Check transport, review timers |
| Emergency | Session down > 5 minutes | Peering failure | Verify connectivity, check peer status |

### OSPF Adjacency Health

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | All neighbors in Full state | Healthy adjacencies | No action needed |
| Warning | Neighbor in ExStart/Exchange > 30 sec | Slow adjacency formation | Check MTU, area config |
| Critical | Neighbor flap in last hour | Adjacency instability | Check interface, review timers |
| Emergency | Expected neighbor missing | Adjacency lost | Verify interface status, check remote device |

### Route Table Size

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | Within 10% of baseline count | Stable routing | No action needed |
| Warning | 10–25% deviation from baseline | Moderate change | Verify expected changes |
| Critical | 25–50% deviation from baseline | Significant change | Investigate route source |
| Emergency | > 50% deviation or total < 50% baseline | Major routing event | Immediate investigation, check for partition |

## Environment Thresholds

### Temperature

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | Below warning threshold (per platform) | Within operating spec | No action needed |
| Warning | Within 5°C of shutdown threshold | Approaching thermal limit | Check fans, airflow, room cooling |
| Critical | Above warning, below shutdown | Thermal stress | Reduce load if possible, fix cooling |
| Emergency | At or above shutdown threshold | Imminent thermal shutdown | Power down non-essential modules, emergency cooling |

### Power Supply

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | All PSUs OK, redundancy active | Fully protected | No action needed |
| Warning | Redundant PSU not present (single PSU) | No power redundancy | Plan PSU installation |
| Critical | Redundant PSU failed, one active | Lost redundancy | RMA failed PSU, schedule replacement |
| Emergency | Single PSU showing degraded output | Risk of total power loss | Schedule emergency maintenance |

### Fan Status

| Level | Condition | Meaning | Action |
|-------|-----------|---------|--------|
| Normal | All fans OK, RPM within spec | Adequate cooling | No action needed |
| Warning | Fan RPM low or one fan degraded | Reduced cooling capacity | Monitor temperature, plan replacement |
| Critical | One fan failed, others compensating | Thermal risk increasing | RMA fan tray, increase monitoring |
| Emergency | Multiple fans failed | Imminent thermal shutdown | Reduce load, emergency hardware service |
