## Description:

代码 helps agents explain code logic with visual diagrams, analogies, architecture overviews, and review-oriented guidance for developers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, code reviewers, and educators use this skill to explain code snippets, functions, and repositories with visual diagrams, analogies, structured analysis, and improvement guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad shell and file-write authority can allow actions beyond normal code explanation.

Mitigation: Install only in a trusted or sandboxed agent environment, review proposed command and file changes before execution, or ask the publisher to narrow exec and write permissions.

Risk: The documented purpose is inconsistent and broader than a focused explain-code skill.

Mitigation: Use explicit code-explanation prompts, verify generated analysis before relying on it, and avoid applying generated commands, configuration, or edits without review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/explain-code-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured explanations, diagrams, JSON examples, and optional code or shell command blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include visual analogies, architecture summaries, review findings, improvement suggestions, and configuration steps.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
