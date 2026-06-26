# FreeCAD Template: Enclosure Box
# Creates a hollow box with walls and optional lid

backend.create_document("enclosure")

# Outer dimensions
outer = backend.create_box(
    {{ outer_length }},
    {{ outer_width }},
    {{ outer_height }},
    "Outer"
)

# Inner cavity (offset from outer by wall thickness)
inner = backend.create_box(
    {{ outer_length }} - 2 * {{ wall_thickness }},
    {{ outer_width }} - 2 * {{ wall_thickness }},
    {{ outer_height }} - {{ wall_thickness }},  # No bottom offset
    "Inner"
)

# Position inner cavity
backend.move(inner, {{ wall_thickness }}, {{ wall_thickness }}, {{ wall_thickness }})

# Cut inner from outer
enclosure = backend.cut(outer, inner, "Enclosure")

{% if lid_height > 0 %}
# Create lid
lid_outer = backend.create_box(
    {{ outer_length }},
    {{ outer_width }},
    {{ lid_height }},
    "LidOuter"
)

lid_inner = backend.create_box(
    {{ outer_length }} - 2 * {{ wall_thickness }},
    {{ outer_width }} - 2 * {{ wall_thickness }},
    {{ lid_height }} - {{ wall_thickness }},
    "LidInner"
)

backend.move(lid_inner, {{ wall_thickness }}, {{ wall_thickness }}, 0)
lid = backend.cut(lid_outer, lid_inner, "Lid")

# Move lid above enclosure
backend.move(lid, 0, 0, {{ outer_height }})
{% endif %}

backend.recompute()
backend.export_step(backend._current_doc, output)
