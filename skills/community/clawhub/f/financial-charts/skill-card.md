## Description:

根据财务数据生成精美的ECharts HTML图表页面，支持折线图、饼图、柱状图、K线图等

This skill is ready for commercial/non-commercial use.

## Publisher:

[novaair026-dev](https://clawhub.ai/user/novaair026-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn supplied financial datasets and chart preferences into a styled, responsive HTML chart page. It supports trend, composition, comparison, relationship, and candlestick-style financial visualizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can execute unsafe user-supplied title or data content when opened.

Mitigation: Use only trusted chart titles and financial datasets until generated HTML and script data are escaped safely.

Risk: Generated chart pages load unverified third-party JavaScript from jsDelivr.

Mitigation: Bundle ECharts locally or use integrity-checked dependencies before deploying generated charts in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/novaair026-dev/skills/financial-charts)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [HTML file plus command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated chart pages load ECharts from jsDelivr when opened.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
