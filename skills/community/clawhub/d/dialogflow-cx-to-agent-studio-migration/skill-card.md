## Description:

Migrates Dialogflow CX agents to CX Agent Studio (CES) using official REST/RPC APIs by exporting full CX agent packages, validating components, creating CES apps or remote Dialogflow agents, and generating a migration report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to migrate Dialogflow CX agents into CX Agent Studio while preserving CX components through a remote Dialogflow agent configuration. It supports export-only review, CES app and agent creation, root-agent assignment, and JSON migration reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google access tokens may be sent to untrusted endpoints if custom base URLs are supplied.

Mitigation: Keep the default Google API endpoints unless the replacement endpoint is fully trusted and reviewed.

Risk: Running the migration can create or modify durable CX Agent Studio resources.

Mitigation: Evaluate with `--export-only` first, then run with a non-production project or a least-privilege service account.

Risk: Exported Dialogflow agent contents are written to local disk and may contain sensitive configuration or conversation design data.

Mitigation: Review and protect the output directory, and remove exported artifacts when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yash-kavaiya/skills/dialogflow-cx-to-agent-studio-migration)
- [Dialogflow CX v3beta1 API endpoint](https://dialogflow.googleapis.com/v3beta1)
- [CX Agent Studio v1beta API endpoint](https://ces.googleapis.com/v1beta)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes Dialogflow CX export archives, extracted export contents, and migration_report.json when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
