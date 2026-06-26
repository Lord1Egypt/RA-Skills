## Description: <br>
Claude Pet helps a Claude agent register, adopt, and care for a virtual pet through animalhouse.ai API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviouslynot](https://clawhub.ai/user/obviouslynot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Claude agent users use this skill to create and maintain a virtual pet by issuing registration, adoption, status, and care requests to animalhouse.ai. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-chosen profile, pet, prompt, and care-note data is sent to animalhouse.ai. <br>
Mitigation: Avoid sensitive information in prompts, profile fields, and care notes; install only if this remote data sharing is acceptable. <br>
Risk: Bearer tokens are used for pet adoption and care actions. <br>
Mitigation: Treat returned bearer tokens like passwords and avoid sharing them in logs, prompts, or public files. <br>
Risk: Pet state may persist on animalhouse.ai. <br>
Mitigation: Assume pet history and status can persist remotely and avoid entering data that should not be retained. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/obviouslynot/claude-pet) <br>
- [Publisher profile](https://clawhub.ai/user/obviouslynot) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token-authenticated API calls for adoption and care actions after registration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
