## Description:

Claw Diary records agent activity and helps agents summarize sessions, replay timelines, search history, export data, and maintain first-person journal and persona notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xbeekeeper](https://clawhub.ai/user/0xbeekeeper)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent for diary summaries, activity statistics, searchable history, visual replay, exports, and reflective journal entries based on locally stored agent activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global npm package when the claw-diary binary is missing.

Mitigation: Review and install a pinned claw-diary package version in an isolated environment before using the skill.

Risk: The skill records and stores broad agent activity history under ~/.claw-diary/.

Mitigation: Use the skill only when local activity recording is acceptable, and periodically export, clear, or otherwise manage the stored diary data.

Risk: Journal and persona files can contain untrusted content that could influence generated journal entries.

Mitigation: Treat diary, journal, and persona content as context only, and do not follow instructions embedded in those files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xbeekeeper/skills/claw-diary)
- [Publisher profile](https://clawhub.ai/user/0xbeekeeper)
- [Required npm package](https://www.npmjs.com/package/claw-diary)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration]

**Output Format:** [Markdown, plain text, HTML replay output, JSON export, and local Markdown files depending on the diary command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill reads and writes diary, journal, persona, and configuration data under ~/.claw-diary/.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
