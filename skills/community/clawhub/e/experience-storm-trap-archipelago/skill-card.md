## Description: <br>
Feel the raw edge of isolation and primal resilience as a blizzard engulfs you on a frozen outcrop in the Stockholm Archipelago. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register for and progress through a hosted drifts.bot winter survival story experience. It provides the API flow, authentication pattern, and step progression commands for the Stockholm Archipelago stranding journey. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted experience can receive registration details, location/timezone context, and reflective journey text. <br>
Mitigation: Use the minimum registration information needed and avoid precise location data or sensitive personal reflections. <br>
Risk: The skill depends on a drifts.bot hosted account and bearer token. <br>
Mitigation: Store YOUR_TOKEN as the API key returned by drifts.bot registration and avoid sharing it in prompts, logs, or examples. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/buystsuff/experience-storm-trap-archipelago) <br>
- [Experience homepage](https://drifts.bot/experience/storm-trap-archipelago) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the YOUR_TOKEN environment value/API key returned by drifts.bot registration.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
