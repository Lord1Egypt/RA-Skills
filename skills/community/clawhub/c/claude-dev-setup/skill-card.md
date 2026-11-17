## Description:

Complete Claude Code CLI integration with session management and APEX cognitive framework. One skill to set up coding agents with persistent task tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhruvarvindsingh](https://clawhub.ai/user/dhruvarvindsingh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure Claude Code CLI workflows, session tracking, AGENTS.md guidance, and APEX references in OpenClaw workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to extract and load local Claude OAuth tokens, which can expose credentials.

Mitigation: Remove raw token extraction and shell-profile token loading before use, and avoid installing it on machines with real Claude credentials unless the workflow has been reviewed.

Risk: The skill recommends running Claude Code with permission checks bypassed.

Mitigation: Avoid --dangerously-skip-permissions and run delegated agents in a constrained environment with explicit approval for sensitive actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dhruvarvindsingh/skills/claude-dev-setup)
- [AGENTS.md session section template](artifact/agents-section.md)
- [Claude Code session tracking template](artifact/sessions-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and local template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Claude Code CLI and targets Linux or macOS environments.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
