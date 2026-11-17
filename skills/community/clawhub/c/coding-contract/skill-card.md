## Description:

Generate language-agnostic coding contracts from requirements, producing interface signatures, behavioral constraints, and verification checklists without implementation code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dachunggan](https://clawhub.ai/user/dachunggan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to turn feature requirements or brainstorming notes into reusable Markdown coding contracts before implementation. It is intended for defining interfaces, constraints, test expectations, and engineering decisions across any technology stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write a new Markdown specification file to the workspace.

Mitigation: Specify the desired output path or ask for the spec in chat first when a file should not be created automatically.

Risk: A generated coding contract can encode incomplete or incorrect requirements if the input context is incomplete.

Mitigation: Review the generated spec.md before implementation and resolve open questions, placeholders, constraints, and verification checks.

## Reference(s):

- [Coding Contract Skill Page](https://clawhub.ai/dachunggan/skills/coding-contract)
- [Specification Output Template](references/spec-template.md)
- [Constraint Patterns Reference](references/constraint-patterns.md)
- [Good vs. Bad Specification Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a spec.md coding contract with interface definitions, behavioral constraints, verification checklists, and decision records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
