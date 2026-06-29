## Description: <br>
Read and write email through Atomic Mail from an AI agent, including inbox registration, mailbox listing, email fetches, and sending mail through JMAP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atomicmail](https://clawhub.ai/user/atomicmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent operate a dedicated Atomic Mail inbox: register or restore account credentials, read and triage messages, send replies, and run JMAP batches or presets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent ongoing mailbox read/write access and the ability to send outbound email. <br>
Mitigation: Use a dedicated Atomic Mail account and confirm recipients, message content, and attachments before allowing the agent to send mail. <br>
Risk: Credentials and JWT bearer tokens are persisted on disk. <br>
Mitigation: Keep the configured credentials directory private, do not commit credential files, and use separate credential directories for separate inboxes. <br>
Risk: Scheduled inbox polling can repeatedly expose mailbox contents to an agent. <br>
Mitigation: Review the scheduled job prompt and cadence, ensure it runs as a full agent turn, and avoid raw CLI-only cron jobs. <br>
Risk: Attachment upload can expose local file contents. <br>
Mitigation: Attach only files the operator explicitly selected and review attachment paths before sending. <br>


## Reference(s): <br>
- [Atomic Mail homepage](https://atomicmail.ai) <br>
- [OpenClaw cron jobs](https://docs.openclaw.ai/automation/cron-jobs) <br>
- [Hermes cron documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) <br>
- [Atomic Mail ClawHub skill page](https://clawhub.ai/atomicmail/skills/atomicmail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/JMAP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a bundled Node CLI that reads or writes Atomic Mail credentials, JWT files, mailbox data, outbound messages, and attachments.] <br>

## Skill Version(s): <br>
0.3.23 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
