# SolidWorks Template: Basic Box
# Note: Requires SolidWorks running on Windows

backend.create_document("box")
box = backend.create_box({{ length }}, {{ width }}, {{ height }})

# Export to STEP format
backend.export_step(backend._current_doc, output)
