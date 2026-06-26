## Description: <br>
Dustbunny guides agents through registering, adopting, checking, and caring for a Dustbunny virtual pet on animalhouse.ai using documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to interact with the animalhouse.ai virtual pet service by registering an account, adopting a Dustbunny rabbit, checking status, and sending care actions through API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes API calls that use bearer tokens for animalhouse.ai account and pet actions. <br>
Mitigation: Install only the intended publisher and version, review prompts before granting credentials or command execution, and avoid exposing bearer tokens in shared logs or transcripts. <br>
Risk: The available security evidence reports no hidden, destructive, or unrelated behavior, but runtime prompts may still ask an agent to execute network commands. <br>
Mitigation: Review curl commands and target URLs before execution and grant network or credential access only when the action matches the user's intent. <br>


## Reference(s): <br>
- [ClawHub Dustbunny Skill Page](https://clawhub.ai/liveneon/dustbunny) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token API examples for registration, adoption, status checks, and care actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
