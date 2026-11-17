## Description:

Brevo is an email marketing API skill for managing contacts, lists, transactional emails, campaigns, subscriptions, and email automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujesyoga](https://clawhub.ai/user/yujesyoga)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to guide Brevo API work such as contact imports, list management, transactional email sends, campaign creation, and subscription-aware automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The contact-import guidance can fail open and may re-add unsubscribed users to mailing lists.

Mitigation: Add fail-closed error handling for blacklist retrieval and block imports whenever unsubscribe status cannot be confirmed.

Risk: The skill can guide send, import, update, and delete actions against a Brevo account.

Mitigation: Use a least-privilege API key and require human review before executing account-changing API calls.

## Reference(s):

- [ClawHub Brevo skill page](https://clawhub.ai/yujesyoga/skills/brevo)
- [Brevo API base URL](https://api.brevo.com/v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Brevo API key and human review before send, import, update, or delete actions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
