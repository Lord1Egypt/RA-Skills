## Description:

Piv orchestrates a Plan, Implement, Validate workflow for phase-based software development with PRD creation, PRP generation, codebase analysis, execution, validation, and debugging support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smokealot420](https://clawhub.ai/user/smokealot420)

### License/Terms of Use:


## Use Case:

Developers and engineers use Piv to plan and execute multi-phase implementation work: discover requirements, create PRDs and PRPs, analyze a codebase, delegate execution, validation, and debugging, and track completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify a target repository and run project-defined commands.

Mitigation: Use it only on trusted repositories, and review proposed file changes and validation commands before execution.

Risk: The skill can spawn sub-agents that perform execution, validation, and debugging work.

Mitigation: Keep PRD and PRP scope explicit, then review each execution and verification summary before allowing the next phase.

Risk: The skill can create branded git commits without enough user control.

Mitigation: Do not allow automatic commits unless you approve the exact changed files and commit message first.

## Reference(s):

- [Piv ClawHub listing](https://clawhub.ai/smokealot420/skills/ftw)
- [Publisher profile](https://clawhub.ai/user/smokealot420)
- [Project homepage](https://github.com/SmokeAlot420/ftw)
- [Codebase Analysis for Feature Planning](references/codebase-analysis.md)
- [Create PRD](references/create-prd.md)
- [Create BASE PRP](references/generate-prp.md)
- [Execute BASE PRP](references/execute-prp.md)
- [PIV Discovery](references/piv-discovery.md)
- [PIV Executor Agent](references/piv-executor.md)
- [PIV Validator Agent](references/piv-validator.md)
- [PIV Debugger Agent](references/piv-debugger.md)
- [Base PRP Template](assets/prp_base.md)
- [Workflow Template](assets/workflow-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses, generated planning files, code edits, shell commands, and validation reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PRDs, PRPs, workflow tracker files, repository commits, and validation summaries in the target project.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
