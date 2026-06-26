---
name: blender-bpy
title: Blender 3D Automation — Python bpy Scripting
description: Comprehensive Blender automation via Python bpy API. Procedural modeling, material nodes, lighting, rendering, and asset generation. Includes verified gear/mechanical parts demo.
version: 2.2.0
author: Approxima (via skillhub.cn)
tags: [blender, 3d, modeling, rendering, bpy, procedural, automation, 3d-printing]
requires:
  bins: [blender]
---

# Blender Python Automation (bpy) — v2.2.0

## When to Use This Skill

Invoke when the user wants to:
- Create 3D objects procedurally (gears, mechanical parts, architectural elements)
- Set up materials with node-based textures (metal, brushed, procedural)
- Configure 3-point lighting and camera
- Render still images or animations in headless mode
- Batch process or automate Blender workflows
- Export to GLB/glTF for web or game engines

## Prerequisites

```bash
# Install Blender
apt-get install blender   # Linux (Debian/Ubuntu)
# Or: brew install blender  # macOS

# Verify
blender --version
```

## Core Patterns

### 1. Headless Execution
```bash
blender --background --python script.py
```

### 2. Scene Setup
```python
import bpy, math

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials):
    bpy.data.materials.remove(mat)
```

### 3. Procedural Gear Creation
```python
def create_gear(name, radius=2.0, teeth=16, thickness=0.8):
    """Create a gear with teeth and center hole"""
    # Base cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=teeth * 4,
        radius=radius,
        depth=thickness,
        location=(0, 0, 0)
    )
    gear = bpy.context.object
    gear.name = name
    
    # Edit mode: select vertices at tooth positions
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    for v in gear.data.vertices:
        angle = math.atan2(v.co.y, v.co.x)
        tooth_angle = 2 * math.pi / teeth
        angle_diff = abs((angle % tooth_angle) - tooth_angle / 2)
        if angle_diff < tooth_angle * 0.35:
            v.select = True
    
    # Extrude and scale for teeth
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, 0)}
    )
    bpy.ops.transform.resize(
        value=((radius + 0.4) / radius,) * 2 + (1,),
        orient_type='GLOBAL'
    )
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Center hole via Boolean
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32, radius=0.5,
        depth=thickness * 1.5, location=(0, 0, 0)
    )
    cutter = bpy.context.object
    bool_mod = gear.modifiers.new(name="Hole", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cutter
    bpy.context.view_layer.objects.active = gear
    gear.select_set(True)
    bpy.ops.object.modifier_apply(modifier="Hole")
    bpy.data.objects.remove(cutter, do_unlink=True)
    
    # Modifier stack
    bevel = gear.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.05; bevel.segments = 2; bevel.limit_method = 'ANGLE'
    subdiv = gear.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 1; subdiv.render_levels = 2
    
    return gear
```

### 4. Procedural Metal Material (Node-based)
```python
def create_metal_material(name, base_color, metallic=0.85, roughness=0.25,
                          noise_scale=30.0, use_brushed=True):
    """Create a procedural metal material with optional brushed effect"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = base_color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    
    if use_brushed:
        tex = nodes.new(type='ShaderNodeTexCoord')
        tex.location = (-400, 100)
        noise = nodes.new(type='ShaderNodeTexNoise')
        noise.location = (-200, 0)
        noise.inputs['Scale'].default_value = noise_scale
        noise.inputs['Detail'].default_value = 2.0
        ramp = nodes.new(type='ShaderNodeValToRGB')
        ramp.location = (0, 100)
        ramp.color_ramp.elements[0].color = (
            base_color[0]*0.8, base_color[1]*0.8, base_color[2]*0.8, 1.0)
        ramp.color_ramp.elements[1].color = (
            base_color[0]*1.1, base_color[1]*1.1, base_color[2]*1.1, 1.0)
        
        links.new(tex.outputs['Object'], noise.inputs['Vector'])
        links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
        links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat
```

### 5. 3-Point Lighting Setup
```python
def setup_lighting(base_intensity=600):
    """Standard 3-point lighting: key, fill, rim"""
    # Key light (main)
    key = bpy.ops.object.light_add(
        type='AREA', location=(5, -4, 6),
        rotation=(0.8, 0, 0.7))
    key = bpy.context.object
    key.data.energy = base_intensity
    key.data.size = 4
    
    # Fill light
    fill = bpy.ops.object.light_add(
        type='AREA', location=(-4, 3, 3),
        rotation=(0.5, 0, -1.0))
    fill = bpy.context.object
    fill.data.energy = base_intensity * 0.5
    fill.data.size = 3
    
    # Rim/back light
    rim = bpy.ops.object.light_add(
        type='AREA', location=(0, 5, 5),
        rotation=(0.5, 0, 1.57))
    rim = bpy.context.object
    rim.data.energy = base_intensity * 0.4
    rim.data.size = 2
```

### 6. Camera Setup & Dynamic Look-At
```python
def setup_camera(location=(5.5, -4.5, 3.5), target=(0, 0, 0)):
    bpy.ops.object.camera_add(location=location)
    cam = bpy.context.object
    
    # Point camera at target dynamically using quaternions (mathutils)
    direction = mathutils.Vector(target) - cam.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot_quat.to_euler()
    
    bpy.context.scene.camera = cam
    return cam
```

### 7. Rendering
```python
def render(output_path="/tmp/render.png", engine='CYCLES',
           width=1080, height=1080, samples=64):
    scene = bpy.context.scene
    scene.render.engine = engine
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = 'PNG'
    
    if engine == 'CYCLES':
        scene.cycles.samples = samples
        scene.cycles.use_denoising = True
        
        # Configure Metal GPU on macOS if available
        try:
            bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'METAL'
            bpy.context.preferences.addons['cycles'].preferences.get_devices()
            for d in bpy.context.preferences.addons['cycles'].preferences.devices:
                if d.type == 'METAL':
                    d.use = True
        except Exception:
            pass
            
    bpy.ops.render.render(write_still=True)
```

### 8. Solid Glass / Ice Material
```python
def create_glass_material(name="Glass", color=(0.9, 0.95, 1.0, 1.0), roughness=0.1, ior=1.309):
    """Create refractive glass or ice material. IOR: 1.309 (ice), 1.5 (glass)"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['IOR'].default_value = ior
    
    # Enable transparency (Transmission)
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in bsdf.inputs:
        bsdf.inputs['Transmission'].default_value = 1.0
        
    return mat
```

### 9. Advanced Boolean Modeling (One-by-One Carving & Overlaps)
When carving grooves or features into a mesh:
* **Avoid Bulk Cuts**: Subtracting a complex, self-intersecting mesh (e.g. intersecting tubes) all at once makes the `EXACT` solver delete the geometry (vertex count becomes 0). Carve individual loops **one-by-one** instead.
* **Overlapping Geometry**: Always make cutter objects overlap the boundaries of the base object (e.g. extending slightly outside and deeper inside). Co-incident boundaries cause the `EXACT` solver to fail and skip subtraction.
* **Capping Curves**: When converting curves to meshes for cutting, set `curve_data.use_fill_caps = True` before conversion. Combine with a `Subdivision Surface` modifier for clean rounded tips.

### 10. 100% Procedural Coordinate Shader Seams (No Mesh Cuts)
For perfect geometry and flawless renderings on regular solids (like spheres), define seams directly in the shader nodes using object coordinates instead of modifying geometry:
* **Basketball Curved Seams Formula**: 
  $$|x| = \sqrt{1 - z^2} \cos\left(\theta_d \sqrt{1 - z^2}\right)$$
* **Map Range & Masking**: Map the resulting distance to a `SMOOTHERSTEP` mask from $[w, w+s]$ to $[0, 1]$. Use this mask to mix Colors (Black vs. Orange), Roughness, and normal Height inputs into a single Bump node.

### 11. 3D Printing & Watertight Export (Solidify/Decimate)
When creating models intended for physical 3D printing (e.g. FDM/SLA):
* **Real-World Units**: Explicitly set the scene scale. Usually, 1 Blender unit represents 1 cm or 1 mm:
  ```python
  scene = bpy.context.scene
  scene.unit_settings.system = 'METRIC'
  scene.unit_settings.scale_length = 0.01  # 1 unit = 1 cm (Pop Mart standard)
  ```
* **Hollow/Wall Thickness**: 3D models cannot have zero-thickness surfaces. Use the `Solidify` modifier to give surfaces a physical thickness (typically 1.2mm to 2.0mm):
  ```python
  solid = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
  solid.thickness = 0.12  # 1.2 mm (if 1 unit = 1 cm)
  solid.offset = -1.0     # Solidify inward
  ```
* **Poly Count Optimization**: Large vertex counts slow down slicers. Use a `Decimate` modifier to reduce poly count prior to export:
  ```python
  decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
  decimate.ratio = 0.15   # Keep 15% of faces
  ```
* **Watertight STL Export**: Ensure geometry is manifold, then export using standard operators:
  ```python
  # Blender 4.0+ uses standard wm operators for STL export
  bpy.ops.wm.stl_export(filepath="model.stl", export_selected=True)
  # Older Blender (<4.0):
  # bpy.ops.export_mesh.stl(filepath="model.stl", use_selection=True)
  ```

### 12. Loading Background Reference Image Planes
To align procedural elements to concept art (front/side/top views), programmatically load images as background planes:
```python
def load_reference_image(filepath, name="ReferenceImage", location=(0, 0, 0), rotation=(1.5708, 0, 0)):
    # Create an empty object of type IMAGE
    bpy.ops.object.empty_add(type='IMAGE', location=location, rotation=rotation)
    empty = bpy.context.object
    empty.name = name
    
    # Load and assign the image data
    try:
        img = bpy.data.images.load(filepath)
        empty.data = img
        empty.empty_display_size = 5.0  # scale size
        # Optional: set opacity
        empty.use_empty_image_alpha = True
        empty.empty_image_depth = 'BACK'  # display behind mesh
    except Exception as e:
        print(f"Error loading reference image: {e}")
```

## Render Engines

| Engine | Best For | Notes |
|--------|----------|-------|
| `BLENDER_EEVEE` | Fast preview, real-time | No denoiser needed, good for quick checks |
| `CYCLES` | Photorealistic | Essential for glass reflection and refraction. Use `samples=64` or `128` with Denoising. |

## Common Pitfalls

* **Boolean Exact solver deletes mesh (Vertices = 0)** → Check for self-intersections or co-incident surfaces in the cutter. Switch to `'FLOAT'` (called `'FAST'` in Blender <4.0), ensure cutter overlapping boundaries, or perform Boolean carving one-by-one.
* **Hollow tubes when converting curves to mesh** → Enable caps before converting: `curve_data.use_fill_caps = True`.
* **Glass rendering looks flat or dark** → Glass requires light reflections to look realistic. Add a dark reflective metallic ground plane (`Roughness=0.3, Metallic=0.85`), a high-contrast rim/back light, and use the `CYCLES` render engine.
* **Deprecation warning on Material.use_nodes** → In Blender 6.0+, `use_nodes` will be removed as nodes are always enabled. Check compatibility but safely use it for current versions.
