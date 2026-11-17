## Description:

轻量级图表生成工具，支持 Mermaid 格式流程图与序列图的快速创建与编辑。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation authors use this skill to turn natural-language descriptions into Mermaid flowcharts and sequence diagrams for Markdown documentation. It can also help read and update existing .mmd diagram files when the host agent grants file and command access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may receive read, exec, and browser capabilities beyond basic diagram text generation.

Mitigation: Grant tool access only in trusted diagram or documentation workspaces and approve shell, npm/npx, network, and file-writing actions deliberately.

Risk: Generated Mermaid diagrams can be incomplete, misleading, or syntactically invalid for complex workflows.

Mitigation: Review the generated diagram, validate Mermaid rendering, and split complex flows into smaller diagrams before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/diagram-gen-tool-free)
- [Mermaid documentation](https://mermaid.js.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Mermaid code blocks and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for direct use in Markdown or .mmd files; image export depends on optional Mermaid CLI tooling.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
