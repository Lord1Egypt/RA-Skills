## Description:

Manage agents in Google Dialogflow CX via REST API for creating, listing, updating, and deleting chatbot agents using the v3beta1 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage Google Dialogflow CX agents in authorized Google Cloud projects, including listing, creating, updating, deleting, exporting, and validating agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delete and export operations can affect production Dialogflow CX agents when run with broad Google Cloud credentials.

Mitigation: Use least-privilege credentials, restrict allowed projects and locations, and avoid granting delete or export permissions unless those operations are required.

Risk: Agent deletion or export may proceed without enough operator confirmation or backup preparation.

Mitigation: Require manual confirmation and verified backups before running delete or export workflows against important agents.

## Reference(s):

- [Agents API Reference](references/agents.md)
- [Dialogflow CX v3beta1 API Base URL](https://dialogflow.googleapis.com/v3beta1)
- [ClawHub Skill Page](https://clawhub.ai/yash-kavaiya/skills/dialogflow-cx-agents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON request examples, and Python CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI prints Dialogflow CX agent details as text or JSON depending on the operation.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
