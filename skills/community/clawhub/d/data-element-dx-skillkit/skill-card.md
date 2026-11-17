## Description:

End-to-end seven-skill kit for data-element transformation of Chinese SOEs and traditional conglomerates, covering industry research, baseline survey, architecture, quality, application planning, delivery orchestration, and executive reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bdhunter](https://clawhub.ai/user/bdhunter)

### License/Terms of Use:

Apache-2.0

## Use Case:

Consultants, enterprise data teams, and transformation leads use this skill suite to plan and package data-element digital transformation work for Chinese SOEs and traditional conglomerates. It helps route work across seven delivery skills and produce asset inventories, quality checks, architecture plans, application roadmaps, and board-facing materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The baseline scanner can enumerate local data files and preview CSV or TSV headers in generated inventories.

Mitigation: Run scans only on explicit approved directories, review header previews before sharing reports, and keep generated inventories in a controlled workspace.

Risk: The suite can produce board-facing and consulting materials that may include business assumptions, data quality conclusions, or data-asset capitalization recommendations.

Mitigation: Treat outputs as draft methodology and analysis; have responsible business, legal, accounting, and data owners review conclusions before external use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bdhunter/skills/data-element-dx-skillkit)
- [DCMM / DMBOK alignment reference](_shared/references/DCMM-DMBOK对标.md)
- [Seven-process methodology](_shared/references/七道工序方法论.md)
- [Data architecture blueprint template](_shared/references/数据架构蓝图模板.md)
- [Data-element policy index](_shared/references/数据要素政策索引.md)
- [Data quality rule library](_shared/references/数据质量规则库.md)
- [Data asset inventory template](_shared/references/数据资产盘点模板.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown deliverables with optional JSON, CSV, Python script output, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces consulting artifacts and local scan or gate-check outputs; generated inventories and reports should remain in a controlled workspace.]

## Skill Version(s):

2.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
