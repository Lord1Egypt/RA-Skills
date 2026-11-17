## Description:

帮助数据工程师设计、生成和审查数据仓库运维材料，涵盖 SSOT、ETL/ELT、维度建模、数据质量、分区策略、成本优化、治理、血缘和 SLA 监控。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to plan, generate, and review data warehouse operations assets across modeling, ETL/ELT, data quality, governance, lineage, cost optimization, and SLA monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL, Python, and warehouse recommendations could be incorrect or unsafe if applied without review.

Mitigation: Review generated code and commands before deploying them to production data warehouse, orchestration, or governance systems.

Risk: Generated files and HTML reports can be affected by untrusted inputs or unintended output paths.

Mitigation: Run the skill in a sandbox, use trusted inputs where possible, avoid hosting reports built from untrusted data, and verify output directories before execution.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/bettermen/skills/data-warehouse-ops)
- [Data Quality Rules Reference](references/data_quality_rules.md)
- [Dimensional Modeling Best Practices](references/dimensional_modeling.md)
- [Data Governance Framework](references/governance_framework.md)
- [Partition Strategies Reference](references/partition_strategies.md)
- [SLA Templates](references/sla_templates.md)
- [SQL Templates for Data Warehouse](references/sql_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with SQL, Python, YAML, JSON, DOT, and HTML outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may write generated files such as DDL, metadata JSON, quality checks, pipeline templates, lineage visualizations, cost reports, and SLA dashboards.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
