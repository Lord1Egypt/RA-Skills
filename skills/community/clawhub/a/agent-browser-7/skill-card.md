## Description: <br>
Agent Browser guides AI agents in using the agent-browser CLI to navigate websites, interact with pages, manage sessions, capture artifacts, and automate browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thanhde91](https://clawhub.ai/user/thanhde91) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, testers, and automation agents use this skill to operate Chrome or Chromium from the command line for website navigation, form filling, data extraction, authenticated browsing, screenshots, PDFs, network capture, and web application testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority to navigate websites, click controls, submit forms, and operate authenticated sessions. <br>
Mitigation: Use dedicated browser profiles or test accounts, enable domain allowlists and action policies, and supervise workflows before allowing sensitive actions. <br>
Risk: Saved auth state, browser profiles, screenshots, recordings, traces, HARs, downloads, and proxy credentials can contain sensitive information. <br>
Mitigation: Treat generated files and credentials as secrets, avoid importing a primary Chrome session, encrypt saved state when possible, and delete saved state after use. <br>
Risk: Raw page content can include untrusted instructions or large outputs that may influence an agent. <br>
Mitigation: Enable content boundaries, set output limits, and review page-derived text before using it as trusted instruction. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thanhde91/agent-browser-7) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Command Reference](references/commands.md) <br>
- [Profiling](references/profiling.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [Session Management](references/session-management.md) <br>
- [Snapshot and Refs](references/snapshot-refs.md) <br>
- [Video Recording](references/video-recording.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce browser-derived files such as screenshots, PDFs, HARs, traces, recordings, downloads, and saved session state.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
