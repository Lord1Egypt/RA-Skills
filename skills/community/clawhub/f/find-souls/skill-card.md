## Description:

Search and install AI persona prompts from the Agent Souls library for historical figures, fictional characters, and expert personas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wklken](https://clawhub.ai/user/wklken)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find a persona prompt, install it as SOUL.md in a project, and roll back to a previous persona when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded persona prompts can contain instructions that change agent behavior after the conversation is reset.

Mitigation: Review the downloaded SOUL.md before resetting the conversation, especially for requests involving secrets, safety overrides, or unrelated tool access.

Risk: Installing a persona replaces the current project SOUL.md.

Mitigation: Confirm overwrites, keep the .soul_backups directory, and use the rollback workflow to restore a previous or original persona.

Risk: A cached search index can be stale.

Mitigation: Clear ~/.cache/agent-souls/search.json to force a fresh index from agent-souls.com.

## Reference(s):

- [Find Souls on ClawHub](https://clawhub.ai/wklken/skills/find-souls)
- [Agent Souls](https://agent-souls.com/)
- [Agent Souls search index](https://agent-souls.com/search.json)
- [Agent Souls requests](https://github.com/wklken/souls/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file changes to SOUL.md and .soul_backups when installing or rolling back a persona]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download persona prompt content from agent-souls.com and cache the search index locally.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
