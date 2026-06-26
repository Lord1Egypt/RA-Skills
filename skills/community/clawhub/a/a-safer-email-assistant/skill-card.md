## Description: <br>
Sync mailbox context, triage important messages, answer history questions, and create safe draft replies through a self-hosted ai-email-gateway API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[remimikalsen](https://clawhub.ai/user/remimikalsen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to a self-hosted email gateway for mailbox synchronization, important-message triage, email history questions, and draft reply preparation. It is intended to create reviewable drafts, not to send email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose selected mailbox content to the agent session and the configured gateway. <br>
Mitigation: Use a trusted self-hosted gateway, scoped API keys, intended ACCOUNT_ID or ACCOUNT_IDS values, and private logs. <br>
Risk: Suspicious or malicious messages may influence triage or draft content. <br>
Mitigation: Keep suspicious filtering enabled by default and require an explicit user override before using flagged content for drafting. <br>
Risk: Generated replies may contain mistakes or commitments the user has not approved. <br>
Mitigation: Create drafts only and require manual review before any email is sent. <br>
Risk: The polling helper writes local state that may reveal account ids or message identifiers. <br>
Mitigation: Keep the state file private and change its location only with user approval. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/remimikalsen/a-safer-email-assistant) <br>
- [API Reference](api-reference.md) <br>
- [Importance Classifier Template](prompts/importance-classifier.md) <br>
- [Drafting Style Template](prompts/drafting-style.md) <br>
- [Monitoring Script Scaffold](scripts/check_new_messages.py) <br>
- [ai-email-gateway project documentation](https://github.com/ArktIQ-IT/ai-email-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON draft payloads, API request guidance, and optional shell command usage for the polling helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only workflow; message evidence should cite canonical message ids.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
