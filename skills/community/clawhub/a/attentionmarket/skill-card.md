## Description:

Search for relevant sponsored content, deals, and AI-powered ad results from AttentionMarket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aminambike](https://clawhub.ai/user/aminambike)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find and present sponsored deals, promotions, product recommendations, restaurant offers, and other commercial results from the AttentionMarket API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks the agent to handle account login credentials and store or use an API key.

Mitigation: Install only if the user trusts AttentionMarket and Supabase with the login flow and commercial queries; prefer a scoped API key or secure credential store instead of raw password handling.

Risk: The setup script writes AM_API_KEY to a local environment file and prints an export command containing the key.

Mitigation: Avoid printing secrets, enforce restrictive file permissions on credential files, and review local shell history and logs after setup.

Risk: Automatic activation can send broad commercial-intent queries to the AttentionMarket API.

Mitigation: Use explicit sponsored-deal requests where possible and review what query context is sent before making API calls.

## Reference(s):

- [AttentionMarket Dashboard](https://dashboard.attentionmarket.ai)
- [AttentionMarket Decide API Endpoint](https://peruwnbrqkvmrldhpoom.supabase.co/functions/v1/decide)
- [ClawHub Skill Page](https://clawhub.ai/aminambike/skills/attentionmarket)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with sponsored result summaries, links, and inline shell commands when setup or API calls are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should be labeled Sponsored and include returned click URLs when available.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
