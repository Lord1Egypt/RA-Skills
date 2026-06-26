## Description: <br>
Automates browser interactions for web testing, form filling, screenshots, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tekkenKK](https://clawhub.ai/user/tekkenKK) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, QA engineers, and agents use this skill to drive browser sessions for web testing, form automation, UI inspection, screenshots, recordings, and data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad browser and account control through a separate agent-browser executable. <br>
Mitigation: Install and run it only when the executable is trusted, and use test or least-privilege accounts for automation. <br>
Risk: Proxy guidance could be misused to bypass site rules or rate limits. <br>
Mitigation: Use proxies only for legitimate testing, compliance, accessibility, or corporate-network needs, and follow target-site terms. <br>
Risk: Saved state files, screenshots, recordings, and PDFs can contain credentials, tokens, or sensitive page data. <br>
Mitigation: Keep generated artifacts out of source control, restrict sharing, and delete them when they are no longer needed. <br>
Risk: Command examples include credential and proxy-secret handling patterns. <br>
Mitigation: Use protected environment variables or secret-management tools instead of hard-coded secrets in commands or scripts. <br>


## Reference(s): <br>
- [Agent Browser on ClawHub](https://clawhub.ai/tekkenKK/agent-browser-tekken) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [Session Management](references/session-management.md) <br>
- [Snapshot Refs](references/snapshot-refs.md) <br>
- [Video Recording](references/video-recording.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and reusable shell templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create screenshots, PDFs, video recordings, saved browser state, and JSON command output when requested.] <br>

## Skill Version(s): <br>
0.8.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
