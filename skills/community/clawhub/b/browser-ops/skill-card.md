## Description:

Browser Ops Publish helps agents choose a cost-aware CLI path for web search, content extraction, page interaction, authenticated browser access, and anti-bot fallbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route web tasks through appropriate CLI tools, starting with lightweight search and fetch paths and escalating only when authentication, JavaScript rendering, browser interaction, or anti-bot handling is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse an active browser login state when handling authenticated pages.

Mitigation: Use a dedicated low-privilege browser profile and avoid internal or sensitive sites unless the authenticated fallback has explicit per-domain approval.

Risk: Bundled helper scripts may expose cookies or run unintended commands when given untrusted URLs, queries, or limit values.

Mitigation: Do not run helper scripts with untrusted inputs until their injection and cookie-file handling issues are fixed; pin and review dependencies before use.

Risk: Cookie snapshots can retain access to logged-in services after export.

Mitigation: Restrict access to exported cookie files, keep them out of shared workspaces, and refresh or delete them when SSO sessions expire or the task is complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/browser-ops)
- [Routing Decision Tree](artifact/references/routing.md)
- [OpenCLI Usage Guide](artifact/references/opencli-usage.md)
- [Setup and Verification](artifact/references/setup.md)
- [Cookie and Session State](artifact/references/state-management.md)
- [Anti-Detection Guidance](artifact/references/anti-detection.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI command suggestions and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are expected to include extracted content, the selected tool path, and actionable failure guidance when a web task cannot be completed.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
