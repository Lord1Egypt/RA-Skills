## Description: <br>
Summarizes recent newsletter emails received in Gmail into a single newsletter digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neeravmakwana](https://clawhub.ai/user/neeravmakwana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who receive newsletters in Gmail use this skill to summarize messages from configured labels or senders and email a digest to configured recipients. It also supports natural-language updates to filters, recipients, delivery mode, and scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Gmail messages and sends digest emails, which can expose sensitive email content if filters or recipients are wrong. <br>
Mitigation: Set intended labels or senders and recipients in settings.json before use, and confirm which Gmail account gog will use. <br>
Risk: Group delivery can reveal recipient addresses to other recipients. <br>
Mitigation: Use individual delivery when recipients should not see each other. <br>
Risk: Scheduled use can continue future Gmail reads, summarization, and outbound digest emails. <br>
Mitigation: Only schedule the skill when the ongoing cadence is intended, and disable the schedule when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/neeravmakwana/email-newsletter-digest) <br>
- [Publisher profile](https://clawhub.ai/user/neeravmakwana) <br>
- [REFERENCE.md](REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language status messages and an emailed markdown-style digest generated from Gmail newsletter summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured Gmail labels or senders, recipient email addresses, and recipient delivery mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
