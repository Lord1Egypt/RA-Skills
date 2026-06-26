---
name: 3d-maker-companion
description: Professional assistant for 3D printing, laser engraving, and 3D modeling workflows. Supports generating visual references for sculpting (Forger/ZBrush), creating 3D models via Meshy AI, and optimizing FDM/Resin print settings. Use when designing, fabricating, or troubleshooting physical maker projects.
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["MESHY_API_KEY"] },
        "install":
          [
            {
              "id": "pip-reqs",
              "kind": "exec",
              "command": "pip install requests",
              "label": "Install Python dependencies (requests)",
            },
          ],
      },
  }
---

# 3D Maker Companion

A specialized workflow guide for bridging the gap between digital AI generation and physical fabrication.

## Meshy AI (AI-Powered 3D Generation & Export)
This skill includes a Python client for Meshy.ai to generate high-quality 3D assets and export them directly to industry-standard software and hardware.

### Connectivity & DCC Bridges
Generated models can be sent directly to major Digital Content Creation (DCC) tools via dedicated bridges:
- **Game Engines:** Unreal Engine, Godot, Unity.
- **Modeling & Animation:** Blender, Maya, 3ds Max.

### 3D Printing & Slicer Integration
Meshy AI supports advanced fabrication workflows directly from the interface:
- **Multicolor Printing:** Enable "Multicolor print" for multi-filament setups.
- **Print Optimization:** "Add platform" for better bed adhesion.
- **Slicer Export:** Direct export options for **Bambu Studio**, **OrcaSlicer**, **Creality Print**, **ElegooSlicer**, **Lychee Slicer**, and **Ultimaker Cura**.
- **Manufacturing:** Support for "Full-color 3D print & Shipping" services.

### Setup & Technical Notes
- **API Key:** Requires `MESHY_API_KEY`. Save locally: `python scripts/meshy_client.py set-key YOUR_KEY`.
- **Image-to-3D:** Ideal for converting AI-generated character references (like Flux/Stable Diffusion) into game-ready or printable meshes.
- **Security:** External network calls are made to `api.meshy.ai`.

## 3D Sculpting Reference Generation
To create effective references for 3D sculpting tools like Forger or ZBrush, use clear anatomical or mechanical descriptors.

- **Perspectives:** Always include "frontal view", "profile view", and "orthographic perspective" for blueprint-like accuracy.
- **Surface Detail:** Use "macro photography", "hyper-detailed textures", and "visible skin pores/material grain" to inform your displacement maps.
- **Lighting:** Request "neutral studio lighting" to avoid deep shadows that hide geometry, or "rim lighting" to define edges.

## 3D Printing Optimization
### FDM (e.g., Bambulab H2S)
- **Geometry Analysis:** Check for steep overhangs and small contact points in the reference image.
- **Material Suggestions:** Recommend PLA for decorative models, PETG for functional parts, and TPU for flexible gaskets or grips.
- **Slicing Tips:** Remind the user to check wall loops and infill patterns (e.g., Gyroid) for structural integrity.

### Resin (SLA/DLP)
- **Orientation:** Advise on tilting models to reduce cross-sectional area per layer.
- **Drain Holes:** For hollow models, ensure the design allows for internal resin drainage.

## Laser Engraving (CO2 Laser)
- **Contrast:** Focus on high-contrast grayscale images for clean engravings on wood or acrylic.
- **Material Safety:** Always cross-reference materials with safe engraving lists (e.g., avoid PVC/Vinyl).
- **Settings:** Store and recall specific Power/Speed settings for different thicknesses (e.g., 80W CO2 laser settings for 3mm birch plywood).

## Maker Workflow Example
1. **Ideation:** Use Flux or similar models to generate a highly detailed 3-view reference (Front, Side, Back).
2. **Modeling:** Import reference into Forger and use the "blueprint" method to sculpt the basic volume.
3. **Refinement:** Use macro-detail references to sculpt fine textures.
4. **Slicing:** Export STL/OBJ and prepare for printing with printer-specific profiles.
