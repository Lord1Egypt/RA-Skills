## Description:

AI Customer Service for Shopify & E-commerce - Query conversations, analyze chatbot performance, and manage your Chaterimo AI assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caebixus](https://clawhub.ai/user/caebixus)

### License/Terms of Use:


## Use Case:

External e-commerce operators and support teams use this skill to query Chaterimo chatbots, browse recent customer conversations, read transcripts, and analyze chatbot support activity across supported store platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read chatbot configuration and customer conversation content from the connected Chaterimo account.

Mitigation: Install only where Chaterimo is trusted with this data, and use a scoped, revocable API key where possible.

Risk: Conversation outputs may still contain sensitive business or customer context even when PII redaction is applied.

Mitigation: Limit access to authorized users and review generated summaries before sharing them outside approved systems.

## Reference(s):

- [Chaterimo website](https://www.chaterimo.com)
- [Chaterimo API keys](https://www.chaterimo.com/account/api-keys/)
- [Shopify AI customer service guide](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/)
- [ClawHub skill page](https://clawhub.ai/caebixus/skills/chaterimo-openclaw-skill)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown responses with API-derived chatbot and conversation summaries plus setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHATERIMO_API_KEY for account-scoped read access.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
