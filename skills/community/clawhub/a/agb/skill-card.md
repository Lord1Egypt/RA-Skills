## Description:

Automates browser interactions for web testing, form filling, screenshots, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cecwap](https://clawhub.ai/user/cecwap)

### License/Terms of Use:


## Use Case:

Developers, QA engineers, and automation agents use this skill to navigate websites, interact with page elements, fill forms, capture screenshots or PDFs, record browser sessions, and extract page information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a live browser and interact with authenticated websites.

Mitigation: Use it only for sites and accounts where browser automation is intended, and explicitly review actions before using sensitive accounts, production admin consoles, or internal applications.

Risk: Saved browser state, screenshots, PDFs, traces, recordings, and extracted page text can contain secrets or personal data.

Mitigation: Treat generated artifacts and state files as secrets: keep them out of repositories, restrict file permissions, and delete them when no longer needed.

Risk: Untrusted proxies, extensions, CDP attachment, or JavaScript evaluation can expose browser data or change page behavior.

Mitigation: Use trusted network paths and browser extensions only, avoid eval on sensitive pages, and close named sessions after use.

## Reference(s):

- [Authentication Patterns](references/authentication.md)
- [Proxy Support](references/proxy-support.md)
- [Session Management](references/session-management.md)
- [Snapshot + Refs Workflow](references/snapshot-refs.md)
- [Video Recording](references/video-recording.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown, Files]

**Output Format:** [Markdown guidance with inline shell commands and references to generated browser artifacts such as screenshots, PDFs, videos, and extracted text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use named browser sessions, saved state files, proxy settings, device emulation, and JSON command output when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
