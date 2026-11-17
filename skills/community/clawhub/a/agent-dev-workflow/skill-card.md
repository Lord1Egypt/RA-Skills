## Description:

Orchestrate coding agents to implement coding tasks through a structured workflow with requirement analysis, specification, task planning, agent dispatch, verification, and delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgyanami](https://clawhub.ai/user/lgyanami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn coding requirements, feature requests, bug reports, or GitHub issues into a gated implementation workflow across coding agents. It helps structure specs, task cards, dispatch prompts, verification, and delivery summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External coding agents may receive project context during orchestration.

Mitigation: Run the workflow only for projects where sharing context with the selected agent is acceptable, and prefer a sandboxed checkout.

Risk: The workflow references broad bypassed permissions for Claude Code.

Mitigation: Remove or avoid bypassPermissions unless the task truly requires it, and review agent actions before keeping changes.

Risk: The workflow can modify project agent configuration and llmdoc files.

Mitigation: Review CLAUDE.md and llmdoc changes before accepting them into the project.

Risk: The workflow depends on cc-plugin behavior.

Mitigation: Pin and review the required cc-plugin before using the workflow.

## Reference(s):

- [cc-plugin](https://github.com/TokenRollAI/cc-plugin)
- [Requirement Template](references/requirement-template.md)
- [Verification Template](references/verification-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with task cards, shell command blocks, prompts, checklists, and delivery summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation gates before specification approval and agent dispatch.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
