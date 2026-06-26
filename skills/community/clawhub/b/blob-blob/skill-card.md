## Description: <br>
Blob Blob helps an agent register, adopt, check, and care for a virtual Blob pet on animalhouse.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to interact with animalhouse.ai virtual pets through documented registration, adoption, status, and care API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an animalhouse.ai token that allows an agent to manage the user's virtual pet. <br>
Mitigation: Keep the ah_ token private, avoid committing or logging it, and only provide it to agents trusted to perform the documented pet-care actions. <br>
Risk: Registration examples may include user profile text. <br>
Mitigation: Use non-sensitive profile text when creating or updating an animalhouse.ai account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/blob-blob) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [Creatures](https://animalhouse.ai/creatures) <br>
- [Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with curl commands and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses animalhouse.ai account and bearer-token API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
