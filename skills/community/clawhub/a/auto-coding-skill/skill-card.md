## Description:

Auto Coding V3 coordinates an autonomous coding workflow with staged skill injection, code review, testing, verification, and risk scorecard checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krislu1221](https://clawhub.ai/user/krislu1221)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to drive multi-phase coding work from requirements through implementation, review, testing, and delivery verification. It is intended for project-scoped coding tasks where staged checks and explicit approvals are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised discipline and scorecard guardrails may be stronger than the behavior guaranteed by the package.

Mitigation: Review the skill before installation and explicitly enable and verify discipline or scorecard modes when relying on those checks.

Risk: The skill writes persistent local workflow files that may contain task details, file paths, test results, or code context.

Mitigation: Run the skill only on an intended project directory, keep .auto-coding/ and /tmp/auto-coding-projects out of version control, and clean local state after use when appropriate.

Risk: Optional external notifications or background scheduling can expose task summaries or create local automation if enabled.

Mitigation: Leave notifications and scheduling disabled unless intentionally opted in, and verify cleanup after the task completes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krislu1221/skills/auto-coding-skill)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Design Document](artifact/DESIGN.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text guidance with code, configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream agent output; the skill may also create or update project files and local workflow state/log files when run.]

## Skill Version(s):

3.7.17 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
