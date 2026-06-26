# AutoCAD Template: Basic Box
# Note: Requires AutoCAD running on Windows

# This template uses COM automation
# Ensure AutoCAD is running before executing

backend.create_document("box")
box = backend.create_box({{ length }}, {{ width }}, {{ height }})

# Export to SAT format (AutoCAD native)
backend.export_step(backend._current_doc, output)
