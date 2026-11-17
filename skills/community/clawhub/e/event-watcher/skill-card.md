## Description:

Event-Watcher subscribes to Redis Streams and webhook JSONL sources, filters and deduplicates events, retries delivery, and wakes OpenClaw sessions through sessions_send or agent_gate when matching events arrive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solitaire2015](https://clawhub.ai/user/solitaire2015)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure long-lived watchers that listen to event sources, apply filters and deduplication, and wake an OpenClaw session only when relevant events arrive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted event payloads can be routed into OpenClaw sessions and may contain prompt-injection content.

Mitigation: Keep wake.add_source_preamble enabled, avoid templates that pass raw payloads wholesale, and disable the preamble only for fully trusted sources.

Risk: Automatic session routing may read broad local session metadata or deliver to unintended chat targets.

Mitigation: Prefer explicit wake.session_id or a scoped OPENCLAW_SESSION_STORE, set wake.disable_session_store_lookup: true when practical, and restrict reply_channel and reply_to to approved destinations.

Risk: Watcher logs, state, webhook JSONL, and dead-letter files can contain sensitive event data in plaintext.

Mitigation: Store log and state files in private directories, redact payload data before ingestion where possible, and control file permissions and retention.

Risk: Python dependencies are declared without pinned versions.

Mitigation: Pin reviewed redis and pyyaml versions before production deployment.

## Reference(s):

- [CONFIG.md](references/CONFIG.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code]

**Output Format:** [Markdown guidance with YAML and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include watcher configuration, filter rules, session routing guidance, and runtime commands.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
