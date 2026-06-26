## Description: <br>
Use when user asks to leverage Codex, GPT-5, or GPT-5.1 to implement coding tasks with non-interactive automation and hands-off execution without approval prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiskyer](https://clawhub.ai/user/feiskyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to guide Codex CLI through coding tasks, isolated worktree setup, long-running agent monitoring, pull request creation, and review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes unattended Codex workflows that may edit code, push branches, open pull requests, post comments, or run for long periods. <br>
Mitigation: Run it in a disposable container or isolated worktree, keep sandboxing and approvals enabled on sensitive machines, and review diffs before commit or push. <br>
Risk: Repository credentials and notification tools could be used by an unattended workflow. <br>
Mitigation: Require explicit confirmation before pull request creation, comments, notifications, cleanup, or any action using repository credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/feiskyer/codex-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational guidance for running, monitoring, retrying, and reviewing Codex CLI agent workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
