## Description: <br>
Codex Hook helps OpenClaw dispatch, execute, monitor, report, and merge coding-agent tasks through shell-based automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lonelybeanz](https://clawhub.ai/user/lonelybeanz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate Codex task execution from OpenClaw, track task status, intervene in running sessions, and manage pull request workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run coding agents with repository write access and can restart or recover work automatically. <br>
Mitigation: Use it first in a disposable or tightly protected repository, and keep branch protections and required reviews enabled. <br>
Risk: The skill can push and merge pull requests and delete branches through GitHub automation. <br>
Mitigation: Limit GitHub permissions, require human review for merges, and verify CI and branch protection settings before enabling auto-merge workflows. <br>
Risk: Task details may be sent to external notification endpoints such as Telegram, Discord, or generic webhooks. <br>
Mitigation: Avoid sensitive task prompts and enable external webhooks only when the destination is trusted. <br>
Risk: Background monitors can automatically retry or recover tasks without continuous user supervision. <br>
Mitigation: Run background monitors only when automatic retry and recovery behavior is intended and observable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lonelybeanz/codex-hook) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and environment-variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local shell tooling such as bash, jq, Codex CLI, and optionally tmux, gh, and curl.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
