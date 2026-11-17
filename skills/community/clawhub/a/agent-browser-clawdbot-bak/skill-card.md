## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjinsong](https://clawhub.ai/user/chenjinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to drive browser workflows through the agent-browser CLI, including navigation, ref-based element interaction, state checks, screenshots, PDFs, sessions, and network controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser authentication files, cookies, localStorage, and sessionStorage can expose account access if shared or committed.

Mitigation: Keep saved browser state local, exclude it from version control and shared artifacts, delete it when no longer needed, and avoid high-privilege accounts unless required.

Risk: Browser automation can act on live web sessions and perform actions under the user's account.

Mitigation: Review the target site, account privilege level, and proposed commands before running multi-step automation.

## Reference(s):

- [agent-browser project homepage](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the agent-browser command-line tool; examples favor JSON snapshots for deterministic parsing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
