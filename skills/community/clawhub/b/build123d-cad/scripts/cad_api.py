#!/usr/bin/env python3
"""Print build123d API cheatsheet as JSON."""

import json

print(json.dumps({
    "primitives_3d": [
        "Box(length, width, height)",
        "Cylinder(radius, height)",
        "Sphere(radius)",
        "Cone(bottom_radius, top_radius, height)",
        "Torus(major_radius, minor_radius)",
        "Wedge(dx, dy, dz, xmin, zmin, xmax, zmax)",
    ],
    "primitives_2d": [
        "Circle(radius)",
        "Rectangle(width, height)",
        "Ellipse(x_radius, y_radius)",
        "Polygon(pts=[(x,y), ...])",
        "RegularPolygon(radius, side_count)",
        "SlotOverall(width, height)",
        "Text(txt, font_size)",
    ],
    "operations": [
        "extrude(amount=N)",
        "revolve(axis=Axis.Z, revolution_arc=360)",
        "loft(sections=[...])",
        "sweep(path=wire)",
        "fillet(edges, radius=N)",
        "chamfer(edges, length=N)",
        "offset(amount=N)",
        "mirror(about=Plane.XZ)",
        "split(bisect_by=Plane.XY)",
        "section(plane=Plane.XY)",
    ],
    "holes": [
        "Hole(radius, depth)",
        "CounterBoreHole(radius, counter_bore_radius, counter_bore_depth, depth)",
        "CounterSinkHole(radius, counter_sink_radius, depth)",
    ],
    "positioning": [
        "Pos(x, y, z)",
        "Rot(x, y, z)  # degrees",
        "Locations((x,y,z), ...)",
        "GridLocations(x_spacing, y_spacing, x_count, y_count)",
        "PolarLocations(radius, count)",
    ],
    "selectors": [
        "part.faces() / .edges() / .vertices()",
        ".filter_by(Axis.Z)",
        ".sort_by(Axis.Z)",
        ".group_by(Axis.Z)",
        "[-1] last, [0] first",
    ],
    "boolean": ["+ (union)", "- (cut)", "& (intersect)"],
    "export": [
        "export_step(part, 'file.step')",
        "export_stl(part, 'file.stl')",
        "export_svg(part, 'file.svg')",
    ],
    "pattern": (
        "from build123d import *\n"
        "with BuildPart() as result:\n"
        "    Box(100, 60, 40)\n"
        "    fillet(result.edges().filter_by(Axis.Z), radius=5)"
    ),
    "notes": [
        "All dimensions in millimeters",
        "Always use `with BuildPart() as result:`",
        "Parameterize dimensions (no magic numbers)",
        "Add fillets to stress concentrations",
    ],
}))
