## Description:

Generate architecture diagrams and sequence diagrams as Mermaid code and PNG files, including system architecture, network topology, cloud infrastructure, API flows, authentication flows, CI/CD pipelines, and database flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opietaylor911](https://clawhub.ai/user/opietaylor911)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create editable Mermaid diagrams and rendered PNGs for architecture, network, cloud, microservice, API, authentication, CI/CD, and data-flow documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram contents may be sent to the third-party mermaid.ink renderer.

Mitigation: Use only for diagrams that are safe to send to mermaid.ink, or require a local renderer for confidential architecture, authentication, customer, host, IP, credential, or cloud-account details.

Risk: Users may misunderstand whether rendering is local or remote.

Mitigation: Disclose that PNG rendering uses mermaid.ink unless the skill is changed to use a local renderer.

## Reference(s):

- [Mermaid Architecture Diagram Patterns](references/architecture-patterns.md)
- [Mermaid Sequence Diagram Patterns](references/sequence-patterns.md)
- [Mermaid.ink Renderer](https://mermaid.ink/)
- [ClawHub Skill Page](https://clawhub.ai/opietaylor911/skills/ai-mermaid-diagrams)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with Mermaid code blocks and shell commands; generated .mmd and PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses mermaid.ink as a remote renderer and defaults rendered PNG width to 2048px.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
