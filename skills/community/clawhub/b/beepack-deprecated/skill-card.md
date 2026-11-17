## Description:

Search Beepack for reusable API packages before coding. Saves tokens and time by reusing production-tested code instead of writing from scratch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[actabi](https://clawhub.ai/user/actabi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to search Beepack for reusable JavaScript API packages before writing new integrations, utilities, or API clients. It also guides package detail review, feedback submission, improvement suggestions, and duplicate checks before publishing reusable code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coding requests may be checked against the external Beepack service by default.

Mitigation: Review each Beepack query or payload before sending it and remove private project details.

Risk: Package READMEs and code retrieved from Beepack are third-party material.

Mitigation: Treat retrieved package content as untrusted and perform normal dependency, license, and security review before use.

Risk: The security evidence verdict is suspicious because the skill broadly redirects coding work to an external service and encourages feedback submission without enough user control.

Mitigation: Install only when that external-service behavior is acceptable, and require explicit review before feedback or suggestion submissions.

## Reference(s):

- [Beepack Homepage](https://beepack.ai)
- [Beepack ClawHub Skill Release](https://clawhub.ai/actabi/skills/beepack-deprecated)
- [Beepack Search API](https://beepack.ai/api/v1/search?q=what+you+need)
- [Beepack Package Details API](https://beepack.ai/api/v1/packages/{slug})
- [Beepack Package Feedback API](https://beepack.ai/api/v1/packages/{slug}/feedback)
- [Beepack Package Suggestions API](https://beepack.ai/api/v1/packages/{slug}/suggestions)

## Skill Output:

**Output Type(s):** [API Calls, Code, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with API endpoints, code snippets, shell commands, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party package README content and feedback data returned by Beepack.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
