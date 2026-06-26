## Description: <br>
Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shahaamirbader](https://clawhub.ai/user/shahaamirbader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to automate browser workflows such as navigation, form filling, screenshots, data extraction, login flows, and web application testing through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over browser sessions, including logged-in sessions. <br>
Mitigation: Use test accounts or dedicated browser profiles, enable domain allowlists and action policies, and confirm before login, payment, posting, or other state-changing actions. <br>
Risk: Saved state, screenshots, recordings, traces, HAR files, and proxy credentials can contain sensitive data. <br>
Mitigation: Treat these artifacts as secrets, avoid importing an everyday browser session, and delete or protect saved browser state when no longer needed. <br>
Risk: Page-sourced content can influence an agent during browsing tasks. <br>
Mitigation: Enable content boundaries and review extracted page content before using it to drive important decisions. <br>
Risk: Proxy rotation can be misused for rate-limit or ban avoidance. <br>
Mitigation: Use proxies only for legitimate testing or corporate access needs and avoid proxy rotation for evasion. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/shahaamirbader/agent-browser-openclaw) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Command Reference](references/commands.md) <br>
- [Profiling](references/profiling.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [Session Management](references/session-management.md) <br>
- [Snapshot and Refs](references/snapshot-refs.md) <br>
- [Video Recording](references/video-recording.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and reusable shell script templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to create screenshots, PDFs, recordings, HAR files, traces, saved session state, and downloaded files through the external CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
