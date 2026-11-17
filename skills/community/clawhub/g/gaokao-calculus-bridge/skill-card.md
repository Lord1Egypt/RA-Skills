## Description:

Gaokao Calculus Bridge helps learners and educators connect 2026 Gaokao math reform themes with higher-math modeling practice for real-world, interdisciplinary problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daigxok](https://clawhub.ai/user/daigxok)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, and curriculum developers use this skill to analyze 2026 Gaokao math reform expectations, generate contextualized calculus and modeling problems, deconstruct long problem statements, map high-school concepts to college mathematics, design project-based learning, and recommend learning paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests API-key environment variables even though the security review describes the core content as educational and locally scoped.

Mitigation: Avoid providing API keys unless the publisher explains how they are used; run without credentials or in an isolated environment when possible.

Risk: The security review flags unused unpinned Python dependencies.

Mitigation: Install in an isolated environment and pin or remove dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daigxok/skills/gaokao-calculus-bridge)
- [ClawHub homepage metadata](https://clawhub.ai/daigxok/gaokao-calculus-bridge)
- [2026 Gaokao Math Reform Reference](references/gaokao_2026_reform.md)
- [Mathematical Modeling Templates](references/modeling_templates.md)
- [Real-World Case Library](references/real_world_cases.md)
- [PBL Project Guide](templates/project_guide.md)
- [Demo Problem: AI Model Training Optimization](assets/demo_problems/demo_problem_1.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, structured text, JSON-capable script output, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Python scripts and optional runtime configuration; educational outputs are intended for review before use.]

## Skill Version(s):

1.0.2 (source: server release metadata; skill frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
