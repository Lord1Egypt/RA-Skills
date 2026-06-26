## Description: <br>
Provides shell helpers for provisioning AgentIzzy inbound AI phone agents, retrieving call history and captured leads, configuring webhooks, and checking usage through the AgentIzzy API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanhall00](https://clawhub.ai/user/ryanhall00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add inbound phone handling to agent workflows, provision AgentIzzy phone agents, retrieve call and lead data, configure webhooks, and route call transcripts, summaries, and sentiment into downstream systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access customer call recordings, transcripts, summaries, sentiment, and lead PII through the AgentIzzy API. <br>
Mitigation: Install only when AgentIzzy is trusted for this data, use a dedicated API key, and confirm legal authority, caller notice, consent, and retention requirements before use. <br>
Risk: Webhook configuration can send call and lead events to an external endpoint. <br>
Mitigation: Configure webhooks only to trusted HTTPS endpoints controlled by the deploying organization. <br>
Risk: Dedicated phone-number provisioning and billing checkout examples may create paid services or account changes. <br>
Mitigation: Require account-owner confirmation before phone-number provisioning or paid-plan checkout. <br>
Risk: The API key authorizes access to provisioned agents and associated call and lead data. <br>
Mitigation: Store AGENTIZZY_API_KEY as a secret, avoid logging it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanhall00/agentizzy-phone-agent) <br>
- [Publisher profile](https://clawhub.ai/user/ryanhall00) <br>
- [AgentIzzy API endpoint](https://api.agentizzy.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON API responses] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTIZZY_API_KEY, curl, and python3; calls AgentIzzy HTTPS API endpoints.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence; SKILL.md frontmatter says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
