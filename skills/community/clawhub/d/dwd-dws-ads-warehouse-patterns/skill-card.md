## Description: <br>
Provides production-tested SQL patterns for DWD, DWS, and ADS layered data warehouse modeling, including dimension explosion, multi-period aggregation, OLAP multi-select deduplication, and historical period freezing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fang-zeqiang](https://clawhub.ai/user/fang-zeqiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data engineers, analytics engineers, and warehouse architects use this skill to design layered DWD/DWS/ADS tables and generate SQL patterns for weekly and monthly rollups, deduplicated OLAP reporting, and dashboard-ready datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL patterns can affect warehouse data if run with incorrect partition dates, INSERT OVERWRITE targets, or table definitions. <br>
Mitigation: Review generated SQL carefully before execution, confirming write partitions, table targets, and DDL column order against the intended warehouse design. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fang-zeqiang/dwd-dws-ads-warehouse-patterns) <br>
- [Publisher homepage](https://zeqiang.fun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL and Mermaid code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated SQL should be reviewed before warehouse execution, especially partition dates, INSERT OVERWRITE targets, and DDL column order.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
