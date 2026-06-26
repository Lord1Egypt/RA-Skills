## Description: <br>
Event watcher skill for OpenClaw. Use when you need to subscribe to event sources (Redis Streams + webhook JSONL) and wake an agent only when matching events arrive. Covers filtering, dedupe, retry, and session routing via sessions_send/agent_gate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solitaire2015](https://clawhub.ai/user/solitaire2015) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure background event watchers that monitor Redis Streams or webhook JSONL input, filter and deduplicate matching events, and wake or message the correct OpenClaw session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured watchers can automatically wake or message OpenClaw sessions from Redis or webhook events. <br>
Mitigation: Keep the source safety preamble enabled for untrusted payloads, use narrow filters, and restrict reply targets to intended channels or users. <br>
Risk: Default session routing may read local OpenClaw session metadata to resolve the latest session. <br>
Mitigation: Set wake.disable_session_store_lookup to true or provide an explicit session_id or session_key when local session-store lookup is not desired. <br>
Risk: Event logs, state files, dead-letter files, and message previews may contain event payloads or routing details. <br>
Mitigation: Protect and rotate runtime files, avoid sending sensitive payloads when possible, and review log locations before running the watcher in production. <br>
Risk: Runtime behavior depends on redis and pyyaml packages. <br>
Mitigation: Pin and review dependencies before production deployment. <br>


## Reference(s): <br>
- [Event Watcher configuration spec](references/CONFIG.md) <br>
- [Redis Stream watcher example](examples/event_watcher.yaml) <br>
- [Webhook watcher example](examples/webhook_watcher.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with YAML configuration examples and Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python packages redis and pyyaml; outputs setup guidance for watcher configuration, routing, filtering, deduplication, retry, and background execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
