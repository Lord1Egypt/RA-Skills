## Description:

Estimates resources, schedule, and cost for experimental or training dataset construction, including labor, samples, reagents, equipment, compute, procurement, and delivery planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users, dataset engineers, and research planning teams use this skill to estimate data availability, compliance posture, project effort, and cost ranges for experimental or machine-learning dataset construction. It is most relevant for drug discovery target and indication workflows that need budget planning or quotation review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and tool-scope declarations are under-specified, and dependencies are not pinned or isolated.

Mitigation: Review the dependency and tool-scope configuration before installation, pin dependencies, and run the skill in an isolated environment.

Risk: PatSnap MCP and Office workflow calls can access external services or generate files beyond a simple local estimate.

Mitigation: Require explicit authorization before enabling PatSnap MCP or Office workflow calls, and scope credentials and workspace access to the current task.

Risk: SAR extraction uses polling and may become costly or long-running at scale.

Mitigation: Cap SAR polling and batch patent extraction, using the documented maximum patent setting as an operational limit.

Risk: Compliance ratings are preliminary planning aids, especially for commercial use of patent-derived SAR data or generated compounds.

Mitigation: Treat compliance outputs as risk-screening guidance and require legal review before commercial release or downstream product decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/experiment-dataset-costing)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)
- [Database coverage reference](references/database_coverage.md)
- [Cost benchmarks reference](references/cost_benchmarks.md)
- [Compliance rules reference](references/compliance_rules.md)
- [Field schema reference](references/field_schema.md)
- [MCP tool routing reference](references/mcp_tool_routing.md)
- [ChEMBL](https://www.ebi.ac.uk/chembl/)
- [BindingDB](https://www.bindingdb.org/)
- [PubChem](https://pubchem.ncbi.nlm.nih.gov/)
- [RCSB PDB](https://www.rcsb.org/)
- [ZINC22](https://zinc22.docking.org/)
- [DrugBank](https://go.drugbank.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated DOCX, JSON, CSV, and command-line outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include a dataset scheme report, structured cost summary, compliance matrix, and data inventory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
