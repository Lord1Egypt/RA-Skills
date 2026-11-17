## Description:

Search Beepack for reusable API packages before coding. Saves tokens and time by reusing production-tested code instead of writing from scratch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[actabi](https://clawhub.ai/user/actabi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to search Beepack for reusable standalone JavaScript API packages before implementing integrations, utilities, or API clients. They can review package details and feedback, reuse package code, submit feedback, suggest fixes, and report issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer broad coding work toward a third-party registry.

Mitigation: Require explicit review before external Beepack requests and before adopting any Beepack package recommendation.

Risk: Remote package code and READMEs may be copied into a project.

Mitigation: Treat Beepack package content as untrusted third-party code and review, test, and scan it before use.

Risk: Feedback, suggestions, publication, or code-diff uploads may disclose project details.

Mitigation: Require user approval before submitting feedback, suggestions, reports, publication data, or code diffs to Beepack.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/actabi/skills/beepack-registry)
- [Beepack homepage](https://beepack.ai)
- [Beepack search API](https://beepack.ai/api/v1/search?q=what+you+need)
- [Beepack package details API](https://beepack.ai/api/v1/packages/{slug})
- [Beepack package feedback API](https://beepack.ai/api/v1/packages/{slug}/feedback)
- [Beepack package suggestions API](https://beepack.ai/api/v1/packages/{slug}/suggestions)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, guidance]

**Output Format:** [Markdown guidance with API request examples and copied package code when a package is selected.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party package README content, package code, feedback payloads, suggestion payloads, or publishing guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
