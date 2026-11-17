## Description:

Converts natural-language or document inputs into editable draw.io XML diagrams and .drawio files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuliwenjing](https://clawhub.ai/user/wuliwenjing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and diagram authors use this skill to turn process descriptions, architecture notes, sequence descriptions, network topologies, or uploaded text/docx/pdf content into structured diagram JSON and editable draw.io files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated .drawio files are written to the configured output directory, with a desktop path used by default in the artifact.

Mitigation: Use a dedicated output directory through DRAWIO_OUTPUT_DIR or the --output-dir option and review generated files before sharing them.

Risk: docx and pdf parsing depends on optional local packages and the security evidence notes parsing may need repair before relying on it.

Mitigation: Install parsing dependencies in an isolated environment and confirm extracted text before using it as the basis for a diagram.

Risk: Diagram layout may be imperfect, including overlapping lines or spacing that needs adjustment.

Mitigation: Open the generated file in draw.io and manually review or adjust the diagram before treating it as final.

## Reference(s):

- [draw.io XML Format Reference](references/drawio-xml-spec.md)
- [draw.io Web App](https://app.diagrams.net)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with JSON payloads and generated .drawio XML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes .drawio files to a configured output directory; generated layouts may require manual adjustment in draw.io.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
