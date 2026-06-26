## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-zaa](https://clawhub.ai/user/liu-zaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and agents use this skill to automate browser navigation, form filling, UI testing, page inspection, screenshots, recordings, and structured data extraction through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can interact with live websites and authenticated sessions. <br>
Mitigation: Use isolated test accounts or disposable browser profiles where possible, and review target URLs and actions before execution. <br>
Risk: Saved session state, cookies, local storage, screenshots, videos, traces, and PDFs can contain sensitive information. <br>
Mitigation: Avoid printing cookies or tokens into logs, do not commit saved auth-state files, and clean up generated artifacts and persistent profiles after use. <br>
Risk: Network interception, JavaScript evaluation, and form automation can change page behavior or submit unintended data. <br>
Mitigation: Limit use to intended testing, debugging, or automation targets and inspect snapshots before performing state-changing actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liu-zaa/agent-browser-0-2-0-1) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, optional JSON command output, and generated browser artifacts such as screenshots, PDFs, traces, videos, or saved session state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm, and invokes only the agent-browser CLI through the documented Bash tool allowance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
