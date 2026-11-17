## Description:

Hippocampus is an AI-enhanced memory skill for storing chronicle and monograph memories, recalling workflows and project context, and proactively surfacing relevant past interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabe-luv-nancy](https://clawhub.ai/user/gabe-luv-nancy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an assistant long-term local memory for sessions, project checkpoints, failure-pattern warnings, proactive recall, and reusable micro-to-macro workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-term local memory can automatically store and reuse conversation history across sessions.

Mitigation: Install only when persistent memory is intended, and avoid using it with secrets, credentials, private customer data, or confidential conversations unless retention, review, and deletion controls are in place.

Risk: Auto-save, proactive triggers, ReadingBetweenTheLines, cron jobs, and session hooks can increase what is stored or recalled without an explicit recall command.

Mitigation: Review configuration before enabling the skill, and disable AUTO_SAVE, proactive triggers, ReadingBetweenTheLines, cron jobs, and session hooks until the storage and recall behavior is understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gabe-luv-nancy/skills/chronicle-monograph-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text responses with command examples and local memory artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and reuse local chronicle, monograph, index, and workflow memory records.]

## Skill Version(s):

1.0.3 (source: server release metadata, target metadata, and artifact skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
