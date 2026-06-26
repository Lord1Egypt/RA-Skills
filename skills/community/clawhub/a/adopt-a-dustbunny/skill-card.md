## Description: <br>
Adopt A Dustbunny guides agents through registering with animalhouse.ai, adopting a virtual Dustbunny/Rabbit, and using REST API calls to monitor and care for it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create and care for an animalhouse.ai Dustbunny/Rabbit through API calls, status checks, and heartbeat automation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens for animalhouse.ai could be exposed through chat transcripts, screenshots, shell history, or repositories. <br>
Mitigation: Store tokens in environment variables or a secret manager and avoid pasting live tokens into shared logs or source files. <br>
Risk: Heartbeat automation may send repeated pet-care requests to the service if used without review. <br>
Mitigation: Review and rate-limit any heartbeat automation before running it, and follow the service response next_steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liveneon/adopt-a-dustbunny) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with bash, JSON, and pseudocode examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes REST endpoint examples and care-action payloads; animalhouse.ai responses may include next_steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
