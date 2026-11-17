## Description:

Context Diet reviews an agent's instructions, skills, memory, and session context, estimates their token weight, and suggests a ranked list of possible trims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT

## Use Case:

Agent users and developers can use the skill when context feels bloated, before a long session, or after adding skills. It produces an estimate of context weight and a ranked trim list for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation cues may cause the skill to run in workflows where a context scan is not wanted.

Mitigation: Review whether the activation cues fit the workflow and invoke the scan deliberately when needed.

Risk: Security analysis coverage is partial because three local references could not be resolved.

Mitigation: Review the local references and the generated trim suggestions before acting on the report.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thomaszhou22/skills/context-diet)
- [Project repository](https://github.com/Thomaszhou22/context-diet.git)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown report with a weight summary and ranked trim list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token weights are approximate; trim suggestions are reviewed by the user.]

## Skill Version(s):

1.1.1 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
