## Description: <br>
数据仓库运维技能帮助数据工程团队设计、生成和检查数仓建模、ETL/ELT、数据质量、分区、成本优化、治理、血缘和 SLA 监控资产。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data engineers, analytics engineers, and warehouse platform teams use this skill to plan warehouse architecture and generate operational assets for modeling, pipelines, quality checks, partitioning, cost optimization, governance, lineage, and SLA monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Warehouse-related files such as SQL, DDL, query logs, billing exports, and pipeline histories may contain sensitive operational or business data. <br>
Mitigation: Use redacted samples where possible and avoid providing production secrets or unnecessary sensitive rows to the agent. <br>
Risk: Generated SQL, Airflow DAGs, and dbt models can affect warehouse tables or pipelines if run without review. <br>
Mitigation: Review generated assets in a non-production environment before execution, especially statements that overwrite, merge, truncate, or drop tables. <br>
Risk: Generated HTML reports load JavaScript from CDN sources. <br>
Mitigation: Open generated reports only in environments where CDN-loaded JavaScript is acceptable under local security policy. <br>


## Reference(s): <br>
- [数据治理框架 (Data Governance Framework)](references/governance_framework.md) <br>
- [SQL 模板库 (SQL Templates for Data Warehouse)](references/sql_templates.md) <br>
- [维度建模最佳实践 (Dimensional Modeling Best Practices)](references/dimensional_modeling.md) <br>
- [数据质量规则库 (Data Quality Rules Reference)](references/data_quality_rules.md) <br>
- [分区策略参考 (Partition Strategies Reference)](references/partition_strategies.md) <br>
- [SLA 定义模板 (SLA Templates)](references/sla_templates.md) <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/data-warehouse-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL, YAML, Python, shell commands, and generated HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate DDL, dbt or Airflow templates, data quality checks, lineage graphs, cost reports, and SLA dashboards for review before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
