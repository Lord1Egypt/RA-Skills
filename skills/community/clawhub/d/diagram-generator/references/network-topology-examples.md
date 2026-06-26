# Network Topology Examples

This file contains reusable JSON patterns for Draw.io network topology diagrams.

For current generation rules, read `playbook-network-topology.md` first.

## Example 1: Basic Datacenter Topology

```json
{
  "format": "drawio",
  "title": "Basic Network Topology",
  "elements": [
    {
      "id": "env-prod",
      "type": "container",
      "name": "Production Environment",
      "level": "environment",
      "geometry": { "x": 40, "y": 40, "width": 900, "height": 560 },
      "children": [
        {
          "id": "dc-primary",
          "type": "container",
          "name": "Primary Datacenter",
          "level": "datacenter",
          "geometry": { "x": 30, "y": 60, "width": 840, "height": 460 },
          "children": [
            {
              "id": "zone-dmz",
              "type": "container",
              "name": "DMZ Zone",
              "level": "zone",
              "geometry": { "x": 30, "y": 60, "width": 360, "height": 160 },
              "children": [
                { "id": "fw-a", "type": "node", "name": "Firewall A", "deviceType": "firewall", "geometry": { "x": 40, "y": 65, "width": 150, "height": 60 } },
                { "id": "fw-b", "type": "node", "name": "Firewall B", "deviceType": "firewall", "geometry": { "x": 200, "y": 65, "width": 150, "height": 60 } }
              ]
            },
            {
              "id": "zone-app",
              "type": "container",
              "name": "Application Zone",
              "level": "zone",
              "geometry": { "x": 430, "y": 60, "width": 360, "height": 160 },
              "children": [
                { "id": "app-a", "type": "node", "name": "Application Server A", "deviceType": "server", "geometry": { "x": 40, "y": 65, "width": 150, "height": 60 } },
                { "id": "app-b", "type": "node", "name": "Application Server B", "deviceType": "server", "geometry": { "x": 200, "y": 65, "width": 150, "height": 60 } }
              ]
            }
          ]
        }
      ]
    },
    { "type": "edge", "source": "fw-a", "target": "app-a", "style": { "lineStyle": "straight" } },
    { "type": "edge", "source": "fw-b", "target": "app-b", "style": { "lineStyle": "straight" } }
  ]
}
```

## Example 2: Multi-Environment Topology

Use separate environment containers when production and disaster recovery are logically distinct.

```json
{
  "format": "drawio",
  "title": "Multi-Environment Network Topology",
  "elements": [
    {
      "id": "env-prod",
      "type": "container",
      "name": "Production Environment",
      "level": "environment",
      "geometry": { "x": 40, "y": 40, "width": 520, "height": 360 },
      "children": [
        {
          "id": "dc-prod",
          "type": "container",
          "name": "Production Datacenter",
          "level": "datacenter",
          "geometry": { "x": 30, "y": 60, "width": 460, "height": 260 },
          "children": [
            {
              "id": "zone-prod-app",
              "type": "container",
              "name": "Application Zone",
              "level": "zone",
              "geometry": { "x": 40, "y": 70, "width": 360, "height": 140 },
              "children": [
                { "id": "prod-app", "type": "node", "name": "Application Server", "deviceType": "server", "geometry": { "x": 100, "y": 55, "width": 160, "height": 60 } }
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "env-dr",
      "type": "container",
      "name": "Disaster Recovery Environment",
      "level": "environment",
      "geometry": { "x": 620, "y": 40, "width": 520, "height": 360 },
      "children": [
        {
          "id": "dc-dr",
          "type": "container",
          "name": "DR Datacenter",
          "level": "datacenter",
          "geometry": { "x": 30, "y": 60, "width": 460, "height": 260 },
          "children": [
            {
              "id": "zone-dr-app",
              "type": "container",
              "name": "Application Zone",
              "level": "zone",
              "geometry": { "x": 40, "y": 70, "width": 360, "height": 140 },
              "children": [
                { "id": "dr-app", "type": "node", "name": "Application Server", "deviceType": "server", "geometry": { "x": 100, "y": 55, "width": 160, "height": 60 } }
              ]
            }
          ]
        }
      ]
    },
    { "type": "edge", "source": "prod-app", "target": "dr-app", "label": "Data replication", "style": { "lineStyle": "straight" } }
  ]
}
```

## Example 3: Four-Level Management Network

Use this structure for environment -> datacenter -> zone -> device hierarchy.

```json
{
  "format": "drawio",
  "title": "Four-Level Network Topology",
  "elements": [
    {
      "id": "env-management",
      "type": "container",
      "name": "Management Network",
      "level": "environment",
      "geometry": { "x": 40, "y": 40, "width": 900, "height": 700 },
      "children": [
        {
          "id": "dc-province",
          "type": "container",
          "name": "Province Center Datacenter",
          "level": "datacenter",
          "geometry": { "x": 40, "y": 70, "width": 820, "height": 560 },
          "children": [
            {
              "id": "zone-uplink",
              "type": "container",
              "name": "Uplink Zone",
              "level": "zone",
              "geometry": { "x": 40, "y": 70, "width": 240, "height": 160 },
              "children": [
                { "id": "router-1", "type": "node", "name": "Router 1", "deviceType": "router", "geometry": { "x": 35, "y": 65, "width": 150, "height": 60 } }
              ]
            },
            {
              "id": "zone-aggregation",
              "type": "container",
              "name": "Aggregation Zone",
              "level": "zone",
              "geometry": { "x": 310, "y": 70, "width": 240, "height": 160 },
              "children": [
                { "id": "agg-switch-1", "type": "node", "name": "Aggregation Switch 1", "deviceType": "switch", "geometry": { "x": 35, "y": 65, "width": 170, "height": 60 } }
              ]
            },
            {
              "id": "zone-terminal",
              "type": "container",
              "name": "Terminal Zone",
              "level": "zone",
              "geometry": { "x": 580, "y": 70, "width": 220, "height": 160 },
              "children": [
                { "id": "pc-1", "type": "node", "name": "Management PC 1", "deviceType": "pc", "geometry": { "x": 35, "y": 65, "width": 150, "height": 60 } }
              ]
            }
          ]
        }
      ]
    },
    { "type": "edge", "source": "router-1", "target": "agg-switch-1", "style": { "lineStyle": "straight" } },
    { "type": "edge", "source": "agg-switch-1", "target": "pc-1", "style": { "lineStyle": "straight" } }
  ]
}
```

## Common Zone Types

| Zone | Typical devices | Purpose |
| --- | --- | --- |
| Uplink Zone | Routers | External or upstream network connections |
| Aggregation Zone | Core switches, aggregation switches | Traffic aggregation |
| Terminal Zone | Switches, PCs | End-user or management terminals |
| Financial Integration Zone | Firewalls, routers | Bank or financial network integration |
| Internal Access Zone | Routers, switches, firewalls | Internal network ingress |
| External Access Zone | Routers, firewalls | Partner or external access |
| DMZ Zone | Firewalls, public servers, load balancers | Public-facing or controlled exposure |
| Application Zone | Application servers, proxies | Application deployment |
| Data Zone | Database servers, storage | Data storage |
| Management Zone | Management servers, jump hosts | Administrative access |
| Core Zone | Core switches | Datacenter core switching |
| Private Cloud Zone | Cloud nodes | Private cloud resources inside the datacenter |

## Connection Patterns

Point-to-point:

```json
{ "type": "edge", "source": "router-a", "target": "router-b", "style": { "lineStyle": "straight" } }
```

Active-active pair to downstream pair:

```json
[
  { "type": "edge", "source": "fw-a", "target": "switch-a" },
  { "type": "edge", "source": "fw-a", "target": "switch-b" },
  { "type": "edge", "source": "fw-b", "target": "switch-a" },
  { "type": "edge", "source": "fw-b", "target": "switch-b" }
]
```

Datacenter-to-cloud:

```json
[
  { "type": "edge", "source": "core-switch-a", "target": "private-cloud" },
  { "type": "edge", "source": "core-switch-b", "target": "private-cloud" }
]
```

## Layout Notes

- For Word documents, use vertical topology: external systems at the top, datacenters below, core and cloud zones lower inside each datacenter.
- For PPT, horizontal peer datacenters can improve readability.
- Keep same-role redundant devices aligned.
- Use two-column pairs for A/B devices.
- Avoid edge labels in dense topology diagrams unless the user explicitly asks for them.
