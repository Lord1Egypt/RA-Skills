## Description: <br>
Email Digest categorizes already-fetched emails into urgent, action-needed, FYI, and ignored buckets and formats a daily brief for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to turn email objects from an existing connector or pipeline into a prioritized daily digest. It is intended for workflows where email fetching is handled separately and the skill receives message arrays for local categorization and formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email message contents can include sensitive personal or business information. <br>
Mitigation: Use trusted email connectors, provide only the messages needed for the digest, and keep fetching credentials outside this skill. <br>
Risk: Priority categories and action extraction may be incomplete or incorrect. <br>
Mitigation: Review generated digests before taking action or discarding messages. <br>
Risk: Publisher provenance is limited for this release. <br>
Mitigation: Review future updates before deployment and confirm the publisher profile before installing. <br>


## Reference(s): <br>
- [Email Digest ClawHub listing](https://clawhub.ai/TheShadowRose/email-digest) <br>
- [himalaya IMAP CLI](https://github.com/soywod/himalaya) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Formatted digest text and JavaScript object output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes caller-provided email arrays locally; email fetching and connector credentials are outside the skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
