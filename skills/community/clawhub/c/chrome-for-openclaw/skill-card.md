## Description: <br>
Browser automation CLI for AI agents using Google Chrome via CDP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joustonhuang](https://clawhub.ai/user/joustonhuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect OpenClaw workflows to an existing Chrome session for web navigation, form filling, screenshots, data extraction, authenticated browsing, and browser task automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can run an unpinned remote script and perform system setup. <br>
Mitigation: Review and pin the setup script before running it, and run installation only in an environment where sudo-level Chrome, XRDP, and XFCE changes are acceptable. <br>
Risk: A CDP-enabled Chrome session can expose logged-in accounts, cookies, local storage, and page control to local automation. <br>
Mitigation: Use a separate Chrome profile or VM for automation, restrict navigation to trusted domains where possible, and close the CDP-enabled browser when work is complete. <br>
Risk: Saved browser state can contain authentication tokens and session cookies. <br>
Mitigation: Avoid saving auth state unless necessary; when saved, encrypt it, restrict file access, keep it out of source control, and delete it after use. <br>
Risk: The browser automation can perform account-changing actions such as purchases, emails, uploads, cookie access, payment entry, or form submissions. <br>
Mitigation: Require explicit user confirmation before high-impact or account-changing actions and use an action policy for destructive operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joustonhuang/chrome-for-openclaw) <br>
- [Chrome CDP for OpenClaw Homepage](https://github.com/joustonhuang/chrome_for_openclaw) <br>
- [Compatible Agent Browser Skill](https://clawhub.ai/hsyhph/openclaw-agent-browser-clawdbot) <br>
- [agent-browser CLI](https://github.com/vercel-labs/agent-browser) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Command Reference](references/commands.md) <br>
- [Profiling](references/profiling.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [Session Management](references/session-management.md) <br>
- [Snapshot and Refs](references/snapshot-refs.md) <br>
- [Video Recording](references/video-recording.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides browser automation through agent-browser commands connected to a Chrome CDP session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
