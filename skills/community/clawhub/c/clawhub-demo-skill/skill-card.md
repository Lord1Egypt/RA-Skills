## Description: <br>
Use this tiny demo skill to verify that a ClawHub skill can be published, installed, and invoked; it returns a short confirmation message and optionally echoes a user-provided phrase. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[colifire](https://clawhub.ai/user/colifire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to smoke-test ClawHub publishing, installation, and invocation flows with a concise confirmation response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can echo user-provided text and may be invoked implicitly for related test prompts. <br>
Mitigation: Avoid giving it secrets or sensitive phrases to repeat, and review the echoed response before sharing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/colifire/clawhub-demo-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns one concise sentence, does not call external services, and does not create files.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
