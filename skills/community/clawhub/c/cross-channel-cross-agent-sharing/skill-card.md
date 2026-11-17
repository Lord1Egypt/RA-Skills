## Description:

Ensures new capabilities gained from workspace-installed tools or packages are documented, verified, and propagated across channels and related agent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skglau](https://clawhub.ai/user/skglau)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after workspace tool, environment, or package changes to record exact capability details, verify availability, and share concise updates with related sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to persist capability notes and alter reusable skill instructions, which can make incorrect or stale capability claims durable across the workspace.

Mitigation: Require explicit review before persistent memory, TOOLS.md, or reusable skill updates are applied, and run the bundled verification helper before claiming a capability.

Risk: The skill can notify related sessions after capability changes, which may create unwanted cross-session sharing or noise.

Mitigation: Limit notifications to active related sessions and include only the invocation details and critical caveats needed for the receiving agent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/skglau/skills/cross-channel-cross-agent-sharing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise cross-session notification text and verification results.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
