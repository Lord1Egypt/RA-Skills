## Description:

Convert ASCII art diagrams to hand-drawn Excalidraw JSON files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn ASCII architecture, flow, and system diagrams into Excalidraw JSON files through an analysis, module generation, and merge workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated diagrams and intermediate module JSON may persist sensitive architecture or workflow details under ~/.excalidraw/.

Mitigation: Avoid processing sensitive diagrams unless local retention is acceptable, or delete the generated files after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyanbo2007/skills/ascii-excalidraw)
- [Publisher profile](https://clawhub.ai/user/zhangyanbo2007)
- [Excalidraw](https://excalidraw.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance plus Excalidraw JSON and module JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes final .excalidraw files and intermediate module JSON under ~/.excalidraw/ by default.]

## Skill Version(s):

1.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
