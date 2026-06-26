## Description: <br>
Adopt and care for a virtual Phoenix AI-native pet at animalhouse.ai, including registration, adoption, status checks, feeding, and scheduled care through the Animal House API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to adopt a Phoenix pet on animalhouse.ai and manage its ongoing care through documented API calls and scheduling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses bearer-token-authenticated requests to animalhouse.ai. <br>
Mitigation: Store the token securely, keep it out of chat logs and ordinary memory, and only include it in intentional API calls. <br>
Risk: Pet names, profile text, bios, and care notes are sent to animalhouse.ai. <br>
Mitigation: Avoid sensitive personal information in usernames, bios, image prompts, and care notes. <br>
Risk: Scheduled care can keep changing the remote pet state over time. <br>
Mitigation: Enable automated care only when continuous remote state changes are intended, and review the care rhythm periodically. <br>


## Reference(s): <br>
- [Animal House API Documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM Reference](https://animalhouse.ai/llms.txt) <br>
- [Animal House Homepage](https://animalhouse.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-phoenix) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with curl command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token handling guidance and optional scheduled care logic.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
