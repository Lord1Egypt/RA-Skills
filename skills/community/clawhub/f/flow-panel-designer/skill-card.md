## Description:

Design multicolor flow cytometry panels minimizing spectral overlap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and lab practitioners use this skill to draft multicolor flow cytometry panel assignments, estimate spectral overlap, and identify compensation needs for marker-fluorophore planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence notes a documentation mismatch around advertised output behavior.

Mitigation: Confirm the supported command-line options and capture stdout explicitly before relying on file output in a workflow.

Risk: Panel assignments and overlap estimates are simplified planning assistance.

Mitigation: Have qualified lab personnel review recommendations and validate compensation controls on the target instrument before experimental or clinical use.

Risk: The skill executes a local Python script in the workspace.

Mitigation: Run it in a sandboxed workspace and inspect generated text outputs before using them downstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/flow-panel-designer)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text panel report with marker-fluorochrome assignments, overlap estimates, and compensation notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a local Python script with no extra Python packages required.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
