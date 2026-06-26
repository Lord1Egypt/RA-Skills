## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaomaju-888](https://clawhub.ai/user/xiaomaju-888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate browser workflows such as navigation, form filling, structured page inspection, UI testing, screenshots, PDFs, recordings, session state, and network interactions through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved browser sessions and captured page artifacts may contain cookies, tokens, passwords, or private page content. <br>
Mitigation: Use dedicated low-privilege browser sessions when possible, avoid saving state for highly sensitive accounts, and treat auth.json, screenshots, PDFs, traces, and recordings as sensitive files. <br>
Risk: Browser automation can act on live websites and authenticated accounts. <br>
Mitigation: Review target URLs and actions before execution, and use isolated sessions or test accounts for sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiaomaju-888/agent-browser-xiaoshu) <br>
- [agent-browser upstream CLI](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser snapshots, screenshots, PDFs, traces, recordings, cookies, storage state, and session files when the documented CLI commands are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
