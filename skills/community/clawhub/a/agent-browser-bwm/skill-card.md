## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to drive headless browser workflows through the agent-browser CLI, including navigation, accessibility-tree snapshots, ref-based interactions, session isolation, state persistence, and browser data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved auth state, cookies, and browser storage can expose account access or sensitive session data.

Mitigation: Keep state files private, avoid logging their contents, use least-privilege test accounts, and delete saved state when it is no longer needed.

Risk: Installing the required agent-browser CLI from an untrusted or unexpected package source could introduce supply-chain risk.

Mitigation: Install only from a trusted npm registry and pin or review the agent-browser version where possible.

## Reference(s):

- [agent-browser GitHub repository](https://github.com/vercel-labs/agent-browser)
- [ClawHub skill page](https://clawhub.ai/blueworldmarketing/skills/agent-browser-bwm)
- [ClawHub publisher profile](https://clawhub.ai/user/blueworldmarketing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is oriented around the agent-browser CLI and may reference saved browser state, cookies, storage, screenshots, PDFs, and network controls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
