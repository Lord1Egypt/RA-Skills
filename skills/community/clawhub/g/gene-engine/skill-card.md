## Description: <br>
Gene系统自动化引擎 — Agent行为规则的退役检查、冷却期管理、主动探测、健康评分。让Agent的规则系统从「人驱动」变成「代码驱动」。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smilepeng0612](https://clawhub.ai/user/smilepeng0612) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Gene Engine to manage OpenClaw Gene rule lifecycle state, including retirement checks, cooldown recovery, active probing, trigger tracking, and health scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill rewrites persistent OpenClaw rule memory. <br>
Mitigation: Back up gene-state.json before recurring use and review early state changes manually. <br>
Risk: A helper script can execute unintended local Python from crafted input text. <br>
Mitigation: Avoid untrusted or free-form text in gene-trigger.sh until its Python argument handling is patched. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/smilepeng0612/gene-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Terminal text reports with a machine-readable JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates OpenClaw Gene state files and appends a metrics log during recurring use.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
