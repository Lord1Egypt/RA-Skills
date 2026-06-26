---
name: blender_bpy
description: Blender Python scripting via bpy API. Use for scene automation, procedural modeling, batch rendering, and object manipulation.
metadata: { "openclaw": { "requires": { "bins": ["blender"] }, "user-invocable": true } }
---

# Blender Python Automation (bpy)

## Prerequisites
- Blender must be installed and accessible from the CLI (`blender --version`).
- Scripts run via: `blender --background --python <script.py>`
- For interactive use: connect via Blender's built-in Python console or the REST server addon.

## Common Snippets

### Create an object
```python
import bpy
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
obj = bpy.context.object
obj.name = "MyCube"
```

### Batch render all frames
```python
import bpy
scene = bpy.context.scene
scene.render.filepath = "//renders/frame_"
bpy.ops.render.render(animation=True)
```

### Apply a material by name
```python
import bpy
mat = bpy.data.materials.get("MyMaterial")
if mat is None:
    mat = bpy.data.materials.new(name="MyMaterial")
obj = bpy.context.object
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)
```

## Tips
- Always use `--background` when running headless (no UI).
- Use `bpy.data` (global access) vs `bpy.context` (active selection) correctly.
- For long renders, consider Cron jobs in OpenClaw so main chat isn't blocked.
