## Description: <br>
Delegate coding tasks to Cline CLI, including one-shot tasks, CI/CD automation, parallel workstreams, and Kanban-mode workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreasthinks](https://clawhub.ai/user/andreasthinks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to operate Cline CLI and Kanban workflows for delegated coding tasks, automated code review, CI/CD assistance, and coordinated multi-agent implementation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended Cline runs can modify code, commit, push, or deploy changes with substantial repository authority. <br>
Mitigation: Use disposable worktrees or protected branches, review diffs before committing or deploying, and limit credentials to the minimum required scope. <br>
Risk: Kanban control exposed beyond the local machine can allow unintended remote task control. <br>
Mitigation: Keep Kanban on localhost unless it is protected by VPN, firewall, and authentication. <br>
Risk: Passing API keys through CLI flags can expose credentials through shell history, process lists, or logs. <br>
Mitigation: Avoid passing API keys as CLI flags and use least-privilege credentials that can be rotated. <br>


## Reference(s): <br>
- [Cline CLI documentation](https://cline.bot/cli) <br>
- [ClawHub release page](https://clawhub.ai/andreasthinks/cline-kanban) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell command examples and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational patterns for Cline CLI and Kanban workflows, including unattended automation patterns that require review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
