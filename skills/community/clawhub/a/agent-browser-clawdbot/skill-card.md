## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection

This skill is ready for commercial/non-commercial use.

## Publisher:

[matrixy](https://clawhub.ai/user/matrixy)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to automate browser workflows through the agent-browser CLI, including navigation, accessibility snapshots, ref-based interactions, extraction, sessions, state persistence, screenshots, PDFs, and network controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser state, cookies, and localStorage can expose authenticated sessions or sensitive data.

Mitigation: Treat state files and storage output like credentials: do not commit, share, or log them, and prefer low-privilege test accounts for automation.

Risk: Global CLI installation can expand local execution and supply-chain exposure.

Mitigation: Install the CLI in an isolated environment and pin or verify the package version where possible.

Risk: Browser automation on logged-in sites can perform unintended actions if commands target the wrong page or session.

Mitigation: Use isolated sessions, re-snapshot after page changes, and review targets before executing actions against authenticated sites.

## Reference(s):

- [Agent Browser CLI homepage](https://github.com/vercel-labs/agent-browser)
- [ClawHub skill page](https://clawhub.ai/matrixy/skills/agent-browser-clawdbot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser state files, screenshots, PDFs, cookies, storage values, and extracted page data when the documented CLI commands are used.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
