## Description:

Turn an overwhelming set of tabs, bookmarks, and snippets into a structured session digest with tasks, reading queue, and archive plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert user-provided browser tabs, bookmarks, and snippets into a practical session digest, reading queue, archive list, and next-hour action plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser tab, bookmark, and snippet inputs may contain sensitive browsing context.

Mitigation: Provide only the tab data intended for organization and review the generated digest before using or sharing it.

Risk: The helper script can write or overwrite a JSON digest at the selected output path.

Mitigation: Choose the output path deliberately and prefer preview or draft workflows before acting on generated files.

## Reference(s):

- [Browser Session Curator on ClawHub](https://clawhub.ai/52yuanchangxing/skills/browser-session-curator)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown session plans and optional local JSON digest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on user-provided tab or bookmark data and may include action, reading, and archive groupings.]

## Skill Version(s):

1.0.0 (source: server release metadata; SKILL.md frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
