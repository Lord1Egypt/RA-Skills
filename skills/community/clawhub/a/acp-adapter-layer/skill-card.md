## Description: <br>
ACP (Agent Control Protocol) Adapter Layer for AI Native Full-Stack Software Factory - provides seamless integration between ASF multi-agent workflows and OpenClaw's ACP protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alshowse-tech](https://clawhub.ai/user/alshowse-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect ACP-capable IDEs with ASF and OpenClaw workflows for session management, prompt routing, and tool protocol conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The adapter bridges IDE clients to local OpenClaw gateway sessions and tools, which may expose write or destructive tools through the IDE workflow. <br>
Mitigation: Confirm trust in the local OpenClaw gateway and review the ASF/OpenClaw tools exposed to the IDE before installing or enabling the adapter. <br>
Risk: Gateway tokens or credentials could be exposed if hard-coded, logged, or stored insecurely. <br>
Mitigation: Store gateway tokens securely and avoid logging or hard-coding real credentials. <br>


## Reference(s): <br>
- [ACP Specification](https://agentclientprotocol.com/) <br>
- [ClawHub skill page](https://clawhub.ai/alshowse-tech/acp-adapter-layer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Structured Markdown with TypeScript and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces adapter design guidance, protocol mappings, session and tool conversion examples, and configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
