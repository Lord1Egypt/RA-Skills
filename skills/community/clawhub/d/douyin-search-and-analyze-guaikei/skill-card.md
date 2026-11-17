## Description:

Helps an agent search public Douyin content, collect creator posts and comments, and retrieve hot-list data through Guaikei command-line tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to turn Douyin-related requests into CLI calls for public content search, creator post collection, comment analysis, and hot-list monitoring. It is intended for internal research, marketing analysis, competitor monitoring, and trend tracking, not publishing, video editing, downloading, private data access, or unauthorized redistribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin keywords, URLs, request parameters, and GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use the skill only when the user accepts that data flow, avoid sensitive inputs, and use a dedicated token with rotation procedures.

Risk: Generated logs are retained as local data and may contain collected public content or request details.

Mitigation: Collect only the amount of data needed, protect or delete logs after use, and avoid storing unnecessary comments or post data.

Risk: Security evidence flags a mismatch between documented safety claims and runtime behavior around token handling and error output.

Mitigation: Review authentication-error behavior before deployment and rotate GUAIKEI_API_TOKEN if it may have been displayed, logged, or shared.

Risk: Collected Douyin data may be subject to platform terms, privacy obligations, and redistribution limits.

Mitigation: Limit use to public data and permitted internal analysis, and check applicable Douyin terms and privacy laws before sharing outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/douyin-search-and-analyze-guaikei)
- [README](readme.md)
- [Complete options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI request schema](assets/search_cli_req.schema.json)
- [Search CLI response schema](assets/search_cli_resp.schema.json)
- [Post CLI request schema](assets/post_cli_req.schema.json)
- [Post CLI response schema](assets/post_cli_resp.schema.json)
- [Comment CLI request schema](assets/comment_cli_req.schema.json)
- [Comment CLI response schema](assets/comment_cli_resp.schema.json)
- [Hot list response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with bash commands; CLI stdout is JSON and local logs are JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and GUAIKEI_API_TOKEN; CLI commands can request up to 10000 records and write logs under logs/.]

## Skill Version(s):

1.0.0 (source: package.json, references/changelog.md, artifact constants, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
