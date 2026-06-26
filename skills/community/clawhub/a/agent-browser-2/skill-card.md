## Description: <br>
Automates browser interactions for web testing, form filling, screenshots, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[murphykobe](https://clawhub.ai/user/murphykobe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to navigate websites, interact with pages, fill forms, capture screenshots or PDFs, record browser sessions, and extract page information for testing or automation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad browser and session authority can expose cookies, storage, credentials, screenshots, recordings, and extracted private page data. <br>
Mitigation: Use least-privilege test accounts where possible, keep saved state and captured artifacts out of source control, and delete sensitive files after use. <br>
Risk: The skill can automate sites and use proxies in ways that may violate site terms, rate limits, or authorization boundaries. <br>
Mitigation: Use it only on sites you are authorized to test or automate, avoid proxy-based ban or rate-limit evasion, and respect target-site usage policies. <br>
Risk: Execution depends on the local agent-browser executable available in PATH. <br>
Mitigation: Install only from a trusted source and verify the local executable before enabling this skill. <br>


## Reference(s): <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [Session Management](references/session-management.md) <br>
- [Snapshot + Refs Workflow](references/snapshot-refs.md) <br>
- [Video Recording](references/video-recording.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots, PDFs, videos, browser state files, traces, and extracted page data through agent-browser commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
