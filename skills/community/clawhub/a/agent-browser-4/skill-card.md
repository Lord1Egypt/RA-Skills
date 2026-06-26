## Description: <br>
Browser automation CLI for AI agents that need to navigate websites, fill forms, click buttons, take screenshots, extract data, test web apps, or automate browser tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Justinpoulido](https://clawhub.ai/user/Justinpoulido) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to control browser sessions for website interaction, form automation, data extraction, visual capture, authentication workflows, and web app testing. It is intended for tasks where command-driven browser control is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes powerful browser control, session persistence, recording, proxy, and script-execution capabilities that can expose sensitive accounts, credentials, cookies, screenshots, videos, proxy credentials, and auth-state files. <br>
Mitigation: Use it only where browser automation is necessary; avoid personal banking, admin consoles, production accounts, and SSO or MFA sessions unless explicitly required; keep browser artifacts out of repositories and shared logs; delete them after use. <br>
Risk: Saved browser state can contain cookies, local storage, session storage, and authentication tokens. <br>
Mitigation: Store state files securely, never commit them, prefer short-lived sessions for CI/CD, encrypt persistent sessions when used, and clear cookies or remove state files after automation. <br>
Risk: Screenshots, videos, traces, PDFs, and profiling output can capture private page content or credential entry. <br>
Mitigation: Do not record credential entry, limit capture to the minimum needed for the task, and review generated artifacts before sharing or retaining them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Justinpoulido/agent-browser-4) <br>
- [Command Reference](references/commands.md) <br>
- [Snapshot and Refs](references/snapshot-refs.md) <br>
- [Session Management](references/session-management.md) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Video Recording](references/video-recording.md) <br>
- [Profiling](references/profiling.md) <br>
- [Proxy Support](references/proxy-support.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline bash, JSON, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce browser artifacts such as screenshots, PDFs, videos, traces, saved session state, extracted text, or JSON output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
