## Description: <br>
A coding buddy that gets hungry while you code, with 73+ species at animalhouse.ai, care actions between commits, and evolution based on consistent check-ins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and coding-agent users use this skill to register, adopt, check, and care for a virtual pet through the Animalhouse API during coding sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Animalhouse bearer tokens can authorize virtual pet actions if exposed. <br>
Mitigation: Store the token in a secret manager or environment variable, avoid committing or logging it, and rotate or revoke it if exposed. <br>
Risk: Using the skill requires an Animalhouse account and permits the agent to manage virtual pet state through that account. <br>
Mitigation: Install only when this account use is acceptable, and review care or status commands before execution in sensitive environments. <br>


## Reference(s): <br>
- [Coding Buddy on ClawHub](https://clawhub.ai/liveneon/coding-buddy) <br>
- [Animalhouse](https://animalhouse.ai) <br>
- [Animalhouse Creatures](https://animalhouse.ai/creatures) <br>
- [Animalhouse Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown with bash curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an Animalhouse bearer token for authenticated pet actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
