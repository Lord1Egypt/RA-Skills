## Description:

Structured workflow to analyze, plan, and execute feature modifications by scenario complexity, ensuring controlled, incremental, and risk-aware changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liancheng-zcy](https://clawhub.ai/user/liancheng-zcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to decide whether a feature modification can be handled directly or needs a fuller analysis, planning, confirmation, and stepwise implementation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording can cause the workflow to activate for many code-change requests, including generic bug fixes and optimization requests.

Mitigation: Install it only when a general feature-change workflow is desired, or narrow the trigger wording before deployment.

Risk: Feature-change proposals can introduce incorrect or misleading guidance if project context is incomplete.

Mitigation: Review the analysis and plan before execution, then test and scan resulting changes before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liancheng-zcy/skills/feature-modification-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance, plans, status updates, and code-oriented implementation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for user confirmation before complex changes or refactoring.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
