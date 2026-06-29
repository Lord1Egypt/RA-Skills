## Description: <br>
Read Rockwell / Allen-Bradley Logix controllers over EtherNet/IP (CIP) for controller identity, controller-scoped tag discovery, single and batch tag reads, and governed tag writes through the ot-aiops MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OT engineers use this skill to route EtherNet/IP tasks to the appropriate MCP tools for Logix controller discovery, tag reads, and change-controlled tag writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live PLC tag writes can alter production control behavior. <br>
Mitigation: Use dry-run first, verify the endpoint and tag, and apply writes only with explicit change-control approval. <br>
Risk: The documented write approval variable may need implementation confirmation before use. <br>
Mitigation: Confirm the ot-aiops implementation enforces the documented approval gate and standardize the approval variable before enabling writes. <br>
Risk: The release was validated with a mocked LogixDriver rather than live controllers. <br>
Mitigation: Test against a CIP/Logix simulator or non-production controller before use in operational environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/ethernetip-tap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON-shaped tool outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-first EtherNet/IP guidance with a high-risk write path that defaults to dry-run.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
