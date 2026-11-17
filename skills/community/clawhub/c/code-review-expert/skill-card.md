## Description:

Multi-agent code review system using Manager-Worker pattern. Provides comprehensive code analysis from syntax, logic, security, and performance perspectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banxian87](https://clawhub.ai/user/banxian87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate multi-perspective code review reports covering syntax, logic, security, and performance concerns. It is suited for pre-merge review support and remediation guidance, not as a sole security gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed source code may be sent to the configured LLM provider and should be treated as sensitive.

Mitigation: Use only approved LLM providers and logging environments, and avoid submitting proprietary code, secrets, or regulated data unless approved.

Risk: Generated review reports can be incomplete or influenced by source-code comments.

Mitigation: Use the report as reviewer assistance and keep independent human review, tests, and security checks in the release process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/banxian87/skills/code-review-expert)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Structured markdown report with severity-ranked findings, summaries, suggestions, and code examples; API usage returns a JavaScript review object.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include score, issues, summary, suggestions, and full report text.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
