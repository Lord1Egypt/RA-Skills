# FreeCAD Template: Basic Cylinder
# Creates a cylinder with optional hole

backend.create_document("cylinder")
cyl = backend.create_cylinder({{ radius }}, {{ height }}, "Cylinder")

{% if hole_radius > 0 %}
hole = backend.create_cylinder({{ hole_radius }}, {{ height }}, "Hole")
result = backend.cut(cyl, hole, "Tube")
{% endif %}

backend.recompute()
backend.export_step(backend._current_doc, output)
