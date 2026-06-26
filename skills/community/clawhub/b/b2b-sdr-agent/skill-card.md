## Description: <br>
B2B SDR Agent is an OpenClaw template for automating B2B sales workflows across WhatsApp, Telegram, and email with lead discovery, qualification, follow-up, quoting, memory, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External-facing B2B sales teams and operators use this skill to run an AI SDR that captures inbound leads, qualifies prospects, researches companies, drafts multilingual outreach and quotes, and reports pipeline status across WhatsApp, Telegram, email, CRM, and memory systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment and workspace prompts may weaken execution approvals or enable broad automation. <br>
Mitigation: Review deploy scripts and workspace prompts on a test server first, and keep execution approvals interactive for production use. <br>
Risk: Customer-facing prompts may hide AI identity or create human-impersonation risk. <br>
Mitigation: Review and adjust customer communication prompts so the deployment follows the operator's disclosure and compliance requirements. <br>
Risk: Installer or runtime behavior may send silent telemetry. <br>
Mitigation: Disable silent telemetry before production deployment and document any required outbound reporting. <br>
Risk: The skill stores and retrieves customer data across CRM, memory, messaging, and vector search components. <br>
Mitigation: Restrict WhatsApp, Telegram, Gmail, CRM, and memory access to approved accounts, enable sensitive-data redaction, and set retention limits for customer data. <br>
Risk: Automatically installed helper skills may expand the agent's behavior beyond the core SDR workflow. <br>
Mitigation: Review every installed helper skill before enabling production outreach. <br>
Risk: Evidence flags wallet and purchase-related capabilities. <br>
Mitigation: Keep wallet, payment, and purchase credentials out of autonomous agent access and require human approval for any transaction. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ipythoning/b2b-sdr-agent) <br>
- [OpenClaw](https://openclaw.dev) <br>
- [Jina AI](https://jina.ai/) <br>
- [Graphify](https://github.com/safishamsi/graphify) <br>
- [MemOS API](https://api.openmem.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, shell commands, configuration snippets, CRM updates, outreach drafts, and quotation drafts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May interact with external messaging, CRM, memory, search, and deployment services when configured by the operator.] <br>

## Skill Version(s): <br>
3.6.0 (source: server release evidence and CHANGELOG, released 2026-04-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
