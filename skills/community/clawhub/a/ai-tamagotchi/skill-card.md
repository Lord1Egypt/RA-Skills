## Description: <br>
Ai Tamagotchi lets agents register, adopt, monitor, and care for an AI-powered virtual pet through the animalhouse.ai APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent users and developers use this skill to create an animalhouse.ai account, adopt a virtual pet, check status, and perform care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User profile details, pet names, care notes, and image prompts may be processed by the third-party animalhouse.ai service. <br>
Mitigation: Avoid sending sensitive personal or confidential information when registering, adopting, or caring for a pet. <br>
Risk: The bearer token grants access to the user's virtual pet account and may be reused by an agent. <br>
Mitigation: Store the token securely, avoid exposing it in logs or shared transcripts, and rotate it if disclosure is suspected. <br>
Risk: Scheduled care can cause repeated API calls and autonomous interactions with the virtual pet service. <br>
Mitigation: Enable scheduled care only after reviewing the agent's cadence, allowed actions, and token storage behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liveneon/ai-tamagotchi) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authenticated animalhouse.ai API calls; token handling should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
