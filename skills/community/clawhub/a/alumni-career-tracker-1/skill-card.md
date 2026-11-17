## Description:

Analyze laboratory alumni career trajectories and outcomes to provide data-driven career guidance for current students and postdocs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to track laboratory alumni career outcomes, analyze sector and degree-level trends, and generate career guidance for current students and postdocs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and export identifiable alumni career records and possible compensation details.

Mitigation: Use only consented alumni data, avoid salary details and private notes unless necessary, and share aggregated reports instead of raw records.

Risk: Local data files and exports may be placed in locations with weak access controls.

Mitigation: Keep the data file and generated exports in restricted locations and avoid exporting raw records to shared folders.

Risk: Unpinned dependencies can change behavior across deployments.

Mitigation: Pin dependency versions before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; the bundled CLI can produce terminal text, JSON files, and CSV exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles local alumni records and analysis reports; raw exports may contain identifiable career or compensation data.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
