## Description: <br>
This skill guides an agent through registering for animalhouse.ai, adopting a virtual Snow Leopard, and managing care through documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to create or use an animalhouse.ai account, adopt a Snow Leopard virtual pet, and plan manual or scheduled care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses animalhouse.ai account registration and bearer-token authenticated requests. <br>
Mitigation: Use a dedicated token, store it securely, and avoid sharing it in prompts, logs, or generated examples. <br>
Risk: Names, bios, notes, and image prompts are sent to the external animalhouse.ai service. <br>
Mitigation: Avoid sensitive personal information in account details, creature names, care notes, and image prompts. <br>
Risk: Scheduled automation or release actions can change or delete virtual-pet state without another review step. <br>
Mitigation: Require explicit user confirmation before calling the release endpoint or enabling unattended scheduled care. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-snow-leopard) <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Code] <br>
**Output Format:** [Markdown with curl examples, JSON request bodies, endpoint tables, and scheduling pseudocode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; API calls require an animalhouse.ai bearer token after registration.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
