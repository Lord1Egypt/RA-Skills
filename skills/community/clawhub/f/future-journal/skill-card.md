## Description:

This skill provides a 49-day guided journal page and daily prompts for writing hoped-for events in the past tense, with optional user-configured syncing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT

## Use Case:

People who want a short daily writing practice use it to follow a themed 49-day journal, write entries, and review or export them. Those who prefer paper can use the command-line script to retrieve the daily prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the journal page may load an external script that could access journal contents, and some files were only partly inspected.

Mitigation: Avoid using the page for private journal entries until the external script and partly inspected files have been reviewed; confirm whether the page makes requests when sync is not configured.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bonniegeng-max/skills/future-journal)
- [Design System](references/DESIGN.md)

## Skill Output:

**Output Type(s):** [HTML, Text, JSON, Shell commands]

**Output Format:** [Single-file HTML journal page, daily prompts, and optional JSON backup/export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Journal entries are stored in browser localStorage; optional syncing requires a user-configured backend.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
