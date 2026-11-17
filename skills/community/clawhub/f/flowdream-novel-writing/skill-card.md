## Description:

Assists writers with long-form fiction workflows, including story bibles, outline anchors, chapter drafting, foreshadowing tracking, consistency checks, writer's-block triage, prose polishing, and chapter review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aitoim](https://clawhub.ai/user/aitoim)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and fiction-focused agent users use this skill to plan and continue novels or serialized fiction, maintain continuity, polish drafts, and review chapter quality. It is especially suited to Chinese-first web-novel workflows while also describing general fiction-writing practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may activate the skill for writing or polishing requests where the user did not intend a fiction workflow.

Mitigation: Scope skill use to fiction-writing tasks and confirm intent before applying the full workflow.

Risk: The workflow may create or update local story files such as story-bible.md.

Mitigation: Review proposed file changes before saving and keep the story bible as the continuity source of truth.

Risk: Chinese-first guidance may not match every user's desired language, market, or genre convention.

Mitigation: Confirm the target language, genre, and reader expectations before drafting or polishing.

## Reference(s):

- [FlowDream homepage](https://flowdream.ai)
- [ClawHub skill page](https://clawhub.ai/aitoim/skills/flowdream-novel-writing)
- [Craft Checklist](references/craft-checklist.md)
- [Polish & De-AI-Flavor Checklist](references/polish-checklist.md)
- [Quality Review](references/quality-review.md)
- [Story Bible Template](references/story-bible-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown prose, checklists, story-bible files, outlines, chapter drafts, review tables, and revision notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local story files such as story-bible.md when the agent has filesystem access.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
