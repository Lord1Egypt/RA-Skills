## Description:

Guides agents through culture and tourism media search on data0086.com, result preview, user-directed selection or purchase, mock transaction handling, and local video download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengyily](https://clawhub.ai/user/fengyily)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search the data0086.com culture-tourism media catalog, inspect previews, select one or more assets, and download selected videos after an explicit purchase command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts data0086.com, opens media links, and writes downloaded videos locally.

Mitigation: Install only when those network and filesystem behaviors are acceptable, and keep downloads constrained to the configured downloads/ directory.

Risk: HTML result rendering and API-provided media fields can expose users to unsafe or misleading embedded content if origins and fields are not checked.

Mitigation: Validate media origins against the configured trusted list, revalidate redirects, and sanitize API-provided fields before rendering them in HTML.

Risk: Batch purchase commands can trigger multiple local media downloads.

Mitigation: Review selections before issuing purchase commands and consider requiring confirmation before large batch downloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengyily/skills/culturetour-skill)
- [文旅素材 API 接口规范](artifact/api.md)
- [文旅素材搜索 API 参考](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or static HTML tables with inline links, plus shell command guidance and local file paths after downloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include structured media fields such as title, category, preview URL, thumbnail URL, commodity code, business code, duration, and download path when purchase is requested.]

## Skill Version(s):

1.0.22 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
