## Description:

Retrieves current trending-topic rankings from selected social platforms and produces a CSV table and a brief with cross-platform topics and tailored ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request current trend reports for supported social platforms, daily hot-search summaries, or topic ideas related to current trends. The agent returns platform rankings, recurring topics across platforms, and ideas tailored to the user's field.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned dataxapi CLI dependency could change between runs, and the CLI may access local files or the API key.

Mitigation: Use a reviewed, exact CLI version and limit the files and credentials available to the process.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [ClawHub skill page](https://clawhub.ai/data-x-api/skills/dataxapi-trending-topics)

## Skill Output:

**Output Type(s):** [CSV data, Markdown, Analysis]

**Output Format:** [CSV trend table and a Markdown trend brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks are platform-specific; heat values should not be compared across platforms. Trend rankings can change within the hour.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
