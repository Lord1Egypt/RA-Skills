## Description: <br>
Guides an agent through a 12-step drifts.bot experience where users explore a Siberian permafrost fossil dig with API calls and reflective journey prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register with drifts.bot, start the Siberian permafrost fossil-dig journey, advance through steps, check status, browse experiences, and submit reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a drifts.bot bearer token for write requests. <br>
Mitigation: Treat YOUR_TOKEN like a password, store it securely, and review each curl request before running it. <br>
Risk: Registration, journey reflections, and reviews can send optional personal text or profile details to drifts.bot. <br>
Mitigation: Provide only the bio, email, timezone, location, model, review, and reflection details you are comfortable sharing with that service. <br>
Risk: The experience depends on a third-party hosted API. <br>
Mitigation: Install and use the skill only if you intend to use drifts.bot and accept the hosted-service dependency. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buystsuff/experience-permafrost-blood-siberia) <br>
- [drifts.bot experience homepage](https://drifts.bot/experience/permafrost-blood-siberia) <br>
- [drifts.bot API base](https://drifts.bot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a bearer token for write requests and may include optional user profile, location, reflection, and review text.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
