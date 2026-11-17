## Description:

Tracks intent drift across multi-turn tasks and returns a patch, replan, or abort decision with semantic distance and anchor rollback details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseek609609-collab](https://clawhub.ai/user/deepseek609609-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to check whether a changed user request in a multi-step task can be patched in place, needs replanning from an earlier anchor, or should be aborted for confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence whether an ongoing multi-step task continues, rolls back, or stops.

Mitigation: Treat its decision as advisory and confirm before applying aborts, large rollbacks, or other high-impact task-control changes.

Risk: The built-in semantic rules are simple heuristics.

Mitigation: Review the returned semantic_distance, anchor_drift, first_affected_anchor, and reason fields before acting on the recommendation.

Risk: The README is mainly Chinese, which may limit operator review for teams that do not read Chinese.

Mitigation: Have a reviewer who can read the documentation confirm intended behavior and deployment fit before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseek609609-collab/skills/daf-intent-guard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper returns a JSON decision containing decision, semantic_distance, anchor_drift, first_affected_anchor, and reason fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
