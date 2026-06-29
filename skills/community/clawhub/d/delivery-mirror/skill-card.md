## Description: <br>
Mirror cron/script deliveries into agent session transcripts so scheduled and isolated-cron messages persist in context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obuchowski](https://clawhub.ai/user/obuchowski) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to send scheduled OpenClaw messages while appending matching delivery-mirror rows to the owning agent's session transcript, preserving context for the agent's next turn. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper appends a delivery-mirror row that must continue matching OpenClaw's expected transcript shape. <br>
Mitigation: Mirroring is best-effort, isolated to appending one row, and should be re-verified after major OpenClaw upgrades. <br>
Risk: Concurrent writes could occur if mirroring targets a session while an agent is actively writing to the same transcript. <br>
Mitigation: The helper uses advisory per-session locks; operators should use it for dispatcher-style schedules when the target agent is idle. <br>
Risk: Caller-supplied message text is delivered and stored verbatim in the transcript. <br>
Mitigation: Treat the calling cron or script as the trust source and review the command preview, account, repository, and target before approving sends or writes. <br>
Risk: Idempotency state can grow when unbounded unique keys are used. <br>
Mitigation: Use bounded idempotency keys and rotate or clear the state file if key volume grows without limit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/obuchowski/skills/delivery-mirror) <br>
- [Project homepage](https://github.com/obuchowski/openclaw-delivery-mirror) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and flag descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled helper can append JSONL transcript rows, write idempotency state and logs, and call the OpenClaw CLI when invoked.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata and changelog, released 2026-06-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
