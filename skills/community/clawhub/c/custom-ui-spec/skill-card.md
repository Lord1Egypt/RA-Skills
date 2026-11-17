## Description:

Custom UI Spec helps agents generate and review highly customized UI implementations with Apple HIG, Microsoft Fluent, and Google Material Design guidance for headless component libraries such as shadcn/ui and Radix UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-focused agents use this skill to choose an Apple HIG, Microsoft Fluent, Google Material, or combined design posture, generate custom UI code with headless components, and review UI implementations against specification checklists and static validation output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled demo HTML pages contain unsafe example JavaScript and filename rendering patterns that could be risky if hosted with sensitive authenticated applications.

Mitigation: Use the demo pages as local examples only, or fix the unsafe rendering before deploying them on any privileged origin.

Risk: Static UI validation can miss design, accessibility, and interaction issues that require human judgment.

Mitigation: Pair validator results with checklist-based manual review before relying on generated or reviewed UI code.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fize/skills/custom-ui-spec)
- [Apple Human Interface Guidelines](references/apple-hig.md)
- [Microsoft Fluent Design System](references/microsoft-fluent.md)
- [Google Material Design 3](references/google-material.md)
- [Component Unified Specification and Comparison](references/component-specs.md)
- [Interaction Guidelines Comparison](references/interaction-guidelines.md)
- [UI Design Specification Validation Checklist](references/checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance, generated UI code, shell commands, and JSON or Markdown validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The validator accepts file or text input, supports HIG, Fluent, Material, or all modes, and skips color checks unless requested.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
