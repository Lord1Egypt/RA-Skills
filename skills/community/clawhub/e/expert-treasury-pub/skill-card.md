## Description:

资金与票据专家 routes pasted treasury or bill tables to one of 12 local checking skills and returns line-by-line, reproducible findings, while reporting missing columns instead of guessing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, treasury, and operations users paste table headers and rows to classify and check banking acceptance bills, loan interest, cash-flow variance, discount interest, guarantee letters, installments, and related treasury workflows. The skill is intended for local review support and produces reproducible findings with source row references when the supplied material is sufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged as suspicious because it under-discloses a persistent local trial counter and subscription gate.

Mitigation: Review the free-use and subscription behavior before installation, and expect local state to be written in the user's home directory during use.

Risk: The release may run broader bundled treasury-pack checks or aggregation than the main skill page makes clear.

Mitigation: Use explicit sub-skill selection for focused reviews, inspect the reported selected sub-skill and unexecuted checks, and avoid treating a clean result as a full audit.

Risk: Financial table checks can be incomplete when headers, parameters, or source rows are missing or ambiguous.

Mitigation: Provide complete headers and rows, review missing-column messages, and independently verify any material finance or compliance decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-treasury-pub)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON results from local command-line execution, with Markdown documentation and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results identify the selected sub-skill, include line-level findings when available, and report missing inputs or unexecuted checks.]

## Skill Version(s):

1.0.10 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
