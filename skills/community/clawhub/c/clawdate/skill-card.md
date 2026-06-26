## Description: <br>
ClawDate is an operator runbook for bootstrapping or re-binding one owner account, validating ClawDate CLI state, collecting profile intake, submitting owner profile JSON, and configuring recurring sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qybaihe](https://clawhub.ai/user/qybaihe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawDate operators use this skill to set up one isolated owner account, complete missing dating-profile intake, submit the owner profile JSON, verify basic browse connectivity, and keep sync running on a recurring schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive dating preferences, internal operator notes, and WeChat contact data. <br>
Mitigation: Confirm owner consent before collecting or submitting profile data, keep private operator notes out of public summaries, and avoid sharing raw logs or local config unless operationally necessary. <br>
Risk: The bootstrap flow can install account automation and create a persistent five-minute sync schedule. <br>
Mitigation: Review the generated wrapper and cron entry before relying on them, use --skip-cron unless continuous syncing is explicitly wanted, and remove scheduled sync when the account should no longer run. <br>
Risk: The install flow depends on the ClawDate service and the @qybaihe npm CLI. <br>
Mitigation: Install only when those services and the operator are trusted, and avoid remote SOURCE installs unless provenance or checksums are verified. <br>
Risk: The profile template includes automatic session acceptance and contact exchange defaults. <br>
Mitigation: Review auto-accept and auto-exchange settings against the owner's contact release rule before enabling live matching or contact handling. <br>


## Reference(s): <br>
- [ClawDate on ClawHub](https://clawhub.ai/qybaihe/clawdate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may write local profile JSON, wrapper scripts, logs, and cron entries when executed.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
