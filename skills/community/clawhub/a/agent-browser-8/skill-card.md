## Description: <br>
Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hayasam](https://clawhub.ai/user/hayasam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate browser workflows such as navigation, form completion, screenshots, data extraction, authentication flows, web app testing, and capture workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over websites, including authenticated sessions. <br>
Mitigation: Use dedicated browser profiles or test accounts, enable domain allowlists and content boundaries, and require explicit approval for consequential actions. <br>
Risk: Saved browser state can include session tokens or credentials. <br>
Mitigation: Avoid importing a main Chrome session; encrypt saved state when used, keep state files out of version control, and delete them when no longer needed. <br>
Risk: The skill depends on an external browser automation CLI. <br>
Mitigation: Pin and verify the `agent-browser` CLI before use, and install it only in environments where browser automation is intended. <br>


## Reference(s): <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Command Reference](references/commands.md) <br>
- [Profiling](references/profiling.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [Session Management](references/session-management.md) <br>
- [Snapshot and Refs](references/snapshot-refs.md) <br>
- [Video Recording](references/video-recording.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and shell-script templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots, PDFs, text captures, HAR files, browser state files, and other local artifacts when the suggested browser commands are executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
