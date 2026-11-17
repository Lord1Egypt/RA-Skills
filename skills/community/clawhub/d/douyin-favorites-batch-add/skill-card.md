## Description:

Batch-save Douyin videos to a chosen favorites folder, verify each addition, log results, and resume interrupted runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdguiai](https://clawhub.ai/user/jdguiai)

### License/Terms of Use:

MIT-0

## Use Case:

Douyin users can organize video IDs from a prepared list into favorites folders, check that each item was added, and resume larger imports after interruptions. The workflow is intended for Windows with Chrome and Node.js.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived background tasks request unnecessary privileges and can interrupt active browser work.

Mitigation: Use ordinary-user task privileges, check browser ownership before unattended runs, and remove the created tasks and schedules when importing finishes.

Risk: The dedicated Chrome profile retains the user's Douyin login, and automated changes require manual reversal.

Mitigation: Keep this profile separate from everyday browsing, start with two items, and review the changes because the scripts do not provide rollback.

Risk: The external scheduling wrapper for unattended imports was not included for review.

Mitigation: Review the wrapper before configuring or enabling scheduled imports.

## Reference(s):

- [ClawHub release](https://clawhub.ai/jdguiai/skills/douyin-favorites-batch-add)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Node.js and PowerShell commands and scripts, with JSON progress state and CSV logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a prepared list of Douyin video details; reports per-item outcomes and verification results.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
