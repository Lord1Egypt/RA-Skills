## Description: <br>
Use this skill for diffraction and scattering data processing with pyFAI, including calibration guidance, 1D and 2D integration, batch and streaming workflows, GIWAXS or fiber maps, profiles, sector integration, corrections, and Python or pyFAI setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianyima96](https://clawhub.ai/user/tianyima96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, beamline users, and scientific data analysts use this skill to inspect .poni geometry files, choose pyFAI integration modes, run diffraction or scattering integrations, and process detector datasets with corrections and streaming output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Environment setup can install or upgrade Python packages for pyFAI workflows. <br>
Mitigation: Run the installer in a project directory or virtual environment you control and review the packages before installation. <br>
Risk: Diffraction and scattering analysis may read detector, mask, dark, flat, and correction files supplied by the user. <br>
Mitigation: Provide only the local data and correction files intended for the analysis. <br>
Risk: Incorrect geometry, units, mode selection, or correction settings can produce misleading scientific outputs. <br>
Mitigation: Confirm the .poni file, integration mode, units, corrections, and output format before using generated results. <br>


## Reference(s): <br>
- [Quick Start](references/quickstart.md) <br>
- [Mode Guide](references/modes.md) <br>
- [Streaming for Large Datasets](references/streaming.md) <br>
- [pyFAI Calibration Tutorial](http://www.silx.org/pub/pyFAI/video/Calibration_15mn.mp4) <br>
- [pyFAI Journal of Applied Crystallography DOI](https://doi.org/10.1107/S1600576715004306) <br>
- [fabio Journal of Applied Crystallography DOI](https://doi.org/10.1107/S0021889813000150) <br>
- [silx Zenodo DOI](https://doi.org/10.5281/zenodo.591709) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional generated CSV, HDF5, NPZ, PNG, and JSONL files from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bundled runners emit JSONL progress, write a manifest.jsonl file, and process large detector datasets frame by frame when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
