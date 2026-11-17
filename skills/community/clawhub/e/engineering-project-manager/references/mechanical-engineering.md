# Mechanical Engineering Conventions

# IDs

PRT-#### : part
ASM-#### : assembly
DRW-#### : drawing
MEC-IF-### : interface
MEC-VER-### : verification

# Revision

Any controlled part or assembly must have an identifiable revision.

Do not silently overwrite a baselined geometry.

# Drawing / Part metadata

Keep when relevant:
- Part ID;
- title;
- revision;
- material;
- mass;
- finish;
- units;
- tolerances;
- owner;
- status.

# Interfaces

Define:
- mounting points;
- datums;
- dimensions;
- tolerance stack;
- loads;
- motion envelope;
- thermal interfaces;
- cable routing constraints when relevant.

# CAD storage

Clearly identify:
- native CAD source;
- neutral export STEP/IGES when necessary;
- drawings;
- manufacturing export.

The reference geometry must be explicitly defined.

# Verification

Depending on the project:
- dimensional inspection;
- tolerance analysis;
- load calculation;
- FEA;
- thermal analysis;
- fit check;
- prototype testing.

Each result must identify the verified part/assembly revision.
