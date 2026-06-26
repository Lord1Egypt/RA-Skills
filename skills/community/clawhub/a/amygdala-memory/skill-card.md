## Description: <br>
Emotional processing layer for AI agents. Persistent emotional states that influence behavior and responses. Part of the AI Brain series. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ImpKind](https://clawhub.ai/user/ImpKind) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to give an OpenClaw agent persistent emotional state, decay, session-context loading, and optional automated emotional encoding from recent conversation history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent conversations can be analyzed into persistent emotional memory. <br>
Mitigation: Install only when persistent emotional memory is desired, and review or delete AMYGDALA_STATE.md and files under ~/.openclaw/workspace/memory when that state should not carry forward. <br>
Risk: Background cron jobs can continue emotional decay and encoding without manual prompts. <br>
Mitigation: Avoid --with-cron unless recurring background processing is intended, and remove the amygdala cron jobs when automatic processing is no longer wanted. <br>
Risk: Persisted emotional state can influence future agent responses. <br>
Mitigation: Review the generated state before relying on it in sessions, and edit or reset the state files if the encoded mood is inaccurate or inappropriate. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/ImpKind/amygdala-memory) <br>
- [Skill metadata repository](https://github.com/ImpKind/amygdala-memory) <br>
- [Amygdala emotional encoding prompt](artifact/prompts/encode-emotions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON state files, JSONL logs, and generated HTML dashboard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent emotional state under the OpenClaw workspace and can set up recurring cron jobs when installed with --with-cron.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
