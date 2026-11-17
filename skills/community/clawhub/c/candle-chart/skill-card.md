## Description:

使用akshare获取股票数据，按Steve Nison《日本蜡烛图技术》逻辑识别形态，生成深色盯盘风格K线图（含信号带+成交量）

This skill is ready for commercial/non-commercial use.

## Publisher:

[wtjjacobj](https://clawhub.ai/user/wtjjacobj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can run this Chinese-language OpenClaw skill to fetch A-share market data, identify common candlestick patterns, and generate a dark themed PNG chart for visual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script contacts akshare/Tencent for market data during execution.

Mitigation: Run it only in environments where outbound market-data requests are allowed and dependency/data-source availability is acceptable.

Risk: The script writes chart PNG files to the Desktop using the stock code as the filename, so repeated runs for the same code may replace prior output.

Mitigation: Check the Desktop output path before running and rename or archive existing charts when retaining earlier output matters.

Risk: The skill is a Chinese-language stock charting tool and may be less usable for readers who cannot review the labels and terminal messages.

Mitigation: Have a Chinese-reading reviewer confirm prompts, labels, and chart annotations before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wtjjacobj/skills/candle-chart)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Files, Guidance]

**Output Format:** [Python script output, terminal status text, and PNG chart file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a chart PNG to the user's Desktop using the stock code in the filename.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
