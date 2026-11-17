## Description:

Checks Google Antigravity model usage quotas, remaining percentages, and reset times for accounts using Google Antigravity OAuth login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t-atlas](https://clawhub.ai/user/t-atlas)

### License/Terms of Use:


## Use Case:

Developers and agents using Google Antigravity OAuth through OpenClaw can use this skill to view model quota status, remaining percentage, and reset times from a local terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published description and implementation behavior do not match, which can lead users to install it expecting a local CodexBar cost summary.

Mitigation: Review and update the public metadata before release so it accurately describes Google Antigravity quota checking.

Risk: The skill reads local OpenClaw OAuth credentials and makes authenticated Google API requests.

Mitigation: Install only for users who explicitly want that behavior, and review credential access before running it.

## Reference(s):

- [Google Antigravity Quota API Reference](references/codexbar-cli.md)
- [ClawHub Skill Page](https://clawhub.ai/t-atlas/skills/ag-model-usage)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text usage report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; uses local OpenClaw authentication state and authenticated Google quota API requests.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
