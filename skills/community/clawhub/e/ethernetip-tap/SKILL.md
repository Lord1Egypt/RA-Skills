---
name: ethernetip-tap
description: >-
  Read Rockwell / Allen-Bradley Logix controllers over EtherNet/IP (CIP) — Logix
  controller identity, controller-scoped TAG DISCOVERY (the headline feature),
  read one tag or array element, batch-read many tags, and a governed MOC-gated
  tag write (OFF by default). ControlLogix / CompactLogix (and GuardLogix) via
  pycomm3 (pure Python). Use when the task names EtherNet/IP, CIP, Rockwell,
  Allen-Bradley, ControlLogix, CompactLogix, Studio 5000/RSLogix, or a Logix tag.
  Routes to the ot-aiops MCP server. Read-first. PLC-5/SLC (PCCC) and Micro800 are
  NOT supported (roadmap). For OPC-UA/Modbus/Siemens/Mitsubishi/MTConnect/MQTT use
  the sibling *-tap skills; not for IT/network gear, Kubernetes, hypervisors, backups.
---

# ethernetip-tap

EtherNet/IP (CIP) read-first telemetry for **Allen-Bradley Logix** controllers via
the **ot-aiops** MCP server, using **pycomm3** (pure Python — no native deps).
Preview — validated against a mocked LogixDriver, NOT a live controller.

## When to use
- A Rockwell/AB **ControlLogix / CompactLogix / GuardLogix** controller reachable
  over EtherNet/IP (TCP 44818): `host` + `slot` (0 for CompactLogix; the CPU slot
  for a ControlLogix chassis).
- Discover the controller's tags, read tags/arrays by name, identify the controller.

## When NOT to use (routing)
- OPC-UA → `opcua-tap`; Modbus → `modbus-tap`; Siemens S7 → `s7-tap`; Mitsubishi →
  `mc-tap`; CNC → `mtconnect-tap`; MQTT/Sparkplug/UNS → `sparkplug-tap`.
- Cross-protocol triage → `industrial-diagnostics`; OEE/asset analytics → `industrial-analytics`.
- **PLC-5 / SLC-500 (PCCC) / Micro800** → not supported (roadmap).
- IT/network/Kubernetes/hypervisor/backup → not this tool.

## Read tools

| Tool | Params | Returns |
|------|--------|---------|
| `eip_controller_info` | `endpoint?` | `{host, slot, controller:{vendor, product_type, product_code, revision, serial, product_name, name}}` |
| `eip_list_tags` | `endpoint?` | `{tag_count, tags:[{name, data_type, tag_type, structure, dimensions}]}` |
| `eip_read_tag` | `tag, endpoint?` | `{tag, value, type, error, good}` |
| `eip_read_many` | `tags[], endpoint?` | `{count, items:[{tag, value, type, error, good}]}` (auto multi-packet) |

`eip_list_tags` is the headline pycomm3 capability — the controller advertises its
symbol table, so you can enumerate tags without prior knowledge. Program-scoped
tags appear as `Program:<prog>.<tag>`; array elements read as `Array[3]`.

Example: `eip_read_tag(tag="Conveyor.Speed", endpoint="cell5")` →
`{"tag":"Conveyor.Speed","value":1500.0,"type":"REAL","error":"","good":true}`

## Write tool (HIGH risk · MOC · off by default)

`eip_write_tag(tag, value, endpoint?, dry_run=true)`
- **OT-DANGEROUS. 未经授权勿对生产控制系统写入.** Defaults to `dry_run=true`
  (nothing written). Captures the **BEFORE** value (read-back) and records an
  **undo** descriptor so the change is reversible.
- Apply: `dry_run=false` **and** set `OPCUA_AUDIT_APPROVED_BY` (a recorded
  approver — MOC). CLI: `ot-aiops eip write-tag Setpoint 42 -e cell5 --apply`
  (double-confirm prompt).

## CLI
```bash
ot-aiops eip info -e cell5                 # controller identity
ot-aiops eip tags -e cell5                 # tag discovery
ot-aiops eip read "Conveyor.Speed" -e cell5
ot-aiops eip read-many Speed Temp -e cell5
ot-aiops eip write-tag Setpoint 42 -e cell5            # dry-run preview
ot-aiops eip write-tag Setpoint 42 -e cell5 --apply    # double-confirm
```

## Setup
`ot-aiops init` (ethernetip: host/slot/port) · `ot-aiops doctor` · `ot-aiops mcp`.
Config: `~/.ot-aiops/config.yaml` (`protocol: ethernetip` or alias `eip`). Test
against a CIP/Logix simulator. Endpoint text is sanitized; every tool runs through
the ot-aiops governance harness (audit/budget/risk-tier). 缺功能提 issue/PR 欢迎留言.
