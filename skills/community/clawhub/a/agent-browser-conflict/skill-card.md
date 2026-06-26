## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nuradil](https://clawhub.ai/user/nuradil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to automate browser navigation, UI testing, form filling, and structured data extraction through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad control over websites, including navigation, clicks, typing, form submission, file uploads, and browser state changes. <br>
Mitigation: Use disposable browser sessions or test accounts, and require explicit approval before submitting forms, uploading files, or making persistent changes on a site. <br>
Risk: Browser automation can expose or retain sensitive session data through cookies, local storage, saved auth state, screenshots, recordings, traces, PDFs, or CDP access. <br>
Mitigation: Avoid sensitive sites unless necessary, approve any cookie or storage access, and minimize, secure, or delete captured browser artifacts after use. <br>
Risk: The skill depends on the upstream agent-browser npm package and local browser automation tooling. <br>
Mitigation: Install only when the publisher and upstream package are trusted, and prefer a pinned package version for repeatable deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nuradil/agent-browser-conflict) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser CLI skill issue tracker](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return browser snapshots, JSON, screenshots, PDFs, recordings, traces, and saved state through the agent-browser CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
