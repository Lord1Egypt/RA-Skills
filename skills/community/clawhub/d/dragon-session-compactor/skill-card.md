## Description: <br>
Dragon Session Compactor helps an agent compact long local conversation sessions into summaries while preserving recent messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhmqq616](https://clawhub.ai/user/xhmqq616) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage long OpenClaw-style chat sessions by checking session size, compacting older messages into summaries, and retaining recent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation history may include secrets, credentials, regulated data, or private personal details that are summarized and persisted locally. <br>
Mitigation: Review .clawsession.json after compaction and avoid using the skill on sensitive sessions unless local persistence is acceptable. <br>
Risk: Automatic heartbeat or cron checks can compact sessions without a manual prompt. <br>
Mitigation: Enable scheduled checks only when automatic compaction is intentional and expected for the workspace. <br>


## Reference(s): <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/xhmqq616/dragon-session-compactor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries, CLI status text, and JSON session files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists compacted conversation state in .clawsession.json and may write a local compaction log when scheduled checks run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
