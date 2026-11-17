## Description:

Guides developers through setting up AINative SDKs, choosing a React, Next.js, Svelte, Vue, or raw API path, obtaining credentials, and making a first API call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to bootstrap AINative SDK usage across common web frameworks, configure credentials, and make an initial chat API call. It is intended for setup guidance rather than runtime automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quickstart recommends running an unpinned initializer that can create credentials and modify agent or IDE MCP configuration.

Mitigation: Use a pinned package version or manual setup, inspect generated MCP configuration before use, and run the initializer only from a trusted package source.

Risk: The examples include browser-visible API key patterns, including a NEXT_PUBLIC_AINATIVE_API_KEY setting.

Mitigation: Keep long-lived API keys server-side and use browser-exposed tokens only when AINative documents a restricted publishable client token for that purpose.

## Reference(s):

- [AINative Studio](https://app.ainative.studio)
- [ClawHub Skill Page](https://clawhub.ai/urbantech/skills/ainative-sdk-quickstart)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes framework-specific examples and credential setup notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
