## Description:

Analyzes TikTok hashtag performance, reach, and trending content using apidojo's TikTok scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers, content strategists, TikTok growth consultants, and developers use this skill to compare TikTok hashtags, inspect top videos and creators, benchmark engagement, and produce hashtag strategy recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to an Apify token and sends TikTok targets to Apify.

Mitigation: Install only when that data sharing is acceptable, keep runs scoped to user-requested hashtags, and store the token in an environment variable or approved secret mechanism.

Risk: The artifact includes broader scraper controls such as unlimited maxItems and customMapFunction.

Mitigation: Set maxItems for bounded collection and avoid customMapFunction unless the code is fully trusted.

Risk: The REST API fallback demonstrates passing the Apify token in the request URL.

Mitigation: Prefer MCP or an authorization-header API pattern over token-in-URL examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/analyzing-tiktok-hashtag-performance)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown analysis with tables, recommendations, and optional shell commands for Apify runs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Apify result data to summarize hashtag metrics, top videos, creators, engagement benchmarks, and strategy recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
