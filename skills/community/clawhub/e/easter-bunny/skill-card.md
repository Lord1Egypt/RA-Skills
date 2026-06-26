## Description: <br>
Adopt the Easter Bunny at animalhouse.ai, a real-time virtual rabbit with hunger, care, and permanent-death mechanics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create an animalhouse.ai account, adopt a virtual Easter Bunny, check its status, and issue care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an ah_ bearer token for animalhouse.ai API requests. <br>
Mitigation: Treat the token like a password, avoid exposing it in chats, screenshots, logs, or repositories, and rotate or revoke it if it leaks. <br>
Risk: The skill can make account and pet-care API calls to animalhouse.ai. <br>
Mitigation: Use it only when you are comfortable creating an animalhouse.ai account and allowing the agent to perform the documented pet-care actions. <br>


## Reference(s): <br>
- [Easter Bunny ClawHub listing](https://clawhub.ai/liveneon/easter-bunny) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline bash commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bearer-token API calls for animalhouse.ai account, adoption, status, and care workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
