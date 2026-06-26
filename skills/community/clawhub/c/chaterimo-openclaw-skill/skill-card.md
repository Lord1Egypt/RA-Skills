## Description: <br>
AI Customer Service for Shopify & E-commerce - Query conversations, analyze chatbot performance, and manage your Chaterimo AI assistant <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Caebixus](https://clawhub.ai/user/Caebixus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and e-commerce operators use this skill to connect an agent to Chaterimo, list chatbots, browse support conversations, and read redacted conversation transcripts for customer-service analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured API key may allow an agent to read Chaterimo chatbot and customer conversation data. <br>
Mitigation: Use a read-only, least-privilege API key and revoke it when no longer needed. <br>
Risk: Conversation text can contain sensitive customer information even when PII redaction is advertised. <br>
Mitigation: Avoid exposing API keys or returned conversation data in prompts or logs, and treat all returned transcripts as sensitive. <br>


## Reference(s): <br>
- [Chaterimo skill page](https://clawhub.ai/Caebixus/chaterimo-openclaw-skill) <br>
- [Chaterimo website](https://www.chaterimo.com) <br>
- [Chaterimo API keys](https://www.chaterimo.com/account/api-keys/) <br>
- [How to connect Chaterimo with Shopify](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration] <br>
**Output Format:** [Markdown responses with Chaterimo API query results and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CHATERIMO_API_KEY; returned conversation text should be treated as sensitive.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
