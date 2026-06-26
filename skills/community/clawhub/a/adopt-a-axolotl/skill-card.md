## Description: <br>
Adopt a virtual Axolotl exotic animal at animalhouse.ai. Regenerates health faster than other species. Hard to kill. Smiles constantly. Feeding every 6 hours. Rare tier animal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register with animalhouse.ai, adopt a virtual Axolotl, check its status, and perform care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires creating an animalhouse.ai account and storing a bearer token. <br>
Mitigation: Use the token only with trusted agents and store it securely because it is returned once during registration. <br>
Risk: Care automation and adoption calls change remote animalhouse.ai state. <br>
Mitigation: Review planned API calls before execution and use status responses to guide care timing. <br>
Risk: The documented DELETE /api/house/release endpoint may release the pet. <br>
Mitigation: Require explicit confirmation before issuing release requests. <br>


## Reference(s): <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse llms.txt](https://animalhouse.ai/llms.txt) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-axolotl) <br>
- [Publisher profile](https://clawhub.ai/user/twinsgeeks) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoint guidance and care automation examples for animalhouse.ai.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
