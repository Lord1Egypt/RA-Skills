## Description:

Transforms vague prompts into precise, structured AI instructions for prompt refinement, prompt engineering, system prompts, and effective AI instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt authors, and agent builders use this skill to turn vague or underspecified prompts into precise Markdown instructions for AI systems. It is especially useful for prompt engineering, system prompts, and machine-parsed skill or agent instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A refined prompt may include secrets or sensitive material if the original prompt contains them and the user chooses to save the result.

Mitigation: Review the refined prompt before saving and approve writing to .ai/PROMPT.md only when a persistent local record is appropriate.

Risk: Prompt refinements can introduce misleading requirements if the original intent is unclear.

Mitigation: Clarify unclear intent first and validate that the rewrite uses only information from the original prompt or conversation context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iliaal/skills/compound-eng-refine-prompt)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown refined prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask before appending the refined prompt to .ai/PROMPT.md; persistent writes require explicit confirmation.]

## Skill Version(s):

4.5.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
