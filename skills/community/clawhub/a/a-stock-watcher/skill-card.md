## Description: <br>
Provides A-share stock quote monitoring, price alerts, technical analysis, automated reports, and risk-profile-based portfolio guidance using multiple Chinese finance data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenjianghua117](https://clawhub.ai/user/chenjianghua117) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents can use this skill to query A-share market data, monitor target prices, generate technical and holding reports, and receive informational portfolio guidance. It is most appropriate for stock watchlist monitoring and analysis workflows, not for automated trading or regulated financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts third-party Chinese finance APIs for stock quotes and market data. <br>
Mitigation: Install only when this external data access is acceptable for the deployment environment. <br>
Risk: Watchlist, holding, cache, and alert data may be stored locally. <br>
Mitigation: Avoid entering sensitive portfolio information unless local storage is approved and protected. <br>
Risk: Investment outputs may be incomplete, delayed, or unsuitable as advice. <br>
Mitigation: Treat all analysis as informational and verify decisions with authoritative market data and qualified financial review. <br>
Risk: DingTalk personal-message delivery depends on the OpenClaw notification setup and may not be guaranteed. <br>
Mitigation: Verify notification configuration before relying on alerts for time-sensitive monitoring. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenjianghua117/a-stock-watcher) <br>
- [Publisher Profile](https://clawhub.ai/user/chenjianghua117) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Full Feature Documentation](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown-style Chinese text responses with stock data tables, alerts, analysis reports, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact third-party Chinese finance APIs and may store watchlist, holding, cache, and alert data locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
