## Description: <br>
Manage conversations and sessions in Google Dialogflow CX via REST API. Use for testing intents, handling user interactions, and managing conversation state. Supports v3beta1 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yash-Kavaiya](https://clawhub.ai/user/Yash-Kavaiya) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to test Dialogflow CX conversation flows, detect or match intents, and create conversation test cases through REST API examples and a Python CLI wrapper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dialogflow CX requests and test cases can include sensitive user text, audio, location, or regulated data. <br>
Mitigation: Use least-privilege Google Cloud credentials and avoid real customer audio, secrets, regulated data, or precise location data in examples and tests. <br>
Risk: Running test cases or conversation operations against a production Dialogflow CX agent can unintentionally affect production workflows. <br>
Mitigation: Prefer test or staging agents, and deliberately confirm the target environment before running test cases against production. <br>


## Reference(s): <br>
- [Conversations & Testing API Reference](references/conversations.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Yash-Kavaiya/dialogflow-cx-conversations) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with REST API examples, curl commands, and Python CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google Cloud Dialogflow CX credentials and the Dialogflow CX API to be enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
