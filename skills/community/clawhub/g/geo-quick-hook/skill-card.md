## Description: <br>
Geo Quick Hook collects a client brand, competitors, and target keywords, then generates an HTML pre-sales comparison report that ranks the client against competitors across configured AI-answer endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanwenyolo-dot](https://clawhub.ai/user/hanwenyolo-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams, marketing consultants, and brand managers use this skill to create quick GEO pre-sales reports that compare a target brand with competitors for one or two sales keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer brand, competitor, and keyword data may be sent to external LLM-compatible endpoints. <br>
Mitigation: Use an approved, scoped LLM API key and avoid confidential customer data unless external processing is permitted. <br>
Risk: The workflow describes serving the Desktop directory over a local HTTP server and delivering a screenshot through Feishu. <br>
Mitigation: Disable or replace the Desktop-wide server flow and require explicit user confirmation before any Feishu delivery. <br>
Risk: The release presents a five-engine comparison, but the artifact uses the same LLM API configuration for all named engines unless separate providers are configured. <br>
Mitigation: Configure independent provider credentials per engine or clearly label the report as using a shared configured endpoint. <br>
Risk: Security evidence flags the release as suspicious because of overbroad sharing and potentially misleading report claims. <br>
Mitigation: Review the workflow before installation and scan the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub release: geo-quick-hook](https://clawhub.ai/hanwenyolo-dot/geo-quick-hook) <br>
- [Publisher profile: hanwenyolo-dot](https://clawhub.ai/user/hanwenyolo-dot) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, HTML file, Guidance] <br>
**Output Format:** [Interactive prompts, bash command examples, configuration instructions, and generated HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report is written as a local HTML file and may be shared through a screenshot delivery flow when explicitly approved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
