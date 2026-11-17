## Description:

Creates causal diagrams and DAG visualizations as PNG images or Mermaid code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyhue1991](https://clawhub.ai/user/lyhue1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, researchers, and content authors use this skill to express variable-level causal relationships, DAGs, confounders, colliders, and backdoor-path examples as editable Mermaid diagrams or PNG illustrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PNG generation writes a file to a user-selected path.

Mitigation: Review the output path before running the command so generated diagrams do not overwrite important files.

Risk: The image generator depends on Pillow, which may not be installed in the agent environment.

Mitigation: Install Pillow in the intended runtime before using PNG output, or use Mermaid output when local image generation is unavailable.

Risk: Documentation and examples are primarily in Chinese.

Mitigation: Use this skill only when Chinese-language guidance is acceptable or have the agent translate user-facing instructions before use.

## Reference(s):

- [Causal Diagram Mermaid Syntax Reference](references/mermaid-syntax.md)
- [ClawHub Skill Page](https://clawhub.ai/lyhue1991/skills/caulsal-diagram)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown with Mermaid code blocks, shell commands, and optional PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PNG generation uses a local Pillow-based script and writes to the output path selected by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
