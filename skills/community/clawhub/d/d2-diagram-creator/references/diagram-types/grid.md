# Grid Diagram

## Use Cases

- Dashboard layout design
- UI prototype design
- Object matrix display
- Heatmap-style visualization
- Structured component arrangement

## Key Patterns

| Element | Syntax | Purpose |
|---------|--------|---------|
| Row Grid | `grid-rows: N` | Specify N rows |
| Column Grid | `grid-columns: N` | Specify N columns |
| Vertical Gap | `vertical-gap: N` | Row spacing |
| Horizontal Gap | `horizontal-gap: N` | Column spacing |
| Unified Gap | `grid-gap: N` | Set both row and column spacing |
| Cell Width | `width: N` | Control cell width |
| Cell Height | `height: N` | Control cell height |

## Basic Examples

### Rows Only

```d2
grid-rows: 3
Executive
Legislative
Judicial
```

### Columns Only

```d2
grid-columns: 3
Executive
Legislative
Judicial
```

### Both Rows and Columns

```d2
grid-rows: 2
grid-columns: 2
Executive
Legislative
Judicial
Fourth Item
```

## Controlling Cell Size

Use `width` and `height` to create specific structures:

```d2
grid-rows: 2
Executive
Legislative
Judicial
The American Government.width: 400
```

When only one of rows or columns is defined, objects will expand automatically:

```d2
grid-rows: 3
Executive
Legislative
Judicial
The American Government.width: 400
Voters
Non-voters
```

## Grid Spacing

| Property | Description |
|----------|-------------|
| `grid-gap` | Set both vertical and horizontal spacing |
| `vertical-gap` | Row spacing (can override grid-gap) |
| `horizontal-gap` | Column spacing (can override grid-gap) |

### Tight Grid (Heatmap Style)

```d2
grid-gap: 0
grid-columns: 3

Cell1
Cell2
Cell3
Cell4
Cell5
Cell6
```

## Nested Grids

Grid diagrams can be nested within other grids to create complex layouts:

```d2
grid-gap: 0
grid-columns: 1

header: "Header"

body: {
  grid-gap: 0
  grid-columns: 2
  content: "Main Content"
  sidebar: "Sidebar"
}

footer: "Footer"
```

## Complete Example: Dashboard Layout

```d2
grid-rows: 5
style.fill: black

classes: {
  white square: {
    label: ""
    width: 120
    style: {
      fill: white
      stroke: cornflowerblue
      stroke-width: 10
    }
  }
  block: {
    style: {
      text-transform: uppercase
      font-color: white
      fill: darkcyan
      stroke: black
    }
  }
}

flow1.class: white square
flow2.class: white square
flow3.class: white square
flow4.class: white square
flow5.class: white square
flow6.class: white square
flow7.class: white square
flow8.class: white square
flow9.class: white square

dagger engine: {
  width: 800
  class: block
  style: {
    fill: beige
    stroke: darkcyan
    font-color: blue
    stroke-width: 8
  }
}

any docker compatible runtime: {
  width: 800
  class: block
  style: {
    fill: lightcyan
    stroke: darkcyan
    font-color: black
    stroke-width: 8
  }
}

any ci: {
  class: block
  style: {
    fill: gold
    stroke: maroon
    font-color: maroon
    stroke-width: 8
  }
}
windows.class: block
linux.class: block
macos.class: block
kubernetes.class: block
```

## Complete Example: User Access Architecture

```d2
direction: right

users -- via -- teleport

teleport -> jita: "all connections audited and logged"
teleport -> infra
teleport -> identity provider
teleport <- identity provider

users: {
  grid-columns: 1

  Engineers: {
    shape: circle
  }
  Machines: {
    shape: circle
  }
}

via: {
  grid-columns: 1

  https: "HTTPS://"
  kubectl: "> kubectl"
  tsh: "> tsh"
  api: "> api"
  db clients: "DB Clients"
}

teleport: Teleport {
  grid-rows: 2

  inp: |md
    # Identity Native Proxy
  | {
    width: 300
  }

  Audit Log
  Cert Authority
}

jita: "Just-in-time Access via" {
  grid-rows: 1

  Slack
  Mattermost
  Jira
  Pagerduty
  Email
}

infra: Infrastructure {
  grid-rows: 2

  ssh
  Kubernetes
  My SQL
  MongoDB
  PSQL
  Windows
}

identity provider: Indentity Provider
```

## Design Principles

1. **Row/Column Priority** - Determine the primary direction first (rows or columns)
2. **Appropriate Spacing** - Use `grid-gap` to control visual rhythm
3. **Nested Composition** - Achieve complex layouts through nesting
4. **Consistent Styling** - Use `class` to unify styles for similar cells

## Common Patterns

### Equal Grid

```d2
grid-columns: 3
grid-gap: 20

Module A
Module B
Module C
```

### Unequal Layout

```d2
grid-columns: 3
grid-gap: 10

Sidebar.width: 200
Main Content.width: 400
Right Panel.width: 150
```

### Compact Heatmap

```d2
grid-gap: 0
grid-columns: 4

1.style.fill: "#ff0000"
2.style.fill: "#ff4444"
3.style.fill: "#ff8888"
4.style.fill: "#ffcccc"
5.style.fill: "#00ff00"
6.style.fill: "#44ff44"
7.style.fill: "#88ff88"
8.style.fill: "#ccffcc"
```
