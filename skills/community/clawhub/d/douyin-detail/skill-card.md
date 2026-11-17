## Description:

Provides Douyin public-data analysis for post details, image-text details, engagement metrics, content research, and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and content teams use this skill to retrieve public Douyin search results, creator posts, comments, and hot-list data for topic research, competitor monitoring, public-opinion review, and marketing analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the API token in URL query strings.

Mitigation: Use a limited-scope or low-quota GUAIKEI_API_TOKEN and rotate it if it has already been used with this package.

Risk: Douyin keywords, target URLs, and public user or comment data are sent to guaikei.com and may be saved in local logs.

Mitigation: Confirm that this data sharing is acceptable before use, then manage or delete generated logs after analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/douyin-detail)
- [Guaikei API service](https://www.guaikei.com)
- [Complete options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search input schema](assets/search_cli_req.schema.json)
- [Search output schema](assets/search_cli_resp.schema.json)
- [Post output schema](assets/post_cli_resp.schema.json)
- [Comment output schema](assets/comment_cli_resp.schema.json)
- [Hot-list output schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; command execution returns JSON on stdout and may save JSON logs locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer and a GUAIKEI_API_TOKEN environment variable.]

## Skill Version(s):

1.0.0 (source: frontmatter metadata, package.json, release evidence, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
