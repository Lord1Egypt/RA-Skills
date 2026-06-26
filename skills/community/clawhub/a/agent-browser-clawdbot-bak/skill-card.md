## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChenJinsong](https://clawhub.ai/user/ChenJinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to drive browser workflows through the agent-browser CLI, including navigation, accessibility-tree snapshots, ref-based element interaction, session isolation, state persistence, screenshots, PDFs, and network controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved cookies and browser storage can expose logged-in sessions if mishandled. <br>
Mitigation: Keep auth-state, cookie, and storage files private, access-controlled, out of version control, and deleted when no longer needed. <br>
Risk: Browser automation can submit consequential actions on approved sites and accounts. <br>
Mitigation: Review consequential actions before submission and use the skill only on sites and accounts explicitly approved by the operator. <br>
Risk: The skill depends on an external agent-browser CLI source. <br>
Mitigation: Install only when the external CLI source is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChenJinsong/agent-browser-clawdbot-bak) <br>
- [agent-browser CLI homepage](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external agent-browser CLI command and may produce browser state files, screenshots, PDFs, and JSON command output when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
