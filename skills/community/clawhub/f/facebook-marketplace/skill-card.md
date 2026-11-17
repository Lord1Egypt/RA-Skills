## Description:

Buy and sell on Facebook Marketplace with pricing discipline, safer messaging, shipping guardrails, scam detection, and account-safe workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for practical Facebook Marketplace buying and selling support, including listing quality, local pricing, safer messaging, pickup or shipping choices, scam screening, and account-health recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Marketplace notes may retain buying, selling, pricing, scam, and account-health context.

Mitigation: Ask before creating local memory, store only durable Marketplace context, and use stateless mode when persistence is declined.

Risk: Live Facebook or Messenger work can send listing, message, and transaction context to Meta.

Mitigation: Keep live Meta actions user-approved and limit external traffic to Facebook, Messenger, and Facebook Help endpoints.

Risk: Unsupported automation could create account-health or policy risk.

Mitigation: Refuse mass messaging, logged-in scraping at scale, auto-posting, repost farms, account farming, anti-detection, and restriction-bypass workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/facebook-marketplace)
- [Skill Homepage](https://clawic.com/skills/facebook-marketplace)
- [Facebook Marketplace](https://www.facebook.com)
- [Messenger](https://www.messenger.com)
- [Facebook Help](https://www.facebook.com/help)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with structured checklists, message drafts, pricing plans, and local memory templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Marketplace notes under ~/facebook-marketplace/ after user consent.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
