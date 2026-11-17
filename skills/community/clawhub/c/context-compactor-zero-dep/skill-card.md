## Description:

Automatic context compression for OpenClaw sessions that summarizes long conversations into structured digests, stores local compact files, and helps inject relevant prior context into new sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgjq](https://clawhub.ai/user/zgjq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to condense long OpenClaw conversations into reusable session memory, recover recent decisions and pending work, and reduce repeated context in later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived information may be stored and reinjected into later sessions, including sensitive project context.

Mitigation: Use only when local cross-session memory is intended, inspect generated compacts, and avoid compacting conversations that contain credentials, customer data, or private infrastructure details.

Risk: Current redaction checks are not a complete secret scanner.

Mitigation: Redact sensitive details before compaction and review compact output instead of relying solely on built-in filtering.

Risk: Opt-in LLM compaction can send conversation text to the configured LLM provider.

Mitigation: Use keyword-based local extraction for sensitive sessions, or confirm that the configured LLM provider is approved for the conversation contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zgjq/skills/context-compactor-zero-dep)
- [Compaction prompt template](artifact/references/compaction_prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown session digests, shell command snippets, and local compact-file operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Standard-library Python workflow; local compact retention is capped at 30 files.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
