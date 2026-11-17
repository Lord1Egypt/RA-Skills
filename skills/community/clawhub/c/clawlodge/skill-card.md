## Description:

Use ClawLodge to search, inspect, download, and publish OpenClaw workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memepilot](https://clawhub.ai/user/memepilot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to find reusable workspaces, inspect registry metadata and versions, download workspace archives, install isolated agents, and publish their current workspace to ClawLodge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install third-party registry workspaces as new OpenClaw agents before a full content review.

Mitigation: Inspect the package metadata, publisher, version, files, scripts, and instructions before installation; use staged download and review for untrusted packages.

Risk: The ClawLodge CLI may send anonymous command-level telemetry.

Mitigation: Check the telemetry setting before use and disable telemetry when the user or environment requires it.

Risk: Publish, favorite, comment, and report actions write to ClawLodge and may require account credentials.

Mitigation: Run write actions only after explicit user intent, confirm the active identity, and avoid exposing tokens in shared logs.

## Reference(s):

- [ClawLodge](https://clawlodge.com)
- [ClawLodge PAT settings](https://clawlodge.com/settings)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference registry metadata, workspace archive paths, agent names, and telemetry settings when relevant.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
