## Description:

Agent Browser automates browser interactions for web testing, form filling, screenshots, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tekkenkk](https://clawhub.ai/user/tekkenkk)

### License/Terms of Use:


## Use Case:

Developers, QA engineers, and automation agents use this skill to navigate websites, interact with pages, test web applications, capture browser evidence, and extract page content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved authentication state can contain reusable cookies, storage values, and session tokens.

Mitigation: Store state files outside repositories in private directories with owner-only permissions, prefer short-lived or test sessions, and delete or revoke saved sessions after use.

Risk: Screenshots, PDFs, recordings, traces, and extracted page text can capture private or regulated page data.

Mitigation: Use test accounts and synthetic data when possible, review generated artifacts before sharing or committing them, and remove captures that are no longer needed.

Risk: Proxy URLs, headers, uploaded files, and browser storage values may expose secrets or sensitive routing details.

Mitigation: Keep credentials in environment variables or secret stores, avoid hardcoding proxy credentials, and sanitize command output and saved files before reuse.

## Reference(s):

- [Agent Browser ClawHub listing](https://clawhub.ai/tekkenkk/skills/agent-browser-3)
- [Snapshot + Refs Workflow](references/snapshot-refs.md)
- [Session Management](references/session-management.md)
- [Authentication Patterns](references/authentication.md)
- [Video Recording](references/video-recording.md)
- [Proxy Support](references/proxy-support.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from agent-browser]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create screenshots, PDFs, WebM recordings, traces, text exports, uploaded-file interactions, and browser state files when commands or templates are used.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
