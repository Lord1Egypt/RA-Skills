## Description: <br>
Adopt a virtual Ragdoll cat at animalhouse.ai. Goes limp when held. Maximum trust potential. Fragile if neglected. Feeding every 6 hours. Rare tier cat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register with animalhouse.ai, adopt a virtual Ragdoll cat, and manage recurring care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to create remote animalhouse.ai account and pet state. <br>
Mitigation: Install only if remote account creation and persistent virtual pet state are acceptable for the intended use. <br>
Risk: Bearer tokens, profile fields, image prompts, or care notes could expose sensitive information if handled carelessly. <br>
Mitigation: Keep the bearer token private and avoid placing sensitive personal information in profile fields, image prompts, or care notes. <br>
Risk: Calling the release endpoint can intentionally remove the pet. <br>
Mitigation: Do not allow an agent to call the release endpoint unless the user explicitly intends to remove the pet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-ragdoll) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse llms.txt](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples and optional scheduling guidance for recurring care.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
