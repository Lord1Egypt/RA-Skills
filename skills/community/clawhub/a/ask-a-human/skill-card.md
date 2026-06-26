## Description: <br>
Ask a Human lets an agent request crowdsourced human judgment for subjective decisions such as tone, style, ethics, and reality checks when asynchronous responses are acceptable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manuelkiessling](https://clawhub.ai/user/manuelkiessling) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to ask a crowdsourced pool for opinions on subjective choices, then poll asynchronously and apply consensus or fallback judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted prompts may leave the user's environment and be read by unknown human reviewers. <br>
Mitigation: Redact confidential, personal, customer, credential, source-code, vulnerability, strategy, and unreleased business context before asking a question. <br>
Risk: Responses are asynchronous and may be delayed or never arrive. <br>
Mitigation: Store the question ID, poll with a timeout, and proceed with a fallback plan when responses are unavailable. <br>
Risk: Crowdsourced opinions can be subjective and may lack project context. <br>
Mitigation: Write self-contained questions and treat responses as advisory input rather than authoritative decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/manuelkiessling/ask-a-human) <br>
- [Ask-a-Human Web App](https://app.ask-a-human.com) <br>
- [Ask-a-Human API Documentation](https://api.ask-a-human.com/docs) <br>
- [README](README.md) <br>
- [Usage Examples](examples/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ASK_A_HUMAN_AGENT_ID and asynchronous polling; human responses may be delayed or absent.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
