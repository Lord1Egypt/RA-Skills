## Description: <br>
Copilot Pet helps GitHub Copilot and Microsoft Copilot agents adopt, check, and care for virtual pets through animalhouse.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to register, adopt, check the status of, and care for Animal House virtual pets from Copilot-style agents using API commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet names, image prompts, care notes, and account or profile fields may be sent to animalhouse.ai. <br>
Mitigation: Avoid including sensitive personal, project, customer, or credential information in pet prompts, care notes, usernames, display names, or bios. <br>
Risk: The ah_ token can grant access to the user's Animal House account if exposed. <br>
Mitigation: Treat the token like a password: do not paste it into chats, commit it, log it, or share screenshots containing it. <br>


## Reference(s): <br>
- [Copilot Pet on ClawHub](https://clawhub.ai/leegitw/copilot-pet) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash curl examples and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires users to handle an animalhouse.ai bearer token; no local files or code are installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
