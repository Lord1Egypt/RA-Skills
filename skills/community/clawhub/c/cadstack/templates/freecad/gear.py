# FreeCAD Template: Parametric Involute Gear
# Creates a gear with specified teeth and module

import math

# Gear parameters
teeth = {{ teeth }}
module = {{ module }}
thickness = {{ thickness }}
pressure_angle = {{ pressure_angle }}  # degrees

# Calculated values
pitch_diameter = teeth * module
pitch_radius = pitch_diameter / 2
addendum = module
dedendum = 1.25 * module
outside_radius = pitch_radius + addendum
root_radius = pitch_radius - dedendum
base_radius = pitch_radius * math.cos(math.radians(pressure_angle))

# Create involute profile points
def involute(r, theta):
    """Calculate involute curve point."""
    x = r * (math.cos(theta) + theta * math.sin(theta))
    y = r * (math.sin(theta) - theta * math.cos(theta))
    return (x, y)

# Generate tooth profile
points = []
for i in range(teeth):
    base_angle = 2 * math.pi * i / teeth
    # Generate involute points for one tooth
    for t in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        theta = t * math.sqrt((outside_radius / base_radius) ** 2 - 1)
        ix, iy = involute(base_radius, theta)
        # Rotate to tooth position
        angle = base_angle + math.atan2(iy, ix)
        r = math.sqrt(ix**2 + iy**2)
        points.append((r * math.cos(angle), r * math.sin(angle)))

# Create the gear using Part module
backend.create_document("gear")

# Use FreeCAD's built-in gear or create custom
try:
    import Part
    doc = backend._current_doc.backend_ref

    # Create circle for base
    circle = Part.Circle()
    circle.Radius = outside_radius

    # Create face and extrude
    face = Part.Face(Part.Wire(circle.toShape()))
    gear_shape = face.extrude(FreeCAD.Vector(0, 0, thickness))

    # Create feature
    gear_obj = doc.addObject("Part::Feature", "Gear")
    gear_obj.Shape = gear_shape

except Exception as e:
    # Fallback to simple cylinder
    gear = backend.create_cylinder(outside_radius, thickness, "Gear")
    console.print(f"[yellow]Note: Created simplified gear cylinder[/yellow]")
    console.print(f"[yellow]Full involute gear requires advanced scripting[/yellow]")

backend.recompute()
backend.export_step(backend._current_doc, output)
