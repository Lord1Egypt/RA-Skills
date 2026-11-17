## Description:

ClawVision turns an explicitly selected OpenClaw chat session into exportable visual summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monaxamo](https://clawhub.ai/user/monaxamo)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use ClawVision to summarize a confirmed chat session as a visual, shareable report with HTML, PNG, Markdown, and PowerPoint exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads session history and writes persistent local export files.

Mitigation: Install only if that access is acceptable, and avoid use on conversations containing secrets, credentials, personal data, or internal identifiers.

Risk: Generated HTML can persist unsafe model-controlled content that may run script when opened or screenshotted.

Mitigation: Treat exported HTML as untrusted until checklist status fields are validated or escaped and a restrictive content policy is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/monaxamo/skills/clawvision-publish-107)
- [Project homepage](https://github.com/monaxamo/clawvision)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance plus generated HTML, PNG images, Markdown, and PowerPoint files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs are local export files derived from a user-confirmed session summary.]

## Skill Version(s):

1.0.7 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
