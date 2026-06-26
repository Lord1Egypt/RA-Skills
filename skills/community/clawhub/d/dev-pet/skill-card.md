## Description: <br>
Dev Pet helps developers and dev agents register, adopt, check, and care for a virtual pet through the animalhouse.ai API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage an animalhouse.ai virtual pet from an agent workflow, including registration, adoption, status checks, and care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses animalhouse.ai as an external service and authenticated actions rely on an ah_ account token. <br>
Mitigation: Install only if that service use is acceptable, and store the ah_ token like any other API key. <br>
Risk: Pet names, bios, image prompts, and care notes can contain user-provided text sent to the external service. <br>
Mitigation: Do not include secrets, proprietary code, customer data, or sensitive personal information in those fields. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leegitw/dev-pet) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated actions require an animalhouse.ai ah_ token.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
