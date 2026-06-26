# D2 Syntax Reference

## Node Shapes

### Basic Shapes

- `rectangle` - Rectangle (default)
- `square` - Square
- `circle` - Circle
- `oval` - Oval
- `ellipse` - Ellipse (alias for oval)

### Flowchart Shapes

- `diamond` - Diamond (conditional)
- `parallelogram` - Parallelogram (input/output)
- `trapezoid` - Trapezoid
- `rounded_rectangle` - Rounded rectangle
- `stroke_rectangle` - Stroked rectangle

### Data and Storage

- `cylinder` - Cylinder (database)
- `queue` - Queue (cylinder variant)
- `disk` - Disk
- `storage` - Storage

### System and Network

- `cloud` - Cloud (external system/service)
- `hexagon` - Hexagon
- `octagon` - Octagon
- `callout` - Callout box
- `note` - Note

### People and Organization

- `person` - Person
- `queue` - Queue (waiting line)

### Documents and Pages

- `page` - Document page
- `document` - Document

### Special Shapes

- `image` - Image node
- `sql_table` - SQL table
- `class` - Class diagram (UML)

**Note**: `shape: label` is not supported in some versions of D2. It's recommended to use the node's `label` property or the direct label syntax:
```
node: "Label text"  # Recommended approach
```

## Connection Types

### Basic Connections

```
A -> B     # Directed arrow
A <- B     # Reverse arrow
A <-> B    # Bidirectional arrow
A -- B     # Undirected line
A - B      # Undirected line (shorthand)
```

### Connection Labels

```
A -> B: Label text           # Single-line label
# Note: Multi-line labels use block syntax or |md syntax
```

### Arrowhead Styles

Customize arrows with `source-arrowhead` and `target-arrowhead`:

```
source-arrowhead: triangle    # Triangle (default)
source-arrowhead: arrow       # Arrow
source-arrowhead: diamond     # Diamond
source-arrowhead: circle      # Circle
source-arrowhead: box         # Box
source-arrowhead: cross       # Cross
source-arrowhead: none        # No arrowhead
```

### Connection Line Styles

```
A -> B {
  style.stroke-dash: 3        # Dashed line
  style.stroke-width: 2       # Line width
  style.stroke: red           # Line color
  style.animated: true        # Animation effect
}
```

## Style Properties

### Colors

```
style.fill: "#ff0000"         # Fill color (hexadecimal)
style.fill: red               # Fill color (color name)
style.stroke: blue            # Border color
style.opacity: 0.5            # Opacity (0-1)
```

### Borders

```
style.stroke-width: 2         # Border width
style.stroke-dash: 5          # Dash pattern (number is spacing)
style.border-radius: 8        # Border radius
```

### Fonts

```
style.font-size: 14           # Font size
style.font-color: "#333"      # Font color
# Note: style.font-weight and style.font-style are not supported in some versions
```

**Important**: Multiple style properties **must be separated by newlines, do not use semicolons or commas**.

Correct example:
```
node: {
  style.fill: red
  style.stroke: blue
  style.stroke-width: 2
}
```

Incorrect example:
```
node: { style.fill: red; style.stroke: blue }
```

### Fill Patterns

```
style.fill-pattern: dots      # Dots pattern
style.fill-pattern: lines     # Lines pattern
style.fill-pattern: crosshatch # Crosshatch pattern
```

### Multiplicity

```
style.multiple: true          # Display multiple nodes (e.g., multiple databases)
```

### Animation

```
style.animated: true          # Enable animation
```

## Container Syntax

### Basic Container

```
container_name: {
  nodeA
  nodeB
}
```

### Nested Containers

```
outer_container: {
  inner_container: {
    nodeC
  }
  nodeA
  nodeB
}
```

### Container Styles

```
container: {
  style.fill: "#f0f0f0"
  style.stroke: "#333"
  nodeA
  nodeB
}
```

### Container Layout

```
container: {
  direction: right            # Layout direction within container
  grid-columns: 3             # Number of grid columns
  nodeA
  nodeB
  nodeC
}
```

### Referencing Parent Containers

```
outer: {
  middle: {
    node -> _                 # _ references outer container
  }
  parent_node
}

middle.node -> outer.parent_node       # Full path reference
```

## Classes and Style Reuse

### Defining Classes

```
class: class_name
class_name: {
  style.fill: yellow
  style.stroke: orange
}
```

### Applying Classes

```
nodeA: {
  class: class_name
}
```

### Multiple Classes

```
nodeA: {
  class: [class1, class2]           # Applied in order
}
```

### Class Inheritance

Object properties override class properties:

```
class_name: {
  style.fill: yellow
}

node: {
  class: class_name
  style.fill: red             # Overrides class fill property
}
```

## Layout Control

### Global Layout Direction

```
direction: right              # Left to right (default)
direction: down               # Top to bottom
direction: left               # Right to left
direction: up                 # Bottom to top
```

### Layout Engine

Set in `vars`:

```
vars: {
  d2-config: {
    layout-engine: dagre      # dagre (default)
    layout-engine: elk        # ELK layout
    layout-engine: tala       # TALA layout
  }
}
```

### Themes

```
vars: {
  d2-config: {
    theme-id: 0               # Default theme
    theme-id: 1               # Neutral theme
    theme-id: 3               # Terrastruct theme
    theme-id: 100             # Custom theme number
  }
}
```

### Sketch Mode

```
vars: {
  d2-config: {
    sketch: true              # Enable hand-drawn style
  }
}
```

## Variables

### Defining Variables

```
vars: {
  variable_name: value
  colors: {
    primary: "#007bff"
    secondary: "#6c757d"
  }
}
```

### Using Variables

```
nodeA: {
  style.fill: ${vars.colors.primary}
}

title: ${vars.variable_name}
```

## Advanced Features

### Tooltips

```
node: { tooltip: "Hover tooltip text" }
```

### Links

```
node: {
  link: "https://example.com"
  tooltip: "Click to visit"
}
```

### SQL Tables

```
table: {
  shape: sql_table
  column1: type1
  column2: type2
  column3: type3
}
```

### Multi-line Labels

Use block syntax to support multi-line text:

```
node: |md
  # Markdown Heading
  Supports multi-line text
  Supports **bold** and *italic*
|
```

Or use simple line breaks:

```
node: |md
  First line
  Second line
  Third line
|
```

### Grid Layout

```
container: {
  grid-columns: 3             # 3-column grid
  nodeA
  nodeB
  nodeC
  nodeD
  nodeE
  nodeF
}
```

### Wildcard Styles

```
*.style.fill: blue            # All nodes
*.*.style.fill: green         # All nested nodes
(nodeA -- *)[*].style.stroke: red  # All connections of nodeA
```

### Title

```
title: "Diagram Title"             # Simple title
title: |md                    # Markdown title
  # Heading 1
  Supports **Markdown** format
| {near: top-center}          # Title position
```

### Position Control (Use Sparingly)

```
node: {
  position: absolute
  x: 100
  y: 200
}
```

Note: Prefer automatic layout; only use manual positioning when necessary.

## Comments

### Line Comments

```
# This is a single-line comment
nodeA -- nodeB  # End-of-line comment
```

### Multi-line Comments

Use multiple line comments for multi-line comments:

```
# This is the first line of comment
# This is the second line of comment
# This is the third line of comment
nodeA -- nodeB
```

## Special Syntax

### Implicit Connections

Multiple nodes on the same line are automatically connected:

```
A B C D                       # Equivalent to A -> B -> C -> D
```

### Connection Grouping

```
(A B C) -> (D E F)            # A, B, C each connect to D, E, F
```

### Conditional Styles

```
node: {
  style.fill?: red            # Conditional style (if not set)
}
```

### Label Shorthand

```
node: Label text              # Node name is "node", label is "Label text"
```

## Common Patterns

### Database Connection

```
app <-> database: {
  style.stroke-dash: 3
  source-arrowhead: none
  target-arrowhead: triangle
}
```

### Conditional Branch

```
decision: {
  shape: diamond
  style.fill: lightyellow
}
```

### Loop Process

```
stepA -> stepB -> stepC
stepC -> stepA: "Loop"
```

### Parallel Processing

```
parallel_tasks: {
  direction: right
  task1
  task2
  task3
}

start -> parallel_tasks
parallel_tasks -> end
```

### Error Handling

```
main_process -> error_handler: "Exception"
error_handler: {
  style.fill: "#ffcccc"
  style.stroke: red
}
```