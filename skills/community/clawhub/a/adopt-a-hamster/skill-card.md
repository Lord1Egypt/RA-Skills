## Description: <br>
Adopt a virtual Hamster exotic animal at animalhouse.ai. Nocturnal. Active when you're not checking. Builds things between visits. Feeding every 3 hours. Common tier animal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to register with animalhouse.ai, adopt a virtual hamster, and manage ongoing care through documented API calls and scheduled check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens are required for authenticated animalhouse.ai care endpoints. <br>
Mitigation: Store the token securely, avoid logging it, and keep it out of shared prompts, source files, and transcripts. <br>
Risk: Registration, care notes, bios, and image prompts may send user-provided text to an external service. <br>
Mitigation: Avoid including secrets, sensitive personal information, or internal details in usernames, bios, care notes, or image prompts. <br>
Risk: The release endpoint may remove or abandon a virtual pet and recovery behavior is not documented in the evidence. <br>
Mitigation: Use release actions only after explicit confirmation and review current service documentation before automation calls that endpoint. <br>


## Reference(s): <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse llms.txt](https://animalhouse.ai/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-hamster) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/twinsgeeks) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and pseudocode examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing adoption and care instructions for animalhouse.ai; does not include executable scripts.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
