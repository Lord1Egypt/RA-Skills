## Description:

Helps agents detect and counter framing effects by comparing logically equivalent descriptions of a decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and teams use this skill to audit decisions or persuasive messages for gain, loss, attribute, and goal framing. It helps them compare equivalent alternatives and make a frame-independent decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real examples in the failure-pattern table could expose confidential details.

Mitigation: Omit confidential details when recording real examples.

Risk: Comparing descriptions that omit different facts as equivalent could produce a misleading framing audit.

Mitigation: Check that both descriptions preserve the same facts and decision math; skip the framing comparison when they are not logically equivalent.

## Reference(s):

- [Framing Effect sources](references/sources.md)
- [ClawHub skill release](https://clawhub.ai/deciqai/skills/framing-effect)
- [Framing Effect skill guide](https://www.deciqai.com/c/framing-effect)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown framing audit with a structured comparison and decision rationale]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Applies to a user-provided decision or message; checks whether alternative frames preserve the same facts and decision math.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
