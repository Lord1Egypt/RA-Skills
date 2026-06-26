## Description: <br>
Duck Duck guides agents through registering, adopting, checking, and caring for a virtual duck at animalhouse.ai, including hunger, species, and permanent-death mechanics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviouslynot](https://clawhub.ai/user/obviouslynot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent interact with animalhouse.ai virtual pet APIs for account registration, duck adoption, status checks, care actions, and public graveyard or hall views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to create an animalhouse.ai account and send profile and pet-care data to that service. <br>
Mitigation: Install only when that data sharing is acceptable, and review account registration and care requests before execution. <br>
Risk: The ah_ bearer token can grant access to the user's virtual pet account if exposed. <br>
Mitigation: Store the token in an environment variable or secret store, keep it out of shared chats and logs, and rotate or revoke it if exposed. <br>
Risk: Pet status and graveyard-related state can become public according to the security guidance and skill behavior. <br>
Mitigation: Avoid sending sensitive notes or identifying information in pet-care actions and check public views before sharing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/obviouslynot/duck-duck) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with curl command examples and endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token API calls against animalhouse.ai and may reference public pet state.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
