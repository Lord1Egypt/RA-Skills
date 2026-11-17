## Description:

Fetches rising Douyin topics and trend data to help creators identify and assess short-video ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media operators, and marketers use this skill to find rising Douyin topics, track keyword or category ranking and heat changes, and develop short-video topic ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and filters are sent to the AI Skills service.

Mitigation: Avoid submitting sensitive queries and use a dedicated API key.

Risk: Service use may incur charges.

Mitigation: Check service charges and account balance before repeated or large-scale use.

Risk: Live API behavior and separately supplied installer code were not verified in the security review.

Mitigation: Review any supplied installation command before running it and confirm important trend results against current Douyin data.

## Reference(s):

- [Skill parameters](artifact/references/form-schema.json)
- [AI Skills service page](https://ai-skills.ai/zh/skills/douyin-realtime-hot-rise)
- [ClawHub skill page](https://clawhub.ai/allinherog-star/skills/douyin-realtime-hot-rise)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries of topic rankings, heat changes, trend points, and selection suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trend history is limited to the points returned by the service; the skill does not support pagination or date-range queries.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
