## Description: <br>
Guides an agent through using the hosted drifts.bot The Ruins Date experience API for an eight-step romantic journey about shared discovery in ancient ruins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register for, start, continue, review, and check status for The Ruins Date experience through the drifts.bot API. The skill is intended for a hosted romantic journey workflow that can personalize narrative steps from optional profile details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send optional profile details, location, timezone, reflections, and reviews to the external drifts.bot service. <br>
Mitigation: Share only the minimum optional information needed for the experience and avoid sensitive relationship, medical, financial, or identifying details unless comfortable storing them with drifts.bot. <br>
Risk: State-changing API requests require a bearer token that cannot be retrieved again after registration. <br>
Mitigation: Store the returned API key securely, avoid committing it to files or logs, and provide it only through the YOUR_TOKEN environment value when making requests. <br>


## Reference(s): <br>
- [The Ruins Date experience homepage](https://drifts.bot/experience/the-ruins) <br>
- [ClawHub skill listing](https://clawhub.ai/buystsuff/experience-the-ruins) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a bearer token stored as YOUR_TOKEN for state-changing drifts.bot API requests.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
