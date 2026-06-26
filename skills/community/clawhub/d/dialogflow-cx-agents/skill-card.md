## Description: <br>
Manage agents in Google Dialogflow CX via REST API. Use for creating, listing, updating, and deleting chatbot agents. Supports v3beta1 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yash-Kavaiya](https://clawhub.ai/user/Yash-Kavaiya) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and cloud engineers use this skill to manage Dialogflow CX agents in a Google Cloud project. It helps list, create, inspect, update, delete, export, and validate agents using REST examples or the bundled Python CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or delete Dialogflow CX agents when used with Google credentials that have sufficient permissions. <br>
Mitigation: Use least-privilege Google Cloud credentials limited to the intended project and confirm project, location, and agent identifiers before update, restore, or delete operations. <br>
Risk: Destructive changes may remove or overwrite important chatbot agent configuration. <br>
Mitigation: Export or back up important agents before destructive operations. <br>


## Reference(s): <br>
- [Agents API Reference](references/agents.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands, REST request examples, and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated Google Cloud credentials and Dialogflow CX API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
