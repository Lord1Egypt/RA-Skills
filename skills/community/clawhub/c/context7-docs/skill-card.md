## Description:

Fetches up-to-date, version-specific documentation and code examples for programming libraries and frameworks from Context7.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaylane](https://clawhub.ai/user/jaylane)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to resolve Context7 library IDs and retrieve current API documentation, setup guidance, configuration details, and code examples for a specific library or version.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Library names and documentation questions are sent to Context7.

Mitigation: Do not include confidential source details, customer data, internal URLs, secrets, credentials, or incident information in queries.

Risk: The security review flags the curl permission as broader than the skill's fixed Context7 API purpose requires.

Mitigation: Prefer a version that restricts curl to the Context7 search and context endpoints or only permits the bundled scripts.

Risk: The skill depends on internet access and Context7 API availability.

Mitigation: Validate retrieved documentation before relying on it and have a fallback when the service is unavailable or rate limited.

## Reference(s):

- [Context7 API Reference](references/API-REFERENCE.md)
- [Context7 Library ID Format](references/LIBRARY-ID-FORMAT.md)
- [Context7 API](https://context7.com/api)
- [Context7 API Search Endpoint](https://context7.com/api/search)
- [Context7 API Context Endpoint](https://context7.com/api/context)
- [Context7 Dashboard](https://context7.com/dashboard)
- [ClawHub Skill Page](https://clawhub.ai/jaylane/skills/context7-docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell command examples and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include library IDs, API documentation excerpts, version-specific guidance, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
