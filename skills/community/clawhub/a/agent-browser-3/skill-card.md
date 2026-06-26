## Description: <br>
Automates browser interactions for web testing, form filling, screenshots, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tekkenKK](https://clawhub.ai/user/tekkenKK) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to navigate websites, inspect interactive elements, fill forms, capture screenshots or PDFs, record browser sessions, and extract web page data through the local agent-browser command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle logged-in browser sessions, captured pages, recordings, and saved authentication state. <br>
Mitigation: Treat saved state files, screenshots, PDFs, traces, and recordings as secrets; keep them out of repositories and delete them when finished. <br>
Risk: Browser automation can change data, submit forms, or upload files on behalf of a user. <br>
Mitigation: Confirm before actions that mutate data or upload files, especially on sensitive accounts or production systems. <br>
Risk: The skill depends on the local agent-browser executable. <br>
Mitigation: Install and run it only when browser automation is needed and the local executable is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tekkenKK/agent-browser-3) <br>
- [Snapshot + Refs Workflow](references/snapshot-refs.md) <br>
- [Session Management](references/session-management.md) <br>
- [Authentication Patterns](references/authentication.md) <br>
- [Video Recording](references/video-recording.md) <br>
- [Proxy Support](references/proxy-support.md) <br>
- [Form Automation Template](templates/form-automation.sh) <br>
- [Authenticated Session Template](templates/authenticated-session.sh) <br>
- [Content Capture Template](templates/capture-workflow.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create screenshots, PDFs, WebM recordings, traces, saved browser state, and extracted text files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
