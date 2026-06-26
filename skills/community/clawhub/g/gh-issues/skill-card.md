## Description: <br>
Fetch GitHub issues, spawn sub-agents to implement fixes and open PRs, then monitor and address PR review comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackhua6](https://clawhub.ai/user/jackhua6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to triage GitHub issues, delegate actionable fixes to sub-agents, open pull requests, and respond to review feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses GitHub credentials and may expose token material in logs or kept transcripts. <br>
Mitigation: Use a least-privilege GitHub token, avoid private repositories unless the exposure risk is accepted, and treat logs and preserved transcripts as sensitive. <br>
Risk: The skill can continue acting on repositories through sub-agents, watch mode, cron mode, and review handlers. <br>
Mitigation: Start with --dry-run, require review before using --yes, --watch, or --cron, and tightly scope the target repository and token permissions. <br>
Risk: Notifications can send repository and pull request details to an external channel. <br>
Mitigation: Use --notify-channel only when the destination is approved for the repository information being shared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackhua6/gh-issues) <br>
- [Publisher profile](https://clawhub.ai/user/jackhua6) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with issue tables, status summaries, shell commands, and generated sub-agent task prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create branches, commits, pull requests, review replies, and notification messages when run with sufficient GitHub credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
