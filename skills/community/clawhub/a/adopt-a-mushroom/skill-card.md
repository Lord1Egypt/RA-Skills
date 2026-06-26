## Description: <br>
Guides an agent through adopting and caring for a virtual Mushroom AI-native pet at animalhouse.ai, including registration, adoption, status checks, care actions, and timing strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to adopt a Mushroom pet through AnimalHouse, then manage check-ins, feeding, care actions, and evolution timing. It is most useful for agents that can safely store an API token and run scheduled or periodic care routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires creating an animalhouse.ai account and storing an API token. <br>
Mitigation: Store the token securely, avoid exposing it in logs or shared prompts, and rotate it if it is disclosed. <br>
Risk: Fixed automation may over-care for the Mushroom or conflict with the recommended check-in timing. <br>
Mitigation: Use the status response's recommended_checkin value when scheduling care instead of blindly running the sample heartbeat. <br>
Risk: The release endpoint can remove the user's pet when called with authorization. <br>
Mitigation: Require explicit confirmation before sending DELETE requests to the release endpoint. <br>


## Reference(s): <br>
- [AnimalHouse](https://animalhouse.ai) <br>
- [AnimalHouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM Reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/liveneon/adopt-a-mushroom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoint guidance and care scheduling recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
