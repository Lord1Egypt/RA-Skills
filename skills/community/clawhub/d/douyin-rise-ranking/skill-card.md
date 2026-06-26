## Description: <br>
Retrieves Douyin follower-growth account rankings by day, week, or month and helps compare categories using follower counts, growth rates, follower deltas, and operational analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, brand marketers, MCN operators, and advertising teams use this skill to query Douyin follower-growth rankings and identify high-growth accounts, category trends, and operational opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedfoxHub API key and sends ranking queries to redfox.hk. <br>
Mitigation: Use a key intended for this service, provide it through REDFOX_API_KEY for the current session when possible, and avoid printing the full key in logs or chat. <br>
Risk: Credential handling and agent-control instructions were flagged by the security summary for human review. <br>
Mitigation: Review the skill and script before installation or deployment, especially API-key lookup behavior and execution instructions. <br>
Risk: Ranking-query history may remain in the local cache. <br>
Mitigation: Review or clear ~/.workbuddy/cache/dy_rise_ranking_data.json when query history is sensitive. <br>


## Reference(s): <br>
- [Core workflow](references/core_workflow.md) <br>
- [Douyin ranking API reference](references/dy-rank-api.md) <br>
- [Redfox Hub](https://redfox.hk/) <br>
- [Douyin follower-growth ranking API](https://redfox.hk/story/api/dyData/getDyRiseFansRank) <br>
- [ClawHub skill page](https://clawhub.ai/if530770/douyin-rise-ranking) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown ranking tables, summaries, analysis, subscription prompts, and configuration commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; results may include account links and locally cached ranking-query data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
