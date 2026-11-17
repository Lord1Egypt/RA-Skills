## Description:

BGsub is a self-contained CLI toolkit for X-ray diffraction, SAXS, and WAXS background subtraction across 2D detector images and 1D curves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyima96](https://clawhub.ai/user/tianyima96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, scientists, and data-processing engineers use this skill to prepare local SAXS, WAXS, and XRD image or curve data by estimating, subtracting, and transmission-correcting backgrounds. It supports single-file and batch workflows for detector images, 1D curves, ionchamber data, and image format conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch commands can write many processed files into an output directory.

Mitigation: Review output paths before execution and use a dedicated output directory for generated data.

Risk: GUI preview or image comparison workflows may open a local window.

Mitigation: Run preview and comparison commands only in an expected GUI-capable session.

Risk: Incorrect background, transmission, or ionchamber matching choices can produce misleading scientific results.

Mitigation: Verify selected background files, transmission values, ionchamber matches, and processing parameters before relying on generated results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tianyima96/skills/diffraction-scatter-background-substract)
- [Quickstart](references/quickstart.md)
- [CLI Commands Reference](references/cli_commands.md)
- [Examples](references/examples.md)
- [fabio: Processing of 2D X-ray diffraction data](http://dx.doi.org/10.1107/S0021889813000150)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands, parameters, and file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The recommended commands operate on user-selected local scientific data files and may write processed image, curve, CSV, HDF5, or converted output files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
