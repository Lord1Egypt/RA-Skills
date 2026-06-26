## Description: <br>
Diagnose and fix OpenClaw cron job delivery failures using scripts that reduce manual configuration errors around silent delivery failures, missing delivery parameters, and invalid session or payload combinations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shimonxin](https://clawhub.ai/user/shimonxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw cron jobs that appear to run but do not deliver scheduled messages. It helps repair delivery configuration for individual jobs or batches after the operator reviews the intended channel, recipient, and account values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk repair scripts can persistently rewrite scheduled message delivery targets. <br>
Mitigation: Run diagnose.sh first, back up or export existing cron configuration, replace hard-coded channel, recipient, and account values with intended values, and prefer single-job repair where possible. <br>
Risk: Using fix-all.sh before review can apply incorrect delivery settings across multiple cron jobs. <br>
Mitigation: Review exactly which jobs will be changed before bulk repair and rerun diagnose.sh after any fix to confirm the resulting configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shimonxin/cron-delivery-fix) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to run diagnostic, single-job repair, bulk repair, or restore scripts after reviewing cron delivery targets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
