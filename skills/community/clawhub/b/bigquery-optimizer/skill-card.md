## Description: <br>
Analyze BigQuery query patterns and storage to dramatically reduce the #1 surprise GCP cost driver. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data engineers, and cloud cost owners use this skill to review user-provided BigQuery job, storage, or billing exports and identify query, partitioning, storage, slot reservation, and materialized view savings opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided BigQuery or billing output may expose query text, account emails, table names, and spending details. <br>
Mitigation: Review and redact sensitive data before pasting outputs into the agent. <br>
Risk: Example commands may run in the wrong project or region or with broader access than intended. <br>
Mitigation: Run commands manually in the intended project and region using least-privilege read-only access. <br>
Risk: Credentials or secret keys could be included accidentally with pasted data. <br>
Mitigation: Do not provide credentials or secret keys, and confirm pasted raw data contains no secrets before analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/bigquery-optimizer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/anmolnagpal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with cost breakdowns, recommendations, query rewrite guidance, and example shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output based on user-provided BigQuery or billing data; no credentials or direct GCP account access.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
