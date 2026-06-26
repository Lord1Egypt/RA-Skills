---
name: ensp
license: MIT
version: 1.1
description: Always use when user asks to create, generate, or design a network topology diagram for eNSP (Enterprise Network Simulation Platform), or mentions creating eNSP topologies, network simulations with Huawei devices (AR routers, S5700 switches, PC, Cloud, etc.).
---

# eNSP Topology Skill

Generate eNSP (Enterprise Network Simulation Platform) topology files as native `.topo` files that can be opened directly in eNSP.

## How to create a topology

1. **Parse user's request** to identify:
   - Network devices (routers, switches, PCs, Cloud, etc.)
   - Connections between devices
   - Optional: text labels, area boxes

2. **Generate UUIDs** for each device using a valid UUID v4 format

3. **Calculate layout coordinates** for devices using auto-layout algorithm

4. **Build the .topo XML** following the format in `references/topo-reference.md`

5. **Write the file** to current directory using Write tool

6. **Open the result** - print the file path so user can open it in eNSP

## Output format

Always output a `.topo` file. The user will open it in eNSP for simulation.

Example filenames:
- `simple-network.topo`
- `ospf-topology.topo`
- `campus-network.topo`

## Device types supported

### Routers

| Model | Description | Interface Config |
|-------|-------------|------------------|
| AR201 | Router | Ethernet x8 + Ethernet x1 |
| AR1220 | Router | 2GE + 8Ethernet |
| AR2220 | Router | GE x1 + GE x2 + Serial x2 |
| AR2240 | Router | GE x1 + GE x2 |
| AR3260 | Router | GE x1 + GE x2 |
| Router | Generic Router | Ethernet x2 + GE x4 + Serial x4 |
| NE40E | Enterprise Router | 10x Ethernet (slot format) |
| NE5000E | Core Router | 10x Ethernet (slot format) |
| NE9000 | Core Router | 10x Ethernet (slot format) |
| R250D | Router | GE x1 |

### Switches

| Model | Description | Interface Config |
|-------|-------------|------------------|
| S3700 | Switch | Ethernet x22 + GE x2 |
| S5700 | Switch | 24GE |
| CE6800 | Data Center Switch | 20x GE (slot format) |
| CE12800 | Data Center Switch | 10x GE (slot format) |
| CX | Switch | 10x Ethernet (slot format) |

### Firewalls

| Model | Description | Interface Config |
|-------|-------------|------------------|
| USG5500 | Firewall | GE x9 |
| USG6000V | Firewall | GE x1 (slot0) + GE x7 (slot1) |

### Wireless

| Model | Description | Interface Config |
|-------|-------------|------------------|
| AC6005 | Wireless AC | 8GE |
| AC6605 | Wireless AC | 24GE |
| AP2050 | Wireless AP | 5GE |
| AP3030 | Wireless AP | 1GE |
| AP4030 | Wireless AP | 2GE |
| AP4050 | Wireless AP | 2GE |
| AP5030 | Wireless AP | 2GE |
| AP6050 | Wireless AP | 2GE |
| AP7030 | Wireless AP | 2GE |
| AP7050 | Wireless AP | 2GE |
| AP8030 | Wireless AP | 3GE |
| AP8130 | Wireless AP | 3GE |
| AP9131 | Wireless AP | 2GE |
| AD9430 | LTE Module | 28GE |
| STA | Wireless Station | Wireless |
| Cellphone | Mobile Device | Wireless |

### Endpoints

| Model | Description | Interface Config |
|-------|-------------|------------------|
| PC | PC | 1GE |
| Laptop | Laptop | 1GE |
| Server | Server | 1Ethernet |
| Client | Client | 1Ethernet |
| MCS | Multicast Server | 1Ethernet |
| Cloud | Cloud/BNI | Ethernet interfaces |
| FRSW | Frame Relay Switch | Serial x16 |
| HUB | Ethernet HUB | Ethernet x16 |

## Connection types

| Type | Description |
|------|-------------|
| Copper | Ethernet cable |
| Serial | Serial cable |
| Auto | Auto-detect |

## Layout algorithm

Use a simple grid-based auto-layout:

```
Grid spacing: 200px horizontal, 150px vertical
Device size: ~80x60px
Start position: (100, 100)

For each row:
  - Place devices horizontally with 200px gap
  - Move to next row when reaching canvas width (~1200px)
```

Adjust positions based on device types and connections to create logical groupings.

## Adding text labels (txttips)

Common labels for network diagrams:
- Loopback addresses: `Loopback0:10.0.1.1/24`
- Network segments: `10.0.12.0/24`
- Area labels: `Area0`, `Area1`, `AS 64512`
- Device roles: `Core Layer`, `Access Layer`

## Adding area boxes (shapes)

Use type="1" shapes with appropriate colors to group devices:
- Same area devices in one rectangle
- Different colors for different areas/zones

## File naming

- Use lowercase with hyphens
- Descriptive name based on topology purpose
- End with `.topo` extension

## Opening the result

After writing the file, print the absolute path:
```
Topology saved to: C:\path\to\topology.topo
Please open this file in eNSP to view and simulate.
```

## XML format reference

Consult `references/topo-reference.md` for complete XML structure including:
- Device XML format with slots and interfaces
- Line XML format with interfacePair details
- Shape XML format for area boxes
- Txttip XML format for text annotations
