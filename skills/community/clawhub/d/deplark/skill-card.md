## Description:

Quickly deploy static websites and Node.js apps to Deplark / 速栈 for fast access from mainland China, using Codex or Claude Code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larksq](https://clawhub.ai/user/larksq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill from Codex or Claude Code to publish static websites and Node.js apps through Deplark, especially for users in mainland China. It guides account connection, target selection, local builds, and deployment.

### Deployment Geography for Use:

China (mainland)

## Known Risks and Mitigations:

Risk: Account authorization or an API key enables network access to Deplark and project operations; the security scan was incomplete.

Mitigation: Review requested account permissions, keep keys out of files, chat, URLs, command arguments, and logs, and inspect the skill before connecting an account.

Risk: The workflow runs local project build commands and publishes selected build output.

Mitigation: Inspect the repository's build steps and output, and exclude credentials and private files before deployment.

## Reference(s):

- [Deplark](https://deplark.com)
- [ClawHub release page](https://clawhub.ai/larksq/skills/deplark)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Deployment status and URL]

**Output Format:** [Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deployment output depends on the selected project and its local build.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
