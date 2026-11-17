## Description:

This skill provides Geode's local transcription and summarization capabilities to OpenClaw and other AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geodeteam](https://clawhub.ai/user/geodeteam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents on macOS use this skill to submit audio or video files to Geode for local asynchronous transcription, optional summarization, and later result retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command templates expose user-supplied paths and task IDs to local shell execution risk.

Mitigation: Review and fix the manifest to use structured, validated command arguments before handling untrusted paths or task IDs.

Risk: Local audio files, copied audio, task metadata, transcripts, and summaries are stored in Geode's shared container.

Mitigation: Review local privacy and retention expectations before installing or using the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/geodeteam/skills/geode-transcribe)
- [Geode App Store Listing](https://apps.apple.com/app/apple-store/id6752685916?pt=127800752&ct=openclaw&mt=8)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task-status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous workflow returns a TASK_ID first, then transcript and optional summary paths after status polling.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
