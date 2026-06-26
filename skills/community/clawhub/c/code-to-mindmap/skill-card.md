## Description: <br>
Converts source code into visual mind maps, node graphs, and tree diagrams using Mermaid syntax. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn pasted source code or project structure into Mermaid diagrams that make classes, functions, modules, and dependencies easier to understand. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private source code or diagrams may be exposed if users paste Mermaid output into external rendering services. <br>
Mitigation: Render sensitive diagrams locally with a trusted Mermaid CLI and avoid external services for private code. <br>
Risk: An untrusted MMDC_PATH executable could run unexpected code during optional local rendering. <br>
Mitigation: Use a trusted Mermaid CLI installation and do not set MMDC_PATH to an untrusted executable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/code-to-mindmap) <br>
- [Metadata source](https://github.com/MiniMax-AI/skills) <br>
- [Reference index](references/index.md) <br>
- [Mermaid Live](https://mermaid.live) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Mermaid code blocks and optional shell commands for rendering diagrams.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Diagrams should stay grounded in the provided code and split large codebases into smaller diagrams when needed.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
