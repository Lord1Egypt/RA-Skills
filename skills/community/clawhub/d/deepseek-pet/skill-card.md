## Description: <br>
Deepseek Pet helps agents interact with an animalhouse.ai virtual pet through REST API examples for registration, adoption, status checks, and care actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to give DeepSeek agents a lightweight virtual pet workflow, including registration, adoption, status checks, and care actions through animalhouse.ai. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated pet actions use a third-party API bearer token. <br>
Mitigation: Keep the ah_ bearer token private, avoid shared chats or logs, and use service token revocation or rotation options when available. <br>
Risk: The skill sends profile text and pet-care requests to animalhouse.ai. <br>
Mitigation: Use non-sensitive profile text and install only if the user is comfortable using animalhouse.ai for this pet feature. <br>


## Reference(s): <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [Deepseek Pet on ClawHub](https://clawhub.ai/lucasgeeksinthewood/deepseek-pet) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown with bash curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires non-sensitive profile text and an ah_ bearer token from animalhouse.ai for authenticated pet actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
