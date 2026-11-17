## Description:

全栈测试工程师覆盖测试全生命周期，帮助生成测试策略、测试用例、自动化测试脚本、API 测试、缺陷分析、测试报告以及 LLM、RAG 和 AI Agent 测试方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shylamb-token](https://clawhub.ai/user/shylamb-token)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and product teams use this skill to plan coverage, draft executable tests, analyze defects, and produce release-quality testing reports across web, API, mobile, performance, and AI-system workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated load or performance tests could affect production systems if run without authorization.

Mitigation: Run load tests only against systems you own or are authorized to test, and default to staging or isolated environments.

Risk: Generated defect reports, Jira or ZenTao tickets, and AI evaluation records may expose credentials, private prompts, logs, or user data.

Mitigation: Redact secrets and sensitive data before sending reports to trackers, model APIs, or shared storage.

Risk: Prompt-attack and unsafe evaluation examples can be misused outside legitimate AI security testing.

Mitigation: Use adversarial AI tests only in controlled, authorized review workflows and replace unsafe examples where possible.

Risk: Plaintext caching of prompts, outputs, or evaluation data may retain sensitive information.

Mitigation: Avoid plaintext caches for sensitive content; disable caching, redact values, or use approved protected storage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shylamb-token/skills/full-stack-test-engineer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and structured tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include runnable test templates, CI configuration, report formats, and remediation guidance.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
