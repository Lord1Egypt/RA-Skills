## Description: <br>
Guides users through deploying an AI receptionist or customer service agent with Solvea, including account setup, agent creation, knowledge-base upload, testing, and channel deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AntiMoron](https://clawhub.ai/user/AntiMoron) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators and support teams use this skill to walk through creating a Solvea AI receptionist, loading business knowledge, testing responses, and deploying the agent across customer-contact channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow directs users into a third-party Solvea signup flow and may involve uploading business support documents. <br>
Mitigation: Verify the solvea.cx domain, pricing, terms, retention, and access controls before use; start with test or low-sensitivity knowledge-base content. <br>
Risk: The deployment steps can connect email, phone, Shopify, Google Calendar, or Google Sheets channels that may expose customer data or grant broad account access. <br>
Mitigation: Use limited test accounts or least-privilege permissions first, review requested integration scopes, and confirm the setup is appropriate before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AntiMoron/ai-receptionist) <br>
- [Solvea registration](https://app.solvea.cx/#/auth/register) <br>
- [Solvea knowledge base](https://app.solvea.cx/?personaId={agentId}#/knowledge/knowledgeManage) <br>
- [Solvea agent testing](https://app.solvea.cx/?personaId={agentId}#/agent) <br>
- [Solvea integrations](https://app.solvea.cx/?personaId={agentId}#/deploy/integration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Step-by-step browser-opening workflow that waits for user confirmation between stages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
