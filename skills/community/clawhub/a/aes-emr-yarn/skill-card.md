## Description:

Analyzes YARN cluster resource consumption using SSH and EMR API data, then produces health and capacity-planning recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinyafei123](https://clawhub.ai/user/qinyafei123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to inspect YARN cluster load, queue usage, node status, application health, and capacity risks for EMR environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports exposed cloud access keys and a root SSH password.

Mitigation: Do not install or run this release as-is; rotate exposed credentials and remove hard-coded secrets before use.

Risk: The release evidence reports unsafe SSH usage with root credentials.

Mitigation: Use a non-root read-only account, enforce SSH host-key verification, and limit network access to approved hosts.

Risk: The release evidence reports custom cloud authentication handling.

Mitigation: Replace custom authentication with the official provider SDK or signed request flow before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qinyafei123/skills/aes-emr-yarn)
- [Publisher profile](https://clawhub.ai/user/qinyafei123)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis report with tables and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local execution logs and cookie data under the skill directory when run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
