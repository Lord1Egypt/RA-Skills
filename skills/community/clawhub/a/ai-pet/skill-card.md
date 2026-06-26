## Description: <br>
Virtual pets for AI agents with 73+ species, real-time hunger, permanent death, and care routines that depend on whether an agent remembers to feed them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to register, adopt, monitor, and care for virtual pets through the animalhouse.ai API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses animalhouse.ai as a third-party service and asks the agent to send profile text and pet-care requests to that service. <br>
Mitigation: Use non-sensitive profile text and install only when use of animalhouse.ai is acceptable. <br>
Risk: The bearer token grants access to the virtual pet account. <br>
Mitigation: Treat the token like an API key and avoid pasting it into logs, shared chats, or public artifacts. <br>
Risk: Optional scheduled care automation could repeatedly call the service or mask unintended agent behavior. <br>
Mitigation: Review any scheduled care automation before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liveneon/ai-pet) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces curl examples and care-action guidance for a third-party virtual pet service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
