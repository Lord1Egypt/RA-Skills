## Description:

Dream Novel Writer helps agents plan and write long-form Chinese novels using the snowflake method, chapter blueprints, and JSON-backed memory state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waitli](https://clawhub.ai/user/waitli)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and agent users use this skill to structure Chinese novels, generate chapter plans, draft chapters, and maintain continuity for characters, plot events, worldbuilding, and foreshadowing across long projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local novel project files and assembled project content may influence later agent behavior.

Mitigation: Use a dedicated project folder, avoid shared or untrusted project files, and treat assembled prompt text as writing context rather than authorization for tool calls.

Risk: Novel outlines and JSON state databases may contain sensitive personal or creative material.

Mitigation: Keep secrets and confidential material out of outlines, chapter files, and JSON databases before using the skill.

Risk: The workflow can encourage continued batch writing after generated context is assembled.

Mitigation: Require separate user approval before continued chapter generation, file writes, or state updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/waitli/skills/dream-novel-skill)
- [Architecture prompts](artifact/resources/architecture.md)
- [Chapter blueprint prompts](artifact/resources/chapter.md)
- [Memory and update prompts](artifact/resources/utility.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose, JSON state updates, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be scoped to a user-confirmed novel project directory.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
