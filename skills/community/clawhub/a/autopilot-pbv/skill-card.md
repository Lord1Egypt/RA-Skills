## Description:

Autopilot 自动循环编排引擎 coordinates a Plan, Build, and Verify loop for complex coding tasks, using a planner, builder, and orchestrator to iterate toward completion for up to five rounds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuscut](https://clawhub.ai/user/qiuscut)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate complex coding work that benefits from explicit planning, automated implementation, and repeated verification. It is aimed at multi-step refactors, automatic repair loops, and changes spanning multiple modules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically run file-changing agents with approval and sandbox protections disabled.

Mitigation: Run it only in a disposable or tightly sandboxed workspace and require explicit human review before any build step that can change files.

Risk: The skill requires an Anthropic API key and stores task artifacts under ~/.openclaw.

Mitigation: Use a scoped API key, avoid sensitive home-directory access, and delete task artifacts when they are no longer needed.

Risk: Generated plans or automated fixes may be incorrect even when the loop reports progress.

Mitigation: Review generated plans before Build and inspect diffs, logs, and verification reports after each run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiuscut/skills/autopilot-pbv)
- [Publisher profile](https://clawhub.ai/user/qiuscut)
- [Plan format reference](references/plan-format.md)
- [Verify guide](references/verify-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown instructions and reports with inline shell commands and task files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plan, build result, verification report, task status, and next-step guidance for a single requested coding task.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
