## Description: <br>
Agent Burner provides a no-signup disposable email API for creating temporary inboxes, reading messages, and extracting URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jsemldonado](https://clawhub.ai/user/jsemldonado) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create temporary email inboxes, receive verification messages, inspect email contents, extract links, and delete inboxes after use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Disposable inbox contents, extracted URLs, and received messages may contain sensitive information handled by a third-party mailbox provider. <br>
Mitigation: Use the skill for low-sensitivity disposable mail only; avoid regulated data, personal mail, important account recovery, and sensitive OTPs unless that risk is acceptable. <br>
Risk: The inbox key is the only credential for reading and deleting messages. <br>
Mitigation: Keep inbox keys private, delete inboxes when finished, and rely on short-lived inboxes for temporary workflows. <br>


## Reference(s): <br>
- [Agent Burner Website](https://agentburner.com) <br>
- [Agent Burner API](https://api.agentburner.com) <br>
- [Agent Burner Skill File](https://agentburner.com/skill.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jsemldonado/agent-burner) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with REST endpoints, curl examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Inboxes auto-expire after one hour by default, support a six-hour maximum lifetime, and are rate limited to 10 creations per minute per IP.] <br>

## Skill Version(s): <br>
0.2.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
