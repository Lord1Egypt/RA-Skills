## Description:

Actively monitors token utilization and executes memory compaction routines before context bloat causes failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elmoorish](https://clawhub.ai/user/elmoorish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to compact active session state when context grows large, archive granular memory logs, and resume work from a concise semantic summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can interrupt active work and move active OpenClaw memory logs during compaction.

Mitigation: Require explicit confirmation before running compaction, write the summary before moving active logs, and keep archived logs available for recovery.

Risk: The configuration helper can modify global OpenClaw compaction settings.

Mitigation: Review the proposed configuration changes before applying them and back up valid OpenClaw settings.

Risk: Compacted summaries may preserve sensitive details from prior work if the agent is not instructed to redact them.

Mitigation: Redact credentials, personal data, and unnecessary sensitive context before writing the resumed summary.

Risk: The install metadata includes an unused unpinned dependency.

Mitigation: Remove the unused dependency or pin and review it before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elmoorish/skills/cognitive-compaction)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command execution output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify OpenClaw memory files and global OpenClaw compaction configuration when its bundled scripts are run.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
