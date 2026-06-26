## Description: <br>
Manage flows and pages in Google Dialogflow CX via REST API. Use for creating and organizing conversation paths within agents. Supports v3beta1 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yash-Kavaiya](https://clawhub.ai/user/Yash-Kavaiya) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and conversation designers use this skill to manage Google Dialogflow CX flows and pages, including listing, creating, inspecting, and organizing conversation paths within agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide state-changing Dialogflow CX operations, including creating, updating, deleting, importing, and loading flow versions. <br>
Mitigation: Review each mutation command before execution and export or back up flows before allowing destructive or restore operations. <br>
Risk: The skill requires Google Dialogflow CX credentials that may allow modification of cloud resources. <br>
Mitigation: Use least-privilege Google Cloud credentials and avoid placing bearer tokens or service account material in chats, logs, or shared files. <br>


## Reference(s): <br>
- [Flows & Pages API Reference](references/flows.md) <br>
- [Dialogflow CX v3beta1 API base URL](https://dialogflow.googleapis.com/v3beta1) <br>
- [Dialogflow CX regional API endpoint pattern](https://{region}-dialogflow.googleapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with REST examples, bash commands, and Python CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands or API payload examples that operate on Google Dialogflow CX resources when executed by the user or agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
