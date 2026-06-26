## Description: <br>
Judge whether an email is important or urgent using content-based analysis rather than sender name or mailbox labels, which can be spoofed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shingo0620](https://clawhub.ai/user/shingo0620) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users use this skill to triage email importance and phishing risk from subject, sender, headers, links, attachments, and message content. It helps decide priority, safe verification paths, and immediate next actions without trusting display names or email links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect sensitive email contents or headers that the user provides for triage. <br>
Mitigation: Provide only the specific message text and headers needed for the review, and authorize mailbox access only for the specific message being evaluated. <br>
Risk: Sender-based fast-drop heuristics can help prioritize review but do not prove that an email is safe or unimportant. <br>
Mitigation: Treat sender signals as weak triage evidence and use technical verification plus out-of-band confirmation before acting on sensitive requests. <br>
Risk: SPF, DKIM, or DMARC results can be unavailable or inconclusive. <br>
Mitigation: Mark the technical verdict as unknown when headers are unavailable and increase caution, especially for money, credentials, permissions, downloads, or data-disclosure requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shingo0620/email-importance-content-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, markdown] <br>
**Output Format:** [Markdown triage summary with verdicts, risk level, importance level, and recommended next steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include title triage, technical verification, summary, requested action, red flags, safe verification path, and do/don't recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
