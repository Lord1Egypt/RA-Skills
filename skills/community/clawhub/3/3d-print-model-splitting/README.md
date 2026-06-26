# 3D Print Model Splitting Skill

OpenClaw AgentSkill for splitting a single complex STL figurine/statue into multiple 3D-printable and physically assemblable parts.

The core lesson encoded here is:

> Printable is not the same as assemblable. Mesh repair and slicer import can make parts printable, but interface clearance is what makes them fit.

## What it covers

- Blender face/material annotation for human-guided semantic splitting
- STL split/cap baseline workflow
- Pre-clearance MeshFix repair guidance
- Manifold Boolean interface clearance using expanded cutters
- Post-clearance simplify without filling intentional cavities
- 3MF object validation and pairwise interference checks
- Bambu Studio handoff guidance

## Skill contents

```text
SKILL.md                 OpenClaw skill entrypoint
references/             SOP, clearance lessons, versioning, case study
scripts/                Reusable helper scripts
.clawhubignore          Files to exclude from ClawHub packaging
.skillignore            Legacy/local ignore mirror
```

## Dependencies

Depending on which scripts you use:

- Blender (`bpy`, `bmesh`, `mathutils`) for annotation, splitting, and Blender-based checks
- Python packages: `trimesh`, `numpy`, `manifold3d`, `pymeshfix`, `Pillow`
- Bambu Studio or another slicer for final print preparation

Install Python dependencies in your project environment, not inside the skill package.

## Public release note

This repository is intended for public distribution of the skill. Generated model files (`.stl`, `.3mf`, `.blend`, preview images, caches, and virtual environments) are intentionally excluded.
