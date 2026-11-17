## Description:

Track expenses via natural language, get spending summaries, set budgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

External users can log expenses, set budgets, and request spending summaries through natural-language messages. The skill is intended for personal expense tracking and budget awareness, not for regulated financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Expense descriptions, merchant-like details, dates, categories, and budget context are sent to the SkillBoss API.

Mitigation: Use the skill only with data appropriate for that service, and avoid entering financial account numbers, credentials, or other highly sensitive financial information.

Risk: Expense records and budgets persist in SkillBoss KV storage across sessions.

Mitigation: Confirm the publisher's retention and deletion controls before using the skill for sensitive or long-lived financial records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abe-expense-tracker-pro)
- [SkillBoss API endpoint](https://api.heybossai.com/v1)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text responses with JSON-formatted parsed expense actions when logging expenses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include logged expense confirmations, spending summaries, budget checks, and report text.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
