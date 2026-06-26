## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cxz9909](https://clawhub.ai/user/cxz9909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to control browser sessions from an agent, including navigation, interaction, form filling, screenshots, PDF capture, UI checks, and structured page extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad browser-session control, including page interaction, uploads, JavaScript evaluation, cookies/storage access, and state save/load. <br>
Mitigation: Use isolated browser sessions and test accounts; require explicit approval before uploads, JavaScript evaluation, cookie/storage access, form submissions, purchases, or saving/restoring authentication state. <br>
Risk: The skill depends on an external npm CLI that can affect local browser state and files. <br>
Mitigation: Pin and verify the agent-browser package where possible, install it only in controlled environments, and test commands before using it on sensitive sites. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cxz9909/cxz9909-agentbrowser) <br>
- [agent-browser CLI repository referenced by the skill](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository referenced by the artifact](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser screenshots, PDFs, recordings, traces, saved session state, cookies/storage output, and network request summaries through the agent-browser CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
