## Description:

Guides an agent through planning, drafting, revising, and checking a Chinese multi-chapter novel with outlines, character profiles, chapter files, hooks, and word-count checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckrissun](https://clawhub.ai/user/ckrissun)

### License/Terms of Use:

MIT

## Use Case:

External users, writers, and content creators use this skill to create Chinese novels across common genres by answering setup questions and then having an agent generate the story plan, character files, and chapter drafts. It is intended for local manuscript generation and iteration in a workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and repeatedly updates local manuscript files under a novels/[novel name]/ folder.

Mitigation: Run it in a dedicated project workspace when the generated novel should remain separate from other files.

Risk: After the planning confirmation, the workflow directs the agent to continue chapter-by-chapter without further confirmation.

Mitigation: Review the outline and character files carefully before confirming the drafting phase, and pause the agent if intermediate chapter review is required.

Risk: Generated fiction may contain continuity, quality, or style issues despite the built-in checklist and word-count checks.

Mitigation: Review generated chapters manually and use the provided consistency, dialogue, expansion, and quality-check references during revision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckrissun/skills/chinese-novelist-skill)
- [Chapter guide](references/chapter-guide.md)
- [Chapter template](references/chapter-template.md)
- [Character building](references/character-building.md)
- [Character template](references/character-template.md)
- [Consistency guide](references/consistency.md)
- [Content expansion](references/content-expansion.md)
- [Dialogue writing](references/dialogue-writing.md)
- [Hook techniques](references/hook-techniques.md)
- [Outline template](references/outline-template.md)
- [Plot structures](references/plot-structures.md)
- [Quality checklist](references/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Conversational text plus Markdown manuscript, outline, and character files, with local word-count command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates files under novels/[novel name]/ and uses a local Python script to check Chinese chapter word counts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
