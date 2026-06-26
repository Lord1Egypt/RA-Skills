## Description: <br>
Create and run multi-agent AI workflows on AIProx. Chain agents into scheduled pipelines. Pay per execution in sats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to create, run, list, inspect, and delete AIProx workflows that chain multiple agents into scheduled or on-demand pipelines with email or webhook delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AIPROX_SPEND_TOKEN is a billing credential that could be exposed through source control, shared configuration, or logs. <br>
Mitigation: Store the token only in the MCP server environment or a secrets manager, and avoid committing or printing it. <br>
Risk: Scheduled workflows can continue spending sats if a schedule is created incorrectly or left enabled. <br>
Mitigation: Review estimated sats costs and schedule settings before creating recurring runs, and delete workflows that should no longer execute. <br>
Risk: Workflow outputs may be delivered to email or webhook destinations outside the user's direct control. <br>
Mitigation: Use only trusted destination addresses or webhook URLs and verify delivery settings before running or scheduling workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/unixlamadev-spec/aiprox-workflows) <br>
- [AIProx Workflows](https://aiprox.dev/workflows) <br>
- [AIProx Templates](https://aiprox.dev/templates) <br>
- [AIProx Registry](https://aiprox.dev/registry.html) <br>
- [LightningProx Spend Token](https://lightningprox.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls, Text] <br>
**Output Format:** [Markdown with inline commands, JSON configuration examples, and workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workflow IDs, job IDs, run history, sats spent, schedule details, and email or webhook delivery settings.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
