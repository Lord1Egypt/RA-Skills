## Description:

Generates and emails a daily Chinese biotech briefing with GitHub Trending repositories and recent WeChat article summaries for five biomedical topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxbjames](https://clawhub.ai/user/cxbjames)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to automate a daily biotech morning email that combines GitHub Trending repositories with filtered WeChat-sourced biomedical updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's verification workflow may load more environment secrets than needed for QQ Mail sending.

Mitigation: Load only QQMAIL_USER and QQMAIL_AUTH_CODE when sending or verifying mail.

Risk: Post-send verification may expose unrelated recent mailbox entries while checking delivery.

Mitigation: Use the narrowest feasible mailbox query or inspect only the expected subject and recipient.

Risk: The artifact contains conflicting guidance about using resolved WeChat article URLs versus Sogou redirect links.

Mitigation: Confirm link handling before sending and reject non-WeChat article URLs when the validation step requires mp.weixin.qq.com links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxbjames/skills/daily-biotech-briefing)
- [GitHub Trending](https://github.com/trending)
- [Email Template](references/email-template.md)
- [Article Filter Rules](references/filter-rules.md)
- [WeChat Search Topics](references/topics.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown email body with shell and Python command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a daily scheduled briefing and requires configured WeChat article search and QQ Mail credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
