## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auroechan](https://clawhub.ai/user/auroechan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to drive headless browser workflows, inspect accessibility-tree snapshots, select elements by stable refs, and automate navigation, form entry, state checks, sessions, cookies, storage, tabs, frames, screenshots, PDFs, and network controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can operate logged-in browser sessions and saved auth state. <br>
Mitigation: Use isolated sessions or separate test accounts, require explicit approval before purchases, account changes, public posts, or admin actions, and treat saved auth files like passwords. <br>
Risk: Cookie and storage commands can expose or modify sensitive authentication values. <br>
Mitigation: Limit use to trusted environments, avoid sharing saved state files, and review cookie or storage changes before reusing authenticated sessions. <br>
Risk: The skill depends on an external agent-browser CLI. <br>
Mitigation: Install only when the external CLI is trusted and browser automation is required for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/auroechan/agent-browser-clawdbot-0) <br>
- [agent-browser homepage](https://github.com/vercel-labs/agent-browser) <br>
- [Publisher profile](https://clawhub.ai/user/auroechan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to execute the external agent-browser CLI and interpret JSON snapshots, refs, browser state, cookies, storage, screenshots, PDFs, and network results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
