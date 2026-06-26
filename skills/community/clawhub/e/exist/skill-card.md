## Description: <br>
Exist provides a managed OAuth integration for agents to read health and fitness data, retrieve correlations and insights, manage attribute ownership, and track wellness metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Exist through ClawLink OAuth, query tracked health and lifestyle data, inspect correlations and insights, and update owned attribute values when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive Exist health and lifestyle data, including profile, attributes, correlations, and insights. <br>
Mitigation: Install it only when this access is intended, grant the minimum OAuth scopes needed, and prompt the agent with the specific Exist data to retrieve. <br>
Risk: Broad activation and confirmation-free read operations may expose more personal data than a user expected. <br>
Mitigation: Review requested read operations before use and treat returned health, fitness, correlation, and insight data as sensitive. <br>
Risk: Ownership-management tools can change or stop data flow for Exist attributes. <br>
Mitigation: Require explicit confirmation for acquire, increment, and release ownership actions, especially release operations. <br>


## Reference(s): <br>
- [Exist API Docs](https://developer.exist.io/) <br>
- [ClawLink Docs for OpenClaw](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/exist) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent outputs can include Exist profile, attribute, correlation, insight, and ownership-management results returned through ClawLink tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
