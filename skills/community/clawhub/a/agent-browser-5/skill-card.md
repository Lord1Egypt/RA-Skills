## Description: <br>
Browser automation CLI for AI agents that helps navigate pages, fill forms, click buttons, take screenshots, extract data, test web apps, and automate browser tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Equalearning](https://clawhub.ai/user/Equalearning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and AI-agent operators use this skill to control Chrome or Chromium through agent-browser for web navigation, form automation, authenticated sessions, page capture, data extraction, and web app testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over real websites and logged-in browser sessions. <br>
Mitigation: Use test accounts or dedicated browser profiles, enable domain allowlists and an action policy before sensitive work, and require explicit confirmation for logins, submissions, uploads, purchases, account changes, deletion, or public posting. <br>
Risk: Authentication state files, sessions, or imported browser profiles can expose session tokens or credentials. <br>
Mitigation: Avoid importing a personal Chrome session unless necessary, use the encrypted auth vault or AGENT_BROWSER_ENCRYPTION_KEY where available, keep state files out of source control, and delete auth state when it is no longer needed. <br>
Risk: Page content returned to an agent can include untrusted instructions or excessive output. <br>
Mitigation: Enable content boundaries for page-sourced output and set output limits before browsing untrusted or large pages. <br>


## Reference(s): <br>
- [Agent Browser ClawHub Listing](https://clawhub.ai/Equalearning/agent-browser-5) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Command Reference](references/commands.md) <br>
- [Profiling](references/profiling.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [Session Management](references/session-management.md) <br>
- [Snapshot and Refs](references/snapshot-refs.md) <br>
- [Video Recording](references/video-recording.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, command examples, and workflow templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser screenshots, PDFs, text extracts, JSON command output, saved session state, video recordings, and profiling traces when the referenced CLI commands are executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
