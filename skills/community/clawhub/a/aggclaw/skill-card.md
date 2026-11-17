## Description:

AppGrowing Global intelligent ad creative analysis assistant that finds relevant global ad creatives based on user instructions, delivers automated analysis, and includes Inspire ideation mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youcloud](https://clawhub.ai/user/youcloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, and developers use this skill to search global ad creatives, analyze campaign patterns, and generate Inspire-mode advertising ideas through the AppGrowing Global service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ad-analysis prompts are sent to AppGrowing/Youcloud.

Mitigation: Use the skill only when that vendor is approved, and avoid confidential campaign data.

Risk: The material download flow gives too much trust to remote file URLs and names.

Mitigation: Constrain downloads to a dedicated folder and validate URLs and filenames before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youcloud/skills/aggclaw)
- [AppGrowing homepage](https://appgrowing.net/)
- [Usage examples](references/example.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with API response summaries, links, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YOUCLOUD_API_KEY and may provide local material download paths after a completed analysis session.]

## Skill Version(s):

1.2.2 (source: server release metadata; artifact frontmatter says 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
