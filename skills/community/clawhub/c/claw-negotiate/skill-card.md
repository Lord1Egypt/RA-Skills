## Description: <br>
APOA-constrained SAFE negotiation on OpenClaw. Two OpenClaws negotiate within user-approved bounds, stream offers in Telegram, and finalize with human-approved sshsign signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juanfiguera](https://clawhub.ai/user/juanfiguera) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run bounded founder-investor SAFE negotiations through OpenClaw, Telegram, APOA authorization checks, and human-approved sshsign signatures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring OpenClaw cron or system crontab entries may keep the workflow active after testing. <br>
Mitigation: Inspect OpenClaw cron and system crontab entries after use and remove any claw-negotiate scan jobs that are no longer needed. <br>
Risk: The workflow handles sensitive negotiation bounds, Telegram messages, signing links, and signing data. <br>
Mitigation: Run it on a dedicated OpenClaw host with dedicated Telegram bot and sshsign keys, and avoid shared machines. <br>
Risk: Shared local output directories can expose or mix negotiation state between chats. <br>
Mitigation: Use private per-chat state and output directories for each negotiation. <br>
Risk: The skill relies on local and remote command execution through python3, openclaw, ssh, Telegram, and sshsign. <br>
Mitigation: Review the skill before installing and run the doctor or smoke checks only in an environment prepared for those dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juanfiguera/claw-negotiate) <br>
- [claw-negotiate demo](https://www.youtube.com/watch?v=T2Y2Tr__g_k) <br>
- [Y Combinator standard SAFE documents](https://www.ycombinator.com/documents) <br>
- [APOA project](https://github.com/agenticpoa) <br>
- [sshsign](https://github.com/agenticpoa/sshsign) <br>
- [The Art of the Automated Negotiation](https://hai.stanford.edu/news/the-art-of-the-automated-negotiation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [OpenClaw and Telegram messages, Markdown-style authorization cards, JSON events, shell command invocations, and executed PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces negotiation status updates, private signing links, local state files, and an executed SAFE PDF with an audit trail.] <br>

## Skill Version(s): <br>
0.1.10 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
