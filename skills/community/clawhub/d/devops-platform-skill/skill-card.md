## Description:

Manage and query DevOps platform data, including applications, iterations, releases, and statistics through configured API access with user token authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanqiuqian](https://clawhub.ai/user/yuanqiuqian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to configure API access and retrieve application, iteration, release, and platform statistics from a DevOps efficiency platform. It supports agent-assisted operational queries and CLI workflows over the configured backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API tokens in ways that could expose credentials through shared shells, prompts, command history, or local configuration files.

Mitigation: Use short-lived or least-privilege tokens, avoid pasting real tokens into shared contexts, protect or remove local configuration files, and rotate any token that may have been exposed.

Risk: A user-configured API host controls where authenticated requests are sent.

Mitigation: Use only approved HTTPS endpoints and install the skill only when the publisher and configured API host are trusted.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yuanqiuqian/skills/devops-platform-skill)
- [README.md](artifact/README.md)
- [INSTALL.md](artifact/INSTALL.md)
- [SUMMARY.md](artifact/SUMMARY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent or user to configure a backend API URL and user token before running DevOps platform queries.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package.json lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
