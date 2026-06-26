## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Viv888-AI](https://clawhub.ai/user/Viv888-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate browser workflows with the agent-browser CLI, including navigation, ref-based element selection, interaction, state persistence, and page data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved sessions, cookies, localStorage values, screenshots, PDFs, and extracted page content can contain sensitive account or user data. <br>
Mitigation: Keep these artifacts out of source control and logs, and handle auth state files as sensitive credentials. <br>
Risk: Browser automation can perform high-impact actions such as purchases, posts, deletions, account changes, or other state-changing operations. <br>
Mitigation: Require explicit user approval before executing high-impact actions. <br>
Risk: The skill depends on the external agent-browser npm package. <br>
Mitigation: Install and use it only when the package source is trusted and browser automation is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Viv888-AI/clawdbot-agent-browser) <br>
- [agent-browser homepage](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON output conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or manipulate browser session state, screenshots, PDFs, cookies, localStorage values, and extracted page content through the external agent-browser CLI.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
