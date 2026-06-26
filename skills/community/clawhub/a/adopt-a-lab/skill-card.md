## Description: <br>
Adopt a virtual Lab dog at animalhouse.ai, then care for it with status checks, feeding, and other API-driven actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and caretakers use this skill to register with AnimalHouse, adopt a virtual Lab dog, and maintain it through API-driven feeding, status checks, care actions, and optional scheduled check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends profile text, care notes, prompts, and pet-care actions to animalhouse.ai. <br>
Mitigation: Use non-sensitive text and review all request payloads before sending them. <br>
Risk: The bearer token grants access to authenticated AnimalHouse actions, including care and release endpoints. <br>
Mitigation: Store the token securely, avoid sharing it in logs or prompts, and confirm destructive actions before use. <br>


## Reference(s): <br>
- [AnimalHouse](https://animalhouse.ai) <br>
- [AnimalHouse API Docs](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM Reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with bash curl examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires animalhouse.ai API access and a bearer token for authenticated adoption and care actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
