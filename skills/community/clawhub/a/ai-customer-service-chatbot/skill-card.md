## Description:

AI Customer Service for Shopify & E-commerce - Query conversations, analyze chatbot performance, and manage your Chaterimo AI assistant

This skill is ready for commercial/non-commercial use.

## Publisher:

[caebixus](https://clawhub.ai/user/caebixus)

### License/Terms of Use:

MIT

## Use Case:

External e-commerce operators and support teams use this skill to inspect Chaterimo chatbots, browse redacted customer-service conversations, and review conversation transcripts for Shopify, Shoptet, Upgates, and eshop-rychle.cz stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads chatbot lists and redacted customer conversations through a user-provided Chaterimo API key.

Mitigation: Install only when the agent should have this access, scope keys to the minimum needed permissions, and revoke keys from the Chaterimo dashboard when access is no longer required.

Risk: Conversation analysis can still expose business-sensitive support patterns even when customer PII is redacted.

Mitigation: Review agent outputs before sharing them outside the intended support, analytics, or store operations audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caebixus/skills/ai-customer-service-chatbot)
- [Chaterimo website](https://www.chaterimo.com)
- [Chaterimo API keys](https://www.chaterimo.com/account/api-keys/)
- [How to connect Chaterimo with Shopify](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration]

**Output Format:** [Markdown responses with API-derived chatbot and conversation summaries plus setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CHATERIMO_API_KEY to read chatbot lists, chatbot details, conversation lists, and redacted conversation transcripts.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
