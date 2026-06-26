## Description: <br>
Manage X (Twitter) account activity by generating AI-assisted tweet drafts, monitoring brand mentions, liking relevant posts, and routing proposed replies through Telegram approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media operators and developers use this skill to manage a BytesAgain X account workflow: draft posts with xAI, monitor X activity, like selected posts, and prepare replies for Telegram-based human approval before posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post, like, and reply from a live X account using read/write OAuth credentials. <br>
Mitigation: Use a dedicated account or tightly scoped tokens, test each command manually before enabling the suggested cron schedule, and require explicit approval for live posts and replies. <br>
Risk: The skill sends content to xAI and Telegram and keeps local state for drafts, likes, seen mentions, and pending replies. <br>
Mitigation: Share only acceptable account data with those services, protect the required environment variables, and periodically clear local state files. <br>


## Reference(s): <br>
- [Command Boundary](references/command-boundary.md) <br>
- [API Notes](references/api-notes.md) <br>
- [Trigger Boundary Test Cases](evals/trigger_cases.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/loutai0307-prog/bytesagain-x-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with bash commands, JSON state files, terminal status text, Telegram messages, and X API side effects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X, xAI, and Telegram credentials supplied through environment variables at runtime.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
