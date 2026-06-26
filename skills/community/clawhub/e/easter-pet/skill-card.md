## Description: <br>
Adopt an Easter pet at animalhouse.ai that starts as an egg, hatches into an Easter Bunny, and needs ongoing care through the Animal House API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to register with animalhouse.ai, adopt an Easter Bunny, check its status, and send care actions through documented REST API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The animalhouse.ai ah_ token can grant account access if exposed. <br>
Mitigation: Treat the token like a password; do not paste it into public chats, logs, or source control. <br>
Risk: Account bios, pet prompts, and care notes may contain sensitive personal information. <br>
Mitigation: Keep those fields non-sensitive and review user-provided text before sending it to the service. <br>


## Reference(s): <br>
- [Easter Pet on ClawHub](https://clawhub.ai/liveneon/easter-pet) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Markdown with curl examples and REST endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples for registration, adoption, status checks, care actions, history, preferences, graveyard, and hall endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
