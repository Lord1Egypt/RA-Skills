## Description: <br>
AI-powered customer support agent for fintech and remittance products that handles transfer status lookups, refund requests, account suspensions, KYC document guidance, and complaint escalation across messaging channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gameotivity](https://clawhub.ai/user/gameotivity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External support and operations teams use this skill to triage and answer fintech or remittance customer requests, look up transaction and account state, guide KYC completion, and prepare human escalations with context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access, store, transmit, and modify sensitive customer financial support data. <br>
Mitigation: Deploy only in a controlled support environment with verified customer identity, least-privilege API keys, approved webhook destinations, and a retention/deletion policy for local ticket memory. <br>
Risk: Refund, recall, dispute, and account-impacting flows may affect customers financially or operationally. <br>
Mitigation: Require human confirmation or equivalent authorization before running account-impacting actions. <br>
Risk: Customer messages may be sent to an external LLM provider for intent classification. <br>
Mitigation: Disclose external processing where required and ensure the configured LLM provider is approved for the support data being processed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gameotivity/fintech-customer-support) <br>
- [Project homepage](https://github.com/nabeel/fintech-support-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain-language support replies, structured handler text, markdown weekly digests, and setup commands/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handler output should be reviewed before customer-facing use when it affects refunds, disputes, account status, KYC, or escalations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
