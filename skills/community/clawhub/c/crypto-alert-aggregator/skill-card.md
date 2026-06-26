## Description: <br>
Aggregates real-time crypto market data and Twitter signals into actionable alerts for traders and researchers. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[jackfeng0614-prog](https://clawhub.ai/user/jackfeng0614-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, traders, and researchers use this skill to generate crypto alert objects that combine market movement thresholds with social-sentiment-style signals. Because server security evidence says the implementation currently uses mock random data, it should be used only for experimentation or evaluation until real data-source behavior is documented. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can present random mock market and Twitter signal data as actionable crypto alerts. <br>
Mitigation: Label outputs as simulation-only and do not use them for trading or research decisions until real data-source calls are implemented and documented. <br>
Risk: The skill requests crypto and Twitter API credentials even though the evidence says the current implementation does not use real external data-source calls. <br>
Mitigation: Do not provide real API keys until the publisher documents live data behavior, credential handling, and the difference between mock and live modes. <br>
Risk: Streaming starts a polling interval without a documented stop mechanism. <br>
Mitigation: Use streaming only in controlled test environments until the publisher provides lifecycle controls for stopping pollers. <br>
Risk: Optional webhook delivery may send alert data outside the local environment without documented data flow. <br>
Mitigation: Leave webhook delivery disabled until the publisher documents outbound webhook behavior and data contents. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jackfeng0614-prog/crypto-alert-aggregator) <br>
- [Publisher profile](https://clawhub.ai/user/jackfeng0614-prog) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, configuration, guidance] <br>
**Output Format:** [JSON alert objects and text callback messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Alerts include timestamp, asset, type, price or value, change, Twitter mentions, sentiment, confidence, and message fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, _meta.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
