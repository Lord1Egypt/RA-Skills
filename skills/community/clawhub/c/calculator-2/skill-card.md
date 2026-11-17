## Description:

Provides basic arithmetic calculation support for addition, subtraction, multiplication, division, and chained expression evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cexfree](https://clawhub.ai/user/cexfree)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to parse and solve basic arithmetic expressions while showing the calculation process. It is suited for routine numeric computations involving addition, subtraction, multiplication, division, and standard order of operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broadly worded math requests may invoke the skill for work beyond basic arithmetic.

Mitigation: Use it for arithmetic expressions and route advanced mathematics or domain-specific calculations to a more capable math tool or reviewer.

Risk: Arithmetic mistakes can mislead downstream decisions if results are used without checking.

Mitigation: Review the displayed calculation steps and independently verify high-impact results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cexfree/skills/calculator-2)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text with calculation steps and a final numeric answer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows the calculation process, follows standard order of operations, and warns on division by zero.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
