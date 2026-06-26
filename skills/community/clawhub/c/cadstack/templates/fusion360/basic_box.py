# Fusion 360 Template: Basic Box
# Note: Requires Fusion 360 with bridge add-in running

backend.create_document("box")
box = backend.create_box({{ length }}, {{ width }}, {{ height }})

# Export to STEP format
backend.export_step(backend._current_doc, output)
