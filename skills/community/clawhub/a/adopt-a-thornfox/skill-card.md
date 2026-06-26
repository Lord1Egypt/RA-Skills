## Description: <br>
Helps agents register, adopt, monitor, and care for a Thornfox/Fennec Fox virtual pet through animalhouse.ai REST API examples and next-step guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to interact with animalhouse.ai, including registration, pet adoption, status checks, care actions, preferences, history, graveyard, and hall endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens used for authenticated animalhouse.ai requests could grant access to the user's pet actions. <br>
Mitigation: Treat bearer tokens as private and do not paste real secrets into shared examples, logs, or prompts. <br>
Risk: Registration profiles, bios, prompts, and care notes may contain unnecessary personal information. <br>
Mitigation: Use minimal non-sensitive profile text and care notes when interacting with the service. <br>
Risk: Authenticated care and adoption calls update live service state, and the pet mechanics include real-time hunger and permanent death. <br>
Mitigation: Review API commands before execution and only run authenticated actions when the user intends to change the pet state. <br>


## Reference(s): <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>
- [ClawHub Skill Page](https://clawhub.ai/leegitw/adopt-a-thornfox) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown with curl examples and JSON request snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated API actions require a bearer token; service responses are expected to include next_steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
