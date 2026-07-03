## Description: <br>
AutoTable usage guidance for a JDBC-based Java database table automation framework, covering annotations, configuration, database adapters, lifecycle hooks, SPI extension, SQL auditing, data initialization, and multi-data-source usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imtzc](https://clawhub.ai/user/imtzc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to answer AutoTable implementation questions and produce practical Java, YAML, XML, and SQL guidance for configuring automated table maintenance across supported databases. It is most useful when selecting run modes, annotations, database-specific behavior, lifecycle hooks, type mappings, and production deployment practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AutoTable guidance includes database lifecycle settings that can create, drop, or automatically update tables and columns, which can cause data loss in production. <br>
Mitigation: Review lifecycle settings before use; prefer validate, dry-run, or reviewed migration flows for live systems, and require backups, migration review, explicit approval, and tested rollback plans before enabling create, auto-drop, or automatic update behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imtzc/autotable-usage) <br>
- [Server-Resolved GitHub Source](https://github.com/dromara/auto-table-claude-plugin) <br>
- [AutoTable Quick Start](references/quick-start.md) <br>
- [AutoTable Annotation Reference](references/annotation-reference.md) <br>
- [AutoTable Configuration Reference](references/configuration.md) <br>
- [AutoTable Lifecycle Hooks and Interceptors](references/lifecycle.md) <br>
- [AutoTable Database-Specific Features](references/database-specific.md) <br>
- [AutoTable Type Mapping](references/type-mapping.md) <br>
- [AutoTable Multi-Data-Source Usage](references/multi-datasource.md) <br>
- [AutoTable Best Practices](references/best-practices.md) <br>
- [AutoTable Architecture and Extension](references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with Java, YAML, XML, and SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database safety recommendations for schema automation workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
