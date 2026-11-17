## Description:

A fix is proposed without first identifying the root cause; the symptom is masked rather than resolved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to avoid superficial bug fixes by first stating the root cause, explaining how the symptom follows, and confirming that the fix addresses the cause.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can shape bug-fix recommendations even when the available evidence is incomplete.

Mitigation: Require the agent to state the root cause and cause-to-symptom chain before accepting proposed code changes.

Risk: A downstream patch may still be proposed when the upstream cause is out of reach.

Mitigation: Document why the upstream fix is not feasible and leave a comment linking the symptom to the cause.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mvogt99/skills/bugfix-without-diagnosis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with concise diagnostic reasoning and code-review recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts the agent to state root cause, trace cause to symptom, and justify any downstream patch.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
