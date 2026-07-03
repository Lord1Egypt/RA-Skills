## Description: <br>
LLM-powered e-commerce customer service email automation for classification, reply generation, escalation, multilingual support, knowledge-base lookup, and dashboard monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce support teams and developers use this agent to triage incoming customer emails, draft or send replies, escalate urgent issues, and monitor support ticket status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can read customer email and send live replies. <br>
Mitigation: Install with a test mailbox first, use least-privilege IMAP and SMTP accounts, and require human review before production automation. <br>
Risk: Message data may be sent to an LLM provider or escalation webhooks. <br>
Mitigation: Review data handling obligations, configure approved providers and webhooks only, and avoid sending sensitive data that is not required for support handling. <br>
Risk: The dashboard may expose ticket data if reachable beyond localhost. <br>
Mitigation: Keep the dashboard bound to localhost or add authentication and network access controls before broader deployment. <br>
Risk: Dependencies are specified without exact pins. <br>
Mitigation: Pin and review dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/ai-email-agent) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Runtime configuration](artifact/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Email reply text, JSON classification results, ticket records, dashboard metrics, and Markdown command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 plus LLM, IMAP, and SMTP credentials; live run mode can send customer replies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
