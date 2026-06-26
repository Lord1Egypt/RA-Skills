#!/usr/bin/env python3
"""Simple test script without Chinese characters"""

import os
import sys
from pathlib import Path

# Add simple ASCII output only
print("=" * 60)
print("Draw.io Flowchart Generator")
print("=" * 60)

# Create test flowchart
workspace = Path(r"C:\Users\opens\.openclaw\workspace")

mermaid_code = """flowchart TD
    Start([Start]) --> Input[User Input]
    Input --> Validate{Validate?}
    Validate -->|Yes| Success[Success]
    Validate -->|No| Error[Error]
    Success --> End([End])
    Error --> Input
"""

# Save Mermaid file
mmd_file = workspace / "test_flow.mmd"
with open(mmd_file, "w", encoding="utf-8") as f:
    f.write(mermaid_code)
print(f"[OK] Mermaid saved: {mmd_file}")

# Create simple Draw.io file
drawio_xml = """<mxfile host="app.diagrams.net">
  <diagram id="test" name="Test Flow">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="note" value="Use: Arrange -&gt; Insert -&gt; Advanced -&gt; Mermaid" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="900" height="200" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""

drawio_file = workspace / "test_flow.drawio"
with open(drawio_file, "w", encoding="utf-8") as f:
    f.write(drawio_xml)
print(f"[OK] Draw.io file: {drawio_file}")

# Try to find and open Draw.io
drawio_path = None
possible_paths = [
    r"C:\Program Files\draw.io\draw.io.exe",
]

for path in possible_paths:
    if os.path.exists(path):
        drawio_path = path
        break

if drawio_path:
    print(f"\n[OPEN] Starting Draw.io: {drawio_path}")
    print(f"[FILE] Opening: {drawio_file}")
    try:
        os.startfile(str(drawio_file))
        print("[OK] Draw.io opened!")
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
else:
    print("\n[WARN] Draw.io not found")
    print("\n[INSTALL] Download from: https://github.com/jgraph/drawio-desktop/releases")
    print("[ONLINE] Or use: https://app.diagrams.net/")

print("\n" + "=" * 60)
print("[DONE] Complete!")
print("=" * 60)
