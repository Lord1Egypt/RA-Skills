## Description:

Analysis compares options thoroughly but doesn't pick one; the skill guides the agent to make a clear recommendation when the evidence supports one.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when drafting comparative analysis so the response names a recommended option, explains the deciding reason, and identifies the uncertainty that could change the recommendation. It is useful for employee, external, and developer-facing writing where a side-by-side comparison should lead to actionable guidance instead of a non-answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause the agent to state a recommendation more often, including cases where uncertainty should remain explicit.

Mitigation: Keep the key uncertainty visible and ask for missing context when the right answer genuinely depends on information the agent does not have.

Risk: A decisive recommendation can be wrong if the stated criteria are incomplete or misapplied.

Mitigation: Tie the recommendation to the stated criteria and include the condition that would change the choice.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or prose guidance in the agent response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, file access, shell commands, or external services are requested by the skill.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
