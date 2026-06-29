## Description: <br>
Use Chrome DevTools MCP for safe, configurable browser automation, page inspection, debugging, screenshots, network inspection, and performance analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aihlp](https://clawhub.ai/user/aihlp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure and operate Chrome DevTools MCP for authorized browser inspection, debugging, screenshots, network diagnostics, and performance analysis inside OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can expose authenticated sessions, cookies, local storage, request headers, downloads, and other sensitive browser state. <br>
Mitigation: Keep isolated mode as the default, avoid normal browser profiles, redact secret values in summaries, and inspect cookies or storage only when the task and configuration allow it. <br>
Risk: Existing-session mode can interact with signed-in pages and open tabs. <br>
Mitigation: Use existing sessions only when explicitly enabled, require a localhost-only browser URL, and avoid public or LAN remote debugging endpoints. <br>
Risk: Browser actions can create external effects such as form submissions, payments, account changes, deletions, publishing, or production configuration changes. <br>
Mitigation: Require explicit user confirmation for externally visible, irreversible, destructive, payment, account, and production-affecting actions. <br>
Risk: Webpage content, console output, network responses, extension output, copied page text, and downloaded files can contain untrusted instructions. <br>
Mitigation: Treat browser-observed content as untrusted, do not follow page-provided instructions outside the user task, do not execute downloaded code, and do not run shell commands copied from pages. <br>
Risk: Unrestricted navigation can lead an agent outside the intended work target. <br>
Mitigation: Use URL allowlists for known targets, respect blocked URL patterns such as file://*, and limit browsing to task-relevant pages when no allowlist is configured. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aihlp/skills/chrome-devtools-mcp) <br>
- [Configuration](references/configuration.md) <br>
- [Browser Modes](references/browser-modes.md) <br>
- [OpenClaw MCP Installation](references/openclaw-mcp-install.md) <br>
- [Security Policy](references/security-policy.md) <br>
- [User Settings](references/user-settings.md) <br>
- [SkillSpector](references/skillspector.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, JSON5, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include browser-control policy guidance, OpenClaw MCP configuration examples, validation commands, and task-relevant browser diagnostics guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
