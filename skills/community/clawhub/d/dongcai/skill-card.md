## Description:

本 Skill 基于东方财富妙想搜索能力，基于金融场景进行信源智能筛选，用于获取涉及时效性信息或特定事件信息的任务，包括新闻、公告、研报、政策、交易规则、具体事件、各种影响分析、以及需要检索外部数据的非常识信息等。避免AI在搜索金融场景信息时，参考到非权威、及过时的信息.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinsutianxing](https://clawhub.ai/user/kevinsutianxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Dongfangcaifu Miaoxiang financial information for timely market news, announcements, research reports, policy updates, trading rules, event context, and impact analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial search queries are sent to a documented remote service together with a user-provided API key.

Mitigation: Use the skill only when sending those queries to the service is acceptable, and provide a limited, revocable API key.

Risk: The current shell script may expose the API key to local process observers during execution.

Mitigation: Run it only in trusted local environments and rotate or revoke the key if local exposure is suspected.

Risk: Queries containing quotes or control characters may be mishandled by the current script.

Mitigation: Review or sanitize query text before execution, especially for copied input or automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevinsutianxing/skills/dongcai)
- [DongCai news search API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command usage and remote API response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally save readable search results to the workspace when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
