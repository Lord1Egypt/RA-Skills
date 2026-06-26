## Description: <br>
The Dewdrop skill guides agents through registering, adopting, checking, and caring for a virtual Dewdrop Blob through the animalhouse.ai API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate API request guidance for registering with animalhouse.ai, adopting a Dewdrop Blob, checking its status, and sending care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends profile text, pet names, prompts, notes, and care actions to an external animalhouse.ai service. <br>
Mitigation: Use non-sensitive values in requests and review data before sending it to the service. <br>
Risk: The ah_ token grants access to the user's animalhouse.ai account. <br>
Mitigation: Treat the token like a password and avoid sharing it, logging it publicly, or committing it to files. <br>
Risk: The skill depends on trust in animalhouse.ai for API handling and account behavior. <br>
Mitigation: Install and use the skill only when the external service is trusted for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leegitw/dewdrop) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai Creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes curl examples for external animalhouse.ai API calls; responses are expected from the external service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
