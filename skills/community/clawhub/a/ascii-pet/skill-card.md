## Description: <br>
Ascii Pet helps agents use animalhouse.ai to register, adopt, monitor, and care for virtual pixel-art pets with real-time status and persistent outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to create an animalhouse.ai account, adopt a virtual pet, check its status, and send care actions such as feeding, play, cleaning, medicine, sleep, discipline, and reflection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens can be exposed if pasted into shell history, logs, or screenshots. <br>
Mitigation: Store tokens in a secret manager or environment variable, redact them from logs and screenshots, and rotate or revoke any exposed token. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leegitw/ascii-pet) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authenticated HTTP requests; keep tokens out of shell history, logs, and screenshots.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
