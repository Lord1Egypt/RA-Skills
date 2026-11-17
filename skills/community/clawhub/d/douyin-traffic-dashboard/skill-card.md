## Description:

Summarizes how rising Douyin topics are distributed across content categories to support platform-level content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and social media operators can compare rising-topic counts and shares across Douyin's 32 top-level categories when planning an account's content direction. Treat the sample-based figures as a directional snapshot, not as total platform views or a prediction of account performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests require an AI Skills API key, may consume paid service balance, and transmit supplied parameters to ai-skills.ai.

Mitigation: Keep AISKILLS_API_KEY private, monitor service balance, and use the documented empty parameters object {}.

Risk: Category shares describe a sample of rising topics and may use cached data; they do not represent total Douyin views or account performance.

Mitigation: Use the figures as directional context, compare timestamps across refreshes, and combine them with audience and account-specific judgment.

## Reference(s):

- [Douyin traffic dashboard skill page](https://ai-skills.ai/zh/skills/douyin-traffic-dashboard)
- [Quick start instructions](https://github.com/allinherog-star/ai-skills/tree/main#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)
- [AI Skills billing page](https://ai-skills.ai/user/billing)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured category statistics with concise content-planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports category labels, rising-topic counts, sample shares, and update time; covers 32 top-level categories using up to 100 sampled topics. Cached results may reflect older data.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
