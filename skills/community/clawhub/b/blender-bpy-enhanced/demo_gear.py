"""
Blender Demo: Procedural Mechanical Gear (Simplified)
Creates an interlocking gear with bolt, using reliable bpy.ops operations
"""
import bpy
import math
import os

# ============================================================
# CLEAN SCENE
# ============================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials):
    bpy.data.materials.remove(mat)

# ============================================================
# CREATE GEAR using screw modifier approach
# ============================================================
def create_gear(name, radius=2.0, teeth=16, thickness=0.8):
    """Create a gear using cylinder + screw + manual teeth inset"""
    
    # Step 1: Base cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=teeth * 4,
        radius=radius,
        depth=thickness,
        location=(0, 0, 0)
    )
    gear = bpy.context.object
    gear.name = name
    
    # Step 2: Enter edit mode and create teeth by scaling vertex groups
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type='VERT')
    
    # Select alternating groups of vertices and push them out for teeth
    obj_data = gear.data
    vert_count = len(obj_data.vertices)
    verts_per_ring = teeth * 4
    rings = 2  # top and bottom rings
    
    for v_idx in range(vert_count):
        v = obj_data.vertices[v_idx]
        angle = math.atan2(v.co.y, v.co.x)
        tooth_idx = round(angle / (2 * math.pi / teeth))
        tooth_angle = tooth_idx * (2 * math.pi / teeth)
        angle_diff = abs((angle - tooth_angle + math.pi) % (2 * math.pi) - math.pi)
        
        if angle_diff < (2 * math.pi / teeth) * 0.35:
            v.select = True
    
    # Extrude teeth outward
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, 0)}
    )
    # Scale the extruded vertices outward
    scale_factor = (radius + 0.4) / radius
    bpy.ops.transform.resize(
        value=(scale_factor, scale_factor, 1),
        orient_type='GLOBAL',
        constraint_axis=(True, True, False)
    )
    
    # Step 3: Add center hole (select center top face and delete)
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type='FACE')
    
    # Create center hole by selecting and deleting center faces
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Instead, use Boolean for the hole - simpler
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create a cylinder to subtract (the hole)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=0.5,
        depth=thickness * 1.5,
        location=(0, 0, 0)
    )
    hole_cutter = bpy.context.object
    hole_cutter.name = "HoleCutter"
    
    # Boolean modifier
    bool_mod = gear.modifiers.new(name="Hole", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = hole_cutter
    
    bpy.ops.object.select_all(action='DESELECT')
    gear.select_set(True)
    bpy.context.view_layer.objects.active = gear
    bpy.ops.object.modifier_apply(modifier="Hole")
    
    # Delete the cutter
    bpy.ops.object.select_all(action='DESELECT')
    hole_cutter.select_set(True)
    bpy.ops.object.delete()
    
    # Step 4: Add Modifiers
    bpy.context.view_layer.objects.active = gear
    gear.select_set(True)
    
    # Bevel for polished edges
    bevel = gear.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.05
    bevel.segments = 2
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(30)
    
    # Subdivision surface for smoothness
    subdiv = gear.modifiers.new(name="Subdivision", type='SUBSURF')
    subdiv.levels = 1
    subdiv.render_levels = 2
    
    return gear


# ============================================================
# CREATE BOLT
# ============================================================
def create_bolt(name, radius=0.4, height=0.6):
    """Create a hexagonal bolt head"""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=6,
        radius=radius,
        depth=height,
        location=(0, 0, thickness/2 + height/2)
    )
    bolt = bpy.context.object
    bolt.name = name
    
    # Smooth it
    bpy.ops.object.shade_smooth()
    return bolt

# ============================================================
# MAIN SCENE
# ============================================================
thickness = 0.8

# Create gear
gear = create_gear("DemoGear", radius=2.0, teeth=16, thickness=thickness)
gear.location = (0, 0, 0)

# Create bolt through center
bolt = create_bolt("CenterBolt", radius=0.45, height=1.0)

# ============================================================
# CREATE MATERIALS
# ============================================================
# Gear material - Bronze metal
mat_gear = bpy.data.materials.new(name="GearBronze")
mat_gear.use_nodes = True
nodes = mat_gear.node_tree.nodes
links = mat_gear.node_tree.links

nodes.clear()

output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (400, 0)

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Base Color'].default_value = (0.72, 0.55, 0.32, 1.0)
bsdf.inputs['Metallic'].default_value = 0.85
bsdf.inputs['Roughness'].default_value = 0.25

tex_coord = nodes.new(type='ShaderNodeTexCoord')
tex_coord.location = (-400, 100)

noise = nodes.new(type='ShaderNodeTexNoise')
noise.location = (-200, 0)
noise.inputs['Scale'].default_value = 30.0
noise.inputs['Detail'].default_value = 2.0

color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.location = (0, 100)
color_ramp.color_ramp.elements[0].color = (0.6, 0.45, 0.2, 1.0)
color_ramp.color_ramp.elements[1].color = (0.8, 0.65, 0.4, 1.0)

links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

if gear.data.materials:
    gear.data.materials[0] = mat_gear
else:
    gear.data.materials.append(mat_gear)

# Bolt material - Steel
mat_bolt = bpy.data.materials.new(name="BoltSteel")
mat_bolt.use_nodes = True
nodes2 = mat_bolt.node_tree.nodes
links2 = mat_bolt.node_tree.links
nodes2.clear()

out2 = nodes2.new(type='ShaderNodeOutputMaterial')
out2.location = (300, 0)

bsdf2 = nodes2.new(type='ShaderNodeBsdfPrincipled')
bsdf2.location = (0, 0)
bsdf2.inputs['Base Color'].default_value = (0.3, 0.3, 0.32, 1.0)
bsdf2.inputs['Metallic'].default_value = 0.95
bsdf2.inputs['Roughness'].default_value = 0.4

links2.new(bsdf2.outputs['BSDF'], out2.inputs['Surface'])

if bolt.data.materials:
    bolt.data.materials[0] = mat_bolt
else:
    bolt.data.materials.append(mat_bolt)

# ============================================================
# GROUND PLANE
# ============================================================
bpy.ops.mesh.primitive_grid_add(
    size=8,
    x_subdivisions=10,
    y_subdivisions=10,
    location=(0, 0, -thickness/2 - 0.01)
)
ground = bpy.context.object
ground.name = "Ground"

mat_ground = bpy.data.materials.new(name="GroundMat")
mat_ground.use_nodes = True
nodes3 = mat_ground.node_tree.nodes
links3 = mat_ground.node_tree.links
nodes3.clear()

out3 = nodes3.new(type='ShaderNodeOutputMaterial')
out3.location = (300, 0)

bsdf3 = nodes3.new(type='ShaderNodeBsdfPrincipled')
bsdf3.location = (0, 0)
bsdf3.inputs['Base Color'].default_value = (0.15, 0.15, 0.18, 1.0)
bsdf3.inputs['Roughness'].default_value = 0.9
bsdf3.inputs['Metallic'].default_value = 0.1

links3.new(bsdf3.outputs['BSDF'], out3.inputs['Surface'])
ground.data.materials.append(mat_ground)

# ============================================================
# LIGHTING
# ============================================================
# Key light
bpy.ops.object.light_add(type='AREA', location=(5, -4, 6), rotation=(0.8, 0, 0.7))
key = bpy.context.object
key.data.energy = 600
key.data.size = 4

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-4, 3, 3), rotation=(0.5, 0, -1.0))
fill = bpy.context.object
fill.data.energy = 300
fill.data.size = 3

# Rim light
bpy.ops.object.light_add(type='AREA', location=(0, 5, 5), rotation=(0.5, 0, 1.57))
rim = bpy.context.object
rim.data.energy = 250
rim.data.size = 2

# ============================================================
# CAMERA
# ============================================================
bpy.ops.object.camera_add(location=(5.5, -4.5, 3.5))
cam = bpy.context.object
cam.rotation_euler = (math.radians(60), 0, math.radians(50))
bpy.context.scene.camera = cam

# ============================================================
# RENDER SETTINGS
# ============================================================
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 50  # 960x540 quick demo
scene.render.filepath = "/tmp/blender_demo_gear.png"
scene.render.image_settings.file_format = 'PNG'

# ============================================================
# SAVE & SUMMARY
# ============================================================
bpy.ops.wm.save_as_mainfile(filepath="/tmp/blender_demo_gear.blend")

print("\n" + "="*60)
print("🎯 BLENDER DEMO - SCENE SUMMARY")
print("="*60)
print(f"📦 Objects: {[o.name for o in bpy.data.objects if o.type == 'MESH']}")
print(f"🎨 Materials: {[m.name for m in bpy.data.materials]}")
print(f"💡 Lights: {[o.name for o in bpy.data.objects if o.type == 'LIGHT']}")
print(f"📷 Camera: {cam.name} @ ({cam.location.x:.1f}, {cam.location.y:.1f}, {cam.location.z:.1f})")
print(f"⚙️  Engine: {scene.render.engine}")
print(f"📐 Resolution: {scene.render.resolution_x}x{scene.render.resolution_y} @ {scene.render.resolution_percentage}%")
print(f"📁 Blend: /tmp/blender_demo_gear.blend")
print("="*60)

# ============================================================
# RENDER
# ============================================================
bpy.ops.render.render(write_still=True)
print(f"\n✅ Rendered! Output: {scene.render.filepath}")
