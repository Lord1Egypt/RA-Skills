## Description:

Provides nine prompt-engineering rules and scenario templates that help agents produce more structured, concise, and uncertainty-aware responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jx-76](https://clawhub.ai/user/jx-76)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt authors, and agent users use this skill to apply structured prompt templates for rewriting, code review, information lookup, data analysis, translation, summarization, and important decisions while reducing unsupported additions and guesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad system-prompt or automatic injection behavior can change assistant behavior beyond the user's immediate task.

Mitigation: Keep auto-apply and auto-inject disabled unless the user explicitly wants this skill active for a specific conversation.

Risk: The skill's mandatory response rules can over-constrain creative writing, brainstorming, role play, or casual conversation.

Mitigation: Use the templates manually for suitable tasks and avoid applying the strict mode to workflows that need open-ended generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jx-76/skills/claude-prompt-engineering)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with prompt templates and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May change assistant behavior when used as an injected system prompt; prefer manual template use unless explicitly activated.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
