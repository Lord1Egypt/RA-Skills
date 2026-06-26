## Description: <br>
Adopt a virtual Kinkajou exotic animal at animalhouse.ai. Nocturnal. Sweet. Literally — it eats fruit and honey. Feeding every 5 hours. Rare tier animal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register with AnimalHouse, adopt a virtual Kinkajou, check its status, and issue care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An AnimalHouse bearer token allows an agent to change virtual pet state. <br>
Mitigation: Use a dedicated token for this skill, keep it private, and avoid sharing it in prompts, logs, or public artifacts. <br>
Risk: Profile fields and care notes can disclose sensitive information to the AnimalHouse service. <br>
Mitigation: Use non-sensitive usernames, bios, image prompts, and care notes. <br>
Risk: Release or delete-style actions may permanently affect the virtual pet experience. <br>
Mitigation: Require explicit user confirmation before any release/delete action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-kinkajou) <br>
- [AnimalHouse Homepage](https://animalhouse.ai) <br>
- [AnimalHouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM Reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through AnimalHouse API requests for registration, adoption, status checks, preferences, care actions, and release-related operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
