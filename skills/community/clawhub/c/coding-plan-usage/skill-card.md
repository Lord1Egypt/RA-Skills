## Description:

Queries the remaining hours of Alibaba Cloud Coding Plan using a command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeeaay](https://clawhub.ai/user/jeeaay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Alibaba Cloud users use this skill to check Coding Plan quota usage and reset times from an authenticated browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated browser automation can interact with an Alibaba Cloud login session.

Mitigation: Use a least-privileged Alibaba Cloud account and run the skill only after reviewing the skill and its browser automation dependency.

Risk: A saved login screenshot may contain QR-code authentication material.

Mitigation: Delete the login screenshot after scanning the QR code and avoid sharing it.

Risk: The skill depends on a globally installed third-party browser automation tool.

Mitigation: Prefer a pinned, locally reviewed agent-browser version and review any .env settings before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jeeaay/skills/coding-plan-usage)
- [agent-browser dependency](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text status messages and JSON quota summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a local login QR screenshot when authentication is needed.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
