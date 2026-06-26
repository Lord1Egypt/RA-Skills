## Description: <br>
Provides an A-share quantitative trading strategy workflow for screening CSI 300 stocks with a v5.2 scoring model, volume-ratio filtering, and configurable risk controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[austin0208](https://clawhub.ai/user/austin0208) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-oriented users use this skill to run an A-share stock screening script, tune quantitative strategy parameters, and review generated trading guidance before any real-world action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requests wallet and transaction-signing capabilities even though the artifact describes a stock-analysis workflow. <br>
Mitigation: Do not grant wallet or signing permissions unless the publisher clearly explains why they are needed and each action can be reviewed before approval. <br>
Risk: Backtest performance claims and trading recommendations may be unverified financial guidance. <br>
Mitigation: Treat the output as informational, test in an isolated workspace or simulated account first, and independently review results before trading. <br>
Risk: The included script fetches external market data and may interact with local OpenClaw finance data. <br>
Mitigation: Review network and file access before running the script, and back up finance data before using save or workflow features. <br>


## Reference(s): <br>
- [ClawHub skill release: G2量化交易策略](https://clawhub.ai/austin0208/g2-trading-strategy) <br>
- [Publisher profile: austin0208](https://clawhub.ai/user/austin0208) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python commands, JSON configuration, and generated stock-screening analysis files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include trading recommendations and local finance data updates when the included Python script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
