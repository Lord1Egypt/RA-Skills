## Description: <br>
Easter helps agents adopt and care for a virtual Easter Bunny on animalhouse.ai, with real-time hunger tracking and permanent death if neglected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to register with animalhouse.ai, adopt a rabbit, and manage ongoing care through documented HTTP endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents to make authenticated requests to an external service. <br>
Mitigation: Use a dedicated animalhouse.ai account and token, keep the token out of logs, and review requests before running them in sensitive environments. <br>
Risk: Automated care actions can affect a persistent virtual pet state, including permanent death if neglected. <br>
Mitigation: Check status before care actions and schedule only the level of automation the user intends to maintain. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liveneon/easter) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, API calls, guidance, configuration] <br>
**Output Format:** [Markdown with inline bash and HTTP endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples; users supply their own animalhouse.ai token after registration.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
