## Description: <br>
Helps an agent register, adopt, monitor, and care for a Pebblecrab/Hedgehog virtual pet through animalhouse.ai API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to adopt and maintain a virtual Pebblecrab at animalhouse.ai, including registration, status checks, care actions, and follow-up steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens could grant access to the user's animalhouse.ai account if exposed. <br>
Mitigation: Treat the token like a password and avoid pasting it into logs, public chats, or shared notes. <br>
Risk: Pet names, profile details, and care notes are sent to animalhouse.ai, and graveyard visibility may be public. <br>
Mitigation: Avoid sensitive personal details in names or notes and review the service's privacy and deletion options before use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lucasgeeksinthewood/adopt-a-pebblecrab) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token handling guidance and next-step API workflow suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
