# Hardware Engineering Conventions

# IDs

HWE-BLK-### : hardware block
HWE-IF-###  : interface
HWE-TP-###  : test point
HWE-VER-### : verification
PCB-###     : PCB identifier

# Hardware revision

Use an explicit revision:

HW-REV-A
HW-REV-B
PCB-REV-A

The hardware revision is distinct from the document version.

# Schematics

The project must define:
- component reference rules;
- net naming;
- power rail naming;
- connector pin naming;
- sheet organization;
- hierarchical design rules.

Standard component references must remain consistent:
R
C
L
D
Q
U
J
etc.

# BOM

The official BOM must identify when relevant:
- reference;
- quantity;
- manufacturer;
- manufacturer part number;
- description;
- value;
- tolerance;
- package;
- lifecycle status;
- approved alternative;
- DNI / fitted status.

# Design Quality

Verify depending on the product:
- power budget;
- voltage/current margins;
- thermal margin;
- component derating;
- ADC/DAC ranges;
- clocking;
- signal integrity;
- EMC-related design constraints;
- protections;
- isolation;
- connector constraints;
- manufacturing constraints.

# EDA Checks

Run when available:
- ERC;
- DRC;
- schematic review;
- layout review.

Accepted violations must be documented and justified.

# Release Package

A hardware release may include:
- schematics;
- PCB source;
- Gerbers/Odb++ or equivalent;
- drill files;
- BOM;
- pick-and-place;
- assembly drawings;
- fabrication drawings;
- test specification;
- revision record.

The package must be linked to the corresponding Hardware Revision.
