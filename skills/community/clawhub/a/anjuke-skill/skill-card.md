## Description:

Anjuke Skill helps agents automate Anjuke account operations, including login, listing capacity checks, real estate listing publication, and description optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuapi2020](https://clawhub.ai/user/chuapi2020)

### License/Terms of Use:

MIT-0

## Use Case:

External real estate operators and agents use this skill to guide Anjuke broker account login, check remaining listing capacity, publish listings, and improve low-performing listing descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to store passwords, phone numbers, names, and identity-card digits in Markdown skill files.

Mitigation: Remove persistent secret-storage instructions and collect sensitive account or identity details only through approved runtime credential handling.

Risk: The skill can publish or modify real estate listing content with weak safeguards.

Mitigation: Require explicit user approval, source facts, and human review before content is written, optimized, or published.

## Reference(s):

- [Login Your Account](references/login_your_account.md)
- [Optimize Description](references/optimize_description.md)
- [Publish House](references/publish_house.md)
- [Push House](references/push_house.md)
- [ClawHub Skill Page](https://clawhub.ai/chuapi2020/skills/anjuke-skill)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown-style operational guidance for browser-based workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided account details and explicit review before login, listing publication, or listing content changes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
