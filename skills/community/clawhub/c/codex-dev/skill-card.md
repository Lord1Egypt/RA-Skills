## Description: <br>
Run Codex as a background local job with an immediate receipt, saved logs and patch artifacts, optional Telegram notifications, and explicit workdir support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fzhlian](https://clawhub.ai/user/fzhlian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to dispatch local Codex development tasks in the background, receive an immediate job receipt, and inspect saved logs and patch artifacts afterward. It is suited for workflows that need explicit workdir control and optional Telegram completion messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is intended for background code-changing jobs, but the security evidence says the package omits the main runtime scripts and includes under-scoped local setup guidance. <br>
Mitigation: Install only after obtaining and reviewing the missing dispatcher, worker, and Telegram helper from a trusted source. <br>
Risk: Background jobs and Telegram approval flows can modify files in a local workspace. <br>
Mitigation: Use explicit --workdir paths for write jobs, replace the example Telegram approver ID and default workdir with local values, limit bot token access, and review saved logs and patches before trusting changes. <br>


## Reference(s): <br>
- [Local setup](references/local-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/fzhlian/codex-dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce job receipts, status summaries, saved logs, and patch artifacts for later review.] <br>

## Skill Version(s): <br>
0.1.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
