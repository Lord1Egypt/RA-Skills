## Description: <br>
Guarded DeFi orchestration layer for OpenClaw agents. Lists named multi-skill workflow recipes, builds quality gates, creates session-scoped workflow run records, and reports workflow status. Trail Marshal holds no keys and performs no on-chain action; every state-changing step remains delegated to the user's separately-installed execution skill under that skill's own confirmation gate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw agents use this skill to list FarmDash DeFi workflow recipes, check which companion skills are available, plan quality gates, and record guarded session workflow status before any separate execution skill asks the user for approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates in a DeFi planning context and may use FarmDash session tokens and public wallet identifiers for run records. <br>
Mitigation: Use it as a workflow planning layer only, keep private keys, seed phrases, wallet exports, and signed transactions out of the skill, and review companion execution skills separately. <br>
Risk: A planned workflow may include trading, swapping, bridging, deposits, or perps actions handled by separately installed companion skills. <br>
Mitigation: Require the owning execution skill to present fresh data and obtain explicit user confirmation for each state-changing step before any action is taken. <br>
Risk: Missing companion skills can make a workflow only partially available or analysis-only. <br>
Mitigation: Classify available, missing, and state-changing steps before presenting a workflow as executable, and continue only with the safe subset when required skills are absent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parmasanandgarlic/farmdash-trail-marshal) <br>
- [Publisher Profile](https://clawhub.ai/user/parmasanandgarlic) <br>
- [FarmDash Agent Hub](https://www.farmdash.one/agents) <br>
- [FarmDash MCP Configuration](https://www.farmdash.one/.well-known/mcp.json) <br>
- [FarmDash OpenAPI Specification](https://www.farmdash.one/agents/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with JSON examples and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns workflow catalog, planning classifications, guarded run records, and workflow status guidance; it does not produce signed transactions or execute on-chain actions.] <br>

## Skill Version(s): <br>
0.1.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
