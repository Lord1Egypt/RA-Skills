# Dify Workflow Node Positioning Guide

This document describes best practices for positioning nodes on the visual workflow canvas.

## Coordinate System

Dify workflows use a standard 2D canvas coordinate system:
- **X-axis**: Horizontal position (left to right)
- **Y-axis**: Vertical position (top to bottom)
- **Origin**: Top-left corner (0, 0)
- **Units**: Pixels

## Node Dimensions

### Standard Node Sizes

Based on the React Flow implementation, nodes have these approximate dimensions:

**Default Node**: 240px width × 90-120px height (varies by content)

**Note**: The actual node width constant in source code is `NODE_WIDTH = 240`.

**Specific Node Types** (width is 240px for all standard nodes):
- **Start Node**: 240px × 90px
- **End Node**: 240px × 100px
- **LLM Node**: 240px × 120px (with model display)
- **Code Node**: 240px × 110px
- **If-Else Node**: 240px × 130px
- **Question Classifier**: 240px × 150px
- **Iteration/Loop Container**: Variable (parent node) + internal graph area
- **HTTP Request**: 240px × 110px
- **Knowledge Retrieval**: 240px × 120px
- **Variable Aggregator**: 240px × 90px

**Note**: Actual rendered sizes may vary based on:
- Node title length
- Number of variables/configurations displayed
- Error messages or status indicators
- Custom node content

## Spacing Guidelines

### Official Layout Constants

From the Dify source code (`workflow/constants.ts`):
- **NODE_WIDTH**: 240px (standard node width)
- **X_OFFSET**: 60px (horizontal offset between nodes)
- **NODE_WIDTH_X_OFFSET**: 300px (NODE_WIDTH + X_OFFSET)
- **Y_OFFSET**: 39px (vertical offset)
- **START_INITIAL_POSITION**: `{ x: 80, y: 282 }` (default start node position)
- **AUTO_LAYOUT_OFFSET**: `{ x: -42, y: 243 }` (auto-layout adjustment offset)

### Horizontal Spacing

**Standard gap between sequential nodes**: 300px (NODE_WIDTH_X_OFFSET)
- Node width: 240px
- Gap between nodes: 60px

This provides comfortable visual separation and room for edge labels.

```
Node A (x=80) → 300px total → Node B (x=380)
```

**Recommended horizontal spacing**:
- **Standard**: 300px (recommended, matches NODE_WIDTH_X_OFFSET)
- **Minimal**: 260px (tight layout, NODE_WIDTH + 20px clearance)
- **Spacious**: 350-400px (for complex workflows with many labels)

### Vertical Spacing

**Same level nodes**: Same y-coordinate

**Branch separation**: 150-250 pixels vertical offset

```
Main path:     y=300
True branch:   y=200 (100px above)
False branch:  y=450 (150px below)
```

**Recommended vertical spacing for branches**:
- **Two branches**: ±150px from main path
- **Three branches**: ±200px from main path
- **Four+ branches**: ±250px from main path

### Canvas Margins

**Initial node position**: Start with generous margins
- **X margin**: 100-200px from left edge
- **Y margin**: 200-300px from top edge

This ensures nodes aren't cut off and provides room for expansion.

## Common Layout Patterns

### 1. Linear Flow (Sequential)

Horizontal left-to-right flow (using official constants):

```yaml
Start:    { x: 80,  y: 282 }  # START_INITIAL_POSITION
LLM:      { x: 380, y: 282 }  # 80 + 300 (NODE_WIDTH_X_OFFSET)
Code:     { x: 680, y: 282 }  # 380 + 300
End:      { x: 980, y: 282 }  # 680 + 300
```

Visual representation:
```
Start → LLM → Code → End
```

### 2. Binary Branching (If-Else)

Y-shaped pattern with two branches converging:

```yaml
Start:      { x: 80,  y: 282 }  # START_INITIAL_POSITION
If-Else:    { x: 380, y: 282 }  # 80 + 300
True-Path:  { x: 680, y: 200 }  # 82px above center
False-Path: { x: 680, y: 400 }  # 118px below center
Aggregator: { x: 980, y: 282 }  # Back to center
End:        { x: 1280, y: 282 }
```

Visual representation:
```
              ┌─ True-Path ─┐
Start → If ───┤              ├─ Aggregator → End
              └─ False-Path ┘
```

### 3. Multi-Branch Classification

Fan-out pattern with multiple paths:

```yaml
Start:       { x: 100,  y: 350 }
Classifier:  { x: 450,  y: 350 }
Branch-1:    { x: 800,  y: 150 }  # 200px above
Branch-2:    { x: 800,  y: 300 }  # 50px above
Branch-3:    { x: 800,  y: 450 }  # 100px below
Branch-4:    { x: 800,  y: 600 }  # 250px below
Aggregator:  { x: 1150, y: 350 }
End:         { x: 1500, y: 350 }
```

### 4. Error Handling Pattern

Success/fail branches with recovery:

```yaml
Start:       { x: 100,  y: 300 }
Code:        { x: 450,  y: 300 }
Success:     { x: 800,  y: 250 }  # 50px above
Fail:        { x: 800,  y: 400 }  # 100px below
Recovery:    { x: 1150, y: 400 }  # Aligned with fail path
Aggregator:  { x: 1500, y: 300 }
End:         { x: 1850, y: 300 }
```

Visual representation:
```
              ┌─ Success ────────────┐
Start → Code ─┤                       ├─ Aggregator → End
              └─ Fail → Recovery ────┘
```

### 5. Iteration/Loop Container

Container with internal graph:

```yaml
# Parent nodes
Start:      { x: 100,  y: 300 }
Iteration:  { x: 450,  y: 300 }
End:        { x: 1400, y: 300 }

# Internal iteration nodes (offset within container)
Iter-Start: { x: 550,  y: 380 }  # Inside container
Process-1:  { x: 800,  y: 380 }
Process-2:  { x: 1050, y: 380 }
Iter-End:   { x: 1300, y: 380 }
```

**Container sizing**: Parent iteration node should be positioned to visually contain internal nodes, typically with 50px padding.

### 6. Vertical Flow (Top to Bottom)

Alternative layout for narrow canvases:

```yaml
Start:  { x: 400, y: 100 }
LLM:    { x: 400, y: 300 }  # 200px below
Code:   { x: 400, y: 500 }  # 200px below
End:    { x: 400, y: 700 }  # 200px below
```

## Position Calculation Formulas

### Sequential Horizontal Layout

```python
# Using official Dify constants
NODE_WIDTH = 240
X_OFFSET = 60
NODE_WIDTH_X_OFFSET = 300  # NODE_WIDTH + X_OFFSET
START_INITIAL_POSITION = {'x': 80, 'y': 282}

node_positions = []
x = START_INITIAL_POSITION['x']
y = START_INITIAL_POSITION['y']

for i, node in enumerate(nodes):
    node_positions.append({
        'x': x + i * NODE_WIDTH_X_OFFSET,
        'y': y
    })

# Result: [80, 380, 680, 980, ...]
```

### Binary Branch Layout

```python
# Main path (using START_INITIAL_POSITION)
main_y = 282

# If-else node
ifelse_x = 80 + 300  # 380
ifelse_y = main_y

# Branches
branch_x = ifelse_x + 300  # 680
true_y = main_y - 82   # 200 (above)
false_y = main_y + 118  # 400 (below)

# Aggregator (convergence)
agg_x = branch_x + 300  # 980
agg_y = main_y  # 282 (back to center)
```

### Multi-Branch Spread

```python
num_branches = 4
main_y = 350
total_spread = 450  # Total vertical range
branch_spacing = total_spread / (num_branches - 1)

branch_positions = []
for i in range(num_branches):
    y = (main_y - total_spread / 2) + (i * branch_spacing)
    branch_positions.append({'x': 800, 'y': y})
```

## Grid Alignment

For cleaner layouts, consider snapping nodes to a grid:

**Grid size**: 50 pixels

```python
def snap_to_grid(position, grid_size=50):
    return {
        'x': round(position['x'] / grid_size) * grid_size,
        'y': round(position['y'] / grid_size) * grid_size
    }
```

Example:
```
Unaligned: { x: 437, y: 289 }
Snapped:   { x: 450, y: 300 }
```

## Auto-Layout Considerations

The Dify visual editor uses React Flow's layout features. When generating DSL programmatically:

1. **Calculate bounds**: Ensure all nodes fit within a reasonable canvas size
2. **Avoid overlaps**: Check for node collisions before finalizing positions
3. **Balance branching**: Spread branches evenly around main path
4. **Maintain flow direction**: Keep consistent left-to-right or top-to-bottom flow
5. **Reserve space**: Leave room for user to add nodes manually

## Canvas Size Recommendations

**Minimum canvas**: 1200px × 800px (for simple flows)
**Standard canvas**: 2000px × 1200px (for moderate complexity)
**Large canvas**: 3000px × 1600px (for complex multi-branch flows)

## Position Validation

Before finalizing node positions, check:

- [ ] No nodes have negative x or y coordinates
- [ ] No nodes overlap (minimum 50px clearance)
- [ ] All nodes are visible within reasonable zoom levels (0.5x to 2x)
- [ ] Edges between nodes don't cross unnecessarily
- [ ] Visual hierarchy is clear (main path is obvious)
- [ ] Branches are symmetrically distributed

## Example: Complete Workflow Layout

```yaml
# Linear flow with branching
nodes:
  - id: "1732007415808"
    position: { x: 100, y: 300 }
    type: start

  - id: "1732007420123"
    position: { x: 450, y: 300 }
    type: llm

  - id: "1732007425456"
    position: { x: 800, y: 300 }
    type: if-else

  - id: "1732007430789"
    position: { x: 1150, y: 200 }  # True branch
    type: code

  - id: "1732007435012"
    position: { x: 1150, y: 450 }  # False branch
    type: http-request

  - id: "1732007440234"
    position: { x: 1500, y: 300 }  # Convergence
    type: variable-aggregator

  - id: "1732007445567"
    position: { x: 1850, y: 300 }
    type: end
```

## Tips for Manual Adjustments

When users manually adjust positions in the visual editor:

1. **Preserve alignment**: Keep related nodes vertically aligned
2. **Maintain spacing**: Try to keep consistent horizontal gaps
3. **Group related nodes**: Position error handlers near their source
4. **Use whitespace**: Don't overcrowd the canvas
5. **Think hierarchically**: Main path should be most prominent

## React Flow Specifics

The Dify visual editor uses React Flow with these defaults:

- **Default zoom**: 1.0 (100%)
- **Min zoom**: 0.1 (10%)
- **Max zoom**: 2.0 (200%)
- **Snap to grid**: Optional (usually disabled for flexibility)
- **Auto-pan**: Enabled (canvas pans when dragging nodes near edge)

**Initial viewport**:
```yaml
viewport:
  x: 0
  y: 0
  zoom: 1.0
```

When generating workflows programmatically, you can set viewport to center on the graph:

```python
# Calculate center of all nodes
center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2

# Set viewport to center on graph
viewport = {
    'x': -center_x + canvas_width / 2,
    'y': -center_y + canvas_height / 2,
    'zoom': 1.0
}
```
