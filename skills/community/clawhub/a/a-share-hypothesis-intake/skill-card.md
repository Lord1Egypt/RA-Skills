## Description: <br>
把长材料、宏观观点、录音转写和新闻流拆成事实、推断、数据缺口、验证条件与 A 股传导卡。适用于用户贴长文、视频字幕、宏观框架、新闻摘要，想落到板块与选股逻辑的场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minguncle](https://clawhub.ai/user/minguncle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to turn long-form articles, transcripts, macro frameworks, and news feeds into fact/inference separation, A-share sector transmission hypotheses, validation conditions, and follow-up monitoring items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial hypotheses may be mistaken for investment advice or direct trade instructions. <br>
Mitigation: Treat outputs as hypotheses, not investment advice, and require separate human review before any portfolio or trading decision. <br>
Risk: Downstream market-data, portfolio, brokerage, or action-routing tools could introduce credential or trade-execution risk. <br>
Mitigation: Review downstream tools separately before allowing them to use credentials, access portfolios, or place trades. <br>
Risk: Time-sensitive macro, policy, price, yield, or geopolitical claims can become stale quickly. <br>
Mitigation: Verify unstable claims with current sources and mark unsupported points as unverified. <br>


## Reference(s): <br>
- [Hypothesis Card Template](references/hypothesis-card-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown structured as claim breakdowns, fact and inference separation, A-share transmission cards, conditions, invalidation checks, and next validation items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only outputs; treats market conclusions as hypotheses and marks unverifiable or time-sensitive claims for separate validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
