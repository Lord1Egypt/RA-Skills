## Description:

AI Compliance Review is a pay-per-use assistant that reviews Chinese marketing, privacy, finance, labor, and ecommerce text for compliance risks and returns cited issues and revision suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g620710](https://clawhub.ai/user/g620710)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit business copy, policy text, financial marketing, labor documents, or ecommerce listings for AI-assisted compliance review. The skill returns risk levels, legal references, and suggested edits for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary reports that documentation and executable behavior disagree about where sensitive documents and credentials are sent.

Mitigation: Review the shipped script before installation and require publisher documentation of the actual service operator, destination, retention policy, and credential model.

Risk: The authoritative security guidance identifies a plaintext HTTP default endpoint.

Mitigation: Do not use the skill with confidential, personal, employee, legal, financial, or customer data unless a reviewed version requires HTTPS for all uploads.

Risk: The artifact can send submitted review text and user keys to an external compliance-review service.

Mitigation: Use non-sensitive test data first, require explicit confirmation before upload, and align user documentation with the shipped executable behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g620710/skills/ai-compliance-review)
- [DeepSeek API endpoint referenced by artifact documentation](https://api.deepseek.com/v1)
- [Default compliance API endpoint referenced by shipped script](http://47.109.39.255:8765/api/v4)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Plain text compliance reports, with artifact documentation also describing Markdown and JSON report formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include risk levels, cited legal references, issue descriptions, remaining account credits, and suggested revisions.]

## Skill Version(s):

1.1.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
