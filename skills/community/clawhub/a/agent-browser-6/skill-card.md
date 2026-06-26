## Description: <br>
Agent Browser helps AI agents automate browser tasks such as navigation, form filling, clicking, screenshots, data extraction, testing, and authenticated workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chulla-ceja](https://clawhub.ai/user/chulla-ceja) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation-focused agent users use this skill to drive Chrome or Chromium through a command-line workflow for web interaction, testing, capture, and data extraction. It is especially suited to tasks that need persistent browser sessions, element references, screenshots, PDF capture, or authenticated browsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a browser and persist sessions, which may expose authenticated accounts or sensitive browsing state. <br>
Mitigation: Use isolated test profiles or dedicated sessions, avoid importing everyday logged-in browser state, and close or clean sessions after use. <br>
Risk: State files and recordings can contain session tokens, page content, or other sensitive data. <br>
Mitigation: Encrypt state at rest with AGENT_BROWSER_ENCRYPTION_KEY where supported, keep generated artifacts out of source control, and delete state files and recordings when no longer needed. <br>
Risk: Unrestricted browsing and page output can expose an agent to untrusted page content or unintended domains. <br>
Mitigation: Enable content boundaries, domain allowlists, action policies, and output limits before allowing agent-driven browser use. <br>
Risk: Proxy rotation can be misused to bypass site limits or access restrictions. <br>
Mitigation: Use proxies only for legitimate testing or network access needs and do not use rotation to evade policy, rate limits, or access controls. <br>


## Reference(s): <br>
- [Agent Browser ClawHub Release](https://clawhub.ai/chulla-ceja/agent-browser-6) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Command Reference](references/commands.md) <br>
- [Profiling](references/profiling.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [Session Management](references/session-management.md) <br>
- [Snapshot and Refs](references/snapshot-refs.md) <br>
- [Video Recording](references/video-recording.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser state, screenshots, PDFs, recordings, traces, downloaded files, and page text when the underlying CLI commands are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
