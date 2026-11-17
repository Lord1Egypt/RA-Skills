## Description:

Curate and post AI trend tweets from X (Twitter) with quote suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yusaku-0426](https://clawhub.ai/user/yusaku-0426)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to collect public AI-related posts from X (Twitter), filter them by engagement and quality signals, prepare Japanese summaries and quote suggestions, and publish curated results to Slack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can post curated content to Slack, which could publish to an unintended workspace or channel if the destination is misconfigured.

Mitigation: Confirm the Slack workspace and channel targeted by openclaw message send before enabling or running the posting step.

Risk: The referenced scripts/ai_trends.js implementation is not present in the artifact evidence.

Mitigation: Verify the source and behavior of scripts/ai_trends.js before use, especially the search, formatting, posting, and mark-posted commands.

Risk: Curated public X content, summaries, translations, and quote suggestions may be inaccurate, incomplete, or unsuitable for publication.

Mitigation: Review the selected posts, generated summary, translations, and suggested quotes before sending Slack messages or publishing related social content.

## Reference(s):

- [Ai Trend Curation ClawHub page](https://clawhub.ai/yusaku-0426/skills/ai-trend-curation)
- [Publisher profile](https://clawhub.ai/user/yusaku-0426)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Slack-ready curation content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces curated tweet selections, categories, author descriptions, Japanese translations when needed, quote suggestions, summaries, and Slack message/thread content.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
