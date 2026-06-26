## Description: <br>
Migrates a Dialogflow CX v3beta1 agent to Google Customer Engagement Suite Conversational Agents format, producing CES agent JSON, golden evaluation CSV, entity type JSON, and a migration report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and migration engineers use this skill to convert authorized Dialogflow CX agents into CES Conversational Agents assets, then review and import the generated files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migration files can contain sensitive Dialogflow CX agent configuration, webhook endpoints, routing phrases, and evaluation content. <br>
Mitigation: Store generated files securely, limit sharing, and review outputs before importing them into CES. <br>
Risk: Running the migration requires access to the target GCP project and Dialogflow CX agent. <br>
Mitigation: Run only with authorized least-privilege credentials and use --dry-run before generating files. <br>
Risk: Migrated webhook URLs, authentication, consent language, and broad routing phrases may need adjustment before production use. <br>
Mitigation: Review webhook endpoints, authentication settings, consent language, and routing phrases before importing or deploying the CES agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yash-kavaiya/dialogflow-cx-to-ces-migration) <br>
- [CES Console](https://ces.cloud.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, markdown, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated artifacts are JSON, CSV, and Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ces_agent.json, golden_evals.csv, entity_types.json, and migration_report.md; supports dry-run preview before writing files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
