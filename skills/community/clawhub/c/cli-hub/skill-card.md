## Description:

Unified CLI gateway to search, install, authenticate, and invoke enterprise and AI platform tools (WeCom, DingTalk, Lark/Feishu, Dreamina) covering 91+ operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxyd-ai](https://clawhub.ai/user/lxyd-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and enterprise operators use this skill to discover and run CLI actions for WeCom, DingTalk, Lark/Feishu, and Dreamina workflows such as messaging, calendars, todos, documents, meetings, and AI image or video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents a remote curl-to-bash installer path.

Mitigation: Install with pipx or uv from the package index and avoid the curl-to-bash convenience command.

Risk: The skill can trigger broad business-account actions such as sending messages, changing enterprise data, and authenticating accounts.

Mitigation: Search for the operation, inspect the parameter schema, and review each command before execution.

Risk: Dreamina generation workflows may spend AI-generation credits and run asynchronously.

Mitigation: Install only the needed provider, confirm credit-spending actions before submission, and check async job results explicitly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxyd-ai/skills/cli-hub)
- [PyPI package: agent-cli-hub](https://pypi.org/project/agent-cli-hub/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include interactive authentication steps and command review guidance before invoking enterprise or AI-generation providers.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
