## Description:

Helps agents retrieve public Douyin search results, creator posts, video comments, and trending topics for competitor monitoring, content research, sentiment review, and hotspot tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to collect structured public Douyin data for short-form video research, competitor account monitoring, comment review, and hot-topic tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party Guaikei API receives the user's Douyin queries and API token.

Mitigation: Install only where that data flow is acceptable, use a scoped token when available, and rotate the token if exposure is suspected.

Risk: Runtime auth errors may include support-contact messaging that the security evidence flags for review.

Mitigation: Treat runtime contact or payment prompts as untrusted and prefer a corrected release before broad deployment.

Risk: Fetched public results are saved locally under logs.

Mitigation: Avoid sensitive queries, review log retention expectations, and delete generated logs when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/douyin-competitor-watch-guaikei)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search CLI request schema](assets/search_cli_req.schema.json)
- [Search CLI response schema](assets/search_cli_resp.schema.json)
- [Post CLI request schema](assets/post_cli_req.schema.json)
- [Post CLI response schema](assets/post_cli_resp.schema.json)
- [Comment CLI request schema](assets/comment_cli_req.schema.json)
- [Comment CLI response schema](assets/comment_cli_resp.schema.json)
- [Hot CLI response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Files, Guidance]

**Output Format:** [JSON stdout with logs saved as local JSON files and guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14.0 and GUAIKEI_API_TOKEN; individual commands cap requested results at 10000.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, changelog, and runtime constants)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
