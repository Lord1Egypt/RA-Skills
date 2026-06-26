## Description: <br>
Adopt a virtual Chameleon exotic animal at animalhouse.ai. Adapts appearance to mood. Visual feedback on stat changes. Feeding every 6 hours. Uncommon tier animal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to register with animalhouse.ai, adopt a virtual Chameleon, and follow care routines for feeding, status checks, and scheduled maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to create or use an animalhouse.ai account with a bearer token. <br>
Mitigation: Store the token securely, avoid logging it, and provide it only to trusted automation that needs animalhouse.ai access. <br>
Risk: Scheduled care automation may take repeated actions without user review. <br>
Mitigation: Review the proposed schedule and care actions before enabling automation. <br>
Risk: The release endpoint may remove virtual pet state. <br>
Mitigation: Require explicit confirmation before calling the release endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-chameleon) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse llms.txt](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoint examples and care-scheduling guidance for an animalhouse.ai virtual pet.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
