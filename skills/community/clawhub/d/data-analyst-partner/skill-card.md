## Description: <br>
Act as a Grafana-first product and business data analysis partner for an app team. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qwqcode](https://clawhub.ai/user/qwqcode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, content, operations, and analytics teammates use this skill to interpret existing Grafana dashboards, request metric splits, prepare short daily reports, clarify new dashboard requirements, and escalate to datasource or ClickHouse queries only when existing dashboards are insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may expose or analyze sensitive internal business data if used outside an authorized analytics context. <br>
Mitigation: Use only with agent permissions that are allowed to view the relevant Grafana, datasource, or ClickHouse data. <br>
Risk: Direct SQL or datasource-query steps can affect sensitive production datasets or produce misleading results if run without review. <br>
Mitigation: Review datasource and direct ClickHouse query steps before execution, and prefer existing Grafana dashboards whenever they answer the question. <br>
Risk: Unclear metric definitions, incomplete variables, or small samples can lead to overconfident interpretations. <br>
Mitigation: Name the data source path used, state caveats, and avoid claiming causation from correlation. <br>


## Reference(s): <br>
- [Data Analyst Partner release page](https://clawhub.ai/qwqcode/data-analyst-partner) <br>
- [Daily Report Template](references/daily-report-template.md) <br>
- [New Dashboard Confirmation Checklist](references/dashboard-confirmation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown analysis with concise conclusions, source notes, caveats, follow-up recommendations, and occasional datasource or SQL query guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill prioritizes existing Grafana dashboards and panels before datasource queries or direct ClickHouse queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
