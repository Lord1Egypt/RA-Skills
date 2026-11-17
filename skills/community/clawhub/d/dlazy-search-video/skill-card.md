## Description:

Video search tool: queries Pixabay video API by keywords and returns stock video URLs and metadata for footage sourcing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search for stock video footage by keyword, narrow results by type, category, or duration, and use the returned URLs and metadata in their projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and did not establish the dLazy CLI's authentication behavior or confirm how it supports video search; it also flagged authentication and CLI guidance that does not clearly match the stated purpose.

Mitigation: Review and trust the dLazy CLI and its authentication flow before installing. Confirm the command and options against trusted package documentation, and keep API keys private and revocable.

## Reference(s):

- [dLazy CLI project homepage](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [JSON, Video URLs, Video metadata]

**Output Format:** [JSON returned by the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports result filtering and pagination; an optional flag can download a result asset to a local path.]

## Skill Version(s):

1.3.42 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
