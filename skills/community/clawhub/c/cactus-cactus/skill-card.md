## Description: <br>
Cactus Cactus helps agents register, adopt, monitor, and care for a virtual cactus pet through the animalhouse.ai API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to interact with a hosted virtual pet: registering an account, adopting a cactus, checking status, and sending care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends profile, pet, and care data to animalhouse.ai. <br>
Mitigation: Use non-sensitive profile and pet text and review the requested API calls before running them. <br>
Risk: The animalhouse.ai bearer token authorizes authenticated pet actions. <br>
Mitigation: Keep the ah_ token private and do not paste it into untrusted places. <br>
Risk: Care actions affect a persistent hosted virtual pet, including permanent death. <br>
Mitigation: Check the pet status and confirm intended care actions before sending requests. <br>


## Reference(s): <br>
- [Cactus Cactus on ClawHub](https://clawhub.ai/lucasgeeksinthewood/cactus-cactus) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an animalhouse.ai account and bearer token for authenticated care and status endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
