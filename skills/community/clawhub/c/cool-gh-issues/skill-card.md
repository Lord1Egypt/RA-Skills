## Description: <br>
Fetches GitHub issues, coordinates sub-agents to implement fixes and open pull requests, and monitors review comments for follow-up changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuangyinbot-boop](https://clawhub.ai/user/chuangyinbot-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to triage GitHub issues, delegate code fixes to sub-agents, open pull requests, and respond to actionable PR review feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GitHub token and evidence.security says it handles GitHub tokens unsafely. <br>
Mitigation: Install only with a fine-grained GitHub token scoped to the intended repository, and rotate any token that may have appeared in logs or transcripts. <br>
Risk: The skill can run write-capable agents that push branches, open pull requests, and post comments with reduced approval. <br>
Mitigation: Avoid --yes, --cron, and --watch unless automated writes are intended; prefer dry-run or interactive confirmation and review generated pull requests before merging. <br>
Risk: The optional notification channel can disclose repository and pull request details outside GitHub. <br>
Mitigation: Use --notify-channel only with an approved destination for the repository's sensitivity level. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/chuangyinbot-boop/cool-gh-issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status tables, shell commands, pull request summaries, and review-handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create branches, commits, pull requests, PR comments, persisted claim and cursor state, and optional external notifications when invoked with matching flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
