## Description:

AI-powered error handling assistant that transforms fragile code into resilient systems by generating error handling, recovery strategies, and graceful degradation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supermario11](https://clawhub.ai/user/supermario11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze JavaScript or TypeScript code for missing or weak error handling and to generate try/catch blocks, retry logic, circuit breaker patterns, fallbacks, logging guidance, and coverage reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated handlers may log raw arguments, request bodies, headers, tokens, secrets, or payment fields.

Mitigation: Review generated logging before use and redact or omit sensitive fields.

Risk: Broad prompts may produce payment, authentication, or database code changes that need domain review.

Mitigation: Invoke the skill with exact paths and function names, and require human review before applying changes to high-impact code.

Risk: Regex-based analysis can miss or misclassify complex JavaScript or TypeScript control flow.

Mitigation: Treat coverage findings as review guidance and verify important functions manually or with project tests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supermario11/skills/cuihua-error-handler)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, shell command examples, and generated JavaScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; generated code and logging should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
