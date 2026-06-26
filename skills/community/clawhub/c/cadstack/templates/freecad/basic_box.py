# FreeCAD Template: Basic Box
# Creates a simple box with optional fillets

backend.create_document("box")
box = backend.create_box({{ length }}, {{ width }}, {{ height }}, "Box")

{% if fillet_radius > 0 %}
filleted = backend.fillet(box, [], {{ fillet_radius }})
{% endif %}

backend.recompute()
backend.export_step(backend._current_doc, output)
