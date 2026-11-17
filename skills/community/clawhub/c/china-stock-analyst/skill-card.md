## Description:

A股短线营收分析助手，聚焦"短线交易信号+营收质量"双轨研判，8位专家并行分析，输出可复核证据链、双轨评分与明确交易条件

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjt0321](https://clawhub.ai/user/wjt0321)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to analyze China A-share short-term opportunities, compare stock candidates, and validate historical stock reports with parallel expert review, data authenticity checks, revenue-quality scoring, and evidence-chain reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist local routing or cache data that may contain stock prompts, portfolio context, strategies, or other personal financial details.

Mitigation: Disable, patch, or regularly purge local route persistence before using sensitive prompts, and avoid entering personal financial details when persistence is enabled.

Risk: Custom EASTMONEY_* URL settings may send API-key-bearing requests to destinations the user did not intend to trust.

Mitigation: Use the default East Money endpoint or only explicitly trusted custom endpoints, and review environment configuration before running network-backed analysis.

Risk: API keys may be exposed if stored in project-local environment files that are copied, shared, or committed outside the expected ignore rules.

Mitigation: Prefer a process environment variable or credential manager for EASTMONEY_APIKEY, keep local .env files out of release artifacts, and rotate any exposed key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjt0321/skills/china-stock-analyst)
- [A股常用估值模型说明](references/估值模型说明.md)
- [china-stock-analyst Agent Teams 编排蓝图](docs/agent-teams-blueprint.md)
- [A股专家 Agent 统一 JSON Schema 标准](docs/agent-json-schema-standard.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with structured JSON expert outputs and shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include evidence chains, timestamps, source URLs, dual-track scores, decision labels, and risk boundaries.]

## Skill Version(s):

2.4.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
