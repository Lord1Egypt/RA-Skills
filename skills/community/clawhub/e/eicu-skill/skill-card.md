## Description: <br>
Query the eICU Collaborative Research Database 2.0 by generating SQL and Python code for extracting ICU data including vital signs, labs, GCS, vasopressors, blood gas, oxygenation, and diagnoses from PostgreSQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongfanbeta](https://clawhub.ai/user/yongfanbeta) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, data analysts, and clinical researchers use this skill to generate SQL and Python extraction code for authorized eICU Collaborative Research Database 2.0 analysis. It helps map user requests to the correct eICU tables, fields, filters, and query patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated queries can extract clinical patient-level data from eICU. <br>
Mitigation: Use the skill only with authorized eICU access, review generated SQL before execution, and handle outputs under institutional data-use rules. <br>
Risk: Some examples include database-changing DROP and CREATE statements. <br>
Mitigation: Run those examples only in a sandbox or clearly namespaced workspace, and prefer least-privilege read-only accounts for extraction workflows. <br>
Risk: Python examples require user-supplied database credentials. <br>
Mitigation: Keep credentials outside shared prompts and files, and use restricted accounts scoped to the minimum required database permissions. <br>


## Reference(s): <br>
- [eICU Data Documentation](https://eicu-crd.mit.edu/) <br>
- [eICU SchemaSpy](https://lcp.mit.edu/eicu-schema-spy/index.html) <br>
- [eICU on PhysioNet](https://physionet.org/content/eicu-crd/2.0/) <br>
- [MIT-LCP eicu-code Repository](https://github.com/MIT-LCP/eicu-code) <br>
- [Database Schema Reference](references/schema.md) <br>
- [Common Query Templates](references/common_queries.md) <br>
- [Vital Signs Reference](references/vital_signs.md) <br>
- [Nursecharting Vital Signs Reference](references/vital_signs_nursecharting.md) <br>
- [Laboratory Tests Reference](references/labs.md) <br>
- [Blood Gas Reference](references/blood_gas.md) <br>
- [GCS Reference](references/gcs.md) <br>
- [Vasopressors Reference](references/vasopressors.md) <br>
- [Infusions Reference](references/infusions.md) <br>
- [Medication Orders Reference](references/medications.md) <br>
- [Urine Output Reference](references/urine_output.md) <br>
- [Oxygenation Reference](references/oxygenation.md) <br>
- [Weight Reference](references/weight.md) <br>
- [Diagnoses Reference](references/diagnoses.md) <br>
- [Demographics Reference](references/demographics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Guidance] <br>
**Output Format:** [Markdown containing SQL and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The user supplies database access details and runs generated queries against their own authorized eICU PostgreSQL instance.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
