## Description: <br>
Deep web search using Codex CLI for complex queries that need multi-source synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangwzh](https://clawhub.ai/user/jiangwzh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to dispatch Codex CLI web research for complex or niche queries that require multi-source synthesis, incremental report writing, and optional callback delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research details may be delivered to Telegram when callback delivery is configured. <br>
Mitigation: Use local-only synchronous output for confidential research, remove or replace hardcoded Telegram targets, and confirm chat IDs before dispatch. <br>
Risk: The skill can trigger a local OpenClaw wake hook after completion. <br>
Mitigation: Audit hook-token behavior and localhost gateway access before installation, or disable the hook path if it is not required. <br>
Risk: The release is marked suspicious because background Codex searches, Telegram result delivery, and local hook signaling are under-scoped for general installation. <br>
Mitigation: Review the script before installing and run it only in trusted workspaces with explicit timeout and output paths. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report files, JSON task metadata, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports background dispatch with optional Telegram callback and synchronous short-query execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
