## Description:

Provides a scheduled autonomous learning loop that selects and runs tasks, extracts reusable patterns, scores confidence, creates skills, and produces daily or weekly reflection and learning-direction outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, learners, project managers, and knowledge-management users use this skill to run a persistent agent learning system that turns completed work into reusable patterns, generated skills, reflection reports, and new learning tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent autonomous agent behavior may run scheduled jobs without repeated user review.

Mitigation: Enable cron only after reviewing setup-cron.js and confirming each scheduled job is intended.

Risk: The skill can modify memory, task queues, and generated skill files with weak safeguards.

Mitigation: Keep the workspace private, review engine scripts before use, and manually review generated skills before trusting or installing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pagoda111king/skills/autonomous-learning-cycle)
- [Publisher profile](https://clawhub.ai/user/pagoda111king)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact release notes](artifact/RELEASE-v1.0.0.md)
- [Artifact package metadata](artifact/package.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON and JSONL state files, generated skill files, and reflection reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create persistent schedules, modify task and memory files, and generate additional skills when enabled]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
