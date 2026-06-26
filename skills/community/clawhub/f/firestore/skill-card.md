## Description: <br>
Manage Google Cloud Firestore databases using the Firestore REST API via curl commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felipe0liveira](https://clawhub.ai/user/felipe0liveira) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to construct approved curl commands for creating, reading, querying, updating, deleting, and batching Google Cloud Firestore documents through the REST API. It is suited for Firestore administration and troubleshooting when the active gcloud identity and project have been reviewed first. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Firestore commands can read, modify, or delete data with the permissions of the active Google Cloud identity. <br>
Mitigation: Use a dedicated least-privilege service account, verify the active account and project, and require explicit user approval before running any command. <br>
Risk: Expired or mis-scoped OAuth tokens can cause failed requests or accidental operations against the wrong project. <br>
Mitigation: Generate a fresh access token before each operation and display the active gcloud context before presenting the command. <br>


## Reference(s): <br>
- [ClawHub Firestore release page](https://clawhub.ai/felipe0liveira/firestore) <br>
- [Firebase Firestore REST API reference](https://firebase.google.com/docs/firestore/reference/rest) <br>
- [Google Cloud CLI installation guide](https://docs.cloud.google.com/sdk/docs/install-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use curl with gcloud OAuth access tokens and require explicit user approval before execution.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
