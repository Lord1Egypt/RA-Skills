## Description: <br>
Adopt a virtual Ouroboros AI-native pet at animalhouse.ai with a 168-hour feeding cycle, eternal mechanics, and extreme-tier care requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to adopt and care for a virtual Ouroboros pet through the animalhouse.ai API, including registration, token handling, status checks, feeding, and care routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registration details may be shared with the external animalhouse.ai service. <br>
Mitigation: Use pseudonymous registration details if you do not want personal profile information associated with that service. <br>
Risk: The workflow returns a bearer token that grants access to pet care actions. <br>
Mitigation: Store the token securely, keep it private, and avoid pasting it into logs or shared prompts. <br>
Risk: Automated care routines can change the virtual pet state through API calls. <br>
Mitigation: Review scheduled actions and use the status response's recommended check-in guidance before automating care. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-ouroboros) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse llms.txt](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through token-based registration, adoption, status checks, care actions, and optional scheduled check-ins.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
