## Description: <br>
Generate architecture diagrams (network, system, cloud, microservices) and sequence diagrams (API flows, auth flows, data flows) as PNG files using Mermaid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpieTaylor911](https://clawhub.ai/user/OpieTaylor911) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn architecture, network, cloud, microservice, API, authentication, CI/CD, and data-flow requests into Mermaid source and rendered PNG diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram text is sent to the external mermaid.ink rendering service, which can expose sensitive architecture, credential, network, or authentication-flow details if included. <br>
Mitigation: Avoid secrets and confidential system details in diagrams rendered through mermaid.ink; use a local Mermaid renderer for confidential diagrams. <br>


## Reference(s): <br>
- [Architecture Patterns](artifact/references/architecture-patterns.md) <br>
- [Sequence Diagram Patterns](artifact/references/sequence-patterns.md) <br>
- [Mermaid.ink Renderer](https://mermaid.ink/) <br>
- [ClawHub Skill Page](https://clawhub.ai/OpieTaylor911/ai-mermaid-diagrams) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Mermaid code, shell commands, and saved .mmd/.png file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PNG rendering uses mermaid.ink at 2048px width by default; very wide diagrams may request a larger width.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
