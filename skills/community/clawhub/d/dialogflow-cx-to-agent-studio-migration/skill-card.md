## Description: <br>
Migrate Dialogflow CX agents to CX Agent Studio (CES) using official REST/RPC APIs. Exports full CX agent packages, validates components (intents, entities, flows, pages, etc.), and creates CES apps/agents (remote Dialogflow agent) with a migration report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yash-Kavaiya](https://clawhub.ai/user/Yash-Kavaiya) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and cloud engineers use this skill to migrate a Dialogflow CX agent into CX Agent Studio while preserving the CX agent as a remote Dialogflow agent. It exports and indexes the source agent package, creates or updates CES resources, and writes a migration report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The migration uses Google Cloud credentials that can export Dialogflow CX data and create or update CX Agent Studio resources. <br>
Mitigation: Use least-privilege Google Cloud credentials, review the target project and location before running, and run export-only first when possible. <br>
Risk: Generated export archives and extracted files may contain sensitive agent configuration. <br>
Mitigation: Store output in a protected location, restrict access to generated files, and delete the export archive and extracted folder when they are no longer needed. <br>
Risk: Custom base URLs can redirect requests away from the default Google API endpoints. <br>
Mitigation: Use the default Dialogflow and CES API endpoints unless a custom endpoint is fully trusted and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Yash-Kavaiya/dialogflow-cx-to-agent-studio-migration) <br>
- [Dialogflow API v3beta1 endpoint](https://dialogflow.googleapis.com/v3beta1) <br>
- [CES API v1beta endpoint](https://ces.googleapis.com/v1beta) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON files] <br>
**Output Format:** [Markdown guidance with bash commands and generated JSON artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Dialogflow CX export archive, extracted export files, and a migration_report.json file when the migration script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
