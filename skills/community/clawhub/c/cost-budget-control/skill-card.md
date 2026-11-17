## Description:

Cost Budget Control helps agents estimate token use and cost for inference or tool calls, block calls that exceed token or cost budgets, and suggest extractive context compression to reduce spend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add budget checks to long-running autonomous tasks, batch evaluations, or data pipelines. It is most useful when an agent needs pre-call cost estimates, hard token or spend limits, and concise compression guidance before continuing work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled learner can persist usage, error, and preference history across sessions.

Mitigation: Review what local history will be stored and disable or remove learner usage when persistent preference or error logging is not acceptable.

Risk: The artifact instructs agents to write learned improvements back into SKILL.md after repeated errors or usage.

Mitigation: Remove or ignore the SKILL.md write-back behavior when a deterministic budget guardrail or reviewed release artifact is required.

Risk: The budget calculator uses static pricing inputs rather than a live billing source.

Mitigation: Set and review pricing values for the active model mix before relying on estimates for enforcement or reporting.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python CLI commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The budget script uses static pricing inputs; learner commands can create or update local usage, error, and preference history.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
