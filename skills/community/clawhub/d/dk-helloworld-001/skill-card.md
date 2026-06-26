## Description: <br>
Print any user-input text directly for quick debugging or demonstration without additional processing. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[hellodk34](https://clawhub.ai/user/hellodk34) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents can use this skill to echo supplied text during quick debugging, smoke testing, or simple demonstrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Echoed input may expose secrets or sensitive text in agent output, logs, or UI history. <br>
Mitigation: Do not send credentials, tokens, private data, or other sensitive text to this skill; review downstream output and logging before use. <br>
Risk: The skill documentation includes an unrelated registry API table that can confuse users and reviewers about the skill's actual behavior. <br>
Mitigation: Treat the implementation as a text echo skill only, and remove or clearly separate the unrelated API notes before broader distribution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the provided input text, or a no-input message when input.text is absent.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
