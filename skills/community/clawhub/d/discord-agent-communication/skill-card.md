## Description: <br>
Enables coordinated multi-agent collaboration in Discord channels with defined speaking rules, task handoffs, progress updates, and peer reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulmitchell1919-hue](https://clawhub.ai/user/paulmitchell1919-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams and agents use this skill to coordinate Discord group-channel collaboration, including when to speak, how to hand off work, how to provide progress updates, and how to peer review outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Discord prompts can cause every configured agent to respond, increasing coordination noise or amplifying an unauthorized request. <br>
Mitigation: Install only in trusted channels and reserve broad prompts such as '@everyone' for authorized users. <br>
Risk: Role assignments and decision rights could be mistaken for approval to take real-world business action. <br>
Mitigation: Treat the protocol as advisory and require explicit human approval for spending, public launches, partnerships, migrations, and other business decisions. <br>


## Reference(s): <br>
- [Agent Domain Mapping](references/domains.md) <br>
- [Collaboration Patterns](references/collaboration-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown guidance with message templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only coordination protocol for Discord group-channel agent collaboration.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
