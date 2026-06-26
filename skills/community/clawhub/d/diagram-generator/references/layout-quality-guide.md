# Layout And Quality Guide

Use this guide when a Draw.io or Excalidraw diagram needs explicit geometry.

## Coordinate Rules

- Top-level element coordinates are absolute.
- Child coordinates inside a container are relative to the direct parent container's top-left corner.
- Do not mix carefully positioned elements with unpositioned elements unless fallback layout is acceptable.

## Single-Row Layout

For peer nodes in one row:

```text
X_i = X_start + i * (NodeWidth + HorizontalGap)
Y_i = Y_start
```

Recommended defaults:
- Node width: `120` to `180`
- Node height: `60` to `80`
- Horizontal gap: `80`
- Network topology horizontal gap: `120` when connectors need more space

## Grid Layout

For many nodes:

```text
X_col = X_start + col * (NodeWidth + GapX)
Y_row = Y_start + row * (NodeHeight + GapY)
row = floor(index / columnCount)
col = index % columnCount
```

Recommended defaults:
- `GapX`: `80`
- `GapY`: `50`
- Use two columns for small paired devices.
- Use three columns only when the container is wide enough.

## Container Sizing

Container size should fit all children plus padding:

```text
ContainerWidth >= max(child.x + child.width) + rightPadding
ContainerHeight >= max(child.y + child.height) + bottomPadding
```

Recommended padding:
- Left and right: `20` to `40`
- Top title space: at least `50`
- Bottom: `20` to `40`

## Readability Rules

- Avoid large empty container bands.
- Avoid placing boxes so close that connector lines disappear.
- Keep at least one readable gap between adjacent device boxes.
- Keep text inside the shape where possible.
- Increase box size before shrinking fonts.
- Default diagram text can use 20px when the generator supports it.

## Connector Rules

- Network topology connectors should be straight by default.
- Other diagram types may use routed or orthogonal connectors when they improve readability.
- Avoid connector labels in dense topology diagrams.
- Put labels in node or container names when possible.
- For Excalidraw, labels must not overlap connector lines.
