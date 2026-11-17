## Description:

Queries the eICU Collaborative Research Database 2.0 by generating SQL and Python code for extracting ICU data including vital signs, labs, GCS, vasopressors, blood gas, oxygenation, and diagnoses from PostgreSQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongfanbeta](https://clawhub.ai/user/yongfanbeta)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and clinical data analysts use this skill to have an agent generate eICU 2.0 PostgreSQL queries and Python extraction scripts for ICU variables such as vital signs, labs, GCS, vasopressors, oxygenation, diagnoses, medications, demographics, urine output, and weight. Users run the generated code against their own authorized eICU database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL or Python may include unsafe SQL construction or destructive DDL such as DROP and CREATE statements.

Mitigation: Review every generated query before execution, parameterize user-provided values, and require explicit approval before running DROP, CREATE, or materialized view statements.

Risk: Generated output may expose patient-level data from an eICU database.

Mitigation: Run queries only on authorized eICU data and avoid printing, exporting, or sharing raw patient-level results unless necessary and compliant.

Risk: Database access examples require connection parameters and could be over-privileged if copied directly.

Mitigation: Use a read-only PostgreSQL role for extraction workflows and keep credentials outside prompts, logs, and generated artifacts.

## Reference(s):

- [eICU Data Documentation](https://eicu-crd.mit.edu/)
- [eICU SchemaSpy](https://lcp.mit.edu/eicu-schema-spy/index.html)
- [eICU on PhysioNet](https://physionet.org/content/eicu-crd/2.0/)
- [MIT-LCP eicu-code Repository](https://github.com/MIT-LCP/eicu-code)
- [Database Schema Reference](references/schema.md)
- [Common Query Templates](references/common_queries.md)
- [Vital Signs Queries](references/vital_signs.md)
- [Nursecharting Vital Signs Queries](references/vital_signs_nursecharting.md)
- [Laboratory Queries](references/labs.md)
- [Blood Gas Queries](references/blood_gas.md)
- [GCS Queries](references/gcs.md)
- [Vasopressor Queries](references/vasopressors.md)
- [Infusion Drug Queries](references/infusions.md)
- [Medication Queries](references/medications.md)
- [Oxygenation Queries](references/oxygenation.md)
- [Urine Output Queries](references/urine_output.md)
- [Demographics Queries](references/demographics.md)
- [Diagnoses Queries](references/diagnoses.md)
- [Weight Queries](references/weight.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with SQL and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated queries require user-supplied database connection parameters and authorized eICU access.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
