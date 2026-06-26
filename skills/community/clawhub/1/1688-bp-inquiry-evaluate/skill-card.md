## Description: <br>
Evaluates 1688 merchant customer-service and salesperson inquiry handling quality, including team summaries, individual salesperson diagnostics, and improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External 1688 merchants and operations teams use this skill to query team-level and individual salesperson inquiry quality reports, identify weak service patterns, and receive improvement suggestions based on real CLI-returned data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Access Key setup is under-scoped and may write credentials under a different skill identity. <br>
Mitigation: Review the OpenClaw credential storage location before installation, avoid pasting production Access Keys into normal chat, and use credentials only where 1688 business report access is intended. <br>
Risk: Generated reports may include sensitive buyer identifiers, inquiry summaries, and employee performance data. <br>
Mitigation: Limit report access to authorized business users and treat exported or shared report content as sensitive operational data. <br>
Risk: The security verdict is suspicious despite clean static scan results and absent VirusTotal telemetry. <br>
Mitigation: Review the skill before deployment and confirm the credential configuration behavior matches the intended environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1688aiinfra/1688-bp-inquiry-evaluate) <br>
- [1688 team service evaluation page](https://air.1688.com/app/bp-boot/a2a-team-newton/index.html) <br>
- [Business staff evaluation summary guide](artifact/references/capabilities/bp_inquiry_evaluate_summary.md) <br>
- [Business staff evaluation detail guide](artifact/references/capabilities/bp_inquiry_evaluate_sales_detail.md) <br>
- [Access Key configuration guide](artifact/references/capabilities/configure.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and JSON CLI results, with configuration prompts when credentials are missing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ALI_1688_AK credential; queries are read-only and limited to recent date ranges.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
