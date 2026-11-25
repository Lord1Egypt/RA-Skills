## Description:

Reads a Douyin video by ID, link, or share text and returns its details or current play count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to retrieve a Douyin video's caption, author, engagement counts, posting time, and current play count from an ID, link, or share text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned `dataxapi` package creates a supply-chain risk, and the scan coverage was partial.

Mitigation: Review the package and service before installing, use an exact reviewed package version, and cap paid calls with `--max-price` or `max_price`.

## Reference(s):

- [Douyin video details API](https://dataxapi.com/apis/douyin/videos/get/)
- [Douyin video metrics API](https://dataxapi.com/apis/douyin/videos/metrics/)
- [DataXAPI agent skill catalog](https://dataxapi.com/.well-known/agent-skills/index.json)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [Structured API results with concise explanatory text and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One result page per endpoint call; returned figures reflect the service's recorded data.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
