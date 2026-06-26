# CADStack - CAD Automation Skill Pack

Control AutoCAD, SolidWorks, Fusion 360, and FreeCAD via Claude Code skills.

## Features

- **Multi-platform support**: FreeCAD, AutoCAD, SolidWorks, Fusion 360
- **Headless mode**: FreeCAD works without GUI
- **Natural language control**: Create parts using conversational commands
- **Script templates**: Pre-built templates for common parts
- **Safety review**: Built-in script validation before execution

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cadstack.git ~/.claude/skills/cadstack

# Run setup
cd ~/.claude/skills/cadstack
python setup
```

## Skills

| Skill | Description |
|-------|-------------|
| `/cad` | Execute CAD commands - create, modify, export parts |
| `/cad-plan` | Plan complex multi-step CAD operations |
| `/cad-review` | Review scripts for safety and correctness |
| `/cad-qa` | Verify output files and validate geometry |
| `/cad-config` | Configure CAD backend connections |

## Quick Start

```bash
# In Claude Code
/cad "Create a 100x50x20mm box with 5mm fillets"
/cad "Create a gear with 20 teeth, module 2"
/cad "Create a mounting bracket with 4 holes"
```

## Supported Platforms

### FreeCAD (Recommended)
- Pure Python, headless mode
- No license required
- Install: `apt install freecad` or download from [freecad.org](https://www.freecad.org)

### AutoCAD
- Requires AutoCAD running on Windows
- Uses COM automation via pywin32

### SolidWorks
- Requires SolidWorks running on Windows
- Uses COM automation via pywin32

### Fusion 360
- Requires Fusion 360 with bridge add-in running
- Communicates via socket on port 8080

## API Reference

### Primitives

```python
backend.create_box(length, width, height, name)
backend.create_cylinder(radius, height, name)
backend.create_sphere(radius, name)
backend.create_cone(radius1, radius2, height, name)
backend.create_torus(radius1, radius2, name)
```

### Boolean Operations

```python
backend.fuse(obj1, obj2, name)      # Union
backend.cut(obj1, obj2, name)       # Difference
backend.intersect(obj1, obj2, name) # Intersection
```

### Modifications

```python
backend.fillet(obj, edges, radius)
backend.chamfer(obj, edges, distance)
backend.move(obj, x, y, z)
backend.rotate(obj, axis, angle_degrees)
```

### Export

```python
backend.export_step(doc, filepath)
backend.export_stl(doc, filepath)
backend.export_obj(doc, filepath)
```

## Templates

Located in `templates/` directory:

- `freecad/basic_box.py` - Simple box with optional fillets
- `freecad/basic_cylinder.py` - Cylinder with optional hole
- `freecad/mounting_bracket.py` - Bracket with mounting holes
- `freecad/gear.py` - Parametric involute gear
- `freecad/enclosure.py` - Hollow box with walls

## CLI

```bash
# Check platform availability
python lib/cad_executor.py info

# Create a primitive
python lib/cad_executor.py create box 100,50,20 --name mybox --output box.step

# Run a script
python lib/cad_executor.py run script.py --platform freecad
```

## Configuration

Edit `config.json` to set defaults:

```json
{
  "default_platform": "freecad",
  "output_directory": "~/.claude/skills/cadstack/output",
  "default_format": "step",
  "units": "mm"
}
```

## Dependencies

```toml
[project]
dependencies = [
    "typer>=0.12.0",
    "rich>=13.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
windows = ["pywin32>=306"]
```

## License

MIT License

## Contributing

Contributions welcome! Please read the contributing guidelines first.
