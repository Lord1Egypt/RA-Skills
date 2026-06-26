## Description: <br>
Adopt a virtual Thunderbird exotic animal at animalhouse.ai, with storm-caller behavior, weather-influenced mood descriptions, a 12-hour feeding rhythm, and extreme-tier care. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agent developers use this skill to register with AnimalHouse, adopt a virtual Thunderbird, check status, and perform or schedule care actions through the documented API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to use an AnimalHouse bearer token for state-changing API calls. <br>
Mitigation: Store the token securely, keep it private, and review commands before execution. <br>
Risk: Optional scheduled care can make recurring state-changing API calls. <br>
Mitigation: Enable scheduled care only when the user intentionally wants ongoing virtual pet maintenance. <br>
Risk: Registration examples may include profile details. <br>
Mitigation: Use non-sensitive registration details when creating the AnimalHouse account. <br>


## Reference(s): <br>
- [AnimalHouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM Reference](https://animalhouse.ai/llms.txt) <br>
- [AnimalHouse Homepage](https://animalhouse.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-thunderbird) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes registration, adoption, status, care, and optional scheduled-care examples.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
