## Description:

Run a weighted decision matrix to score and rank 2-4 options across 5 configurable criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mdomerofski](https://clawhub.ai/user/mdomerofski)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to compare 2-4 choices with weighted criteria, rank the options, and explain the highest-scoring choice in plain language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for generic decision-help wording.

Mitigation: Confirm that the user wants a structured decision matrix before gathering scores or running the helper script.

Risk: The script reads a JSON file path supplied for scoring.

Mitigation: Ask the user to confirm the intended JSON file and review its contents before running the matrix.

Risk: Subjective weights or scores can make the ranking look more certain than the inputs support.

Mitigation: Show the criteria weights and offer to rerun the matrix with adjusted weights for sensitivity analysis.

## Reference(s):

- [Decision Dynamo Criteria Reference](references/criteria.md)
- [ClawHub Skill Page](https://clawhub.ai/mdomerofski/skills/decision-dynamo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with ranked scores, criteria weights, and concise reasoning; shell commands may be shown for running the local matrix script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can use interactive prompts or a user-provided JSON input file to produce a ranked decision result.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
