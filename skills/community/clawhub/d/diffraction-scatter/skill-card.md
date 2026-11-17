## Description:

Use this skill for diffraction and scattering data processing with pyFAI, including PONI inspection, 1D and 2D integration, GIWAXS/fiber maps, sector and cake workflows, large HDF5/Eiger handling, uncertainty-aware integration, corrections, and pyFAI environment setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyima96](https://clawhub.ai/user/tianyima96)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, beamline scientists, and developers use this skill to inspect PONI geometry and run pyFAI-based diffraction/scattering integrations for EDF, TIFF, HDF5, Eiger, and NPY detector data. It supports command generation and workflow guidance for radial, azimuthal, sector, cake, and GIWAXS/fiber outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The environment helper can install Python packages into a local virtual environment.

Mitigation: Use the default pyFAI-related packages or trusted package names only, and do not run the helper with administrator privileges.

Risk: Integration commands read user-selected detector data and write derived files to the selected output directory.

Mitigation: Run commands only on intended input paths, choose an explicit output directory, and review generated manifests and per-frame outputs before sharing results.

Risk: Incorrect mode, unit, HDF5 dataset path, channel, or correction settings can produce misleading scientific outputs.

Mitigation: Confirm mode, units, corrections, dataset path, and output format before execution, especially for GIWAXS/fiber and large Eiger/HDF5 workflows.

## Reference(s):

- [Quick Start](references/quickstart.md)
- [Mode Guide](references/modes.md)
- [Streaming for Large Datasets](references/streaming.md)
- [pyFAI calibration tutorial](http://www.silx.org/pub/pyFAI/video/Calibration_15mn.mp4)
- [pyFAI paper DOI](https://doi.org/10.1107/S1600576715004306)
- [fabio paper DOI](https://doi.org/10.1107/S0021889813000150)
- [silx Zenodo DOI](https://doi.org/10.5281/zenodo.591709)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python command templates, and JSONL-oriented workflow descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated commands may create a local Python virtual environment and may write per-frame CSV, HDF5, NPZ, manifest.jsonl, and JSONL progress outputs when run by the user.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
