## Description: <br>
Monitor Bank of China FX rates and manage reusable GBP/HKD/JPY alert workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiehuapeng](https://clawhub.ai/user/xiehuapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check current Bank of China GBP, HKD, and JPY rates, compare them with local history, and receive Chinese alert messages or status reports. It also supports setup and troubleshooting for recurring FX monitor cron runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron setup could enable or modify recurring local execution in a way the user did not intend. <br>
Mitigation: Review the exact cron entry before applying it and keep only the FX monitor cron enabled unless the user asks otherwise. <br>
Risk: The checker depends on a public Bank of China page and may fail or produce an error if the page, network, or parser behavior changes. <br>
Mitigation: Handle ERROR status as a short failure message and inspect the page or script before relying on alert decisions. <br>
Risk: Alerts are produced in Chinese by default, which may not fit every user's workflow. <br>
Mitigation: Ask for English or another language when Chinese alert text is not suitable. <br>
Risk: A host-specific script path in the skill instructions may not match the user's installed skill path. <br>
Mitigation: Confirm the actual skill installation path before running or scheduling the checker. <br>


## Reference(s): <br>
- [FX Monitor ClawHub release](https://clawhub.ai/xiehuapeng/fx-monitor) <br>
- [xiehuapeng publisher profile](https://clawhub.ai/user/xiehuapeng) <br>
- [Bank of China foreign exchange rates](https://www.boc.cn/sourcedb/whpj/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and concise Chinese text derived from key-value command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local CSV history file and may return NO_REPLY when no alert is triggered.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
