## Description:

Guides an agent through collecting replies and comments from public Meta Threads posts with the Apify Threads replies scraper actor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurizerush](https://clawhub.ai/user/futurizerush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run an Apify actor that extracts original posts and replies from public Threads URLs for conversation review, reporting, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify API tokens may be exposed when placed in request URLs shown in examples.

Mitigation: Prefer an Authorization header or other non-logged secret handling, use a narrowly scoped Apify token, avoid shell tracing around commands, and rotate any token that may have appeared in logs or shared output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/futurizerush/skills/apify-threads-replies)
- [Apify actor page](https://apify.com/futurizerush/threads-replies-scraper?fpr=rush)
- [Apify API documentation](https://docs.apify.com/api/v2)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python and bash examples plus JSON result schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes asynchronous Apify actor execution, polling, dataset retrieval, and expected original_post and reply fields.]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
