## Description:

Update cspr preference memory from accumulated feedback and recent newspaper outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happywalkers](https://clawhub.ai/user/happywalkers)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to curate CSPR preference memory from accumulated feedback and recent newspaper outputs, updating topics, source preferences, and disliked patterns conservatively.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent preference-memory updates can influence future CSPR sessions if broad changes are applied without review.

Mitigation: Ask the agent to show the proposed profile diff and get user confirmation before running prefmem update.

Risk: Preference updates based on a single reaction can overfit topics, sources, or disliked patterns.

Mitigation: Keep updates conservative and base them on accumulated feedback or several recent runs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and YAML configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a complete updated CSPR profile YAML to a run folder and apply it with prefmem update.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
