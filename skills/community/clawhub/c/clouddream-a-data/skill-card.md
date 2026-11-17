## Description:

获取A股市场资金流向、新闻、筹码分布、龙虎榜、涨停板、盘口异动、板块异动和单只股票详情等多维度数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[glory904649854](https://clawhub.ai/user/glory904649854)

### License/Terms of Use:

MIT

## Use Case:

Developers and market-data agents use this skill to query A-share market data and return normalized OpenClaw-style results for stock research workflows. It is suited for retrieving current records and details, not for making unsupervised investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies can change behavior across installs.

Mitigation: Install in an isolated environment and pin or lock pandas, requests, and beautifulsoup4 before deployment.

Risk: The skill sends requested stock symbols to Eastmoney and Sina Finance and depends on those services being reachable.

Mitigation: Use it only where those external requests are acceptable, and handle request failures or rate limits in the calling workflow.

Risk: Yesterday limit-up and market-anomaly outputs may be unreliable until the referenced endpoints are corrected.

Mitigation: Treat those outputs as advisory data and cross-check them before using them in downstream market analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glory904649854/skills/clouddream-a-data)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [OpenClaw-style JSON objects with success, data, and message fields; data contains stock records, news records, market lists, or stock detail dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Functions may contact Eastmoney and Sina Finance endpoints and may return failure messages when remote requests fail or data is unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, setup.py, and __init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
