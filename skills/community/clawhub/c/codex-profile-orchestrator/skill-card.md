## Description: <br>
Deterministic OpenClaw Codex profile failover for Windows workspaces with duplicate detection, workspace variant aliases, quota-aware profile choice, Telegram session sync, network outage protection, and install helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugurinanc12](https://clawhub.ai/user/ugurinanc12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw Codex workspaces use this skill to inspect auth-profiles.json, choose the healthiest Codex OAuth profile, sync session overrides, and package a safer replacement for ad hoc profile rotation logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apply and daemon modes can modify OpenClaw auth profile order, session overrides, registry state, and remove profiles after repeated invalid-token findings. <br>
Mitigation: Back up auth and session files, run dry-run first, inspect the JSON plan, and use apply or daemon mode only after the selected profile and planned removals are acceptable. <br>
Risk: The skill operates on sensitive OAuth profile and session state. <br>
Mitigation: Install and run it only in a trusted OpenClaw workspace, keep credential files local, and avoid sharing dry-run or report output unless redacted. <br>
Risk: Optional Telegram/OpenClaw notifications may reveal profile-switching or quota state to a configured target. <br>
Mitigation: Leave notifications disabled unless needed and verify the configured notification target and account before enabling them. <br>


## Reference(s): <br>
- [State Model](references/state-model.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ugurinanc12/codex-profile-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, code] <br>
**Output Format:** [Markdown guidance with inline shell commands; bundled scripts emit JSON reports or text summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode reports planned profile and session changes before apply mode mutates workspace state.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
