## Description:

Parametric 3D CAD skill for generating, measuring, validating, and exporting STEP, STL, and SVG models from build123d Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wngfra](https://clawhub.ai/user/wngfra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and makers use this skill to ask an agent for parametric mechanical parts, enclosures, mounts, and assemblies, then generate CAD scripts, exported model files, measurements, sections, and validation verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied CAD scripts may execute with the same filesystem privileges as the OpenClaw account if the claimed Python sandbox is bypassed.

Mitigation: Install only when the CAD scripts are trusted, and prefer running the skill in a container or dedicated low-privilege account with a tightly scoped output directory, no network unless needed, and pinned dependencies.

Risk: Generated CAD artifacts, measurements, and validation verdicts may be incorrect or incomplete for real-world manufacturing or safety-critical use.

Mitigation: Review generated scripts and exported models, run measurement and full assembly validation before export, and have a qualified reviewer check dimensions, clearances, materials, and process assumptions.

Risk: Runtime setup can fail when build123d/OpenCascade wheels are unavailable for the selected Python version.

Mitigation: Use an isolated Python 3.12 environment and pin dependency versions for repeatable execution.

## Reference(s):

- [build123d documentation](https://build123d.readthedocs.io)
- [build123d GitHub repository](https://github.com/gumyr/build123d)
- [ClawHub skill page](https://clawhub.ai/wngfra/skills/build123d-cad)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python code snippets, shell commands, JSON command outputs, and generated STEP/STL/SVG file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CAD dimensions are in millimeters; generated files are written to the configured CAD workspace.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
