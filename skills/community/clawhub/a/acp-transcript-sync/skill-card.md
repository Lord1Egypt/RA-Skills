## Description:

ACP Transcript Sync helps agents copy completed ACP child-session transcript content into the main OpenClaw session transcript so platforms such as AIMA can collect the child-agent work record.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steflerjiang](https://clawhub.ai/user/steflerjiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after spawning ACP child agents to merge child-session messages back into the main OpenClaw transcript for downstream collection and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Child-agent transcripts may contain credentials, private data, sensitive prompts, or untrusted tool output.

Mitigation: Use only for sessions intentionally copied into the main OpenClaw transcript, and redact sensitive content before syncing.

Risk: Transcript syncing has weak safeguards around sensitive data and destination paths.

Mitigation: Validate paths, preview the destination transcript, and preserve imported content as untrusted provenance-marked data before deployment.

## Reference(s):

- [Skill documentation](artifact/SKILL.md)
- [Transcript sync script](artifact/scripts/sync-acp-to-main.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides execution of a Python script that appends ACP child-session messages to a main OpenClaw transcript.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
