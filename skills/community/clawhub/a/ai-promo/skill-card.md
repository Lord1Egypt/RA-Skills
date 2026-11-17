## Description:

AI Promo helps agents query, submit, and manage subscriptions for large-model platform promotion information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[destinyd](https://clawhub.ai/user/destinyd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use AI Promo to find categorized large-model platform promotions, submit new offers for review, and manage daily promotional notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts cli.aipromo.workers.dev and can submit user-provided promotion data.

Mitigation: Review the service endpoint and submitted fields before use, and avoid sending private or sensitive promotion data.

Risk: The skill stores a stable local user ID and subscription records in the user's home directory.

Mitigation: Inspect or delete ~/.promo_user_id and ~/.promo_subscribers.json when tracking or subscription persistence is not desired.

Risk: Daily push behavior may be enabled through cron-style scheduling.

Mitigation: Review, disable, or remove any cron configuration before installation if recurring notifications are not desired.

Risk: Some links are referral-style promotional links.

Mitigation: Review destination URLs and referral implications before using or sharing them.

## Reference(s):

- [AI Promo ClawHub listing](https://clawhub.ai/destinyd/skills/ai-promo)
- [AI Promo API](https://cli.aipromo.workers.dev)
- [AI Promo landing page](https://cli.aipromo.workers.dev/landing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with shell command examples and promotion links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remote API results, locally cached fallback data, user IDs, subscription status, submitted promotion details, and referral-style links.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
