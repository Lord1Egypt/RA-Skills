## Description: <br>
AI Customer Service for Shopify & E-commerce - Query conversations, analyze chatbot performance, and manage your Chaterimo AI assistant <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Caebixus](https://clawhub.ai/user/Caebixus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External e-commerce operators and support teams use this skill to inspect Chaterimo chatbots, browse redacted customer-service conversations, and review anonymized transcripts for Shopify, Shoptet, Upgates, and eshop-rychle.cz stores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent access to Chaterimo chatbot metadata and redacted customer conversation transcripts can expose sensitive support context if the API key is over-broad or mishandled. <br>
Mitigation: Use a least-privilege or read-only API key if available, keep it out of source control and shared logs, and rotate it if exposed. <br>
Risk: Unclear user requests may cause the agent to access the connected Chaterimo account when that was not intended. <br>
Mitigation: Phrase requests with "Chaterimo" when this skill should access the account, and review returned transcript content before sharing it outside the authorized context. <br>


## Reference(s): <br>
- [Chaterimo Website](https://www.chaterimo.com) <br>
- [Chaterimo API Keys](https://www.chaterimo.com/account/api-keys/) <br>
- [Shopify AI Customer Service Guide](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/) <br>
- [ClawHub Skill Listing](https://clawhub.ai/Caebixus/ai-customer-service-chatbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with occasional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns Chaterimo chatbot metadata and redacted conversation transcript summaries when authorized with CHATERIMO_API_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
