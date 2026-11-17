## Description:

Helps agents inspect CSV/XLSX files, preview rule-based cleaning changes, and execute only after the user confirms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

People cleaning CSV or XLSX data use this skill to inspect a file, review the expected impact of explicit cleaning rules, and receive a cleaned file and audit summary after confirming execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files are uploaded to the service for processing and may contain sensitive data.

Mitigation: Upload only files the user approves and share private result links only with that user.

Risk: Cleaning rules can change data unexpectedly if the preview is misunderstood.

Mitigation: Show rules, affected counts, and representative samples; execute only after explicit user confirmation.

Risk: A shared platform API key can be reused across skills.

Mitigation: Use the product-specific API key when credential isolation is needed, and never expose full keys in conversation or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youteacher/skills/data-cleaning)
- [AI Skills platform](https://ai-skills.open-idea.net)
- [API key configuration and pricing](https://ai-skills.open-idea.net/skill-docs/data-cleaning/API-KEY.md)
- [HTTP requests and task polling](https://ai-skills.open-idea.net/skill-docs/data-cleaning/HTTP-REQUESTS.md)
- [Cleaning operations and rules](https://ai-skills.open-idea.net/skill-docs/data-cleaning/OPERATIONS.md)
- [Safety and confirmation rules](https://ai-skills.open-idea.net/skill-docs/data-cleaning/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [Guidance, Files, Audit summaries]

**Output Format:** [Markdown guidance and audit summary with private CSV/XLSX file artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows sample changes and affected counts before execution; delivers files only after explicit user confirmation.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
