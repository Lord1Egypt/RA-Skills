## Description:

Full production-grade migration of a Dialogflow CX agent (v3beta1) to Google Customer Engagement Suite (CES) Conversational Agents, including flows, pages, intents, entity types, webhooks, test cases, retry logic, dry-run mode, and a migration report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and migration engineers use this skill to convert Dialogflow CX agents into CES Conversational Agents assets, including an importable agent JSON, golden evaluation CSV, exported entity types, and a migration report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CES instructions may carry over prompt-injection text or unsuitable behavior from the source Dialogflow CX agent.

Mitigation: Review every generated instruction in ces_agent.json before importing the agent into CES.

Risk: Migrated webhook tools may reference endpoints or authentication settings that are not appropriate for the target CES environment.

Mitigation: Confirm each webhook endpoint and authentication setting before production use.

Risk: Running the migration requires Google Cloud access to the source Dialogflow CX agent.

Mitigation: Run in an isolated environment using the minimum GCP permissions needed to read the source agent.

Risk: Unpinned Python dependencies can change behavior across migration runs.

Mitigation: Pin dependencies for production migration workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yash-kavaiya/skills/dialogflow-cx-to-ces-migration)
- [CES Console](https://ces.cloud.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands plus generated JSON, CSV, and Markdown migration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ces_agent.json, golden_evals.csv, entity_types.json, and migration_report.md; supports dry-run mode.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
