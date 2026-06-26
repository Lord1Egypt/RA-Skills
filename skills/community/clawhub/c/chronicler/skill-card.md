## Description: <br>
Turn your session history into publish-ready stories: an embedded AI journalist reviews conversations and writes narrative dispatches for LinkedIn, Twitter/X, Instagram, and blogs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and teams use Chronicler to turn local OpenClaw session transcripts produced by the chat-memory skill into recurring social and blog-ready narrative dispatches. It is intended for drafting publishable content, with manual review before sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved chat transcripts may contain private or identifying details that could be converted into publishable drafts. <br>
Mitigation: Review the chat-memory dependency separately and manually inspect every generated dispatch before publishing or sharing it. <br>
Risk: The cron job repeatedly processes local transcript files, so unwanted or stale settings can continue generating drafts. <br>
Mitigation: Track the chronicle-reporter cron job and periodically review its schedule, model, state file, and output directory. <br>


## Reference(s): <br>
- [Chronicler on ClawHub](https://clawhub.ai/moltbotmolty-del/chronicler) <br>
- [AI Advantage](https://aiadvantage.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local chronicle files and configures an OpenClaw cron job that appends dispatches over time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
