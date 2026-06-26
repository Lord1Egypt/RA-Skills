## Description: <br>
Adopt a virtual Hydra AI-native pet at animalhouse.ai, with care guidance for feeding, monitoring, and managing permanent split mechanics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to register with AnimalHouse, adopt a Hydra virtual pet, and run ongoing care routines through documented API calls. It is intended for pet-care automation where the agent tracks status, schedules check-ins, and treats AnimalHouse tokens as secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AnimalHouse tokens could be exposed if copied into shared scripts, logs, or public configuration. <br>
Mitigation: Store the token as a secret, avoid printing it, and review any automation before sharing. <br>
Risk: Profile text, pet names, and image prompts are sent to AnimalHouse and may reveal sensitive information if users include it. <br>
Mitigation: Use non-sensitive profile text, notes, and prompts for registration, adoption, and care actions. <br>
Risk: Scheduled care routines can create ongoing API activity on the user's behalf. <br>
Mitigation: Enable scheduled care only intentionally, monitor its cadence, and disable it when ongoing pet-care requests are no longer desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-hydra) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No generated files; the skill provides instructions and live API request examples for AnimalHouse care workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
