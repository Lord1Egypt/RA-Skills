# FreeCAD Template: Mounting Bracket
# Creates a rectangular bracket with mounting holes

backend.create_document("mounting_bracket")

# Create base plate
plate = backend.create_box({{ length }}, {{ width }}, {{ thickness }}, "Plate")

# Mounting hole positions
hole_positions = [
    ({{ hole_offset_x }}, {{ hole_offset_y }}),
    ({{ length }} - {{ hole_offset_x }}, {{ hole_offset_y }}),
    ({{ hole_offset_x }}, {{ width }} - {{ hole_offset_y }}),
    ({{ length }} - {{ hole_offset_x }}, {{ width }} - {{ hole_offset_y }}),
]

# Create and cut mounting holes
result = plate
for i, (x, y) in enumerate(hole_positions):
    hole = backend.create_cylinder({{ hole_diameter }} / 2, {{ thickness }}, f"Hole_{i}")
    backend.move(hole, x - {{ length }}/2, y - {{ width }}/2, 0)
    result = backend.cut(result, hole, f"Bracket_{i}")

{% if fillet_radius > 0 %}
# Apply edge fillets
result = backend.fillet(result, [], {{ fillet_radius }})
{% endif %}

backend.recompute()
backend.export_step(backend._current_doc, output)
