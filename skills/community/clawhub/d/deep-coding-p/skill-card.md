## Description:

Advanced multi-agent development system for complex software projects that uses Orchestrator, Builder, and Reviewer agents to decompose modules, implement code, and perform iterative quality reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate complex software builds across orchestrator, builder, and reviewer agents, including module decomposition, implementation, review, and end-to-end verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local dashboard and project file serving may expose project files, logs, or secrets from the workspace.

Mitigation: Run the skill only in a dedicated workspace or container, keep the dashboard on localhost, avoid storing secrets in the workspace, and restrict file serving to an allowlist before wider use.

Risk: Generated or reviewed project code may execute arbitrary commands or start local services.

Mitigation: Use the skill only where executing generated code is acceptable, prefer containers or virtual machines for untrusted projects, and stop dashboard or preview servers when work is complete.

Risk: Dashboard markdown rendering and external frontend or npx dependencies can add supply-chain and content-rendering exposure.

Mitigation: Sanitize rendered markdown and pin or vendor frontend and npx dependencies before broader deployment.

## Reference(s):

- [Deep Coding Harness Architecture](references/architecture.md)
- [Orchestrator Rules](references/orchestrator-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/deep-coding-p)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project requests, module plans, agent prompts, review notes, local dashboard files, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
