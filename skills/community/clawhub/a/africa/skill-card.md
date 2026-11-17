## Description:

Africa provides multilingual query and analysis support for African market policies, regulations, and investment environments using configurable data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and business users use this skill to query African market policy information and summarize investment, trade, tax, labor, and environmental policy context in Chinese or English.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured API keys or sensitive data source values can be returned and cached in normal query results.

Mitigation: Use environment variables for secrets and avoid placing real credentials in dataSources unless the implementation is changed to redact them from returned results, logs, and cache entries.

## Reference(s):

- [ClawHub Africa skill page](https://clawhub.ai/yezhaowang888-stack/skills/africa)
- [DeepSeek](https://deepseek.com)
- [Huimai documentation](https://docs.huimai.ai)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown prose with JavaScript configuration examples and JSON-like query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English output; configured data source values may appear in returned results.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
