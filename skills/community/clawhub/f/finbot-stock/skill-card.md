## Description:

A股短线量化分析工具 — 实时行情、9因子选股、多空辩论+风控审查、推荐追踪闭环。数据源：新浪财经+东方财富（免费行情）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhubohan190601-crypto](https://clawhub.ai/user/zhubohan190601-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect free A-share market data, calculate short-term technical factors, generate long/short debate analysis with risk review, and track recommendation outcomes. It supports market screening and reporting workflows, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial analysis can be incorrect or misleading, and the skill's own compliance statement says outputs are not investment advice.

Mitigation: Treat results as informational analysis only and require independent human review before any trading decision.

Risk: Some market data is fetched over unauthenticated HTTP or public finance endpoints, which can affect integrity and availability.

Mitigation: Cross-check important prices, flows, and indicators against trusted market data before acting on the output.

Risk: Recommendation, report, audit, and tracking files may persist strategy details locally.

Mitigation: Run the skill as an unprivileged user and keep generated local records in an access-controlled workspace.

Risk: Untrusted stock-code strings may be passed into command-line or data-fetching workflows.

Mitigation: Use known stock-code formats and avoid passing untrusted or unexpected strings to the scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhubohan190601-crypto/skills/finbot-stock)
- [Sina Finance data source](https://finance.sina.com.cn)
- [Sina K-line API endpoint](https://quotes.sina.cn/cn/api/json_v2.php)
- [Eastmoney data source](http://data.eastmoney.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON-like Python dictionaries, shell commands, and Python import snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local reports, audit logs, and tracking records under the skill directory when its scripts are executed.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
