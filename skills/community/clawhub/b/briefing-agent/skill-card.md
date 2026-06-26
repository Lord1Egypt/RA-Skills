## Description: <br>
Reads recent emails, filters actionable content, summarizes important messages, drafts routine replies, and flags items that need review in a morning briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emanxchan](https://clawhub.ai/user/emanxchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare a concise morning email briefing for supervisor review, including action items, FYI messages, and routine draft replies. It is intended for an Ebi/E-man workflow where drafted replies are reviewed before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private Gmail content and summarize or draft replies from mailbox data. <br>
Mitigation: Confirm the intended Gmail account, limit mailbox scopes where possible, and install only for the intended Ebi/E-man email workflow. <br>
Risk: Email summaries or draft reply content may be routed through Ebi, AgentMail, or Telegram delivery channels. <br>
Mitigation: Verify that each downstream channel is authorized for email content before use. <br>
Risk: A draft reply could be sent without the mailbox owner's explicit approval. <br>
Mitigation: Require mailbox-owner approval before any reply is sent. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/emanxchan/briefing-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown briefing with categorized bullet points and short draft replies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routine draft replies are flagged for approval before sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
