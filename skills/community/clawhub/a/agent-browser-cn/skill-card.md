## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[v585](https://clawhub.ai/user/v585) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, testers, and agents use this skill to drive browser workflows from the command line, including navigation, structured page snapshots, form entry, data extraction, screenshots, PDFs, recordings, session state, and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over logged-in browser sessions. <br>
Mitigation: Use a separate browser profile or test account and avoid sensitive logged-in sites unless the workflow requires them. <br>
Risk: Browser automation can expose cookies, local storage, saved auth state, credentials, uploaded files, or private page content. <br>
Mitigation: Require explicit approval before reading cookies or storage, entering credentials, uploading files, saving auth state, recording sessions, or extracting private content. <br>
Risk: Automated browser actions can submit forms, change account data, or trigger external side effects. <br>
Mitigation: Review snapshots and planned actions before clicks, submissions, account changes, network route changes, or destructive operations. <br>
Risk: Screenshots, PDFs, videos, traces, and saved state files may contain sensitive information. <br>
Mitigation: Store generated browser artifacts in controlled locations, review them before sharing, and delete private artifacts when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/v585/agent-browser-cn) <br>
- [agent-browser upstream CLI](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown usage guidance with inline shell commands, CLI text or JSON output, and optional generated file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm to install or run agent-browser; workflows may create screenshots, PDFs, video recordings, traces, or saved browser state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
