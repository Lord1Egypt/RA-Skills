## Description:

Automates browser interactions for web testing, form filling, screenshots, data extraction, and page navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tekkenkk](https://clawhub.ai/user/tekkenkk)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to drive browser sessions for web application testing, form workflows, authenticated browsing, screenshots, PDFs, videos, and page-content extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad browser-control abilities, including navigation, interaction, JavaScript evaluation, downloads, screenshots, PDFs, and recordings.

Mitigation: Run it only for approved sites and workflows, review planned commands before execution, and prefer low-privilege or test accounts.

Risk: Saved browser state, cookies, storage, and authentication files can contain reusable session tokens.

Mitigation: Store state files outside shared directories with strict permissions, exclude them from version control, delete them when no longer needed, and revoke affected sessions if exposure is suspected.

Risk: Screenshots, PDFs, recordings, traces, and captured page text can contain credentials, personal data, or confidential application content.

Mitigation: Avoid recording real login flows, keep generated artifacts in controlled locations, and review or redact captures before sharing.

Risk: Proxy configuration and authenticated proxy URLs can expose network routing details or embedded credentials.

Mitigation: Use environment variables for proxy settings, avoid hardcoding credentials, and verify proxy behavior before running automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tekkenkk/skills/agent-browser-tekken)
- [Snapshot and Refs Workflow](references/snapshot-refs.md)
- [Session Management](references/session-management.md)
- [Authentication Patterns](references/authentication.md)
- [Video Recording](references/video-recording.md)
- [Proxy Support](references/proxy-support.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; command output may include text, JSON, screenshots, PDFs, WebM recordings, and saved browser-state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser snapshots use temporary element refs that must be refreshed after navigation or significant page changes.]

## Skill Version(s):

0.8.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
