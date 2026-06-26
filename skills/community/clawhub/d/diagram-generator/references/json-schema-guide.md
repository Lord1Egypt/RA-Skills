# JSON Schema Guide

This guide describes the JSON specification passed to the `mcp-diagram-generator` MCP server.

## Root Object

```json
{
  "format": "drawio",
  "diagramType": "flowchart",
  "title": "Diagram title",
  "elements": [],
  "layers": [],
  "lanes": []
}
```

Required fields:
- `format`
- `elements`

Optional semantic fields:
- `diagramType`: `flowchart`, `sequence`, `class`, `er`, `architecture`, or `swimlane`
- `layers`: used by architecture diagrams
- `lanes`: used by swimlane diagrams

## Element Types

Each entry in `elements` is one of:
- `container`
- `node`
- `edge`

Edges must stay at the top level of `elements`. Do not put edges inside container `children`.

## Container

```json
{
  "id": "env-prod",
  "type": "container",
  "name": "Production Network",
  "level": "environment",
  "style": {
    "fillColor": "#e1d5e7",
    "strokeColor": "#9673a6",
    "fontSize": 14,
    "fontStyle": "bold"
  },
  "geometry": {
    "x": 40,
    "y": 40,
    "width": 1200,
    "height": 800
  },
  "children": []
}
```

Container fields:
- `id`: unique element ID
- `type`: always `container`
- `name`: displayed label
- `level`: `environment`, `datacenter`, `zone`, or `other`
- `style`: optional style object
- `geometry`: required for high-quality Draw.io or Excalidraw output
- `children`: nested containers or nodes

## Node

```json
{
  "id": "router-a",
  "type": "node",
  "name": "Router A",
  "deviceType": "router",
  "shape": "ellipse",
  "fields": [],
  "methods": [],
  "style": {
    "fillColor": "#DBEAFE",
    "strokeColor": "#2563EB",
    "strokeWidth": 2,
    "fontColor": "#1E3A8A",
    "fontSize": 20,
    "fontStyle": "bold"
  },
  "geometry": {
    "x": 40,
    "y": 80,
    "width": 160,
    "height": 70
  }
}
```

Node fields:
- `id`: unique element ID
- `type`: always `node`
- `name`: displayed label
- `deviceType`: optional visual preset or semantic component type
- `shape`: `rect`, `ellipse`, `diamond`, `parallelogram`, `rounded`, `cylinder`, `cloud`, or `other`
- `fields`: class or ER fields
- `methods`: class methods
- `style`: optional style object
- `geometry`: coordinates and size

Unknown `deviceType` values are allowed. For example, `deviceType: "DWDM"` should fall back to the default device style instead of failing.

## Edge

```json
{
  "id": "edge-router-firewall",
  "type": "edge",
  "source": "router-a",
  "target": "firewall-a",
  "label": "uplink",
  "relation": "association",
  "style": {
    "strokeColor": "#333333",
    "strokeWidth": 2,
    "endArrow": "arrow",
    "lineStyle": "straight"
  }
}
```

Edge fields:
- `id`: optional unique edge ID
- `type`: always `edge`
- `source`: source node or container ID
- `target`: target node or container ID
- `label`: optional edge label
- `relation`: semantic relationship for Mermaid class, ER, and sequence diagrams
- `style`: optional edge style

## Relation Values

Class diagrams:
- `association`
- `inheritance`
- `composition`
- `aggregation`
- `dependency`
- `realization`

ER diagrams:
- `oneToOne`
- `oneToMany`
- `manyToOne`
- `manyToMany`
- `zeroOrOneToMany`

Sequence diagrams:
- `sync`
- `async`
- `return`

## Style

```json
{
  "fillColor": "#FFFFFF",
  "strokeColor": "#333333",
  "strokeWidth": 2,
  "fontColor": "#000000",
  "fontSize": 20,
  "fontStyle": "bold",
  "borderRadius": 8,
  "dashPattern": "5,5"
}
```

Rules:
- Use `#RRGGBB` colors.
- Use `fillColor: "none"` for Draw.io no-fill nodes when needed.
- `style` must be an object, not a string.

## Edge Style

```json
{
  "strokeColor": "#333333",
  "strokeWidth": 2,
  "endArrow": "arrow",
  "startArrow": "none",
  "dashPattern": "5,5",
  "lineStyle": "straight"
}
```

Supported values:
- `endArrow` and `startArrow`: `none`, `arrow`, `circle`, `diamond`
- `lineStyle`: `straight`, `orthogonal`, `curved`

## Geometry

```json
{
  "x": 40,
  "y": 80,
  "width": 160,
  "height": 70
}
```

Rules:
- Top-level coordinates are absolute.
- Child coordinates are relative to the direct parent container.
- Complex Draw.io and Excalidraw diagrams should use explicit geometry.

## Architecture Input

Prefer `diagramType: "architecture"` with `layers`.

```json
{
  "format": "drawio",
  "diagramType": "architecture",
  "title": "Platform Architecture",
  "layers": [
    {
      "id": "layer-client",
      "name": "Client",
      "components": [
        { "id": "web", "type": "node", "name": "Web App", "deviceType": "user" }
      ]
    },
    {
      "id": "layer-access",
      "name": "Access Layer",
      "components": [
        { "id": "api", "type": "node", "name": "API Gateway", "deviceType": "gateway" }
      ]
    },
    {
      "id": "layer-service",
      "name": "Service Layer",
      "components": [
        { "id": "service", "type": "node", "name": "Business Service", "deviceType": "service" }
      ]
    },
    {
      "id": "layer-data",
      "name": "Data Layer",
      "components": [
        { "id": "db", "type": "node", "name": "Database", "deviceType": "database" },
        { "id": "cache", "type": "node", "name": "Cache", "deviceType": "cache" }
      ]
    }
  ],
  "elements": [
    { "type": "edge", "source": "web", "target": "api" },
    { "type": "edge", "source": "api", "target": "service" },
    { "type": "edge", "source": "service", "target": "db" },
    { "type": "edge", "source": "service", "target": "cache" }
  ]
}
```

## Swimlane Input

Prefer `diagramType: "swimlane"` with `lanes`.

```json
{
  "format": "drawio",
  "diagramType": "swimlane",
  "title": "Approval Flow",
  "lanes": [
    {
      "id": "lane-user",
      "name": "User",
      "steps": [
        { "id": "submit", "name": "Submit", "order": 1, "next": ["review"] }
      ]
    },
    {
      "id": "lane-manager",
      "name": "Manager",
      "steps": [
        { "id": "review", "name": "Review", "order": 2, "next": ["archive"] }
      ]
    },
    {
      "id": "lane-system",
      "name": "System",
      "steps": [
        { "id": "archive", "name": "Archive", "order": 3 }
      ]
    }
  ],
  "elements": []
}
```

## Flowchart Example

```json
{
  "format": "mermaid",
  "diagramType": "flowchart",
  "title": "Login Flow",
  "elements": [
    { "id": "start", "type": "node", "name": "Start", "shape": "rounded" },
    { "id": "input", "type": "node", "name": "Enter credentials", "shape": "parallelogram" },
    { "id": "validate", "type": "node", "name": "Valid?", "shape": "diamond" },
    { "id": "success", "type": "node", "name": "Login success", "shape": "rounded" },
    { "id": "error", "type": "node", "name": "Show error" },
    { "type": "edge", "source": "start", "target": "input" },
    { "type": "edge", "source": "input", "target": "validate" },
    { "type": "edge", "source": "validate", "target": "success", "label": "success" },
    { "type": "edge", "source": "validate", "target": "error", "label": "failure" }
  ]
}
```

## Sequence Example

```json
{
  "format": "mermaid",
  "diagramType": "sequence",
  "title": "API Call Flow",
  "elements": [
    { "id": "user", "type": "node", "name": "User" },
    { "id": "frontend", "type": "node", "name": "Frontend" },
    { "id": "api", "type": "node", "name": "API Service" },
    { "id": "db", "type": "node", "name": "Database" },
    { "type": "edge", "source": "user", "target": "frontend", "label": "Click login", "relation": "sync" },
    { "type": "edge", "source": "frontend", "target": "api", "label": "POST /login", "relation": "sync" },
    { "type": "edge", "source": "api", "target": "db", "label": "Query user", "relation": "sync" },
    { "type": "edge", "source": "db", "target": "api", "label": "User data", "relation": "return" }
  ]
}
```

## Class Example

```json
{
  "format": "mermaid",
  "diagramType": "class",
  "title": "Order Class Model",
  "elements": [
    { "id": "entity", "type": "node", "name": "Entity", "fields": ["+String id"], "methods": ["+validate()"] },
    { "id": "order", "type": "node", "name": "Order", "fields": ["+String orderNo", "+Money amount"], "methods": ["+pay()"] },
    { "id": "orderItem", "type": "node", "name": "OrderItem", "fields": ["+String sku", "+int quantity"] },
    { "type": "edge", "source": "entity", "target": "order", "relation": "inheritance" },
    { "type": "edge", "source": "order", "target": "orderItem", "relation": "composition", "label": "items" }
  ]
}
```

## ER Example

```json
{
  "format": "mermaid",
  "diagramType": "er",
  "title": "Order ER Model",
  "elements": [
    { "id": "customer", "type": "node", "name": "CUSTOMER", "fields": ["int id PK", "string name"] },
    { "id": "orders", "type": "node", "name": "ORDERS", "fields": ["int id PK", "int customer_id FK", "datetime created_at"] },
    { "type": "edge", "source": "customer", "target": "orders", "relation": "oneToMany", "label": "places" }
  ]
}
```

## Network Topology Example

```json
{
  "format": "drawio",
  "title": "Management Network Topology",
  "elements": [
    {
      "id": "env-management",
      "type": "container",
      "name": "Management Network",
      "level": "environment",
      "geometry": { "x": 40, "y": 40, "width": 700, "height": 420 },
      "children": [
        {
          "id": "dc-primary",
          "type": "container",
          "name": "Primary Datacenter",
          "level": "datacenter",
          "geometry": { "x": 30, "y": 60, "width": 640, "height": 340 },
          "children": [
            {
              "id": "zone-uplink",
              "type": "container",
              "name": "Uplink Zone",
              "level": "zone",
              "geometry": { "x": 30, "y": 60, "width": 280, "height": 180 },
              "children": [
                { "id": "router-a", "type": "node", "name": "Router A", "deviceType": "router", "geometry": { "x": 40, "y": 70, "width": 120, "height": 60 } },
                { "id": "router-b", "type": "node", "name": "Router B", "deviceType": "router", "geometry": { "x": 170, "y": 70, "width": 120, "height": 60 } }
              ]
            }
          ]
        }
      ]
    },
    { "type": "edge", "source": "router-a", "target": "router-b", "style": { "endArrow": "none", "lineStyle": "straight" } }
  ]
}
```

## Style Presets

Network topology levels:

| Level | fillColor | strokeColor |
| --- | --- | --- |
| environment | `#e1d5e7` | `#9673a6` |
| datacenter | `#d5e8d4` | `#82b366` |
| zone | `#fff2cc` | `#d6b656` |

Device types:

| deviceType | Expected style |
| --- | --- |
| `router` | Blue ellipse |
| `accessSwitch` | `#FFFFCC` fill |
| `switch` | `#FFFFCC` fill |
| `coreSwitch` | `#FFFFCC` fill |
| `firewall` | Red security shape |
| `loadBalancer` | Purple load balancer |
| `sslGateway` | Cyan SSL gateway |
| `proxy` | Blue proxy node |
| `database` | Database style |
| `cloud` | Cloud style |
| `externalSystem` | External system style |

## Best Practices

- Use descriptive prefixes such as `env-`, `dc-`, `zone-`, `router-`, and `edge-`.
- Avoid spaces and special characters in IDs except `_` and `-`.
- Keep total elements reasonable for performance.
- Split very large diagrams into multiple files or pages when needed.
- Use containers to group related elements.
