## Description: <br>
Monitor and manage Flowtriq DDoS detection in real time using the Flowtriq API for active attacks, node status, incident history, traffic metrics, PCAP captures, agent config, and mitigation status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacob-masse](https://clawhub.ai/user/jacob-masse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators, developers, and network operations teams use this skill to query Flowtriq-monitored infrastructure, summarize DDoS incidents, inspect node configuration, and interpret attack telemetry in plain language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive Flowtriq operational data for the configured node. <br>
Mitigation: Use a least-privileged Flowtriq key and avoid sharing generated outputs in public or shared contexts. <br>
Risk: The skill includes write and provisioning paths such as incident creation or updates, PCAP upload, and node registration. <br>
Mitigation: Require explicit user confirmation before any POST action and keep deploy tokens separate from node API keys. <br>
Risk: API credentials and node identifiers are required for authenticated Flowtriq access. <br>
Mitigation: Provide FLOWTRIQ_API_KEY and FLOWTRIQ_NODE_UUID through environment configuration and rotate keys that are expired, overprivileged, or exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jacob-masse/flowtriq) <br>
- [Flowtriq API Endpoints Reference](references/api-endpoints.md) <br>
- [Flowtriq Attack Types Reference](references/attack-types.md) <br>
- [Flowtriq platform](https://flowtriq.com) <br>
- [Flowtriq dashboard](https://flowtriq.com/dashboard) <br>
- [Flowtriq API rate limits](https://flowtriq.com/docs?section=rate-limits) <br>
- [Flowtriq API error reference](https://flowtriq.com/docs?section=errors) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration guidance] <br>
**Output Format:** [Markdown summaries with JSON/API details and inline shell commands when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require FLOWTRIQ_API_KEY and FLOWTRIQ_NODE_UUID; POST actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
