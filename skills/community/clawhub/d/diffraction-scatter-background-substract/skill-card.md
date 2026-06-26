## Description: <br>
BGsub is a self-contained CLI toolkit for X-ray diffraction background subtraction across 2D detector images and 1D curves, including SSRF ionchamber transmission correction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianyima96](https://clawhub.ai/user/tianyima96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, beamline scientists, and data analysts use this skill to run or adapt BGsub commands for SAXS, WAXS, and XRD background subtraction, ionchamber transmission correction, batch processing, and file format conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch commands can read many matching input files and write processed outputs. <br>
Mitigation: Confirm input directories, filename patterns, and output paths before executing generated commands. <br>
Risk: Broad trigger wording can activate the skill for unrelated uses of terms such as transmission. <br>
Mitigation: Confirm the user task concerns SAXS, WAXS, XRD, diffraction, scattering, or ionchamber data before applying the workflow. <br>
Risk: Scientific results depend on the selected background, transmission value, and subtraction method. <br>
Mitigation: Review parameters and inspect outputs against domain expectations before using processed data for downstream analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianyima96/diffraction-scatter-background-substract) <br>
- [README](artifact/README.md) <br>
- [Quickstart](artifact/references/quickstart.md) <br>
- [CLI Commands Reference](artifact/references/cli_commands.md) <br>
- [Examples](artifact/references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code examples, and processing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may describe local files produced by the bundled CLI scripts when the user executes them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
