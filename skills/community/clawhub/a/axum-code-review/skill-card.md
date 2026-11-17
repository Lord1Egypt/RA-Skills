## Description:

Reviews axum web framework code for routing patterns, extractor usage, middleware, state management, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Rust Axum services for routing, extractor ordering, state handling, middleware, and response/error handling issues before submitting findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill prompts an agent to read project code and produce review findings, so unsupported or stale evidence could lead to misleading results.

Mitigation: Require each finding to cite the current file and line and to pass the skill's documented review gates before reporting.

Risk: The skill may rely on a separate review-verification-protocol skill when available, which can affect the depth of category-specific checks.

Mitigation: Confirm whether the companion verification protocol is available and document any review categories that could not be checked with it.

## Reference(s):

- [Axum Code Review skill page](https://clawhub.ai/anderskev/skills/axum-code-review)
- [Routing reference](references/routing.md)
- [Extractors reference](references/extractors.md)
- [Middleware reference](references/middleware.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review findings with file and line citations, severity, and concise issue descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are gated on reading current project files and matching category-specific review checks before reporting.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
