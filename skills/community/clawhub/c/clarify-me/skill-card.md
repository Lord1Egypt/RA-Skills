## Description:

Analyze user's conversation to identify unclear parts and suggest better questions. Helps users express their problems more clearly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdchi](https://clawhub.ai/user/jdchi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review recent conversation context, identify ambiguous wording or missing details, and draft clearer questions for an LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent conversation text may be summarized or quoted back when the skill is explicitly invoked.

Mitigation: Avoid invoking it on exchanges containing information that should not be repeated, and review the generated clarification before sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jdchi/skills/clarify-me)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with quoted unclear phrases and suggested revised questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the same language as the user's question when possible.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
