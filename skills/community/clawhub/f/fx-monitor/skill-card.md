## Description:

Monitor Bank of China FX rates and manage reusable GBP/HKD/JPY alert workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiehuapeng](https://clawhub.ai/user/xiehuapeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check current Bank of China exchange rates, compare GBP/HKD/JPY values against saved history, produce Chinese alert text, and help configure recurring FX monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the release suspicious because it can run a user-specific external script path.

Mitigation: Review the skill before installing and adjust the workflow to execute the bundled checker through a relative or otherwise trusted path.

Risk: Cron management could disable unrelated scheduled jobs.

Mitigation: Do not let the skill manage cron unless the workflow is changed or confirmed to preserve all existing scheduled jobs.

Risk: The checker fetches a public FX page and writes local CSV history.

Mitigation: Run it only in environments where outbound Bank of China page access and local history storage are acceptable.

## Reference(s):

- [FX Monitor ClawHub page](https://clawhub.ai/xiehuapeng/skills/fx-monitor)
- [Bank of China foreign exchange rates](https://www.boc.cn/sourcedb/whpj/)
- [Publisher profile](https://clawhub.ai/user/xiehuapeng)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese alert text, NO_REPLY status, or concise Markdown status with command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit ALERT, NO_ALERT, or ERROR handling guidance based on checker key-value output.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
