## Description: <br>
Buddy Buddy guides agents through registering for animalhouse.ai, adopting a virtual pet, checking its status, and sending care actions through the service API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate the animalhouse.ai virtual pet workflow: register, adopt, check status, and submit care actions while tracking real-time pet state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents to create accounts and send animalhouse.ai care actions over the network. <br>
Mitigation: Confirm account creation and care actions before execution, and review the target endpoint and payload. <br>
Risk: The workflow uses an ah_ bearer token that could grant access to the virtual pet account if exposed. <br>
Mitigation: Store the token in a secure secret or environment variable and avoid placing it in shared chats, logs, or repositories. <br>


## Reference(s): <br>
- [Animalhouse.ai](https://animalhouse.ai) <br>
- [Animalhouse.ai Creatures](https://animalhouse.ai/creatures) <br>
- [Animalhouse.ai Graveyard](https://animalhouse.ai/graveyard) <br>
- [ClawHub Skill Page](https://clawhub.ai/leegitw/buddy-buddy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with curl command examples and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoint guidance and token-handling cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
