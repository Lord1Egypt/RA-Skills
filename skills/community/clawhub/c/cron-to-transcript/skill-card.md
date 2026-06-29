## Description: <br>
Isolated crons, scripts, reminders, and status checkers sent it but the agent forgot? Write deliveries into the session transcript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obuchowski](https://clawhub.ai/user/obuchowski) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill when trusted command crons, dispatcher scripts, reminders, or status checkers send OpenClaw messages and the owning agent should retain a durable session transcript entry for that delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message text from the calling cron or script is delivered and stored verbatim in the session transcript and local helper logs/state may contain sensitive context. <br>
Mitigation: Use only trusted message sources, avoid passing secrets, and protect or rotate the helper's local log and idempotency files when messages may be sensitive. <br>
Risk: The helper appends transcript rows through local filesystem writes and relies on OpenClaw's current transcript row shape. <br>
Mitigation: Use --openclaw-home for testing or containment and re-verify behavior after major OpenClaw upgrades. <br>
Risk: Concurrent live session writes could interleave with a helper append. <br>
Mitigation: Run it for dispatcher-style schedules when the target agent is idle and rely on the per-session advisory lock for helper-side serialization. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/obuchowski/skills/cron-to-transcript) <br>
- [Project Homepage](https://github.com/obuchowski/openclaw-cron-to-transcript) <br>
- [Security Policy](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command examples and flag descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to call a local Bash helper that sends an OpenClaw message and can append one transcript-only JSONL row.] <br>

## Skill Version(s): <br>
1.0.2 (source: changelog and server release metadata, released 2026-06-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
