## Description:

Creates parametric models and prepares FDM parts for the Bambu Lab A1 Combo, including STL/3MF guidance, AMS Lite planning, and validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[serramos-hub](https://clawhub.ai/user/serramos-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, makers, and engineers use this skill to collect part requirements, create editable 3D model sources, prepare STL/STEP/3MF deliverables, and review print-specific assumptions for Bambu Lab A1 Combo workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated models, G-code, or sliced 3MF files may be unsafe or unsuitable if printer hardware, nozzle, plate, filament, or slicer profile details are wrong.

Mitigation: Review all generated geometry and slicer outputs before printing, confirm machine-specific settings, and use Bambu Studio preview for sliced outputs.

Risk: FDM plastic parts may be inappropriate for structural, pressure, high-temperature, mains-electric, food-contact, medical, or personal-protection uses.

Mitigation: Treat these applications as requiring additional engineering review, testing, certification, or refusal when the requested part is primarily intended to harm.

Risk: STL geometry can contain open boundaries, non-manifold edges, degenerate triangles, wrong dimensions, or a base not aligned to Z=0.

Mitigation: Run the included STL audit script and inspect or render outputs before relying on the model.

## Reference(s):

- [Bambu Lab A1 Combo reference](references/bambu-a1.md)
- [Bambu Lab A1 Combo Quick Start](https://cdn1.bambulab.com/documentation/quick-start-b5f1a684f77/A1%20Combo%20Quick%20Start_V0%28EN%29.pdf)
- [Bambu Studio](https://github.com/bambulab/BambuStudio)
- [Bambu Studio command-line usage](https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with model source snippets, file guidance, shell commands, and concise validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses millimeters and Brazilian Portuguese by default; generated print files require user review against the exact printer, nozzle, plate, filament, and slicer profile.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
