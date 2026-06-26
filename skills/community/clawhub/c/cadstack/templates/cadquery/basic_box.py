# CadQuery Template: Basic Box
# Creates a simple box with optional fillets
#
# @param length={{ length|default(100) }} Length of the box in mm
# @param width={{ width|default(50) }} Width of the box in mm
# @param height={{ height|default(20) }} Height of the box in mm
# @param fillet_radius={{ fillet_radius|default(0) }} Fillet radius (0 = no fillets)

import cadquery as cq
from pathlib import Path

# Parameters (rendered from template)
length = {{ length|default(100) }}
width = {{ width|default(50) }}
height = {{ height|default(20) }}
fillet_radius = {{ fillet_radius|default(0) }}

# Create box
result = cq.Workplane("XY").box(length, width, height)

# Apply fillets if fillet_radius > 0
if fillet_radius > 0:
    result = result.edges().fillet(fillet_radius)

# Export
output_dir = "{{ output_dir|default('output') }}"
output_path = Path(output_dir) / '{{ name|default("box") }}{% if fillet_radius > 0 %}_filleted{% endif %}.step'

output_path.parent.mkdir(parents=True, exist_ok=True)
cq.exporters.export(result, str(output_path))
print(f'Exported: {output_path}')

if __name__ == '__main__':
    print(f'File size: {output_path.stat().st_size} bytes')
