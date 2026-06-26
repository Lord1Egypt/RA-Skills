## Description: <br>
AI-powered email reply generation for B2B sales that classifies incoming emails, retrieves knowledge base context, generates draft replies, and routes replies for human review via Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and support teams use this skill to process B2B sales emails, classify customer intent, retrieve relevant product or CRM context, generate reply drafts, and route drafts for human approval before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live customer email content can influence shell execution during knowledge-base retrieval. <br>
Mitigation: Review the shell-command issue in kb-retrieval.js before installation, constrain runtime paths and inputs, run with least privilege, and validate behavior with dry-run tests before live or scheduled processing. <br>
Risk: Sensitive email content may be sent to third-party services or stored in drafts, reviews, logs, and test reports. <br>
Mitigation: Use a dedicated mailbox, restricted Discord channel, limited bot permissions, least-privilege API keys, redaction or minimization for email content, and explicit cleanup rules for generated artifacts. <br>
Risk: Live email processing can affect customers if credentials, channels, or review workflows are misconfigured. <br>
Mitigation: Start with dry-run testing, limit mailbox scope and batch size, confirm Discord bot permissions, and require human review before enabling live sends or cron scheduling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cjboy007/email-smart-reply) <br>
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions) <br>
- [Farreach Electronic](https://farreach-electronic.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Draft email text and JSON records, with Markdown documentation and shell-command examples for setup and testing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts are intended for human review before sending; the artifact documents a dry-run mode for testing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
