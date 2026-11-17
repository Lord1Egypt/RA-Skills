## Description:

DNFM 周本进度追踪。用于查询/更新新超越本、老超越本、周本、雷龙、团本进度。支持周五自动重置新超越本等刷新逻辑。支持自定义总量和启用/禁用副本。自动从 /root/.openclaw/workspace/dnfm-tracker/progress.json 读写数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[crazzies](https://clawhub.ai/user/crazzies)

### License/Terms of Use:


## Use Case:

External DNFM players use this skill to query and update weekly dungeon progress, adjust run totals, and enable or disable tracked dungeon categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tracker stores and mutates progress in fixed local JSON files.

Mitigation: Confirm the configured file paths before use and keep a backup of important progress or configuration data.

Risk: Progress may be reset when the tracker is invoked repeatedly on a refresh day after 06:00.

Mitigation: Check the refresh schedule before updating progress and avoid repeated invocations after a reset unless the reset is intended.

Risk: An unrelated MLOL documentation file is bundled with the artifact and may confuse the skill scope.

Mitigation: Ignore that documentation when evaluating or using the DNFM tracker unless it is intentionally retained as reference material.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local JSON progress and configuration files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
