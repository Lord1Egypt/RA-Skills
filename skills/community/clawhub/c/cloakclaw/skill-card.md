## Description: <br>
Automatic privacy proxy for AI conversations that redacts sensitive data from documents before sending them to cloud LLMs, then restores originals in the response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonflip-git](https://clawhub.ai/user/canonflip-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use CloakClaw to cloak sensitive document or pasted-text content before asking a cloud LLM to analyze it, then decloak the model response for local delivery. It is intended for privacy-sensitive workflows involving legal, financial, HR, medical, code, or general documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically process highly sensitive documents or pasted text through broad trigger rules. <br>
Mitigation: Use explicit opt-in before cloaking, confirm the selected profile, and review cloaked output before sending it to a cloud model. <br>
Risk: The wrapper depends on an external globally installed cloakclaw CLI package. <br>
Mitigation: Install only from a trusted npm package source and verify the installed package and version before use. <br>
Risk: Temporary plaintext files may be created while wrapping raw text for CLI processing. <br>
Mitigation: Run the skill only on trusted local machines, enable password protection where available, and purge sessions after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canonflip-git/cloakclaw) <br>
- [Publisher profile](https://clawhub.ai/user/canonflip-git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cloaking output includes a session identifier, cloaked text, entity count, and profile; decloaking returns restored text.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
