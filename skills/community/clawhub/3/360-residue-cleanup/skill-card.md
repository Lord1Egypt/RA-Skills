## Description:

先以只读扫描识别 Windows 上 360 产品的活跃安装与残留，再经逐项确认、备份和分批可回滚清理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要处理 Windows 电脑上 360 产品残留的用户，帮助他们先查看扫描清单，再确认目标、备份数据并分批清理。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup may disrupt active security software, drivers, or services, or remove personal browser data.

Mitigation: Review every proposed target before proceeding, confirm no matched driver or service is active, and back up browser data and registry keys before cleanup.

Risk: The scan may miss relevant items, and rollback protections have gaps.

Mitigation: Treat scan results as incomplete, inspect the generated plan and elevated script before running them, and stop if a target or recovery step is unclear.

## Reference(s):

- [360-fingerprints.md](artifact/references/360-fingerprints.md)
- [sandbox-limits.md](artifact/references/sandbox-limits.md)
- [Project homepage](https://github.com/oracis/360-residue-cleanup)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Code, Shell commands, Guidance]

**Output Format:** [JSON scan inventory, PowerShell cleanup script, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cleanup targets require user review and confirmation; backups and rollback paths are documented.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
