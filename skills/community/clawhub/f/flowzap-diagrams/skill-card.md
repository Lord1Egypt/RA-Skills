## Description: <br>
Generate, validate and publish workflow, sequence and architecture diagrams using FlowZap Code DSL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flowzap-xyz](https://clawhub.ai/user/flowzap-xyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to turn natural-language workflow, sequence, process, and architecture requests into FlowZap Code diagrams and shareable playground links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated diagram text may be sent to FlowZap for validation or playground link creation. <br>
Mitigation: Avoid submitting secrets, tokens, private infrastructure details, or sensitive logs when using the MCP server. <br>


## Reference(s): <br>
- [FlowZap Code full spec](https://flowzap.xyz/flowzap-code) <br>
- [FlowZap MCP server docs](https://flowzap.xyz/docs/mcp) <br>
- [FlowZap Code syntax schema](https://flowzap.xyz/api/flowzap-code-schema.json) <br>
- [FlowZap Code syntax reference](references/syntax.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with FlowZap Code, installation commands, MCP configuration snippets, and shareable playground URLs when tools are available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [FlowZap Code should be returned as raw .fz content when showing the diagram.] <br>

## Skill Version(s): <br>
1.3.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
