## Description: <br>
Automatic context compression for OpenClaw sessions that summarizes long conversations into structured digests, saves compressed summaries locally, and helps inject prior context into new sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zgjq](https://clawhub.ai/user/zgjq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to compact long OpenClaw conversations into concise session memory, preserving decisions, facts, pending actions, blockers, and technical context for later work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation summaries may preserve sensitive work context or secrets if a session is compacted without review. <br>
Mitigation: Avoid compacting sessions that contain secrets or sensitive internal details, and review compact files when privacy matters. <br>
Risk: Redaction reduces exposure but may not remove every sensitive detail from generated compacts. <br>
Mitigation: Use the skill's redaction checks and manually remove sensitive paths, URLs, credentials, and personal information before relying on a compact. <br>


## Reference(s): <br>
- [Compaction Prompt Template](references/compaction_prompt.md) <br>
- [ClawHub skill page](https://clawhub.ai/zgjq/context-compactor-zero-dep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown session digests and shell commands for local compaction scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local compact files under the configured OpenClaw workspace and keeps up to 30 compacts.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
