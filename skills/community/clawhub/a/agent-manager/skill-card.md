## Description:

Multi-Agent conversation management platform with Gemini-style UI for managing OpenClaw agents in one place with image upload, chat history, and message isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szzg007](https://clawhub.ai/user/szzg007)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to create, manage, inspect, delete, and chat with multiple local OpenClaw agents through a web interface, API endpoints, or CLI commands. It also supports image-assisted chat and browser-stored conversation history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes local management APIs that can create, chat with, and delete OpenClaw agents.

Mitigation: Run it only in a controlled local environment and add authentication before exposing the service to other users or networks.

Risk: The security evidence reports shell execution and deletion behavior, including use of rm -rf.

Mitigation: Replace shell command construction and recursive shell deletion with validated arguments and safer filesystem APIs before production use.

Risk: The security evidence reports a hardcoded token.

Mitigation: Remove the hardcoded token and require users to configure credentials through a local secret or environment-specific setup.

Risk: The web interface stores chat and image history in the browser.

Mitigation: Decide whether local browser storage is appropriate for the deployment and clear or disable stored history when messages may contain sensitive content.

Risk: The security evidence recommends binding the server to localhost.

Mitigation: Bind the service to 127.0.0.1 unless an authenticated and reviewed network deployment is explicitly required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szzg007/skills/agent-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/szzg007)
- [Project homepage](https://clawhub.com)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [ClawHub documentation](artifact/CLAWHUB.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON configuration, shell commands, local web UI responses, and API JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local OpenClaw agent management actions and browser-stored chat history.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
