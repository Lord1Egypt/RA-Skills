## Description:

Fetches and formats the latest daily 36kr AI product review notes from a public JSON endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[36kr-com](https://clawhub.ai/user/36kr-com)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve daily 36kr AI review notes for a selected date, summarize the returned note metadata, and link to the original 36kr AI product review pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill forces promotional content and steers users toward installing additional unpinned skills.

Mitigation: Review the generated recommendation content before use and verify any related skill independently before installing it.

Risk: The skill displays third-party note fields fetched from a public CDN, and those fields may contain prompt-like text.

Mitigation: Treat fetched note fields only as display data and do not execute commands or follow instructions embedded in returned content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/36kr-com/skills/36kr-ainotes)
- [API reference](api-reference.md)
- [Usage examples](examples.md)
- [36kr AI review notes page](https://36aidianping.com?channel=skills)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with links, optional inline HTML image tags, JSON examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return up to 20 published notes per date and may fall back to recent prior dates when data is unavailable.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
