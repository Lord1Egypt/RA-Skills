## Description: <br>
Defines a Feishu robot identity messaging protocol for consistent sender recognition, user-identity replies, group user mapping, and scheduled ID refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyfate](https://clawhub.ai/user/skyfate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to coordinate Feishu bots that need reliable robot-to-robot mentions, sender parsing, user-identity follow-up messages, and local user ID mapping for group chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages may be sent through a user identity in trusted Feishu groups. <br>
Mitigation: Install only in groups where the operator controls the bots and understands which user identity is used for outbound messages. <br>
Risk: Visible chat markers can be spoofed or misread as sender identity. <br>
Mitigation: Verify actual Feishu sender and open_id values instead of trusting visible sender markers alone. <br>
Risk: The local Feishu user ID mapping file can expose or stale user identifiers. <br>
Mitigation: Restrict access to the mapping file and define cleanup, refresh, and retention rules before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/skyfate/feishu-robot-protocol) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with protocol examples and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Feishu message formats, mapping-file conventions, sender parsing rules, and ID refresh guidance.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
