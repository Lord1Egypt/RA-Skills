## Description:

Multi-Agent conversation management platform with Gemini-style UI for managing OpenClaw agents with image upload, chat history, and message isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szzg007](https://clawhub.ai/user/szzg007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to manage multiple local OpenClaw agents, create or delete agent profiles, and interact with agents through a web UI, CLI, or local API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes powerful local OpenClaw agent controls with weak boundaries and unsafe command handling.

Mitigation: Install only in a trusted local environment after reviewing the code, and do not expose the server to a network.

Risk: Configuration and documentation may lead users to handle operator tokens or token-like values insecurely.

Mitigation: Avoid pasting secrets into configuration or logs, and rotate any real token resembling the README value before use.

Risk: Create, chat, and delete actions can affect local agent state and should be treated as privileged operations.

Mitigation: Treat these endpoints as admin actions until authentication, input validation, safe process spawning, deletion safeguards, and HTML escaping are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/szzg007/skills/agent-manager-v100)
- [Publisher Profile](https://clawhub.ai/user/szzg007)
- [ClawHub Homepage](https://clawhub.com)
- [README.md](README.md)
- [QUICKSTART.md](QUICKSTART.md)
- [CLAWHUB.md](CLAWHUB.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, JavaScript source files, and local API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for local OpenClaw agent management through a browser UI, CLI, and localhost API.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
