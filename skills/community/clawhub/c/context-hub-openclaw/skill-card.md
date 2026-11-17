## Description:

Use Context Hub (chub) to fetch versioned API docs/skills before coding, then persist learnings with annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[victorlin-houzz](https://clawhub.ai/user/victorlin-houzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to fetch current API, SDK, and integration documentation before implementation, then capture concise annotations for reusable project knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or rely on an unpinned Context Hub CLI.

Mitigation: Install only from a trusted Context Hub CLI source and consider pinning the package version in controlled environments.

Risk: Annotations can send project-derived text to an external Context Hub.

Mitigation: Review and sanitize annotations before use, excluding secrets, private code, customer data, internal URLs, request bodies, and environment-specific identifiers.

## Reference(s):

- [Context Hub GitHub Repository](https://github.com/andrewyng/context-hub)
- [Context Hub CLI npm Package](https://www.npmjs.com/package/@aisuite/chub)
- [ClawHub Skill Listing](https://clawhub.ai/victorlin-houzz/skills/context-hub-openclaw)
- [ClawHub Publisher Profile](https://clawhub.ai/user/victorlin-houzz)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON output from chub commands and local project notes.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
