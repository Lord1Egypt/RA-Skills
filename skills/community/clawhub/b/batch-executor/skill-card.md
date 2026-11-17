## Description:

Batch Executor guides agents through corpus-scale task execution by ingesting large file or export dumps, classifying items, triaging work, spawning limited sub-agent waves, checkpointing progress, and reporting outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to process large document or conversation corpora, turn mixed content into prioritized work, execute eligible items, and produce manifests, checkpoints, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes and acts on large private document exports.

Mitigation: Require an explicit execution plan before use and avoid sensitive sources unless they are redacted.

Risk: The skill saves raw corpus content and may commit progress to git.

Mitigation: Keep raw corpora out of git and review any commit that includes imported content.

Risk: The skill may execute tasks found in imported content through inline work or sub-agents.

Mitigation: Approve sub-agent work, file mutations, API calls, shell commands, and commits before they proceed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dodge1218/skills/batch-executor)
- [Publisher profile](https://clawhub.ai/user/dodge1218)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, manifests, execution plans, status updates, and task-specific artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May spawn up to three concurrent sub-agents and checkpoint progress every five completed items.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
