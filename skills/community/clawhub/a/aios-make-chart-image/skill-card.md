## Description:

AIOS Chart Image renders JSON data, Markdown tables, or ECharts options into PNG, SVG, JPEG, or WebP chart images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AIOS or OpenClaw agents use this skill to convert structured JSON, Markdown tables, or existing ECharts options into chart image files for review or delivery to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File path handling can exceed the workspace boundaries the skill promises to enforce.

Mitigation: Review before installing, reject symlinked paths, enforce the documented upload/download/generated input allowlist, and keep outputs inside generated using canonical path checks.

Risk: The security guidance flags the sharp dependency before shared or multi-sender use.

Mitigation: Update the flagged sharp dependency before using the skill in a shared or multi-sender environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kadbbz/skills/aios-make-chart-image)
- [Publisher profile](https://clawhub.ai/user/kadbbz)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Chart image files in PNG, SVG, JPEG, or WebP format plus JSON status on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs and optional saved ECharts option files are intended to stay under the current senderId generated directory.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
