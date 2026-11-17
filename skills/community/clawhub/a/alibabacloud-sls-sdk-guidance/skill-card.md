## Description: <br>
Provides Alibaba Cloud SLS and Aliyun Log SDK installation, quickstart, usage guidance, and SDK selection advice across programming languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and apply Alibaba Cloud SLS SDKs for installation, log writing, log consumption, log querying, and integration with Producer, Consumer, or logging framework Appender libraries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SDK examples may involve credentials for Alibaba Cloud SLS. <br>
Mitigation: Prefer STS or role-based credentials, avoid static AccessKeys in mobile apps, and apply least-privilege SLS permissions before production use. <br>
Risk: Generated logging examples may send secrets, personal data, or regulated data to SLS. <br>
Mitigation: Redact sensitive fields and review retention, consent, and data-residency requirements before sending log data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-sls-sdk-guidance) <br>
- [SLS SDK Route](references/route.md) <br>
- [Install SLS SDKs](references/scenarios/install.md) <br>
- [Write Logs](references/scenarios/write-logs.md) <br>
- [Consume Logs](references/scenarios/consume-logs.md) <br>
- [Query Logs](references/scenarios/query-logs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with SDK recommendations, commands, code examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill with no executable behavior.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
