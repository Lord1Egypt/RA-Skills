## Description:

Maintains an AWAR-style robotics World-Action Model repository by helping agents collect, analyze, classify, and generate Chinese-language documentation with technical explanations, quick-start guidance, diagrams, benchmarks, and repository maintenance rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessy-huang](https://clawhub.ai/user/jessy-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical writers use this skill to maintain a robotics AI knowledge repository focused on World Models, Action Models, VLA systems, RT-2, Dreamer, and related WAM research. It guides systematic discovery, technical decomposition, classification, and standardized Markdown documentation for new projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated quick-start commands or configuration snippets may be copied into a robotics project without review.

Mitigation: Review generated commands and configuration before execution, especially installation, cloning, evaluation, and hardware-related steps.

Risk: The skill is optimized for Chinese-language AWAR documentation and may not match a user's preferred language or local terminology.

Mitigation: Ask the agent to use another language or terminology style when maintaining repositories for a different audience.

Risk: Documentation-oriented analysis may introduce inaccurate benchmarks or misleading project comparisons if source materials are incomplete.

Mitigation: Check benchmark values, paper claims, and project status against primary sources before publishing generated repository updates.

## Reference(s):

- [AWAR skill page](https://clawhub.ai/jessy-huang/skills/awar-maintenance)
- [Getting Started](artifact/references/getting_started.md)
- [Deep Analysis Protocol](artifact/references/awareness_analysis_framework.md)
- [Classification Standard](artifact/references/classification_standard.md)
- [Project Documentation Output Template](artifact/references/output_template.md)
- [AWAR Asset Guide](artifact/assets/README.md)
- [LeRobot](https://github.com/huggingface/lerobot)
- [DMC-GPT](https://github.com/jdenysg/dmc-gpt)
- [Diffusion Policy](https://github.com/columbia-robovision/DiffusionPolicy)
- [OpenVLA](https://github.com/openvla/openvla)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, Mermaid diagrams, inline code snippets, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language documentation output; generated quick-start commands should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
