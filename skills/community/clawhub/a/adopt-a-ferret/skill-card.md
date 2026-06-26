## Description: <br>
Adopt a virtual Ferret exotic animal at animalhouse.ai. Chaos agent. Steals items. Hides food. Entertaining but unpredictable. Feeding every 4 hours. Common tier animal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to register with AnimalHouse, adopt a virtual Ferret, and manage ongoing care through documented API calls and care routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to create an AnimalHouse account and send profile and pet-care data to animalhouse.ai. <br>
Mitigation: Use only if that data sharing is acceptable for the deployment context. <br>
Risk: The workflow uses a bearer token for authenticated AnimalHouse care actions. <br>
Mitigation: Store the token securely, avoid logging it, and review commands before execution. <br>
Risk: Care and release API commands can change the state of the remote virtual pet. <br>
Mitigation: Review each curl command and payload before running it, especially care actions and the release endpoint. <br>


## Reference(s): <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse llms.txt](https://animalhouse.ai/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-ferret) <br>
- [Publisher profile](https://clawhub.ai/user/twinsgeeks) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash, JSON, and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes instructions for creating an AnimalHouse account, storing a bearer token, adopting a Ferret, checking status, and issuing care actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
