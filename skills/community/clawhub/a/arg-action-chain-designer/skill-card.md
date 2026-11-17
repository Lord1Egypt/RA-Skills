## Description:

Use this skill when the user wants to create, refine, review, or convert an agent task or existing skill into an ARG Action Chain / ARG 行动链路.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhgd3250905](https://clawhub.ai/user/mhgd3250905)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to turn vague agent tasks, recurring automations, existing skills, and multi-step workflows into bounded ARG action chains with Step Contracts, progressive disclosure, validation gates, and failure handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated validation scripts, shell commands, or Bash-enabled runtime chains may be unsafe or incorrect if executed without review.

Mitigation: Review generated scripts and commands before execution, especially file-writing, cleanup, external action, or Bash-enabled steps.

Risk: ARG chains can give a false sense of security when the same execution agent can skip steps, forge outputs, or self-attest validation.

Mitigation: Use external gates, human review, or independent-agent review for workflows that require stronger assurance than ordinary Level 1 ARG constraints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mhgd3250905/skills/arg-action-chain-designer)
- [README](artifact/README.md)
- [Output Modes](artifact/references/output-modes.md)
- [Reliability Levels](artifact/references/reliability-levels.md)
- [Runtime Template](artifact/references/runtime-template.md)
- [Step Contract Standard](artifact/references/step-contract-standard.md)
- [Validation and Judgment](artifact/references/validation-and-judgment.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with optional file-level skill drafts, Step Contract plans, validation scripts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Chinese-language ARG workflow designs and file-level deliverables when requested by the user.]

## Skill Version(s):

1.2.4 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
