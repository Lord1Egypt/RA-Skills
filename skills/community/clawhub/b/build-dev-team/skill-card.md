## Description:

Builds and configures a complete AI software development team inside OpenClaw, including agent setup, project coordination files, workflow rules, model handoffs, Asana project setup guidance, and repository wiring guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to set up a coordinated AI software development team with PM, engineering, development, QA, and optional automation roles. It guides agent configuration, workspace file creation, sprint workflow, Asana task coordination, repository conventions, and mockup-aware UI handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad, persistent changes to agents, coordination files, heartbeat scheduling, dependency skills, repositories, and PM chat completions.

Mitigation: Review planned side effects before installation, take a pre-setup snapshot when the recovery skill is available, and verify the post-setup state before active use.

Risk: Dependency skills may be installed or delegated sensitive actions without sufficient trust checks.

Mitigation: Pin every dependency skill to a trusted publisher and version before use.

Risk: Incorrect project names, Asana identifiers, or repository SSH URLs can configure agents against the wrong workspace or repository.

Mitigation: Validate project names, Asana GIDs, queue or section GIDs, and repository SSH URLs before writing agent and project configuration.

Risk: Repository actions delegated through dependency skills can affect protected branches.

Mitigation: Require explicit human confirmation with the PR number and branch before any merge to main.

Risk: Credential exposure is possible if users provide token values instead of environment variable names.

Mitigation: Keep token values in a secret manager and collect only environment variable names for credential references.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/encryptshawn/skills/build-dev-team)
- [Project files reference](references/project-files.md)
- [Workflow reference](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline command blocks and structured project file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance and file templates for OpenClaw agent teams; dependent skills perform external Asana, Git, email, and OpenClaw configuration actions.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
