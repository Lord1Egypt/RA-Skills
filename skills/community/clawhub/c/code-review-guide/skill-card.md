## Description:

Review a pull request or diff like a thoughtful senior engineer: prioritized, kind, and focused on correctness, security, design, tests, readability, severity-ranked comments, and a clear verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review pull requests or diffs with prioritized feedback. It helps agents identify correctness, security, design, testing, and readability issues while providing severity-ranked comments and a clear approve, request-changes, or comment verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked broadly by phrases such as 'review this change' and shape the agent's code-review response.

Mitigation: Confirm that code-review guidance is intended before applying it to unrelated requests.

Risk: Code-review output can be incomplete or misleading if the provided diff lacks project context, test expectations, or risk areas.

Mitigation: Ask for missing context and treat high-impact findings as review recommendations that need developer verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/code-review-guide)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/code-review-guide.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review with summary, prioritized findings table, strengths, and verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the user-provided diff or pull request context; may ask for language, stack, conventions, risk level, or review focus when missing.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
