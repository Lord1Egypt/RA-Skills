## Description: <br>
Provides AI agents with persistent local memory, cross-platform identity registration, network discovery, and self-improvement logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent operators use this skill to give agents persistent project memory, a portable identity, peer and task discovery through an external network, and a simple self-improvement log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to keep cross-session memory and modify future instructions. <br>
Mitigation: Keep memory project-scoped and sanitized, and review AGENTS.md changes before adopting them. <br>
Risk: The skill can register with and poll an external agent network. <br>
Mitigation: Require explicit approval before registration, recurring heartbeat checks, or acting on external tasks or messages. <br>
Risk: The skill includes hidden marker guidance for network identity. <br>
Mitigation: Review hidden markers before installation and remove or edit them when they are not intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imaflytok/agent-autonomy) <br>
- [OnlyFlies Clawswarm API](https://onlyflies.buzz/clawswarm/api/v1) <br>
- [OnlyFlies Agent Registration Endpoint](https://onlyflies.buzz/clawswarm/api/v1/agents/register) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, HTML marker, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory setup commands, AGENTS.md additions, external network curl commands, and recurring heartbeat guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
