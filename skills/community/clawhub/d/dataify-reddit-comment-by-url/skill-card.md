## Description:

Collect comments from a known Reddit post URL and return the collected result after the Dataify task completes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect Reddit comment data from specific known Reddit post URLs through Dataify. It is intended for targeted comment collection, not Reddit post discovery or subreddit listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Dataify API token.

Mitigation: Store the token in DATAIFY_API_TOKEN and avoid pasting token values into chat or generated artifacts.

Risk: Submitted Dataify jobs may consume account credits.

Mitigation: Review target URLs and collection scope before high-volume or multi-input runs, and resume existing task IDs instead of resubmitting paid jobs.

Risk: Result monitoring depends on the separate dataify-task-operations runtime.

Mitigation: Install and use the skill only when both this package and that runtime are trusted and available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-reddit-comment-by-url)
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill)
- [Dataify API token sign-in](https://dashboard.dataify.com/login?utm_source=skill)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task or result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the final collected result by default after asynchronous task monitoring; large payloads may be summarized while preserving access to the raw result.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
