## Description:

Creates a local Codegirl pair-programming companion skill from user-provided chat logs, GitHub activity, code snippets, photos, and profile notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmlans](https://clawhub.ai/user/xmlans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual users use this skill to create and evolve a local pair-programming companion persona from personal chat, coding, and profile materials for technical conversation and reflection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes and stores sensitive personal chat logs, photos, and identity-shaping persona instructions.

Mitigation: Use only data you own or have clear consent to process, avoid importing full private chats or GPS-bearing photos, and inspect generated files before invoking them.

Risk: Generated persona content can be persisted into future agent behavior in ways the user may not fully review.

Mitigation: Do not place generated persona text into .agents/rules; keep generated skills scoped to the intended local directory and review each generated SKILL.md before use.

Risk: Delete, rollback, and generated-file workflows can affect local files if the slug or resolved path is unsafe.

Mitigation: Use simple slugs and verify the resolved path is visibly confined to the intended gfs directory before running destructive workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xmlans/skills/codegirl-skill)
- [Project Repository Link Mentioned by Release Notes](https://github.com/xmlans/codegirl-skill)
- [AgentSkills Standard](https://agentskills.io)
- [WeChatMsg Export Tool](https://github.com/LC044/WeChatMsg)
- [PyWxDump Export Tool](https://github.com/xaoyaoo/PyWxDump)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, JSON metadata, generated skill code, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local files under a generated skill directory plus setup, update, rollback, and deletion guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
