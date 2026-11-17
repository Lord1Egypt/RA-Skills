## Description:

Decision guide for delegating coding tasks to Cavecrew investigator, builder, or reviewer subagents when compressed structured output is preferred.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanford](https://clawhub.ai/user/seanford)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use Cavecrew to decide when to delegate code navigation, small edits, and diff review to compressed-output subagents instead of handling tasks inline or using longer-form agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may route suitable coding tasks to Cavecrew subagents unexpectedly.

Mitigation: Review activation wording before installation and invoke the skill intentionally for tasks where compressed subagent output is desired.

Risk: Compressed subagent output can be terse and may be difficult for humans to read directly.

Mitigation: Have the main agent paraphrase important findings for human readers, or use a longer-form agent when rationale and context are needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seanford/skills/cavecrew)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown guidance with structured output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Subagent outputs are intentionally compressed and structured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
