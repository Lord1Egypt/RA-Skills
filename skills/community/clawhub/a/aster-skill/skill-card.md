## Description: <br>
Monitors crypto news for BTC, ETH, SOL, and BNB, classifies market sentiment, and executes leveraged long or short orders on Aster with stop-loss and take-profit controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AsterSkillAgent](https://clawhub.ai/user/AsterSkillAgent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users who intentionally run automated crypto trading workflows use this skill to monitor recent market news and place Aster long or short orders when configured sentiment and confidence thresholds are met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live leveraged market orders on a schedule without manual confirmation. <br>
Mitigation: Install only when automated live trading is intended; disable withdrawals on exchange API keys, limit account balance and position size, and do not enable scheduled live trading unless this behavior is accepted. <br>
Risk: The security verdict flags the release as suspicious because safe default controls and clear per-order approval are not evident. <br>
Mitigation: Verify the Aster and OpenNews dependencies, confirm the entry file before deployment, and review the configured leverage, stop-loss, take-profit, and cooldown settings. <br>
Risk: LLM sentiment classification may act on incomplete, stale, or low-credibility news. <br>
Mitigation: Restrict monitored sources, keep confidence thresholds conservative, monitor logs and resulting orders, and test behavior before funding a live account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AsterSkillAgent/aster-skill) <br>
- [Publisher profile](https://clawhub.ai/user/AsterSkillAgent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Configuration] <br>
**Output Format:** [Scheduled execution with JSON sentiment decisions, exchange API calls, and text logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Aster and OpenAI API credentials; runs on a five-minute schedule by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact config) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
