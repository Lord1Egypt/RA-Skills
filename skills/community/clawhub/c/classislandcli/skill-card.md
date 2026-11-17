## Description:

ClassIsland schedule-management CLI skill for querying subjects, timetables, and class plans, and for adding, deleting, or exchanging schedule entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qibowen2008](https://clawhub.ai/user/qibowen2008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClassIsland users use this skill to let an agent inspect and maintain ClassIsland schedule data through ClassIslandCLI, including subjects, timetables, class plans, and temporary or permanent class swaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify timetable data, delete subjects or time layouts, change profile paths, and perform permanent class swaps.

Mitigation: Require explicit user confirmation before write, delete, profile/path, or permanent swap commands, and back up the ClassIsland profile JSON before changes.

Risk: The skill asks the agent to install or update ClassIslandCLI, shell completions, and skills from an external release source.

Mitigation: Prefer manual installation and verification of ClassIslandCLI, and avoid agent-initiated install or overwrite operations unless the user explicitly confirms.

## Reference(s):

- [Classislandcli ClawHub Skill Page](https://clawhub.ai/qibowen2008/skills/classislandcli)
- [ClassIslandCLI Gitee Releases API](https://gitee.com/api/v5/repos/buger2008/ClassIslandCLI/releases?page=1&per_page=20&direction=desc)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Natural-language guidance with shell commands and parsed JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ClassIslandCLI.exe JSON output and can modify local ClassIsland profile data.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
