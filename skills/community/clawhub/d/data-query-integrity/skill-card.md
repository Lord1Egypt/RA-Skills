## Description:

Enforces data query integrity checks for API queries, summaries, and statistics by requiring pagination validation, source tracing, and tool-verified date and time conversions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyinli811-crypto](https://clawhub.ai/user/xiyinli811-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent queries APIs or summarizes returned records, especially calendar, document, and table data, to reduce omissions and fabricated fields caused by incomplete pagination or unsourced conversions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to run simple local date or time conversion commands when validating calendar or timestamp transformations.

Mitigation: Review proposed commands before execution and keep verification commands read-only, such as date conversion checks.

Risk: The source instructions are written in Chinese, which may reduce reviewer comprehension for operators who do not read Chinese.

Mitigation: Have a Chinese-reading reviewer confirm the workflow semantics before deployment or maintain an approved translation for operational review.

## Reference(s):

- [Detailed data query integrity workflow](references/workflow.md)
- [ClawHub skill page](https://clawhub.ai/xiyinli811-crypto/skills/data-query-integrity)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown guidance with optional inline shell commands for date and time verification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state query counts, pagination status, incomplete-data warnings, and field-level source limitations when relevant.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
