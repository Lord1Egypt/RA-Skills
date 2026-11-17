## Description:

Find what your audience is searching for now by scouting X/Twitter and Reddit for trending topics, analyzing competitors, and identifying content gaps with Citedy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nttylock](https://clawhub.ai/user/nttylock)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, SEO practitioners, and content teams use this skill to turn current social conversations, competitor activity, and content gaps into prioritized content opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-research terms, competitor URLs, and selected subreddits are sent to Citedy.

Mitigation: Use non-sensitive research inputs and confirm that users are comfortable sharing those terms with Citedy before starting runs.

Risk: Started runs spend Citedy credits.

Mitigation: Review the workflow and estimated credit cost before launching a scout, gap, or competitor-analysis run.

Risk: The registration script defaults the agent name from the local hostname when no name is provided.

Mitigation: Provide an explicit non-sensitive agent name during registration.

Risk: The Citedy API key authenticates API access.

Mitigation: Store CITEDY_API_KEY like any other service credential and avoid exposing it in prompts, logs, or shared outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nttylock/skills/citedy-trend-scout)
- [Citedy Agent Registration API](https://www.citedy.com/api/agent/register)
- [Citedy](https://www.citedy.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with HTTP examples, JSON response examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trend summaries, competitor analysis, content-gap recommendations, polling steps, rate-limit handling, and credit-use estimates.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
