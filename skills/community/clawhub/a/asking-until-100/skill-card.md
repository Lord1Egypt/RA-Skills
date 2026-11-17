## Description:

Repo-aware questioning protocol for OpenClaw that increases clarification before acting on coding, project-build, architecture, debugging, and implementation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongyi3](https://clawhub.ai/user/hongyi3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to pause before ambiguous coding, build, architecture, debugging, and implementation work, inspect repo-discoverable context when relevant, and ask higher-signal clarification questions before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repo-aware clarification can read limited local project structure and a repo-local .asking-until-100.yaml file when relevant.

Mitigation: Review or remove repo-local configuration that should not influence questioning behavior, and invoke the skill only in workspaces where project metadata may be inspected.

Risk: High-rigor coding and build modes can block execution until decision-critical gaps are answered.

Mitigation: Use lower-intensity bundled profiles or explicitly authorize progress with assumptions when speed is more important than clarification depth.

## Reference(s):

- [Readiness Protocol](references/protocol.md)
- [Config](references/config.md)
- [Question Patterns](references/question-patterns.md)
- [Coding Report Format](references/coding-report-format.md)
- [Build Playbook](references/build-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, Shell commands]

**Output Format:** [Markdown question sets and structured reports, with optional configuration guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a provisional project structure, working hypothesis, execution gate summary, blocking dimensions, suggested answer options, and decision-critical unknowns.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
