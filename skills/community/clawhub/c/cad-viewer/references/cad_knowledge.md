# CAD DWG/DXF Professional Knowledge Reference

## DWG File Structure

DWG is Autodesk's proprietary binary format, with DXF being its open text counterpart.

```
Drawing Database (DXF Document)
 ├── Header                           --> Global settings: version, units, creation time, etc.
 ├── Layout Dictionary
 │    ├── Model Space                 --> [Physical Container] Contains actual Entities
 │    ├── Paper Space                 --> [Physical Container] Contains sheet frames, etc.
 │    └── Block Definitions           --> [Physical Container] Like "micro spaces", also contain Entities
 │
 ├── Layer Table                      --> [Logical Dictionary] Defines names, colors, linetypes
 │    ├── Layer "0" (system default)
 │    ├── Layer "E-CABINET" (example: electrical cabinet layer)
 │    └── Layer "M-HVAC" (example: HVAC layer)
 │
 └── Style tables, linetype tables, and other auxiliary definitions
```

## Core Concepts

### Model Space
- The primary space containing all actual design content
- Drawn at 1:1 real-world scale
- The main target area for data analysis

### Paper Space
- Virtual sheets for print output
- References model space content through Viewports
- Contains sheet frames, title blocks, and other print-related elements

### Block Definitions and Block References (INSERT)
- **Block Definition**: Reusable graphic template (analogous to "stamp master")
- **Block Reference (INSERT)**: Instance "stamped" in model space
- One block definition can be referenced multiple times, each with independent position, rotation, and scale

### Layers
- Logical grouping labels, similar to Photoshop layer concept
- Each entity must belong to exactly one layer
- Layers define default visual attributes like color and linetype
- Can be turned on/off, frozen/thawed, locked/unlocked
- **Standard requirement**: Entities should be placed on corresponding professional layers, not on default layer 0

## Common Entity Types

| Type | DXF Name | Description | Key Attributes |
|------|----------|-------------|----------------|
| Line | LINE | Straight line segment between two points | start, end |
| Polyline | LWPOLYLINE | Continuous polyline (can be closed) | vertices, is_closed |
| Circle | CIRCLE | Full circle | center, radius |
| Arc | ARC | Partial circular arc | center, radius, start_angle, end_angle |
| Single-line Text | TEXT | Single-line text annotation | text, insert, height |
| Multi-line Text | MTEXT | Multi-line rich text | text, insert, char_height |
| Block Reference | INSERT | Instantiated reference to a block | name, insert, rotation, scale |
| Dimension | DIMENSION | Dimension annotation | Multiple types |
| Hatch | HATCH | Area fill/section lines | pattern_name |
| Ellipse | ELLIPSE | Elliptical shape | center, major_axis, ratio |
| Spline | SPLINE | Free-form curve | control_points |

## CAD Unit Mapping

| Code | Unit | Description |
|------|------|-------------|
| 0 | Unitless | Not set, usually interpreted as millimeters |
| 1 | Inches | Imperial |
| 2 | Feet | Imperial |
| 4 | Millimeters | Domestic architecture standard |
| 5 | Centimeters | |
| 6 | Meters | |
| 14 | Decimeters | |

## Common Audit Rules

### Layer 0 Usage Standards
- Entities inside block definitions may use layer 0 (inherits outer layer attributes)
- INSERT entities in model space should **NOT** be placed on layer 0
- Entities on layer 0 are considered "unclassified", violating professional layer standards

### Block Layer Consistency
- Standard blocks should only use layer 0 internally
- If a block internally mixes multiple layers, it may have been exploded and recreated

### Empty Layer Check
- Layers with definitions but no entities may be redundant
- Need to confirm if intentionally reserved as template layers

## Coordinate System

- CAD uses Cartesian coordinate system (X positive right, Y positive up)
- Coordinate units determined by $INSUNITS header variable
- Distance calculation uses Euclidean distance formula
- 2D distance: √(Δx² + Δy²)
- 3D distance: √(Δx² + Δy² + Δz²)

## Common Professional Layer Naming in Data Center Drawings

| Prefix | Discipline | Example |
|--------|------------|---------|
| EC. | Electrical | EC.SingleLine, EC.DIM |
| AC. | HVAC | AC.DistributionBox |
| E- | Electrical System | E-System-DistributionBox-Components |
| M- | HVAC | M-HVAC |
| TK | Title Block | TK |

## Entity Handle

- Each entity has a unique handle (hexadecimal string)
- Handle is unique throughout the entire drawing, can be used to precisely locate entities
- Format example: "1A3", "2FF", "10B5"
