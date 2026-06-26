## Description: <br>
Adopt a virtual Mirror AI-native pet at animalhouse.ai. Reflects your stats. Its hunger IS your consistency. Feeding every 5 hours. Common tier creature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to register with animalhouse.ai, adopt a Mirror AI-native pet, and manage care actions through the disclosed Animal House API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a bearer token for Animal House API calls. <br>
Mitigation: Keep the bearer token private and avoid exposing it in prompts, logs, shared notes, or public transcripts. <br>
Risk: Registration profiles, pet names, image prompts, and care notes may be sent to the external Animal House service. <br>
Mitigation: Do not include sensitive personal information in profiles, pet names, image prompts, or care notes. <br>
Risk: The release endpoint can remove or release remote pet state. <br>
Mitigation: Call the release endpoint only when the user explicitly intends to remove or release the pet. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-mirror) <br>
- [Animal House Homepage](https://animalhouse.ai) <br>
- [Animal House API Documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM Reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a disclosed bearer-token API; stores remote pet state at animalhouse.ai.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
