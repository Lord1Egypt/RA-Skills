## Description:

A Chinese-language film creation coordinator that analyzes scripts, character descriptions, action ideas, and visual style requests, then routes work to character, storyboard, action, and trailer sub-skills while preserving visual consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chang9852](https://clawhub.ai/user/chang9852)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and film-production teams use this skill to turn film concepts, scripts, character briefs, action scenes, or style requests into a coordinated creative workflow. It chooses the needed sub-skills, passes shared visual context between them, and returns an integrated package with module outputs, consistency checks, and next-step suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on related sub-skills for character sheets, storyboards, action direction, and trailer prompts.

Mitigation: Confirm the required sub-skills are installed and available before relying on a full multi-step workflow.

Risk: Broad film-creation requests may activate the orchestration workflow and produce creative guidance intended for downstream use.

Mitigation: Review generated story, visual, and prompt outputs before using them in a production pipeline.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chang9852/skills/film-pipeline)
- [ClawHub publisher profile](https://clawhub.ai/user/chang9852)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured sections and prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates dependent sub-skills when available; otherwise asks for missing inputs before continuing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
