## Description:

Query and analyze SLS logs with Source Models or Context Models, or delegate multi-turn analysis to SLS DataAgent Chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use it to investigate SLS logs through Context or Source Models, review model readiness, and submit or continue multi-turn DataAgent Chat analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The chat workflow sends the user's request and constraints to a cloud DataAgent.

Mitigation: Exclude secrets and sensitive data unless your organization's cloud data policy permits sharing them.

Risk: The skill includes executable scripts that use environment, file, network, and shell capabilities.

Mitigation: Review the selected workflow before execution and keep credentials and RAM permissions scoped to the SLS resources it needs.

## Reference(s):

- [Model-based data analysis](references/model-data-qa.md)
- [SLS DataAgent Chat workflow](references/data-agent-chat.md)
- [RAM permissions](references/ram-policies.md)
- [CLI installation and configuration](references/cli-installation-guide.md)
- [Aliyun CLI installation](https://help.aliyun.com/zh/cli/)
- [Aliyun CLI credential configuration](https://help.aliyun.com/zh/cli/configure-credentials/)
- [Configure SLS DataAgent permissions](https://help.aliyun.com/zh/sls/configure-sls-dataagent-permissions)

## Skill Output:

**Output Type(s):** [Analysis, Text, SQL, Shell commands, JSON, Guidance]

**Output Format:** [Markdown summaries with SQL or shell commands and structured JSON results as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include query evidence, data sources, model readiness findings, and follow-up guidance.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata; manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
