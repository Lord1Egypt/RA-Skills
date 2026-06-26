## Description: <br>
Multi-channel customer service auto-responder with FAQ matching, escalation, and daily summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External support teams and developers use this skill to configure and run a customer-service autoresponder that monitors messaging channels, matches customer inquiries to FAQ entries, escalates unresolved or sensitive messages, and summarizes daily support activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic replies may send incorrect, off-brand, or poorly scoped responses when connected to real customer channels. <br>
Mitigation: Test replies in a sandbox, review FAQ coverage and tone settings, and require escalation for low-confidence or sensitive messages before production use. <br>
Risk: Conversation logs may contain sensitive customer content. <br>
Mitigation: Use a protected log directory, redact or avoid storing sensitive data, and define an explicit retention policy before handling real customer messages. <br>
Risk: Production integrations with messaging or LLM providers may introduce data-sharing and credential-handling obligations. <br>
Mitigation: Review provider terms, keep credentials out of logs and configuration files, and replace commented shell examples with scoped API integrations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/cs-autoresponder) <br>
- [Publisher profile](https://clawhub.ai/user/mupengi-bot) <br>
- [OpenClaw skills homepage](https://github.com/openclaw/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Node.js command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces customer reply text, escalation notices, JSONL conversation logs, and daily summary text when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
