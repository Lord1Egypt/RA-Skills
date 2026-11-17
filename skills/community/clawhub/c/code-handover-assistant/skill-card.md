## Description:

Helps developers and engineers analyze a handed-over codebase and produce structured handover documentation with a quick-start checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxyzcyxpp](https://clawhub.ai/user/chenxyzcyxpp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when receiving an unfamiliar codebase and needing a formal, structured handover document. It guides codebase inspection across business context, module structure, execution flow, dependencies, risks, and onboarding actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect codebases that contain sensitive business logic or secrets.

Mitigation: Use it only on repositories and paths that are appropriate for the agent to read, and review the generated handover before sharing it.

Risk: The default output language is Chinese, which may not match every team handover process.

Mitigation: Request English or another language explicitly when assigning the analysis task.

## Reference(s):

- [Anti-Patterns Reference](references/anti-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/chenxyzcyxpp/skills/code-handover-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown handover document and quick-start checklist with inline shell commands where relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected outputs are HANDOVER.md and QUICKSTART.md; default prose is formal Chinese unless the user requests another language.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
