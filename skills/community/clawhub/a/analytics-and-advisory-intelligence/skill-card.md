## Description:

Cross-client analytics for Greek accounting firms. Surfaces trends, anomalies, and risks across financial data. Read-only, outputs to /data/reports/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

External accounting teams and OpenClaw operators use this skill to generate read-only portfolio and client analytics, including trends, anomalies, compliance risk scores, and cash-flow advisory reports from local Greek accounting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local access to client financial, compliance, correspondence, banking, and EFKA data may expose sensitive client records if installed in the wrong workspace.

Mitigation: Confirm the local data scope before installation and run the skill only in approved accounting workspaces.

Risk: The setup example includes installing jq with sudo.

Mitigation: Install jq through the normal administrator or package-management process rather than letting a skill invoke sudo.

Risk: Analytical findings may be incomplete or low-confidence when client history or sector sample sizes are too small.

Mitigation: Keep accountant review in the workflow and preserve confidence labels, data source notes, and minimum-period checks in outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/skills/analytics-and-advisory-intelligence)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell command examples and local report file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only advisory outputs; reports are described as written only under /data/reports/analytics/.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
