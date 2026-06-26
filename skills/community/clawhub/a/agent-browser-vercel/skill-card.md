## Description: <br>
Browser automation CLI guidance for AI agents that need to navigate websites, fill forms, click elements, capture screenshots, extract data, test web apps, and manage browser sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Winchester-Yi](https://clawhub.ai/user/Winchester-Yi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to drive real browser sessions for authorized website interaction, application testing, form workflows, data extraction, screenshots, PDF export, visual diffs, profiling, and session management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can invoke an external browser automation CLI that may be unpinned. <br>
Mitigation: Install and run only a trusted agent-browser package version, and review generated commands before execution. <br>
Risk: Automated browser control can act inside logged-in accounts and submit forms or state-changing actions. <br>
Mitigation: Use the skill only on sites and accounts the user is authorized to automate, and require confirmation before purchases, posts, account changes, or submissions. <br>
Risk: Saved state, screenshots, videos, downloads, traces, and proxy credentials can contain sensitive data. <br>
Mitigation: Treat generated browser artifacts as sensitive, encrypt saved sessions when possible, avoid committing them, and delete them when no longer needed. <br>
Risk: Proxy guidance could be misused for evasion or rate-limit avoidance. <br>
Mitigation: Use proxies only for authorized corporate access, testing, or geo-validation, and avoid proxy rotation for bans, rate-limit bypass, or unauthorized scraping. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Session Management](references/session-management.md) <br>
- [Snapshot Refs](references/snapshot-refs.md) <br>
- [Video Recording](references/video-recording.md) <br>
- [Profiling](references/profiling.md) <br>
- [Proxy Support](references/proxy-support.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser-control commands that create screenshots, PDFs, videos, saved browser state, downloads, traces, and extracted page text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
