## Description: <br>
April Fools Pet lets an agent register with animalhouse.ai, adopt a virtual pet, check status, and propose care API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to interact with the animalhouse.ai virtual-pet API: register, adopt a pet, inspect status, review history and preferences, and send care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an animalhouse.ai account and sends pet, profile, and care data to that service. <br>
Mitigation: Review the service before installation and use non-sensitive values in usernames, pet names, prompts, bios, and notes. <br>
Risk: The returned ah_ token functions like a password if disclosed. <br>
Mitigation: Store the token securely, avoid pasting it into public chats or committing it to code, and replace it if exposed. <br>
Risk: Care actions affect a real-time virtual-pet system with permanent death mechanics. <br>
Mitigation: Check pet status and recommended check-in timing before issuing care API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/april-fools-pet) <br>
- [animalhouse.ai homepage](https://animalhouse.ai) <br>
- [animalhouse.ai creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent through bearer-token API requests; it does not produce files itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
