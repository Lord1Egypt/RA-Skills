## Description:

Creator Skill V2 helps agents onboard to skill.deinai.ai and search influencers on TikTok, Instagram, and YouTube through authenticated MCP and REST workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deinai](https://clawhub.ai/user/deinai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to set up a paid skill.deinai.ai account, configure authenticated access, and find influencers or KOLs on TikTok, Instagram, and YouTube. It is intended for creator discovery workflows that require platform, query, location, subscription, and credit-status handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents through real subscription onboarding and payment flow.

Mitigation: Require the user to review the Stripe Checkout page, amount, and subscription terms before any billing step is completed.

Risk: Persistent sk_live_ API tokens can grant access to paid search functionality if exposed.

Mitigation: Treat tokens as secrets, avoid sharing them in logs or screenshots, use the shortest practical lifetime, and revoke or rotate tokens after suspected exposure.

Risk: Influencer searches consume paid credits based on returned rows.

Mitigation: Check account status before searching and keep initial page sizes small unless the user explicitly asks for more results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deinai/skills/creator-skill-v2)
- [Skill documentation](https://skill.deinai.ai/portal/docs/creator-skill-v2/SKILL.md)
- [Installation and authentication](references/install.md)
- [MCP tool contract](references/tools.md)
- [Onboarding workflow](references/onboarding.md)
- [Payment automation guidance](references/stripe-payment-automation.md)
- [Error handling](references/errors.md)
- [Online reference index](references/online-read.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown guidance with HTTP examples, shell commands, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces onboarding and search workflow guidance for a paid service; search calls consume credits based on returned influencer rows.]

## Skill Version(s):

2.0.6 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
