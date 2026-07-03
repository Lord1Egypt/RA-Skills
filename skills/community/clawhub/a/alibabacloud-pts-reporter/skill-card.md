## Description: <br>
Analyzes historical Alibaba Cloud PTS stress-testing reports, compares optional baselines, and returns ranked report-observable findings with evidence and suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, performance engineers, and SREs use this skill to interpret historical Alibaba Cloud PTS reports, rank report-level issues, and decide when to hand off to PTS scenario or instance-level diagnostic workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read PTS scenes, reports, baselines, and possible live running data even though its primary purpose is historical report analysis. <br>
Mitigation: Run it with a least-privilege RAM role limited to the documented PTS Get/List actions and confirm the requested report identifiers before execution. <br>
Risk: Broad Alibaba Cloud CLI guidance can go beyond the stated PTS reporting scope. <br>
Mitigation: Keep execution to the PTS plugin and read-only PTS reporting commands; avoid unrelated ECS, VPC, RDS, or FC examples unless a separate skill explicitly requires them. <br>
Risk: CLI setup and AI-mode lifecycle commands can change local agent or CLI state. <br>
Mitigation: Confirm setup actions with the user, install only the needed PTS plugin, and disable AI mode at every exit point. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-pts-reporter) <br>
- [Aliyun CLI documentation](https://help.aliyun.com/zh/cli/) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [RAM Policies - alibabacloud-pts-reporter](references/ram-policies.md) <br>
- [Report-Analysis Knowledge Base - alibabacloud-pts-reporter](references/tuning-knowledge-base.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with ranked findings and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a bounded findings list with area, severity, evidence, and suggestion fields; defaults to TopN 5 and does not perform instance-level diagnostics or PTS scenario mutations.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
