## Description:

Smart answering framework that adapts to question types and delivers evidence-based, natural responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[belugarex](https://clawhub.ai/user/belugarex)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to structure general-purpose question answering with clear conclusions, supporting evidence, reasoning, and tone adjustments. It is especially useful when prompts call for concise explanations, comparisons, viewpoints, clarification, or Chinese-English bilingual responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary requests for explanation or comparison may activate structured-answer behavior when the user expected an unstructured reply.

Mitigation: Preserve explicit user formatting preferences and adjust or simplify the response when the requested style conflicts with the framework.

Risk: Mixed Chinese-English prompts may receive bilingual output even when the user wanted a single-language answer.

Mitigation: Follow any explicit language preference in the prompt and switch to one language when the user asks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/belugarex/skills/answer-framework)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language answers, often in Markdown; bilingual output may be used for mixed Chinese-English prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add an activation marker and adjust answer depth, tone, and structure based on the user's prompt.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
