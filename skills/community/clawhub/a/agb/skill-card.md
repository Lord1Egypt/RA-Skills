## Description: <br>
Automates browser interactions for web testing, form filling, screenshots, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cecwap](https://clawhub.ai/user/cecwap) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to drive browser sessions for web testing, form automation, authenticated workflows, screenshots, video capture, and web data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad control over live browser sessions. <br>
Mitigation: Install it only for trusted agents and workflows, and review proposed browser actions before using sensitive accounts or sites. <br>
Risk: Saved state files, screenshots, videos, PDFs, traces, cookies, and storage dumps can contain sensitive data. <br>
Mitigation: Treat generated artifacts as sensitive, keep authentication state out of shared folders and version control, and delete captures that are no longer needed. <br>
Risk: Page JavaScript execution can expose or alter sensitive site state. <br>
Mitigation: Avoid arbitrary JavaScript evaluation on sensitive sites and scope evaluation to reviewed, task-specific snippets. <br>
Risk: Proxy configuration can be misused to bypass site rules or rate limits. <br>
Mitigation: Use proxies only for legitimate testing or approved network access, and do not use proxy examples to evade site policies. <br>


## Reference(s): <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [Session Management](references/session-management.md) <br>
- [Snapshot Refs](references/snapshot-refs.md) <br>
- [Video Recording](references/video-recording.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser commands may create screenshots, PDFs, video recordings, traces, cookies, storage dumps, and saved authentication state files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
