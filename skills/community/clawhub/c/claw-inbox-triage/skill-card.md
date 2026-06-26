## Description: <br>
Automates inbox management by categorizing messages into urgent, normal, or spam, generating daily digests, and drafting responses for low-priority items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigas](https://clawhub.ai/user/indigas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual users use this skill to sort high-volume inboxes, generate daily summaries, and prepare draft replies for review across configured message sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process private messages from explicitly configured sources, and weak scoping could expose more inbox content than intended. <br>
Mitigation: Use exported message files or narrowly chosen sources when possible, keep generated digests in private locations, and confirm the configured sources before running triage. <br>
Risk: Message classification and generated draft replies may be wrong, especially for urgent or sensitive conversations. <br>
Mitigation: Review all categorizations and drafts before acting or sending, tune the classification rules, and avoid using the skill for high-stakes legal, medical, or financial communication. <br>


## Reference(s): <br>
- [Priority Classification Rules](references/priority-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON triage reports with optional draft-response text and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs group messages by urgent, normal, and spam/noise categories and may include draft responses that require review before sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
