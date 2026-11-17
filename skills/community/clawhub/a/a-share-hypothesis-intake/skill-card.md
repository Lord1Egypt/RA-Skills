## Description:

把长材料、宏观观点、录音转写和新闻流拆成事实、推断、数据缺口、验证条件与 A 股传导卡，帮助用户把材料落到板块与选股逻辑。

This skill is ready for commercial/non-commercial use.

## Publisher:

[minguncle](https://clawhub.ai/user/minguncle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to decompose Chinese-language long-form materials, transcripts, macro views, and news into fact/inference labels, A-share sector transmission hypotheses, trigger conditions, invalidation conditions, and next verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market views and time-sensitive financial claims may be stale, unverifiable, or mistaken.

Mitigation: The skill requires unstable dates, policy events, prices, yields, and sector moves to be verified with current sources or marked as unverified.

Risk: Users may treat decomposed hypotheses as final trading instructions.

Mitigation: The skill states that it does not provide final buy or sell instructions unless followed by market scanning and action routing.

## Reference(s):

- [Hypothesis Card Template](references/hypothesis-card-template.md)
- [ClawHub skill page](https://clawhub.ai/minguncle/skills/a-share-hypothesis-intake)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown sections and structured hypothesis cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs distinguish facts, inferences, unverified claims, value stances, A-share transmission chains, conditions, invalidation criteria, and follow-up checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
