## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayakolin](https://clawhub.ai/user/ayakolin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate web navigation, data extraction, form filling, UI testing, screenshots, recordings, and browser state management through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can submit forms, upload files, change accounts, post content, purchase items, or delete data. <br>
Mitigation: Confirm high-impact browser actions before execution and review the target page state after navigation or DOM changes. <br>
Risk: Saved browser state, cookies, screenshots, videos, traces, and PDFs may contain credentials or private session data. <br>
Mitigation: Protect state files such as auth.json as credentials and keep recordings, traces, screenshots, and PDFs out of logs and version control. <br>
Risk: The skill depends on the upstream agent-browser package and browser tooling. <br>
Mitigation: Install only trusted versions of the upstream package and keep node, npm, and browser dependencies current. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ayakolin/agent-browser-zh) <br>
- [agent-browser upstream repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser CLI skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also guide agents to request JSON output from the CLI for machine-readable page snapshots and element data.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata; artifact frontmatter and _meta.json show 0.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
