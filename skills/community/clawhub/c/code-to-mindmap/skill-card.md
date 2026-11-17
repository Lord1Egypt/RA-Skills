## Description:

Converts source code into Mermaid-compatible mind maps, node graphs, and tree diagrams so users can visualize code structure and relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn source code, snippets, or project structures into concise Mermaid diagrams for code review, onboarding, and architecture understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional diagram rendering depends on local Mermaid tooling or an external Mermaid rendering service.

Mitigation: Use a trusted local Mermaid CLI when possible and pin or lock renderer dependencies before use.

Risk: Diagrams generated from private source code may expose sensitive structure if pasted into a public or third-party renderer.

Mitigation: Avoid sending diagrams derived from private code to mermaid.live unless the content has been approved and sanitized.

## Reference(s):

- [Code To Mindmap on ClawHub](https://clawhub.ai/wangjipeng977/skills/code-to-mindmap)
- [Skill metadata source](https://github.com/MiniMax-AI/skills)
- [Reference index](references/index.md)
- [Mermaid Live](https://mermaid.live)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Mermaid code blocks and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits diagrams to about 30 nodes and may split larger codebases into multiple diagrams.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
