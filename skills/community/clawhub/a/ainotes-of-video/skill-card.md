## Description:

Generate AI-powered notes from videos in document, outline, or graphic-text formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn public video URLs into structured notes for review, documentation, or summarization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted video URLs are shared with HeyBossAI/SkillBoss for note generation.

Mitigation: Use public, non-sensitive URLs only; do not submit private, internal, signed, or token-bearing links.

Risk: The artifact references helper scripts that are not included in the release artifact.

Mitigation: Confirm required scripts are available in the execution environment before relying on automated create, query, or polling commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/ainotes-of-video)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and structured note text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and public video URLs; note formats include document, outline, and graphic-text notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
