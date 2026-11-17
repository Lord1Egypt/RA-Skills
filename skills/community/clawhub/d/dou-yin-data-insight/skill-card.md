## Description:

Dou Yin Data Insight helps brands, content operators, and creators collect public Douyin data for competitor research, content comparisons, trend tracking, and brand content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, content operators, creators, and developers use this skill to retrieve public Douyin search, hot list, creator post, and comment data for content research, competitor monitoring, trend tracking, and downstream reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive Douyin research targets, account URLs, comments, and the GUAIKEI_API_TOKEN may be exposed through execution or saved results.

Mitigation: Use a dedicated token with the minimum necessary access, avoid running the skill on sensitive targets without review, and restrict access to generated logs and outputs.

Risk: The skill depends on a third-party API service for data access.

Mitigation: Confirm the API provider's authorization, retention, and privacy terms before using the skill with confidential research plans or client data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/dou-yin-data-insight)
- [Guaikei API and token service](https://www.guaikei.com)
- [Complete options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Post request schema](assets/post_cli_req.schema.json)
- [Post response schema](assets/post_cli_resp.schema.json)
- [Hot list response schema](assets/hot_cli_resp.schema.json)
- [Comment request schema](assets/comment_cli_req.schema.json)
- [Comment response schema](assets/comment_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands; CLI execution returns structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; logs may be saved by the CLI.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, SKILL.md metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
