## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddbq](https://clawhub.ai/user/ddbq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate multi-step browser workflows with deterministic accessibility-tree snapshots, ref-based element selection, isolated sessions, and browser state management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser state, cookies, and localStorage can contain credentials or other sensitive session data.

Mitigation: Keep saved state files outside repositories, restrict file permissions, avoid sharing them, and delete them when no longer needed.

Risk: The skill installs and runs a broad browser automation dependency that can change local browser behavior or dependencies.

Mitigation: Install only in a trusted workspace, prefer a pinned local install or sandbox, and avoid administrative installs unless necessary.

## Reference(s):

- [agent-browser homepage](https://github.com/vercel-labs/agent-browser)
- [ClawHub skill page](https://clawhub.ai/ddbq/skills/agent-browser-clawdbot-0-1-0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on using the agent-browser CLI and interpreting JSON snapshot output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
